#This final year project is focused on providing alternative ways to communicate with the computer on Linux platform

### Built on top of
* Julius
* OpenCV
* Festival
* Tornado

###Features
* Controls through Speech Recognition (this is not an exhaustive list, many more features are added)
 * Media player controls such as play, pause, next song, previous song. Currently Rhythmbox is supported.
 * Increase or Reduce Brightness, Lock Computer
 * Browse web
* Controls through Web Camera
 * Pauses video when the face is turned away from screen (Supports only Totem)
 * Seeking video using gesture recognition (Supports only Totem)
 * Automatically locks computer when the user is not recognized for a particular amount of time


### Installation Procedure

## This is outdated. Multiple changes in the directory structure need an updated install procedure. 
* Clone the project
* Install julius, julius-voxforge
* Command for running julius : julius -input mic -C julius.jconf | python -u getcommand.py
* Install festival
* Install festlex-cmu
* Install the downloaded voice file : 
	cd /usr/share/festival/voices/english/
	sudo wget -c http://www.speech.cs.cmu.edu/cmu_arctic/packed/cmu_us_clb_arctic-0.95-release.tar.bz2
	sudo tar jxf cmu_us_clb_arctic-0.95-release.tar.bz2 
	sudo ln -s cmu_us_slt_arctic cmu_us_slt_arctic_clunits
	sudo cp /etc/festival.scm /etc/festival.scm.backup
	sudo echo "(set! voice_default 'voice_cmu_us_slt_arctic_clunits)" >> /etc/festival.scm
* Install xbacklight for brightness control from terminal
* Installed Tornado for the webserver stuff. The commands are 
	after unzipping the package, python setup.py build
	sudo python setup.py install
* Install OpenCV
* Install python-opencv
* Install python-numpy
* Install lxml
* Install python-dev

## Below demo was created at a very early stage of the project. After many changes, some features are removed while many others are added.

### Demo: http://www.youtube.com/watch?v=CAmQRpxrQlk

## MIT Licence 