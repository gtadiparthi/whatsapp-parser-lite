#The purpose of this code is to 
# Read input from debate transcript
# Parse the debate transcript into the following fields:
# 1. Sentence No. 2. Paragraph No. 3. Speaker 4. Conversation Text


from __future__ import division
import codecs
import re
import operator
import sys
import json
import csv
import pandas as pd
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from os import path
from PIL import Image, ImageFile
import numpy as np
import matplotlib.pyplot as plt
from transcript import *
import re, string

table = string.maketrans("","")

stopwordshearing = set(["mr","go","said","one","two","three","clip",
	"four","know","want","time","think","now","u","say","let","will","well","says","ph","ask","CROSSTALK","APPLAUSE"])


def parse_whatsapp():
    if len(sys.argv) < 3:
        print "Run: python main.py < Input TextFileName>  <Output csv filename>[regex. patterns]"
        sys.exit(1)
    c = Transcript(sys.argv[1], sys.argv[2])
    c.open_file()
    c.feed_lists()
    c.write_transcript()
    data = pd.read_csv(sys.argv[2])
    print(data)
    # Print all the unique speakers to clean up any unwanted sentences and only keep speakers
    print(c.get_speakers())
    data = pd.read_csv(sys.argv[2])
    data = data [~data.Speaker.isin(['MALE','SANTELLI','(UNKNOWN)','UNIDENTIFIED MALE','HARMAN', 'HARWOOD','CRAMER','EPPERSON','QUICK','QUINTANILLA'])]
    print 'Unique Speakers: ', sorted(list(data.Speaker.unique()))
    #Count the number of words each speaker spoke
    def countWords(speaker):
        speakerData = data[data.Speaker == speaker]
        allText = ""
        for index, row in speakerData.iterrows():
        	allText += str(row['Text'])+" "

        words_all = len(allText.split())
        print 'Total words:   ',speaker,': ', words_all
    	
    for name in data.Speaker.unique():
    	countWords(name);
if __name__ == "__main__":
    parse_whatsapp()
   	