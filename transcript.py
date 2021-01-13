#Include all the subtleties that are required to read a whatsapp chat transcript


import sys
import csv
import pandas as pd
import numpy as np
import codecs

class Transcript():
	def __init__(self, inputFileName,outputFileName):
		self.inputFileName = inputFileName
		self.outputFileName = outputFileName
		self.raw_messages = []
		self.speakerlist = []
		self.messagelist = []
		self.paragraphList = []

		self.datelist = []
		self.timelist = []

	def open_file(self):
		arq = codecs.open(self.inputFileName, "r", "utf-8-sig")
		content = arq.read()
		arq.close()
		lines = content.split("\n")
		lines = [l for l in lines if len(l) > 4]
		for l in lines:
			self.raw_messages.append(l.encode("utf-8"))
	def valid_date(self,date_str):
		valid = True
		separator="/"
		try:
			year, month, day = map(int, date_str.split(separator))
		except ValueError:
			valid = False
		return valid
	def feed_lists(self):
		lineNo = 0
		seqNo = 0
		for l in self.raw_messages:
			l = l.rstrip()
			msg_date, sep, msg = l.decode().partition("- ")
			#Date and time has a , separator
			raw_date, sep, time = msg_date.partition(", ")
			speaker, sep, message = msg.partition(": ")
			#speaker = speaker.encode('utf-8')
			lineNo += 1
			# A proper whatsapp conversation with date, time, speaker, text
			if message:
				self.datelist.append(raw_date)
				self.timelist.append(time)
				self.speakerlist.append(speaker)
				self.messagelist.append(message)
				# store the previous speaker so that you can use it to print when there is only a line
				prevSender = speaker
				prevRawDate = raw_date
				prevTime = time
				seqNo +=1
			# A message. date, time, message
			elif ((speaker != "") & (self.valid_date(raw_date))):
				self.datelist.append(raw_date)
				self.timelist.append(time)
				self.speakerlist.append('MESSAGE')
				self.messagelist.append(speaker)
				# store the previous speaker so that you can use it to print when there is only a line
				prevSender = 'MESSAGE'
				prevRawDate = raw_date
				prevTime = time
				seqNo +=1
			# A continuing conversation with no date time or name
			else:
				self.datelist.append(prevRawDate)
				self.timelist.append(prevTime)
				self.speakerlist.append(prevSender)
				self.messagelist.append(l)
			self.paragraphList.append(seqNo)

	def write_transcript(self, end=0):
		if end == 0:
			end = len(self.messagelist)
		writer = csv.writer(open(self.outputFileName, 'w'))
		writer.writerow(["SentenceNo","SequenceNo","Date","Time","Speaker","Text"])
		for i in range(len(self.messagelist[:end])):
			writer.writerow([i,self.paragraphList[i],self.datelist[i], self.timelist[i],self.speakerlist[i], self.messagelist[i]])

	def get_speakers(self):
		speakers_set = set(self.speakerlist)
		return [e for e in speakers_set]
