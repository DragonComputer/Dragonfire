#! /usr/bin/python -u
# (Note: The -u disables buffering, as else we don't get Julius's output.)
#
# Command and Control Application for Julius
#
# How to use it:
#  julius -quiet -input mic -C julian.jconf 2>/dev/null | ./command.py
#
# Copyright (C) 2008, 2009 Siegfried-Angel Gevatter Pujals <rainct@ubuntu.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Supported commands:
#
# This file is provided as an example, and should be modified to suit
# your needs. As is, it only supports a few commands and executes them on
# either Rhythmbox or Banshee.

import sys
import os

class Rhythmbox:
	
	name = "Rhythmbox"
	
	commands = {
			'play': 'play',
			'pause': 'pause',
			'next': 'next',
			'prev': 'previous',
			'show': 'notify',
			'pause': 'pause',
			'silence': 'pause',
	}
	
	def parse(self, word):
		if word in self.commands:
			return 'rhythmbox-client --%s' % self.commands[word]

class Banshee:
	
	name = "Banshee"
	
	commands = {
			'play': 'play',
			'pause': 'pause',
			'stop': 'stop',
			'next': 'next',
			'prev': 'previous',
			'pause': 'pause',
			'silence': 'pause',
	}
	
	def parse(self, word):
		if word in self.commands:
			return 'banshee --no-present --%s %% ' % self.commands[word]

class CommandAndControl:
	
	def __init__(self, file_object):
		
		# Determine which media player to use
		if os.system('ps xa | grep -v grep | grep banshee >/dev/null') == 0:
			self.mediaplayer = Banshee()
		elif os.system('ps xa | grep -v grep | grep rhythmbox >/dev/null') == 0:
			self.mediaplayer = Rhythmbox()
		elif os.system('which banshee >/dev/null') == 0:
			self.mediaplayer = Banshee()
			os.system('bash -c "nohup banshee >/dev/null 2>&1 <&1 & disown %%"')
		elif os.system('which rhythmbox >/dev/null') == 0:
			self.mediaplayer = Rhythmbox()
		else:
			print 'Couldn\'t find a supported media player. ' \
				'Please install Rhythmbox or Banshee.'
			sys.exit(1)
		print 'Taking control of %s media player.' % self.mediaplayer.name
		
		startstring = 'sentence1: <s> '
		endstring = ' </s>'
		
		while 1:
			line = file_object.readline()
			if not line:
				break
			if 'missing phones' in line.lower():
				print 'Error: Missing phonemes for the used grammar file.'
				sys.exit(1)
			if line.startswith(startstring) and line.strip().endswith(endstring):
				self.parse(line.strip('\n')[len(startstring):-len(endstring)])
	
	def parse(self, line):
		# Parse the input
		params = [param.lower() for param in line.split() if param]
		if not '-q' in sys.argv and not '--quiet' in sys.argv:
			print 'Recognized input:', ' '.join(params).capitalize()
		
		# Execute the command, if recognized/supported
		command = self.mediaplayer.parse(params[1])
		if command:
			os.system(command)
		elif not '-q' in sys.argv and not '--quiet' in sys.argv:
			print 'Command not supported by %s.' % self.mediaplayer.name

if __name__ == '__main__':
	try:
		CommandAndControl(sys.stdin)
	except KeyboardInterrupt:
		sys.exit(1)
