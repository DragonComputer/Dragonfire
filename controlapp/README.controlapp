Example Media Player Control And Command Application
-----------------------------------------------------------

This directory contains a simple example of how to control a media player
with some simple voice commands, using the Julius voice recognition engine.

The included sample script works for Rhythmbox and Banshee.

== QUICK START ==

First, copy the example files to a directory where you can write, like your
home folder, uncompress the gziped files and adapt the configuration file:

  mkdir ~/julius-controlapp; cd ~/julius-controlapp
  cp /usr/share/doc/julius-voxforge/examples/controlapp/* .
  cp /usr/share/doc/julius-voxforge/examples/*.jconf* .
  gunzip * 2>&1 | grep -v ignored
  sed -i 's/sample\.dfa/mediaplayer\.dfa/' *.jconf
  sed -i 's/sample\.dict/mediaplayer\.dict/' *.jconf

Now let's compile the grammar (you will need package "julius" to be installed
for this and the next steps to work):

  mkdfa mediaplayer

Now you can try it out:

  julius -quiet -input mic -C julian.jconf 2>/dev/null | ./command.py

If this works as expected, you can now proceed customizing this to suit your
needs. Take a look at /usr/share/doc/julius-voxforge/examples/README, try
modifying the included files and read some of the numerous documentation
available at http://voxforge.org/home/dev for this.

Note that the .dfa, .dict and .term files are automatically generated with the
"mkdfa" command mentioned above, so whenever you change the .grammar or .voca
files you'll need to repeat that command for your changes to take effect.

 -- Siegfried-A. Gevatter <rainct@ubuntu.com>. 19/06/2009
