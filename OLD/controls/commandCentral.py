import api
import os
from lxml import etree
flag = 1
videopause = videocontrol = brightness = systemlock = speechability = systemlock = 0
while True:
	os.system("sleep 3")
	tree = etree.parse("config.xml")
	for element in tree.iter():
		if element.tag == "status":
			xmlspeech = element.text
		elif element.tag == "IntelVideoPause":
			xmlvideopause = element.text
		elif element.tag == "IntelVideoControl":
			xmlvideocontrol = element.text
		elif element.tag == "IntelBrightnessControl":
			xmlbrightness = element.text
		elif element.tag == "IntelSystemLock":
			xmlsystemlock = element.text
	print xmlvideopause
	if xmlspeech == "on" and speechability == 0:
		commandcentral = api.Data(["./startSpeechRecognition"],"Started speech recognition",True)
		commandcentral.interact()
		speechability = 1
	elif xmlspeech == "off" and speechability == 1:
		os.system("killall -9 julius")
		speechability = 0
	if xmlvideopause == "on" and videopause == 0:
		os.system("killall -9 IntelVideoControl")
		os.system("killall -9 IntelBrightnessControl")
		os.system("killall -9 IntelSystemLock")
		commandcentral = api.Data(["./IntelVideoPause"],"intelligent video pause, started",True)
		print commandcentral
		commandcentral.interact()
		videopause = 1
	elif xmlvideopause == "off" and videopause == 1:
		os.system("killall -9 IntelVideoPause")
		videopause = 0
	if xmlvideocontrol == "on" and videocontrol == 0:
		os.system("killall -9 IntelVideoPause")
		os.system("killall -9 IntelBrightnessControl")
		os.system("killall -9 IntelSystemLock")
		commandcentral = api.Data(["./IntelVideoControl"],"intelligent video control, started",True)
		commandcentral.interact()
		videocontrol = 1
	elif xmlvideocontrol == "off" and videocontrol == 1:
		os.system("killall -9 IntelVideoControl")
		videocontrol = 0
	if xmlbrightness == "on" and brightness == 0:
		os.system("killall -9 IntelVideoPause")
		os.system("killall -9 IntelVideoControl")
		os.system("killall -9 IntelSystemLock")
		commandcentral = api.Data(["./IntelBrightnessControl"],"intelligent brightness control, started",True)
		commandcentral.interact()
		brightness = 1
	elif xmlbrightness == "off" and brightness == 1:
		os.system("killall -9 IntelBrightnessControl")
		brightness = 0
	if xmlsystemlock == "on" and systemlock == 0:
		os.system("killall -9 IntelVideoPause")
		os.system("killall -9 IntelVideoControl")
		os.system("killall -9 IntelBrightnessControl")
		commandcentral = api.Data(["./IntelSystemLock"],"intelligent system lock, started",True)
		commandcentral.interact()
		systemlock = 1
	elif xmlsystemlock == "off" and systemlock == 1:
		os.system("killall -9 IntelSystemLock")
		systemlock = 0
