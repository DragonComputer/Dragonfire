"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
import os
from setuptools.command.develop import develop
from setuptools.command.install import install
from setuptools.command.egg_info import egg_info
#import getpass

here = path.abspath(path.dirname(__file__))
#username = getpass.getuser()

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
	long_description = f.read()

class PostDevelopCommand(develop):
	"""Post-installation for development mode."""
	def run(self):
		import nltk

		#nltk.download("punkt")
		#nltk.download("averaged_perceptron_tagger")
		#nltk.download("tagsets")
		nltk.download("brown")
		nltk.download("names")

		os.system("apt-get -y install julius festival festlex-cmu python-xlib")
		os.system("cd /usr/share/festival/voices/english/ && wget -c http://www.speech.cs.cmu.edu/cmu_arctic/packed/cmu_us_clb_arctic-0.95-release.tar.bz2 && tar jxf cmu_us_clb_arctic-0.95-release.tar.bz2 && ln -s cmu_us_clb_arctic cmu_us_clb_arctic_clunits && cp /etc/festival.scm /etc/festival.scm.backup && chmod o+w /etc/festival.scm && echo \"(set! voice_default 'voice_cmu_us_clb_arctic_clunits)\" >> /etc/festival.scm")
		#os.system("cd /usr/share/ && wget http://ml.nec-labs.com/senna/senna-v3.0.tgz && tar zxvf senna-v3.0.tgz")
		#os.system("sudo apt-get -y install openjdk-7-jdk git && cd /home/" + username + "/ && sudo -u " + username + " git clone https://github.com/brmson/yodaqa.git ; cd yodaqa/ && sudo -u " + username + " git pull && sudo -u " + username + " ./gradlew check && sudo -u " + username + " echo | ./gradlew run")
		#os.system("sudo apt-get -y install openjdk-7-jdk git && cd /var/tmp/ && git clone https://github.com/brmson/yodaqa.git ; cd yodaqa/ && git pull && ./gradlew check && echo | ./gradlew run")

		develop.run(self)

class PostInstallCommand(install):
	"""Post-installation for installation mode."""
	def run(self):
		import nltk
		nltk.download("brown")
		nltk.download("names")
		os.system("apt-get -y install julius festival festlex-cmu python-xlib")
		os.system("cd /usr/share/festival/voices/english/ && wget -c http://www.speech.cs.cmu.edu/cmu_arctic/packed/cmu_us_clb_arctic-0.95-release.tar.bz2 && tar jxf cmu_us_clb_arctic-0.95-release.tar.bz2 && ln -s cmu_us_clb_arctic cmu_us_clb_arctic_clunits && cp /etc/festival.scm /etc/festival.scm.backup && chmod o+w /etc/festival.scm && echo \"(set! voice_default 'voice_cmu_us_clb_arctic_clunits)\" >> /etc/festival.scm")

		install.run(self)

class PostInstallegg_info(egg_info):
	"""Post-installation for sdist."""
	def run(self):
		import nltk
		nltk.download("brown")
		nltk.download("names")
		os.system("apt-get -y install julius festival festlex-cmu python-xlib")
		os.system("cd /usr/share/festival/voices/english/ && wget -c http://www.speech.cs.cmu.edu/cmu_arctic/packed/cmu_us_clb_arctic-0.95-release.tar.bz2 && tar jxf cmu_us_clb_arctic-0.95-release.tar.bz2 && ln -s cmu_us_clb_arctic cmu_us_clb_arctic_clunits && cp /etc/festival.scm /etc/festival.scm.backup && chmod o+w /etc/festival.scm && echo \"(set! voice_default 'voice_cmu_us_clb_arctic_clunits)\" >> /etc/festival.scm")

		egg_info.run(self)

setup(
	name='dragonfire',

	# Versions should comply with PEP440.  For a discussion on single-sourcing
	# the version across setup.py and the project code, see
	# https://packaging.python.org/en/latest/single_source_version.html
	version='0.8.3',

	description='Dragonfire is an open source virtual assistant project for Ubuntu based Linux distributions',
	long_description=long_description,

	# The project's main homepage.
	url='https://github.com/mertyildiran/Dragonfire',

	# Author details
	author='Mehmet Mert Yildiran',
	author_email='mert.yildiran@bil.omu.edu.tr',

	# Choose your license
	license='MIT',

	# See https://pypi.python.org/pypi?%3Aaction=list_classifiers
	classifiers=[
		# How mature is this project? Common values are
		#   3 - Alpha
		#   4 - Beta
		#   5 - Production/Stable
		'Development Status :: 3 - Alpha',

		# Indicate who your project is intended for
		'Intended Audience :: Developers',
		'Topic :: Scientific/Engineering :: Human Machine Interfaces',

		# Pick your license as you wish (should match "license" above)
		'License :: OSI Approved :: MIT License',

		# Intended language
		'Natural Language :: English',

		# Target Operating System
		'Operating System :: POSIX :: Linux',

		# Specify the Python versions you support here. In particular, ensure
		# that you indicate whether you support Python 2, Python 3 or both.
		'Programming Language :: Python :: 2.7',
	],

	# What does your project relate to?
	keywords='virtual assistant machine learining artifical intelligence chat bot',

	# You can just specify the packages manually here if your project is
	# simple. Or you can use find_packages().
	packages=find_packages(),

	# Alternatively, if you want to distribute just a my_module.py, uncomment
	# this:
	#   py_modules=["my_module"],

	# List run-time dependencies here.  These will be installed by pip when
	# your project is installed. For an analysis of "install_requires" vs pip's
	# requirements files see:
	# https://packaging.python.org/en/latest/requirements.html
	install_requires=['wikipedia','PyUserInput','google-api-python-client','SpeechRecognition','nltk','egenix-mx-base','httplib2>=0.9.1'],

	# List additional groups of dependencies here (e.g. development
	# dependencies). You can install these using the following syntax,
	# for example:
	# $ pip install -e .[dev,test]
	extras_require={},

	# If there are data files included in your packages that need to be
	# installed, specify them here.  If using Python 2.6 or less, then these
	# have to be included in MANIFEST.in as well.
	package_data={
		# If any package contains *.txt files, include them:
		'': ['*.txt'],
		'': ['*.ini'],
		'': ['*.jconf'],
		'': ['*.dfa'],
		'': ['*.dict'],
		'': ['*.grammar'],
		'': ['*.term'],
		'': ['*.voca'],
		'': ['*.aiml'],
	},

	# Although 'package_data' is the preferred approach, in some case you may
	# need to place data files outside of your packages. See:
	# http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
	# In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
	data_files=[],

	cmdclass={
		'develop': PostDevelopCommand,
		'install': PostInstallCommand,
		'egg_info': PostInstallegg_info,
	},

	# To provide executable scripts, use entry points in preference to the
	# "scripts" keyword. Entry points provide cross-platform support and allow
	# pip to create the appropriate form of executable for the target platform.
	entry_points={
		'console_scripts': [
			'dragonfire=dragonfire:initiate',
		],
	},
)
