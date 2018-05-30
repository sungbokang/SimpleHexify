# Simple Hexify for Sublime Text 3 by Sung on 180530
import os
import sys
import datetime

import sublime
import sublime_plugin

# HEX stands for hex(16)
HEX = 16

class SimpleHexifyCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# get the current sheet file name
		self.inputFileName = self.view.file_name()
		print("inputFileName = " + self.inputFileName)
		if self.inputFileName is not None:
			self.openFiles()
		else:
			print("%s does not exist" % (self.inputFileName))

		try:
			self.hexify()

			# open the output file with a new window
			sublime.active_window().open_file(self.outputFileName)
		except:
			pass
		finally:
			self.inFile.close()
			self.outFile.close()

	def openFiles(self):
		try:
			self.inFile = open(self.inputFileName, "rb")
		except:
			print("%s file open exception" % (self.inputFileName))
			assert "Input File Excpetion"

		try:
			now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
			self.outputFileName = self.inputFileName + "." + now + ".hex"
			self.outFile = open(self.outputFileName, "w")
		except:
			print("%s file open exception" % (self.outputFileName))
			assert "Output File Exception"

	def hexify(self):
		# print header
		header = " " * 9
		header = header + "\t{:47s}".format("HEX VALUES")
		header = header + "\t{:16s}".format("ASCII CHARACTERS")
		header = header + "\t{:143s}".format("BINARY VALUES")
		print(header, file = self.outFile)

		# print column number layout
		layout = " " * 9
		layout = layout + "\t" + " ".join("{:02x}".format(x) for x in range(HEX))
		layout = layout + "\t" + "".join("{:x}".format(x) for x in range(HEX))
		layout = layout + "\t" + " ".join("{:8x}".format(x) for x in range(HEX))
		print(layout, file = self.outFile)

		content = self.inFile.read(HEX)
		cnt = 0
		while len(content) > 0:
			# row numbers
			record = ("%s" % (format(cnt, "02x"))).zfill(11)
			print(record)
			# hexs
			record = record + "\t" + " ".join("{:02x}".format(x) for x in content)
			print(record)
			# fill spaces when the length is shorter than 16
			if len(content) < HEX:
				record = record + "   " * (HEX - len(content))
			print(record)
			# visible ascii characters
			record = record + "\t" + "".join([self.getAscii(x) for x in content])
			print(record)
			# fill spaces when the length is short than 16
			if len(content) < HEX:
				record = record + " " * (HEX - len(content))
			print(record)
			# bits
			record = record + "\t" + " ".join("{:08b}".format(x) for x in content)
			print(record)
			print(record, file = self.outFile)

			cnt = cnt + 1
			content = self.inFile.read(HEX)

	def getAscii(self, i):
		# values between 32 and 127 are printable only
		if i > 31 and i < 128:
			ret = chr(i)
		else:
			ret = "."

		return ret
