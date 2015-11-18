#The purpose of this code is to 
# Read input from whatsapp chat
# Parse the debate transcript into the following fields:
# 1. Sentence No. 2. Paragraph No. 3. Speaker 4. Conversation Text

import csv
from os import path
from transcript import *

def parse_whatsapp():
    if len(sys.argv) < 3:
        print ("Run: python parse_whatsapp.py < Input TextFileName>  <Output csv filename>")
        sys.exit(1)
    c = Transcript(sys.argv[1], sys.argv[2])
    c.open_file()
    c.feed_lists()
    c.write_transcript()
    data = pd.read_csv(sys.argv[2])

    # Print all the unique speakers to clean up any unwanted sentences and only keep speakers
    data = pd.read_csv(sys.argv[2])
    print (('Unique Speakers: ', sorted(list(data.Speaker.unique()))))

if __name__ == "__main__":
    parse_whatsapp()
   	