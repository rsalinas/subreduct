#! /usr/bin/env python3
# -*- coding: UTF-8 -*-


"""This script reduces SRT subtitle files, leaving just the first 
appearance of each word, replacing already seen words by underscores.

Each entry/screenful in a SRT consists of:
1                    (entry number)
00:00:01,000 --> 00:00:04,074       (time interval) 
Subtitles downloaded from www .OpenSubtitles .org   (one or more text lines)
 (blank line)
"""

__author__ = 'Raúl Salinas Monteagudo <rausalinas@gmail.com>'

import sys, __future__, re
from optparse import OptionParser


if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option("-f", "--file", dest="filename",
					  help="input SRT file", metavar="INFILE")
	parser.add_option("-o", "--output", dest="outfile",
					  help="output SRT file", metavar="OUTFILE")

	(options, args) = parser.parse_args()

	n=1

	seen={}

	def joint(ch) :
		return ch == '.' or ch == ',' or ch == '?'
		
	def special(ch) :
		return joint(ch) or ch== '-' 

	try:
		if options.filename and options.filename != '-':
			inf = open(options.filename, "rU") 
		else:
			inf = sys.stdin
	except IOError as e:
		print ("Exception opening input file: "+options.filename)	
		sys.exit(1)
		
		
	try:
		if options.outfile and options.outfile != '-':
			of = open(options.outfile, "w") 
		else:
			of = sys.stdout
	except IOError as e:
		print ("Exception opening output file: "+options.outfile+" "+str(e))		
		sys.exit(1)
		
		
	try:
		l=inf.readline().rstrip('\r')
		while l:	
			## First, expect the screenful number (an increasing number starting at 1)
			if (l.rstrip() != str(n)):  
				raise Exception("Bad msg id: "+l)
			n+=1
			print(l.rstrip(), file=of)
			
			## Then read the time interval
			l=inf.readline()		
			if not l:
				raise IOError("Premature EOF expecting time interval")		    
			print(l.rstrip(), file=of)
			
			l=inf.readline()
			while l and len(l.rstrip()) != 0:
				nl=""
				for s in l.rstrip().replace(".", " .").replace("?", " ?").replace(",", " ,").replace("!", " !").split(" "):
					if (not joint(s) and len(nl)):
						nl+= " "
					if (not special(s) and s in seen):
						nl+= "_"*len(s) 
					else:						
						nl+=s
						seen[s]=1				
				print(nl, file=of)
				l=inf.readline()
			print("", file=of)
			l=inf.readline()				
		print ("Different words: "+str(len(seen)))	
		
	except IOError as e:
		print ("IOError: ",str(e), file=sys.stderr)	
	finally:
		inf.close()

