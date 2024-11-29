import os

class MakeTextFile:
	fileName=""

	def __init__(self,fileName):
		directory_path = os.path.dirname(fileName)
		os.makedirs(directory_path, exist_ok=True)
		self.fileName = fileName

	def writeSave(self, str):
		if os.path.isfile(self.fileName):
			f = open(self.fileName, 'a')
		else:
			f = open(self.fileName, 'w')
		f.write(str)
		f.close()

	def writeSaveln(self, str):
		if os.path.isfile(self.fileName):
			f = open(self.fileName, 'a')
		else:
			f = open(self.fileName, 'w')
		f.write(str)
		f.write("\n")
		f.close()

	def writeFile(self, file_name):
		if os.path.isfile(self.fileName):
			f = open(self.fileName, 'a')
		else:
			f = open(self.fileName, 'w')
		f.write(str)
		f.write("\n")
		f.close()

	def closeFile(self):
		pass

	def printMessage(self, message):
		print(message)

if __name__ == "__main__":
	textFile = makeTextOneOpenFile("cli_test.txt")
	textFile.writeSave("hello")
