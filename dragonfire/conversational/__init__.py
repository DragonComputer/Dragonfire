from __future__ import print_function
import argparse  # Command line parsing
import configparser  # Saving the models parameters
import datetime  # Chronometer
import os  # Files management
import tensorflow as tf
import numpy as np
import math
from random import choice

from tqdm import tqdm  # Progress bar
from tensorflow.python import debug as tf_debug

from dragonfire.conversational.textdata import TextData
from dragonfire.conversational.model import Model


class DeepConversation:
    """
    Main class which launch the training or testing mode
    """

    class TestMode:
        """ Simple structure representing the different testing modes
        """
        ALL = 'all'
        INTERACTIVE = 'interactive'  # The user can write his own questions
        DAEMON = 'daemon'  # The chatbot runs on background and can regularly be called to predict something

    def __init__(self):
        """
        """
        # Global options
        self.test = None
        self.createDataset = False
        self.playDataset = None
        self.reset = False
        self.verbose = False
        self.debug = False
        self.keepAll = False
        self.modelTag = None
        self.rootDir = None
        self.watsonMode = False
        self.autoEncode = False
        self.device = None
        self.seed = None

        # Dataset options
        self.corpus = TextData.corpusChoices()[0]
        self.datasetTag = ''
        self.ratioDataset = 1.0
        self.maxLength = 10
        self.filterVocab = 1
        self.skipLines = False
        self.vocabularySize = 40000

        # Network options (Warning: if modifying something here, also make the change on save/loadParams() )
        self.hiddenSize = 512
        self.numLayers = 2
        self.softmaxSamples = 0
        self.initEmbeddings = False
        self.embeddingSize = 64
        self.embeddingSource = "GoogleNews-vectors-negative300.bin"

        # Training options
        self.numEpochs = 30
        self.saveEvery = 2000
        self.batchSize = 256
        self.learningRate = 0.002
        self.dropout = 0.9

        # Task specific object
        self.textData = None  # Dataset
        self.model = None  # Sequence to sequence model

        # Tensorflow utilities for convenience saving/logging
        self.writer = None
        self.saver = None
        self.modelDir = ''  # Where the model is saved
        self.globStep = 0  # Represent the number of iteration for the current model

        # TensorFlow main session (we keep track for the daemon)
        self.sess = None

        # Filename and directories constants
        self.MODEL_DIR_BASE = "/usr/share/dragonfire/conversational" + os.sep + 'model'
        self.MODEL_NAME_BASE = 'model'
        self.MODEL_EXT = '.ckpt'
        self.CONFIG_FILENAME = 'params.ini'
        self.CONFIG_VERSION = '0.5'
        self.TEST_IN_NAME = 'data' + os.sep + 'test' + os.sep + 'samples.txt'
        self.TEST_OUT_SUFFIX = '_predictions.txt'
        self.SENTENCES_PREFIX = ['Q: ', 'A: ']

        """
        Launch the training and/or the interactive mode
        """
        print('TensorFlow detected: v{}'.format(tf.__version__))

        # General initialisation

        self.modelTag = 'pretrainedv2'
        self.test = 'interactive'
        self.rootDir = os.getcwd()  # Use the current working directory

        #tf.logging.set_verbosity(tf.logging.INFO) # DEBUG, INFO, WARN (default), ERROR, or FATAL

        self.loadModelParams()  # Update the self.modelDir and self.globStep, for now, not used when loading Model (but need to be called before _getSummaryName)

        self.textData = TextData(self)
        # TODO: Add a mode where we can force the input of the decoder // Try to visualize the predictions for
        # each word of the vocabulary / decoder input
        # TODO: For now, the model are trained for a specific dataset (because of the maxLength which define the
        # vocabulary). Add a compatibility mode which allow to launch a model trained on a different vocabulary (
        # remap the word2id/id2word variables).
        if self.createDataset:
            print('Dataset created! Thanks for using this program')
            return  # No need to go further

        # Prepare the model
        with tf.device(self.getDevice()):
            self.model = Model(self, self.textData)

        # Saver/summaries
        self.writer = tf.summary.FileWriter(self._getSummaryName())
        self.saver = tf.train.Saver(max_to_keep=200)

        # TODO: Fixed seed (WARNING: If dataset shuffling, make sure to do that after saving the
        # dataset, otherwise, all which cames after the shuffling won't be replicable when
        # reloading the dataset). How to restore the seed after loading ??
        # Also fix seed for random.shuffle (does it works globally for all files ?)

        # Running session
        self.sess = tf.Session(config=tf.ConfigProto(
            allow_soft_placement=True,  # Allows backup device for non GPU-available operations (when forcing GPU)
            log_device_placement=False)  # Too verbose ?
        )  # TODO: Replace all sess by self.sess (not necessary a good idea) ?

        if self.debug:
            self.sess = tf_debug.LocalCLIDebugWrapperSession(self.sess)
            self.sess.add_tensor_filter("has_inf_or_nan", tf_debug.has_inf_or_nan)

        print('Initialize variables...')
        self.sess.run(tf.global_variables_initializer())

        # Reload the model eventually (if it exist.), on testing mode, the models are not loaded here (but in predictTestset)
        if self.test != DeepConversation.TestMode.ALL:
            self.managePreviousModel(self.sess)

        # Initialize embeddings with pre-trained word2vec vectors
        if self.initEmbeddings:
            self.loadEmbedding(self.sess)

    def respond(self, question, user_prefix=None):
        answer = self.singlePredict(question)
        if not answer:
            return choice([
                    "Sorry, " + user_prefix + ". But it's beyond my intelligence.",
                    "I'm too primitive to answer that.",
                    "Unfortunately, I am not capable to give a respond to such a hard question.",
                    user_prefix + ", I beg your pardon. But I'm not a human equivalent entity, yet...",
                    "Wow, that's a new level. My circuits are burned."
                ])

        #self.sess.close()
        #print("The End! Thanks for using this program")
        return self.textData.sequence2str(answer, clean=True).replace("n't", "not")

    def mainTrain(self, sess):
        """ Training loop
        Args:
            sess: The current running session
        """

        # Specific training dependent loading

        self.textData.makeLighter(self.ratioDataset)  # Limit the number of training samples

        mergedSummaries = tf.summary.merge_all()  # Define the summary operator (Warning: Won't appear on the tensorboard graph)
        if self.globStep == 0:  # Not restoring from previous run
            self.writer.add_graph(sess.graph)  # First time only

        # If restoring a model, restore the progression bar ? and current batch ?

        print('Start training (press Ctrl+C to save and exit)...')

        try:  # If the user exit while training, we still try to save the model
            for e in range(self.numEpochs):

                print()
                print("----- Epoch {}/{} ; (lr={}) -----".format(e+1, self.numEpochs, self.learningRate))

                batches = self.textData.getBatches()

                # TODO: Also update learning parameters eventually

                tic = datetime.datetime.now()
                for nextBatch in tqdm(batches, desc="Training"):
                    # Training pass
                    ops, feedDict = self.model.step(nextBatch)
                    assert len(ops) == 2  # training, loss
                    _, loss, summary = sess.run(ops + (mergedSummaries,), feedDict)
                    self.writer.add_summary(summary, self.globStep)
                    self.globStep += 1

                    # Output training status
                    if self.globStep % 100 == 0:
                        perplexity = math.exp(float(loss)) if loss < 300 else float("inf")
                        tqdm.write("----- Step %d -- Loss %.2f -- Perplexity %.2f" % (self.globStep, loss, perplexity))

                    # Checkpoint
                    if self.globStep % self.saveEvery == 0:
                        self._saveSession(sess)

                toc = datetime.datetime.now()

                print("Epoch finished in {}".format(toc-tic))  # Warning: Will overflow if an epoch takes more than 24 hours, and the output isn't really nicer
        except (KeyboardInterrupt, SystemExit):  # If the user press Ctrl+C while testing progress
            print('Interruption detected, exiting the program...')

        self._saveSession(sess)  # Ultimate saving before complete exit

    def predictTestset(self, sess):
        """ Try predicting the sentences from the samples.txt file.
        The sentences are saved on the modelDir under the same name
        Args:
            sess: The current running session
        """

        # Loading the file to predict
        with open(os.path.join(self.rootDir, self.TEST_IN_NAME), 'r') as f:
            lines = f.readlines()

        modelList = self._getModelList()
        if not modelList:
            print('Warning: No model found in \'{}\'. Please train a model before trying to predict'.format(self.modelDir))
            return

        # Predicting for each model present in modelDir
        for modelName in sorted(modelList):  # TODO: Natural sorting
            print('Restoring previous model from {}'.format(modelName))
            self.saver.restore(sess, modelName)
            print('Testing...')

            saveName = modelName[:-len(self.MODEL_EXT)] + self.TEST_OUT_SUFFIX  # We remove the model extension and add the prediction suffix
            with open(saveName, 'w') as f:
                nbIgnored = 0
                for line in tqdm(lines, desc='Sentences'):
                    question = line[:-1]  # Remove the endl character

                    answer = self.singlePredict(question)
                    if not answer:
                        nbIgnored += 1
                        continue  # Back to the beginning, try again

                    predString = '{x[0]}{0}\n{x[1]}{1}\n\n'.format(question, self.textData.sequence2str(answer, clean=True), x=self.SENTENCES_PREFIX)
                    if self.verbose:
                        tqdm.write(predString)
                    f.write(predString)
                print('Prediction finished, {}/{} sentences ignored (too long)'.format(nbIgnored, len(lines)))

    def mainTestInteractive(self, sess):
        """ Try predicting the sentences that the user will enter in the console
        Args:
            sess: The current running session
        """
        # TODO: If verbose mode, also show similar sentences from the training set with the same words (include in mainTest also)
        # TODO: Also show the top 10 most likely predictions for each predicted output (when verbose mode)
        # TODO: Log the questions asked for latter re-use (merge with test/samples.txt)

        print('Testing: Launch interactive mode:')
        print('')
        print('Welcome to the interactive mode, here you can ask to Deep Conversation the sentence you want. Don\'t have high '
              'expectation. Type \'exit\' or just press ENTER to quit the program. Have fun.')

        while True:
            question = input(self.SENTENCES_PREFIX[0])
            if question == '' or question == 'exit':
                break

            questionSeq = []  # Will be contain the question as seen by the encoder
            answer = self.singlePredict(question, questionSeq)
            if not answer:
                print('Warning: sentence too long, sorry. Maybe try a simpler sentence.')
                continue  # Back to the beginning, try again

            print('{}{}'.format(self.SENTENCES_PREFIX[1], self.textData.sequence2str(answer, clean=True)))

            if self.verbose:
                print(self.textData.batchSeq2str(questionSeq, clean=True, reverse=True))
                print(self.textData.sequence2str(answer))

            print()

    def singlePredict(self, question, questionSeq=None):
        """ Predict the sentence
        Args:
            question (str): the raw input sentence
            questionSeq (List<int>): output argument. If given will contain the input batch sequence
        Return:
            list <int>: the word ids corresponding to the answer
        """
        # Create the input batch
        batch = self.textData.sentence2enco(question)
        if not batch:
            return None
        if questionSeq is not None:  # If the caller want to have the real input
            questionSeq.extend(batch.encoderSeqs)

        # Run the model
        ops, feedDict = self.model.step(batch)
        output = self.sess.run(ops[0], feedDict)  # TODO: Summarize the output too (histogram, ...)
        answer = self.textData.deco2sentence(output)

        return answer

    def daemonPredict(self, sentence):
        """ Return the answer to a given sentence (same as singlePredict() but with additional cleaning)
        Args:
            sentence (str): the raw input sentence
        Return:
            str: the human readable sentence
        """
        return self.textData.sequence2str(
            self.singlePredict(sentence),
            clean=True
        )

    def daemonClose(self):
        """ A utility function to close the daemon when finish
        """
        print('Exiting the daemon mode...')
        self.sess.close()
        print('Daemon closed.')

    def loadEmbedding(self, sess):
        """ Initialize embeddings with pre-trained word2vec vectors
        Will modify the embedding weights of the current loaded model
        Uses the GoogleNews pre-trained values (path hardcoded)
        """

        # Fetch embedding variables from model
        with tf.variable_scope("embedding_rnn_seq2seq/rnn/embedding_wrapper", reuse=True):
            em_in = tf.get_variable("embedding")
        with tf.variable_scope("embedding_rnn_seq2seq/embedding_rnn_decoder", reuse=True):
            em_out = tf.get_variable("embedding")

        # Disable training for embeddings
        variables = tf.get_collection_ref(tf.GraphKeys.TRAINABLE_VARIABLES)
        variables.remove(em_in)
        variables.remove(em_out)

        # If restoring a model, we can leave here
        if self.globStep != 0:
            return

        # New model, we load the pre-trained word2vec data and initialize embeddings
        embeddings_path = os.path.join(self.rootDir, 'data', 'embeddings', self.embeddingSource)
        embeddings_format = os.path.splitext(embeddings_path)[1][1:]
        print("Loading pre-trained word embeddings from %s " % embeddings_path)
        with open(embeddings_path, "rb") as f:
            header = f.readline()
            vocab_size, vector_size = map(int, header.split())
            binary_len = np.dtype('float32').itemsize * vector_size
            initW = np.random.uniform(-0.25,0.25,(len(self.textData.word2id), vector_size))
            for line in tqdm(range(vocab_size)):
                word = []
                while True:
                    ch = f.read(1)
                    if ch == b' ':
                        word = b''.join(word).decode('utf-8')
                        break
                    if ch != b'\n':
                        word.append(ch)
                if word in self.textData.word2id:
                    if embeddings_format == 'bin':
                        vector = np.fromstring(f.read(binary_len), dtype='float32')
                    elif embeddings_format == 'vec':
                        vector = np.fromstring(f.readline(), sep=' ', dtype='float32')
                    else:
                        raise Exception("Unkown format for embeddings: %s " % embeddings_format)
                    initW[self.textData.word2id[word]] = vector
                else:
                    if embeddings_format == 'bin':
                        f.read(binary_len)
                    elif embeddings_format == 'vec':
                        f.readline()
                    else:
                        raise Exception("Unkown format for embeddings: %s " % embeddings_format)

        # PCA Decomposition to reduce word2vec dimensionality
        if self.embeddingSize < vector_size:
            U, s, Vt = np.linalg.svd(initW, full_matrices=False)
            S = np.zeros((vector_size, vector_size), dtype=complex)
            S[:vector_size, :vector_size] = np.diag(s)
            initW = np.dot(U[:, :self.embeddingSize], S[:self.embeddingSize, :self.embeddingSize])

        # Initialize input and output embeddings
        sess.run(em_in.assign(initW))
        sess.run(em_out.assign(initW))


    def managePreviousModel(self, sess):
        """ Restore or reset the model, depending of the parameters
        If the destination directory already contains some file, it will handle the conflict as following:
         * If --reset is set, all present files will be removed (warning: no confirmation is asked) and the training
         restart from scratch (globStep & cie reinitialized)
         * Otherwise, it will depend of the directory content. If the directory contains:
           * No model files (only summary logs): works as a reset (restart from scratch)
           * Other model files, but modelName not found (surely keepAll option changed): raise error, the user should
           decide by himself what to do
           * The right model file (eventually some other): no problem, simply resume the training
        In any case, the directory will exist as it has been created by the summary writer
        Args:
            sess: The current running session
        """

        print('WARNING: ', end='')

        modelName = self._getModelName()

        if os.listdir(self.modelDir):
            if self.reset:
                print('Reset: Destroying previous model at {}'.format(self.modelDir))
            # Analysing directory content
            elif os.path.exists(modelName):  # Restore the model
                print('Restoring previous model from {}'.format(modelName))
                self.saver.restore(sess, modelName)  # Will crash when --reset is not activated and the model has not been saved yet
            elif self._getModelList():
                print('Conflict with previous models.')
                raise RuntimeError('Some models are already present in \'{}\'. You should check them first (or re-try with the keepAll flag)'.format(self.modelDir))
            else:  # No other model to conflict with (probably summary files)
                print('No previous model found, but some files found at {}. Cleaning...'.format(self.modelDir))  # Warning: No confirmation asked
                self.reset = True

            if self.reset:
                fileList = [os.path.join(self.modelDir, f) for f in os.listdir(self.modelDir)]
                for f in fileList:
                    print('Removing {}'.format(f))
                    os.remove(f)

        else:
            print('No previous model found, starting from clean directory: {}'.format(self.modelDir))

    def _saveSession(self, sess):
        """ Save the model parameters and the variables
        Args:
            sess: the current session
        """
        tqdm.write('Checkpoint reached: saving model (don\'t stop the run)...')
        self.saveModelParams()
        model_name = self._getModelName()
        with open(model_name, 'w') as f:  # HACK: Simulate the old model existance to avoid rewriting the file parser
            f.write('This file is used internally by Deep Conversation to check the model existance. Please do not remove.\n')
        self.saver.save(sess, model_name)  # TODO: Put a limit size (ex: 3GB for the modelDir)
        tqdm.write('Model saved.')

    def _getModelList(self):
        """ Return the list of the model files inside the model directory
        """
        return [os.path.join(self.modelDir, f) for f in os.listdir(self.modelDir) if f.endswith(self.MODEL_EXT)]

    def loadModelParams(self):
        """ Load the some values associated with the current model, like the current globStep value
        For now, this function does not need to be called before loading the model (no parameters restored). However,
        the modelDir name will be initialized here so it is required to call this function before managePreviousModel(),
        _getModelName() or _getSummaryName()
        Warning: if you modify this function, make sure the changes mirror saveModelParams, also check if the parameters
        should be reset in managePreviousModel
        """
        # Compute the current model path
        self.modelDir = os.path.join(self.rootDir, self.MODEL_DIR_BASE)
        if self.modelTag:
            self.modelDir += '-' + self.modelTag

        # If there is a previous model, restore some parameters
        configName = os.path.join(self.modelDir, self.CONFIG_FILENAME)
        if not self.reset and not self.createDataset and os.path.exists(configName):
            # Loading
            config = configparser.ConfigParser()
            config.read(configName)

            # Check the version
            currentVersion = config['General'].get('version')
            if currentVersion != self.CONFIG_VERSION:
                raise UserWarning('Present configuration version {0} does not match {1}. You can try manual changes on \'{2}\''.format(currentVersion, self.CONFIG_VERSION, configName))

            # Restoring the the parameters
            self.globStep = config['General'].getint('globStep')
            self.watsonMode = config['General'].getboolean('watsonMode')
            self.autoEncode = config['General'].getboolean('autoEncode')
            self.corpus = config['General'].get('corpus')

            self.datasetTag = config['Dataset'].get('datasetTag')
            self.maxLength = config['Dataset'].getint('maxLength')  # We need to restore the model length because of the textData associated and the vocabulary size (TODO: Compatibility mode between different maxLength)
            self.filterVocab = config['Dataset'].getint('filterVocab')
            self.skipLines = config['Dataset'].getboolean('skipLines')
            self.vocabularySize = config['Dataset'].getint('vocabularySize')

            self.hiddenSize = config['Network'].getint('hiddenSize')
            self.numLayers = config['Network'].getint('numLayers')
            self.softmaxSamples = config['Network'].getint('softmaxSamples')
            self.initEmbeddings = config['Network'].getboolean('initEmbeddings')
            self.embeddingSize = config['Network'].getint('embeddingSize')
            self.embeddingSource = config['Network'].get('embeddingSource')

            # No restoring for training params, batch size or other non model dependent parameters

            # Show the restored params
            print()
            print('Warning: Restoring parameters:')
            print('globStep: {}'.format(self.globStep))
            print('watsonMode: {}'.format(self.watsonMode))
            print('autoEncode: {}'.format(self.autoEncode))
            print('corpus: {}'.format(self.corpus))
            print('datasetTag: {}'.format(self.datasetTag))
            print('maxLength: {}'.format(self.maxLength))
            print('filterVocab: {}'.format(self.filterVocab))
            print('skipLines: {}'.format(self.skipLines))
            print('vocabularySize: {}'.format(self.vocabularySize))
            print('hiddenSize: {}'.format(self.hiddenSize))
            print('numLayers: {}'.format(self.numLayers))
            print('softmaxSamples: {}'.format(self.softmaxSamples))
            print('initEmbeddings: {}'.format(self.initEmbeddings))
            print('embeddingSize: {}'.format(self.embeddingSize))
            print('embeddingSource: {}'.format(self.embeddingSource))
            print()

        # For now, not arbitrary  independent maxLength between encoder and decoder
        self.maxLengthEnco = self.maxLength
        self.maxLengthDeco = self.maxLength + 2

        if self.watsonMode:
            self.SENTENCES_PREFIX.reverse()


    def saveModelParams(self):
        """ Save the params of the model, like the current globStep value
        Warning: if you modify this function, make sure the changes mirror loadModelParams
        """
        config = configparser.ConfigParser()
        config['General'] = {}
        config['General']['version']  = self.CONFIG_VERSION
        config['General']['globStep']  = str(self.globStep)
        config['General']['watsonMode'] = str(self.watsonMode)
        config['General']['autoEncode'] = str(self.autoEncode)
        config['General']['corpus'] = str(self.corpus)

        config['Dataset'] = {}
        config['Dataset']['datasetTag'] = str(self.datasetTag)
        config['Dataset']['maxLength'] = str(self.maxLength)
        config['Dataset']['filterVocab'] = str(self.filterVocab)
        config['Dataset']['skipLines'] = str(self.skipLines)
        config['Dataset']['vocabularySize'] = str(self.vocabularySize)

        config['Network'] = {}
        config['Network']['hiddenSize'] = str(self.hiddenSize)
        config['Network']['numLayers'] = str(self.numLayers)
        config['Network']['softmaxSamples'] = str(self.softmaxSamples)
        config['Network']['initEmbeddings'] = str(self.initEmbeddings)
        config['Network']['embeddingSize'] = str(self.embeddingSize)
        config['Network']['embeddingSource'] = str(self.embeddingSource)

        # Keep track of the learning params (but without restoring them)
        config['Training (won\'t be restored)'] = {}
        config['Training (won\'t be restored)']['learningRate'] = str(self.learningRate)
        config['Training (won\'t be restored)']['batchSize'] = str(self.batchSize)
        config['Training (won\'t be restored)']['dropout'] = str(self.dropout)

        with open(os.path.join(self.modelDir, self.CONFIG_FILENAME), 'w') as configFile:
            config.write(configFile)

    def _getSummaryName(self):
        """ Parse the argument to decide were to save the summary, at the same place that the model
        The folder could already contain logs if we restore the training, those will be merged
        Return:
            str: The path and name of the summary
        """
        return self.modelDir

    def _getModelName(self):
        """ Parse the argument to decide were to save/load the model
        This function is called at each checkpoint and the first time the model is load. If keepAll option is set, the
        globStep value will be included in the name.
        Return:
            str: The path and name were the model need to be saved
        """
        modelName = os.path.join(self.modelDir, self.MODEL_NAME_BASE)
        if self.keepAll:  # We do not erase the previously saved model by including the current step on the name
            modelName += '-' + str(self.globStep)
        return modelName + self.MODEL_EXT

    def getDevice(self):
        """ Parse the argument to decide on which device run the model
        Return:
            str: The name of the device on which run the program
        """
        if self.device == 'cpu':
            return '/cpu:0'
        elif self.device == 'gpu':
            return '/gpu:0'
        elif self.device is None:  # No specified device (default)
            return None
        else:
            print('Warning: Error in the device name: {}, use the default device'.format(self.device))
            return None


if __name__ == "__main__":
    dc = DeepConversation()
    print(dc.respond("What color?"))
    print(dc.respond("What is immoral?"))
    print(dc.respond("Are you evil?"))
    print(dc.respond("Are you happy?"))
