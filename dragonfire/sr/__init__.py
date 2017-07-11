__author__ = 'Mehmet Mert Yildiran, mert.yildiran@bil.omu.edu.tr'

import pyaudio # Provides Python bindings for PortAudio, the cross platform audio API
import wave # Provides a convenient interface to the WAV sound format
import datetime # Supplies classes for manipulating dates and times in both simple and complex ways
import os.path # The path module suitable for the operating system Python is running on, and therefore usable for local paths
import audioop # Operates on sound fragments consisting of signed integer samples 8, 16 or 32 bits wide, stored in Python strings.
import numpy # The fundamental package for scientific computing with Python.
import multiprocessing # A package that supports spawning processes using an API similar to the threading module.
import imutils # A series of convenience functions to make basic image processing functions such as translation, rotation, resizing, skeletonization etc.
import pyqtgraph as pg # A pure-python graphics and GUI library built on PyQt4 / PySide and numpy
from PyQt4 import QtCore, QtGui # A comprehensive set of Python bindings for Digia's Qt cross platform GUI toolkit.
import time # Provides various time-related functions.
import Tkinter # Python's de-facto standard GUI (Graphical User Interface) package
import peakutils.peak # Peak detection utilities for 1D data

CHUNK = 1024 # Smallest unit of audio. 1024 bytes
FORMAT = pyaudio.paInt16 # Data format
CHANNELS = 2 # Number of channels
RATE = 44100 # Bit Rate of audio stream / Frame Rate
THRESHOLD = 1000 # Threshhold value for detecting stimulant
SILENCE_DETECTION = 5 # Wait number of frames to decide whether it fell silent or not
EMPTY_CHUNK = chr(int('000000', 2)) * CHUNK * 4 # Create an empty unit of audio for just once
WAVE_OUTPUT_FILENAME = "/tmp/" +  str(datetime.date.today()) + ".wav" # Example path if saving needed
root = Tkinter.Tk()
SCREEN_WIDTH = root.winfo_screenwidth()
SCREEN_HEIGHT = root.winfo_screenheight()

class SpeechRecognition():

	# A function that will save recordings to a file
	@staticmethod
	def save_file():
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
			f, Pxx = SpeechRecognition.find_frequency(data) # Call find frequency function. f is frequency, Pxx is amplitude.
			Pxx = numpy.absolute(Pxx) # Calculate the absolute value element-wise. (complex input a + ib to sqrt(a^2 + b^2))
			peak_indexes = peakutils.peak.indexes(Pxx, thres=50.0/max(Pxx), min_dist=5) # Find the peaks. thres (amplitude threshold) is a rational value in here like 10/2000 on y-axis. min_dist is the minimum distance criteria for the peaks on x-axis.
			peak_indexes = peak_indexes.tolist() # Numpy array to list
			peak_values = list(Pxx[peak_indexes]) # Automatically map into list using peak indexes
			peak_indexes = list(f[peak_indexes]) # Automatically map into list using peak indexes
			f = f.tolist() # Numpy array to list
			Pxx = Pxx.tolist() # Numpy array to list
			try: # Try this block
				if thresh_frames[-1:][0] == EMPTY_CHUNK: # If last thresh frame is equal to EMPTY CHUNK
					pw.plot(x=f,y=Pxx, clear=True, pen=pg.mkPen('w', width=1.0, style=QtCore.Qt.SolidLine)) # Then plot with white pen
				else: # If last thresh frame is not equal to EMPTY CHUNK
					pw.plot(x=f,y=Pxx, clear=True, pen=pg.mkPen('y', width=1.0, style=QtCore.Qt.SolidLine)) # Then plot with yellow pen
					pw.plot(x=peak_indexes, y=peak_values, pen=None, symbol='t') # Draw a scatter plot to the peak points
					pw.plot(x=peak_indexes, y=peak_values, pen=pg.mkPen('b', width=0.5, style=QtCore.Qt.SolidLine)) # Draw faint lines between the peak poits
			except IndexError: # If we are getting an IndexError because of this -> thresh_frames[-1:][0]
				pw.plot(x=f,y=Pxx, clear=True, pen=pg.mkPen('w', width=1.0, style=QtCore.Qt.SolidLine)) # Then plot with white pen
			pg.QtGui.QApplication.processEvents() # ???
			time.sleep(0.016) # Wait a few miliseconds

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
			time.sleep(0.016) # Wait a few miliseconds

	# MAIN CODE BLOCK
	@staticmethod
	def start(audio_input):

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

		shared_memory = multiprocessing.Manager() # Shared memory space manager
		clause_data = [] # Define clause data array
		all_frames = shared_memory.list() # Define all_frames array in shared memory
		thresh_frames = shared_memory.list() # Define thresh_frames array in shared memory

		if audio_input == "0":
			data = stream.read(CHUNK) # Get first data frame from .wav file
		else:
			data = wf.readframes(CHUNK) # Get first data frame from .wav file

		all_frames.append(data) # Append to all frames
		thresh_frames.append(EMPTY_CHUNK) # Append an EMPTY CHUNK to thresh frames

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
				stream.write(data) # Monitor current chunk
				data = wf.readframes(CHUNK) # Read a new chunk from the stream

			all_frames.append(data) # Append this chunk to all frames
			thresh_frames.append(EMPTY_CHUNK) # Append an EMPTY CHUNK to thresh frames

			rms = audioop.rms(data, 2) # Calculate Root Mean Square of current chunk
			if rms >= THRESHOLD: # If Root Mean Square value is greater than THRESHOLD constant
				starting_time = datetime.datetime.now() # Starting time of the clause
				thresh_frames.pop() # Pop out last frame of thresh frames
				thresh_frames.pop() # Pop out last frame of thresh frames
				clause_data.append(previous_data) # Append previous chunk to clause data
				thresh_frames.append(previous_data) # APpend previos chunk to thresh frames
				clause_data.append(data) # Append current chunk to clause data
				thresh_frames.append(data) # Append current chunk to thresh frames
				silence_counter = 0 # Define silence counter
				while silence_counter < SILENCE_DETECTION: # While silence counter value less than SILENCE_DETECTION constant

					if audio_input == "0":
						data = stream.read(CHUNK) # Read a new chunk from the stream
					else:
						stream.write(data) # Monitor current chunk
						data = wf.readframes(CHUNK) # Read a new chunk from the stream

					all_frames.append(data) # Append this chunk to all frames
					clause_data.append(data) # Append this chunk to clause data
					thresh_frames.append(data) # Append this chunk to thresh frames
					rms = audioop.rms(data, 2) # Calculate Root Mean Square of current chunk again

					if rms < THRESHOLD: # If Root Mean Square value is less than THRESHOLD constant
						silence_counter += 1 # Then increase silence counter
					else: # Else
						silence_counter = 0 # Assign zero value to silence counter

				del clause_data[-(SILENCE_DETECTION-2):] # Delete last frames of clause data as much as SILENCE_DETECTION constant
				del thresh_frames[-(SILENCE_DETECTION-2):] # Delete last frames of thresh frames as much as SILENCE_DETECTION constant
				for i in range(SILENCE_DETECTION-2): # SILENCE_DETECTION constant times
					thresh_frames.append(EMPTY_CHUNK) # Append an EMPTY_CHUNK
				ending_time = datetime.datetime.now() # Ending time of the clause

				clause_data = ''.join(clause_data)
				# Handle/Use clause_data
				clause_data = [] # Empty clause data

		process1.terminate() # Terminate draw waveform process
		process2.terminate() # Terminate drar spectrum analyzer process
		stream.stop_stream() # Stop the stream
		stream.close() # Close the stream
		p.terminate() # Terminate the session


if __name__ == "__main__":
	import argparse # Makes it easy to write user-friendly command-line interfaces.
	ap = argparse.ArgumentParser() # Define an Argument Parser
	ap.add_argument("-a", "--audio", help="path to the audio file") # Add --audio argument
	args = vars(ap.parse_args()) # Parse the arguments

	SpeechRecognition.start(args["audio"])
