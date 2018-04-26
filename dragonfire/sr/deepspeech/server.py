from deepspeech.model import Model
from .config import ConfigDeepSpeech

# These constants control the beam search decoder

# Beam width used in the CTC decoder when building candidate transcriptions
BEAM_WIDTH = 500

# The alpha hyperparameter of the CTC decoder. Language Model weight
LM_WEIGHT = 1.75

# The beta hyperparameter of the CTC decoder. Word insertion weight (penalty)
WORD_COUNT_WEIGHT = 1.00

# Valid word insertion weight. This is used to lessen the word insertion penalty
# when the inserted word is part of the vocabulary
VALID_WORD_COUNT_WEIGHT = 1.00


# These constants are tied to the shape of the graph used (changing them changes
# the geometry of the first layer), so make sure you use the same constants that
# were used during training

# Number of MFCC features to use
N_FEATURES = 26

# Size of the context window used for producing timesteps in the input vector
N_CONTEXT = 9


class SpeechServerMain:
    name = 'speech_server_main'
    conf = ConfigDeepSpeech()
    model = conf.get_config('model')
    alphabet = conf.get_config('alphabet')
    lm = conf.get_config('lm')
    trie = conf.get_config('trie')

    ds = Model(model, N_FEATURES, N_CONTEXT, alphabet, BEAM_WIDTH)
    if lm and trie:
        ds.enableDecoderWithLM(alphabet, lm, trie, LM_WEIGHT, WORD_COUNT_WEIGHT, VALID_WORD_COUNT_WEIGHT)

    def ready(self):
        print("Deepspeech Server Initialization")
