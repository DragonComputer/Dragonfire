from __future__ import absolute_import, print_function

import audioop  # Operates on sound fragments consisting of signed integer samples 8, 16 or 32 bits wide, stored in Python strings.
import datetime  # Supplies classes for manipulating dates and times in both simple and complex ways
import multiprocessing  # A package that supports spawning processes using an API similar to the threading module.
import os  # The path module suitable for the operating system Python is running on, and therefore usable for local paths
# import peakutils.peak # Peak detection utilities for 1D data
import random  # Pseudo-random number generators for various distributions
import time  # Provides various time-related functions.
import Tkinter  # Python's de-facto standard GUI (Graphical User Interface) package
import wave  # Provides a convenient interface to the WAV sound format

import matplotlib.pyplot as plt  # Simple graph plotting library
import numpy  # The fundamental package for scientific computing with Python.
import pyaudio  # Provides Python bindings for PortAudio, the cross platform audio API
import pyqtgraph as pg  # A pure-python graphics and GUI library built on PyQt4 / PySide and numpy
from PyQt4 import QtCore  # A comprehensive set of Python bindings for Digia's Qt cross platform GUI toolkit.

from .nnet import RNN  # Import the Recurrent Neural Network class from Dragonfire's Neural Network Library

__author__ = 'Mehmet Mert Yildiran, mert.yildiran@bil.omu.edu.tr'
# This submodule is experimental and not functional


CHUNK = 1024 # Smallest unit of audio. 1024 bytes
FORMAT = pyaudio.paInt16 # Data format
CHANNELS = 2 # Number of channels
RATE = 44100 # Bit Rate of audio stream / Frame Rate
THRESHOLD = 1000 # Threshhold value for detecting stimulant
SILENCE_DETECTION = 5 # Wait number of frames to decide whether it fell silent or not
EMPTY_CHUNK = chr(int('000000', 2)) * CHUNK * 4 # Create an empty unit of audio for just once
WAVE_OUTPUT_FILENAME = "/tmp/" +  str(datetime.date.today()) + ".wav" # Example path if saving needed
TRAINING_DATA_DIRECTORY = "training_data/"
PLOTS_DIRECTORY = "plots/" # Directory to save the plots
OUT_DIRECTORY = "out/" # Output directory for training results (model.npz & words.txt)
root = Tkinter.Tk()
SCREEN_WIDTH = root.winfo_screenwidth()
SCREEN_HEIGHT = root.winfo_screenheight()
HIDDEN_NEURON = 20 # Hidden neuron count in the network
REPEAT_N_TIMES = 10 # How many times repeated? For 3 for example; one, one, one, two, two, two, three, ...
TRAINING_ITERATION = 1000 # How many iterations for training

try:
    raw_input          # Python 2
except NameError:
    raw_input = input  # Python 3
try:
    xrange             # Python 2
except NameError:
    xrange = range     # Python 3


class SpeechRecognition():

	# A function that will save recordings to a file
	@staticmethod
	def save_file(frames):
		p = pyaudio.PyAudio() # Create a PyAudio session
		if not os.path.isfile(WAVE_OUTPUT_FILENAME): # If there is not such a file
			wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb') # Create the file
			wf.setnchannels(CHANNELS) # Set number of channels
			wf.setsampwidth(p.get_sample_size(FORMAT)) # Set sampling format
			wf.setframerate(RATE) # Set Bit Rate / Frame Rate
			wf.writeframes("") # Write nothing
			wf.close() # Close the session

		wf = wave.open(WAVE_OUTPUT_FILENAME, 'rb') # Open the file with only read permission
		n_frames = wf.getnframes() # Get all frames in it
		previous_wav = wf.readframes(n_frames) # Assign all frames to a variable
		wf.close() # Close the session

		wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb') # Open the file with write permission
		wf.setnchannels(CHANNELS) # Set number of channels
		wf.setsampwidth(p.get_sample_size(FORMAT)) # Set sampling format
		wf.setframerate(RATE) # Set Bit Rate / Frame Rate
		wf.writeframes(previous_wav + b''.join(frames)) # Write the all frames including previous ones
		wf.close() # Close the session

	@staticmethod
	def save_training_data(training_data,words):
		file_id = str(random.randint(100000,999999)) # Random file ID
		if not os.path.exists(TRAINING_DATA_DIRECTORY): # Check whether the directory is exist or not
			os.makedirs(TRAINING_DATA_DIRECTORY) # If there is none then create one
		p = pyaudio.PyAudio() # Create a PyAudio session
		wf = wave.open(TRAINING_DATA_DIRECTORY + file_id + ".wav", 'wb') # Create the .wav file with a random name
		wf.setnchannels(CHANNELS) # Set number of channels
		wf.setsampwidth(p.get_sample_size(FORMAT)) # Set sampling format
		wf.setframerate(RATE) # Set Bit Rate / Frame Rate
		wf.writeframes(''.join(training_data)) # Write the all frames of training_data
		wf.close() # Close the session

		with open(TRAINING_DATA_DIRECTORY + file_id + ".txt", "w") as thefile:
			for word in words:
				thefile.write("%s\n" % word)

	# A function that will compute frequency of chunk using Fourier Transform
	@staticmethod
	def find_frequency(data):
		T = 1.0/RATE # Reciprocal of Bit Rate
		N = data.shape[0] # Number of rows in data(numpy array)
		Pxx = (1./N)*numpy.fft.fft(data) # Compute the one-dimensional n-point discrete Fourier Transform (DFT) of data with the efficient Fast Fourier Transform (FFT) algorithm [CT]
		f = numpy.fft.fftfreq(N,T) # Return the Discrete Fourier Transform sample frequencies
		Pxx = numpy.fft.fftshift(Pxx) # Shift the zero-frequency component to the center of the spectrum
		f = numpy.fft.fftshift(f) # Shift the zero-frequency component to the center of the spectrum
		return f, Pxx # Return the results

	# A function that will draw a spectrum analyzer graphic to screen (PyQtGraph)
	@staticmethod
	def draw_spectrum_analyzer(all_frames, thresh_frames):
		time.sleep(1) # Wait just one second
		pw = pg.plot(title="Spectrum Analyzer") # Window title
		pg.setConfigOptions(antialias=True) # Enable antialias for better resolution
		pw.win.resize(1600, 300) # Define window size
		pw.win.move(160 * SCREEN_WIDTH / 1920, 500 * SCREEN_HEIGHT / 1080) # Define window position
		while True: # Loop over the frames of the audio / data chunks
			data = ''.join(all_frames[-1:]) # Get only the last frame of all frames
			data = numpy.fromstring(data, 'int16') # Binary string to numpy int16 data format
			pw.setMouseEnabled(y=False) # Disable mouse
			pw.setYRange(0,1000) # Set Y range of graph
			pw.setXRange(-(RATE/2), (RATE/2), padding=0) # Set X range of graph relative to Bit Rate
			pwAxis = pw.getAxis("bottom") # Get bottom axis
			pwAxis.setLabel("Frequency [Hz]") # Set bottom axis label
			f, Pxx = SpeechRecognition.find_frequency(data) # Call find frequency function. f is frequency, Pxx is energy.
			Pxx = numpy.absolute(Pxx) # Calculate the absolute value element-wise. (complex input a + ib to sqrt(a^2 + b^2))
			#peak_indexes = peakutils.peak.indexes(Pxx, thres=50.0/max(Pxx), min_dist=5) # Find the peaks. thres (energy threshold) is a rational value in here like 10/2000 on y-axis. min_dist is the minimum distance criteria for the peaks on x-axis.
			#peak_indexes = peak_indexes.tolist() # Numpy array to list
			#peak_values = list(Pxx[peak_indexes]) # Automatically map into list using peak indexes
			#peak_indexes = list(f[peak_indexes]) # Automatically map into list using peak indexes
			f = f.tolist() # Numpy array to list
			Pxx = Pxx.tolist() # Numpy array to list
			try: # Try this block
				if thresh_frames[-1:][0] == EMPTY_CHUNK: # If last thresh frame is equal to EMPTY CHUNK
					pw.plot(x=f,y=Pxx, clear=True, pen=pg.mkPen('w', width=1.0, style=QtCore.Qt.SolidLine)) # Then plot with white pen
				else: # If last thresh frame is not equal to EMPTY CHUNK
					pw.plot(x=f,y=Pxx, clear=True, pen=pg.mkPen('y', width=1.0, style=QtCore.Qt.SolidLine)) # Then plot with yellow pen
					#pw.plot(x=peak_indexes, y=peak_values, pen=None, symbol='t') # Draw a scatter plot to the peak points
					#pw.plot(x=peak_indexes, y=peak_values, pen=pg.mkPen('b', width=0.5, style=QtCore.Qt.SolidLine)) # Draw faint lines between the peak poits
			except IndexError: # If we are getting an IndexError because of this -> thresh_frames[-1:][0]
				pw.plot(x=f,y=Pxx, clear=True, pen=pg.mkPen('w', width=1.0, style=QtCore.Qt.SolidLine)) # Then plot with white pen
			pg.QtGui.QApplication.processEvents() # ???
			time.sleep(0.03) # Wait a few miliseconds

	# A function that will draw a waveform graphic to screen (PyQtGraph)
	@staticmethod
	def draw_waveform(all_frames, thresh_frames):
		time.sleep(1) # Wait just one second
		pw = pg.plot(title="Waveform") # Window title
		pg.setConfigOptions(antialias=True) # Enable antialias for better resolution
		pw.win.resize(1300, 160) # Define window size
		pw.win.move(300 * SCREEN_WIDTH / 1920, 850 * SCREEN_HEIGHT / 1080) # Define window position
		pw.showAxis('bottom', False) # Hide bottom axis
		while True: # Loop over the frames of the audio / data chunks
			data = ''.join(all_frames[-20:]) # Join last 20 frames of all frames
			data = numpy.fromstring(data, 'int16') # Binary string to numpy int16 data format
			data2 = ''.join(thresh_frames[-20:]) # Join last 20 frames of thrsh frames
			data2 = numpy.fromstring(data2, 'int16') # Binary string to numpy int16 data format
			pw.setMouseEnabled(x=False) # Disable mouse
			pw.setRange(yRange=[-10000,10000]) # Set Y range of graph
			pw.plot(data, clear=True, pen=pg.mkPen('w', width=0.5, style=QtCore.Qt.DotLine)) # Plot all frames with white pen
			pw.plot(data2, pen=pg.mkPen('y', width=0.5, style=QtCore.Qt.DotLine)) # Plot thresh frames with yellow pen
			text = pg.TextItem("Seconds : " + str(int(len(all_frames)/(RATE/CHUNK))), color=(255, 255, 255)) # Define seconds according to number of total frames as a text
			pw.addItem(text) # Display seconds according to number of total frames
			text.setPos(500, 0) # Set text position
			pg.QtGui.QApplication.processEvents()
			time.sleep(0.03) # Wait a few miliseconds

	# MAIN CODE BLOCK
	@staticmethod
	def start(audio_input,graphs=True,verbose=True):
		words = []
		txt_path = os.path.join(OUT_DIRECTORY, "words.txt")
		with open(txt_path) as f:
			words = words + [x.strip() for x in f.readlines()] # Load words from words.txt into an array
		rnn = RNN(CHUNK*2, HIDDEN_NEURON, len(words)) # Create a Recurrent Neural Network instance (input,hidden,output)
		rnn.importdump(OUT_DIRECTORY + "model.npz") # Import the dump

		if audio_input == "0":
			pass
		else:
			wf = wave.open(audio_input, 'rb') # Open .wav file from given path as audio_input in arguments

		p = pyaudio.PyAudio() # Create a PyAudio session
		# Create a stream
		if audio_input == "0":
			stream = p.open(format=FORMAT,
						channels=CHANNELS,
						rate=RATE,
						input=True,
						frames_per_buffer=CHUNK)
		else:
			stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
						channels=wf.getnchannels(),
						rate=wf.getframerate(),
						output=True)

		all_frames = []
		thresh_frames = []
		if graphs:
			shared_memory = multiprocessing.Manager() # Shared memory space manager
			all_frames = shared_memory.list() # Define all_frames array in shared memory
			thresh_frames = shared_memory.list() # Define thresh_frames array in shared memory

		if audio_input == "0":
			data = stream.read(CHUNK) # Get first data frame from the microphone
		else:
			data = wf.readframes(CHUNK) # Get first data frame from .wav file

		all_frames.append(data) # Append to all frames
		thresh_frames.append(EMPTY_CHUNK) # Append an EMPTY CHUNK to thresh frames

		if graphs:
			process1 = multiprocessing.Process(target=SpeechRecognition.draw_waveform, args=(all_frames, thresh_frames)) # Define draw waveform process
			process1.start() # Start draw waveform process

			process2 = multiprocessing.Process(target=SpeechRecognition.draw_spectrum_analyzer, args=(all_frames, thresh_frames)) # Define draw spectrum analyzer process
			process2.start() # Start drar spectrum analyzer process

		# Loop over the frames of the audio / data chunks
		while data != '':
			previous_data = data # Get previous chunk that coming from end of the loop

			if audio_input == "0":
				data = stream.read(CHUNK) # Read a new chunk from the stream
			else:
				if graphs:
					stream.write(data) # Monitor current chunk
				data = wf.readframes(CHUNK) # Read a new chunk from the stream

			all_frames.append(data) # Append this chunk to all frames
			thresh_frames.append(EMPTY_CHUNK) # Append an EMPTY CHUNK to thresh frames

			rms = audioop.rms(data, 2) # Calculate Root Mean Square of current chunk
			word_data = [] # Define single word data
			if rms >= THRESHOLD: # If Root Mean Square value is greater than THRESHOLD constant
				#starting_time = datetime.datetime.now() # Starting time of the word
				thresh_frames.pop() # Pop out last frame of thresh frames
				thresh_frames.pop() # Pop out last frame of thresh frames
				word_data.append(previous_data) # Append previous chunk to training data
				word_data.append(data) # Append current chunk to training data
				thresh_frames.append(previous_data) # Append previous chunk to thresh frames
				thresh_frames.append(data) # Append current chunk to thresh frames
				silence_counter = 0 # Define silence counter
				while silence_counter < SILENCE_DETECTION: # While silence counter value less than SILENCE_DETECTION constant

					if audio_input == "0":
						data = stream.read(CHUNK) # Read a new chunk from the stream
					else:
						if graphs:
							stream.write(data) # Monitor current chunk
						data = wf.readframes(CHUNK) # Read a new chunk from the stream

					all_frames.append(data) # Append this chunk to all frames
					word_data.append(data) # Append this chunk to training data
					thresh_frames.append(data) # Append this chunk to thresh frames
					rms = audioop.rms(data, 2) # Calculate Root Mean Square of current chunk again

					if rms < THRESHOLD: # If Root Mean Square value is less than THRESHOLD constant
						silence_counter += 1 # Then increase silence counter
					else: # Else
						silence_counter = 0 # Assign zero value to silence counter

				#del word_data[-(SILENCE_DETECTION-2):] # Delete last frames of training data as much as SILENCE_DETECTION constant
				#del thresh_frames[-(SILENCE_DETECTION-2):] # Delete last frames of thresh frames as much as SILENCE_DETECTION constant
				#for i in range(SILENCE_DETECTION-2): # SILENCE_DETECTION constant times
				#	thresh_frames.append(EMPTY_CHUNK) # Append an EMPTY_CHUNK
				#ending_time = datetime.datetime.now() # Ending time of the training
				for i in xrange(len(word_data)):
					word_data[i] = numpy.fromstring(word_data[i], 'int16') # Convert each frame from binary string to int16
				word_data = numpy.asarray(word_data) # Convert the word data into numpy array
				word_data = word_data / word_data.max() # Normalize the input
				output = rnn.run(word_data) # Run the network to get the output/result (feedforward)
				print(words[numpy.argmax(output)] + '\t\t', output) # Print the best guess


		if graphs:
			process1.terminate() # Terminate draw waveform process
			process2.terminate() # Terminate drar spectrum analyzer process
		stream.stop_stream() # Stop the stream
		stream.close() # Close the stream
		p.terminate() # Terminate the session

	@staticmethod
	def _teststart():
		rnn = RNN(2048, HIDDEN_NEURON, 5)
		rnn.importdump("out/model.npz")
		words_data = []
		words = []
		for filename in os.listdir(TRAINING_DATA_DIRECTORY):
			if filename.endswith(".wav"):
				wav_path = os.path.join(TRAINING_DATA_DIRECTORY, filename)
				words_data = words_data + SpeechRecognition.extract_words_from_audio(wav_path)
				txt_path = os.path.join(TRAINING_DATA_DIRECTORY, filename[:-4] + ".txt")
				with open(txt_path) as f:
					words = words + [x.strip() for x in f.readlines()]
		for i in xrange(len(words_data)):
			for j in xrange(len(words_data[i])):
				words_data[i][j] = numpy.fromstring(words_data[i][j], 'int16') # Convert each frame from binary string to int16
			words_data[i] = numpy.asarray(words_data[i]) # Convert the word data into numpy array
			words_data[i] = words_data[i] / words_data[i].max() # Normalize the input
		for i in xrange(len(words_data)):
			print(words[i/REPEAT_N_TIMES] + '\t\t', rnn.run(words_data[i]))

	@staticmethod
	def extract_words_from_audio(audio_input,graphs=False,verbose=False):
		try:
			if audio_input == "0":
				pass
			else:
				wf = wave.open(audio_input, 'rb') # Open .wav file from given path as audio_input in arguments

			p = pyaudio.PyAudio() # Create a PyAudio session
			# Create a stream
			if audio_input == "0":
				stream = p.open(format=FORMAT,
							channels=CHANNELS,
							rate=RATE,
							input=True,
							frames_per_buffer=CHUNK)
			else:
				stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
							channels=wf.getnchannels(),
							rate=wf.getframerate(),
							output=True)

			words_data = [] # Define words data array
			all_frames = []
			thresh_frames = []
			if graphs:
				shared_memory = multiprocessing.Manager() # Shared memory space manager
				all_frames = shared_memory.list() # Define all_frames array in shared memory
				thresh_frames = shared_memory.list() # Define thresh_frames array in shared memory

			if audio_input == "0":
				data = stream.read(CHUNK) # Get first data frame from the microphone
			else:
				data = wf.readframes(CHUNK) # Get first data frame from .wav file

			all_frames.append(data) # Append to all frames
			thresh_frames.append(EMPTY_CHUNK) # Append an EMPTY CHUNK to thresh frames

			if graphs:
				process1 = multiprocessing.Process(target=SpeechRecognition.draw_waveform, args=(all_frames, thresh_frames)) # Define draw waveform process
				process1.start() # Start draw waveform process

				process2 = multiprocessing.Process(target=SpeechRecognition.draw_spectrum_analyzer, args=(all_frames, thresh_frames)) # Define draw spectrum analyzer process
				process2.start() # Start drar spectrum analyzer process

			# Loop over the frames of the audio / data chunks
			while data != '':
				previous_data = data # Get previous chunk that coming from end of the loop

				if audio_input == "0":
					data = stream.read(CHUNK) # Read a new chunk from the stream
				else:
					if graphs:
						stream.write(data) # Monitor current chunk
					data = wf.readframes(CHUNK) # Read a new chunk from the stream

				all_frames.append(data) # Append this chunk to all frames
				thresh_frames.append(EMPTY_CHUNK) # Append an EMPTY CHUNK to thresh frames

				rms = audioop.rms(data, 2) # Calculate Root Mean Square of current chunk
				word_data = [] # Define single word data
				if rms >= THRESHOLD: # If Root Mean Square value is greater than THRESHOLD constant
					#starting_time = datetime.datetime.now() # Starting time of the word
					thresh_frames.pop() # Pop out last frame of thresh frames
					thresh_frames.pop() # Pop out last frame of thresh frames
					word_data.append(previous_data) # Append previous chunk to training data
					word_data.append(data) # Append current chunk to training data
					thresh_frames.append(previous_data) # Append previous chunk to thresh frames
					thresh_frames.append(data) # Append current chunk to thresh frames
					silence_counter = 0 # Define silence counter
					while silence_counter < SILENCE_DETECTION: # While silence counter value less than SILENCE_DETECTION constant

						if audio_input == "0":
							data = stream.read(CHUNK) # Read a new chunk from the stream
						else:
							if graphs:
								stream.write(data) # Monitor current chunk
							data = wf.readframes(CHUNK) # Read a new chunk from the stream

						all_frames.append(data) # Append this chunk to all frames
						word_data.append(data) # Append this chunk to training data
						thresh_frames.append(data) # Append this chunk to thresh frames
						rms = audioop.rms(data, 2) # Calculate Root Mean Square of current chunk again

						if rms < THRESHOLD: # If Root Mean Square value is less than THRESHOLD constant
							silence_counter += 1 # Then increase silence counter
						else: # Else
							silence_counter = 0 # Assign zero value to silence counter

					#del word_data[-(SILENCE_DETECTION-2):] # Delete last frames of training data as much as SILENCE_DETECTION constant
					#del thresh_frames[-(SILENCE_DETECTION-2):] # Delete last frames of thresh frames as much as SILENCE_DETECTION constant
					#for i in range(SILENCE_DETECTION-2): # SILENCE_DETECTION constant times
					#	thresh_frames.append(EMPTY_CHUNK) # Append an EMPTY_CHUNK
					#ending_time = datetime.datetime.now() # Ending time of the training
					words_data.append(word_data)
					if verbose:
						print(len(words_data))


			if graphs:
				process1.terminate() # Terminate draw waveform process
				process2.terminate() # Terminate drar spectrum analyzer process
			stream.stop_stream() # Stop the stream
			stream.close() # Close the stream
			p.terminate() # Terminate the session
			return words_data
		except KeyboardInterrupt: # We will use KeyboardInterrupt to finish the microphone session
			if graphs:
				process1.terminate() # Terminate draw waveform process
				process2.terminate() # Terminate drar spectrum analyzer process
			stream.stop_stream() # Stop the stream
			stream.close() # Close the stream
			p.terminate() # Terminate the session
			return words_data

	@staticmethod
	def create_training_data(audio_input,graphs=True,verbose=True):
		try:
			words_data = SpeechRecognition.extract_words_from_audio(audio_input,graphs,verbose)
		except KeyboardInterrupt:
			pass
		else:
			words = raw_input("Enter the words separating them by comma(,): ").split(',')
			if len(words) == (len(words_data)/REPEAT_N_TIMES):
				training_data = [frame for word_data in words_data for frame in word_data] # Flatten the words data into single big array of frames
				SpeechRecognition.save_training_data(training_data,words) # Then save it
			else:
				print("Sorry, word counts don't match. Please try again.")

	@staticmethod
	def load_training_data():
		words_data = []
		words = []
		for filename in os.listdir(TRAINING_DATA_DIRECTORY):
			if filename.endswith(".wav"):
				wav_path = os.path.join(TRAINING_DATA_DIRECTORY, filename)
				words_data = words_data + SpeechRecognition.extract_words_from_audio(wav_path)
				txt_path = os.path.join(TRAINING_DATA_DIRECTORY, filename[:-4] + ".txt")
				with open(txt_path) as f:
					words = words + [x.strip() for x in f.readlines()]
		return (words_data,words)

	@staticmethod
	def train():
		words_data, words = SpeechRecognition.load_training_data() # Load the training data
		target = numpy.identity(len(words)) # Create a unit matrix (identity matrix) as our target
		ri = []
		for i in xrange(len(words)):
			ri += [i] * REPEAT_N_TIMES
		target = target[ri]
		for i in xrange(len(words_data)):
			for j in xrange(len(words_data[i])):
				words_data[i][j] = numpy.fromstring(words_data[i][j], 'int16') # Convert each frame from binary string to int16
			words_data[i] = numpy.asarray(words_data[i]) # Convert the word data into numpy array
			words_data[i] = words_data[i] / words_data[i].max() # Normalize the input
		rnn = RNN(len(words_data[0][0]), HIDDEN_NEURON, len(words)) # Create a Recurrent Neural Network instance
		#print len(words_data[0][0]), len(words_data)
		#print numpy.asarray(words_data[0]).shape # Input shape
		#print target[0].shape # Target shape
		lr = 0.01 # Learning rate
		e = 1 # Initial error = 1
		vals = [] # Values for plotting
		n_iteration = TRAINING_ITERATION
		for i in xrange(n_iteration): # Iterate (n_iteration) times
			for j in xrange(len(words_data)): # For each word in words
				u = words_data[j] # Input (2048)
				t = target[j] # Target (word count)
				c = rnn.train_step(u, t, lr) # Cost
				print("iteration {0}: {1}".format(i, numpy.sqrt(c)))
				e = (1.0/len(words_data))*numpy.sqrt(c) + ((len(words_data) - 1.0)/len(words_data))*e # Contributes to error 1 / word count
				if i % (n_iteration/100) == 0:
					vals.append(e)

		if not os.path.exists(OUT_DIRECTORY): # Check whether the directory is exist or not
			os.makedirs(OUT_DIRECTORY) # If there is none then create one
		rnn.dump(OUT_DIRECTORY) # Dump model.npz (reusable training result) to out/ directory
		print("The neural network dump saved into: " + OUT_DIRECTORY + "model.npz")

		with open(OUT_DIRECTORY + "words.txt", "w") as thefile:
			for word in words:
				thefile.write("%s\n" % word) # Dump the words line by line
		print("The word list saved into: " + OUT_DIRECTORY + "words.txt")

		plt.plot(vals) # Plot the graph
		if not os.path.exists(PLOTS_DIRECTORY): # Check whether the directory is exist or not
			os.makedirs(PLOTS_DIRECTORY) # If there is none then create one
		plt.savefig(PLOTS_DIRECTORY + 'error.png') # Save the graph
		print("Graph of the decline of error by the time is saved as: " + PLOTS_DIRECTORY + "error.png")

		print("--- TESTING ---")
		del rnn
		rnn = RNN(len(words_data[0][0]), HIDDEN_NEURON, len(words))
		rnn.importdump(OUT_DIRECTORY + "model.npz")
		for i in xrange(len(words_data)):
			print(words[i/REPEAT_N_TIMES] + '\t\t', rnn.run(words_data[i]))


if __name__ == "__main__":
	import argparse # Makes it easy to write user-friendly command-line interfaces.
	ap = argparse.ArgumentParser() # Define an Argument Parser
	ap.add_argument("-a", "--audio", help="path to the audio file") # Add --audio argument
	ap.add_argument("-c", "--create", help="create training data, use with --audio")
	ap.add_argument("-t", "--train", help="train the network, use just by itself")
	args = vars(ap.parse_args()) # Parse the arguments

	if args["train"]:
		SpeechRecognition.train()
	elif args["create"] and args["audio"]:
		SpeechRecognition.create_training_data(args["audio"])
	elif args["audio"]:
		SpeechRecognition.start(args["audio"])
	else:
		print("You tried to use it with a wrong combination. Check out --help")
