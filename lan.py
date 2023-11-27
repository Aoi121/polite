import sys
import time

ID, INT, SLIT, VAR, OP, EOF = "ID", "INT", "SLIT", "VAR", "OP", "EOF"
KEYWORDS = ["request","become","output","ask","for","value"]
KEYWORD_TO_TYPE = {
	"request":"ID",
	"become":"ID",
	"output":"ID",
	"ask":"ID",
	"for":"ID",
	"value":"ID"
}
fileName = sys.argv[1]
tokenLocation = 0

variables = {}
#var:value
currentVariableName = ""
tokens = []
#identifier:value
class Token:
	def __init__(self, identifier, type):
		self.identifier = identifier
		self.type = type
	def __repr__(self):
		return f"({self.identifier}, {self.type})"

class Lexer:
	def __init__(self, file):
		self.isFindVar = False
		self.isFindVarVal = False
		self.isFindBracket = False
		self.file = file
		self.text = file.readlines()
		self.text[-1] = self.text[-1] + '\n'
	def get_next_token(self,lineNum):
		global tokenLocation
		global currentVariableName
		print(self.text)
		try:
			line = self.text[lineNum].replace(" ","")
		except IndexError:
			return 1
		word = ""

		#Base token
		if(self.isFindVar == False and self.isFindVarVal == False and self.isFindBracket == False):
			for x in range(tokenLocation, len(line)):
				word = word + line[x]
				if(word in KEYWORDS):
					#print(word[len(word)-5:len(word)])
					#Change this to a switch case
					match word:
						case "request":
							self.isFindVar = True
						case "become":
							self.isFindVarVal = True
						case "output":
							self.isFindBracket = True
						case "ask":
							self.isFindVar = True
						case "value":
							self.isFindBracket = True
					tokenLocation = x+1
					tokens.append(Token(word,KEYWORD_TO_TYPE[word]))
				print(word)
		#Variable Identifier
		elif self.isFindVar:
			print("var")
			for x in range(tokenLocation, len(line)):
				word = word + line[x]
				#var before become
				if(word[len(word)-6:len(word)] == "become"):
					variables[word[0:len(word)-6]] = None
					currentVariableName = word[0:len(word)-6]
					tokenLocation = x-5
					tokens.append(Token(word[0:len(word)-6],VAR))
				#var before for
				elif(word[len(word)-3:len(word)] == "for"):
					tokenLocation = x-2
					tokens.append(Token(word[0:len(word)-3],VAR))
				print(word)
			self.isFindVar = False
		#Variable Value
		elif self.isFindVarVal:
			print("val")
			for x in range(tokenLocation, len(line)):
				word = word + line[x]
				if("\n" in word[-1]):
					print('val')
					tokenLocation = x+1
					tokens.append(Token(int(word),INT))
			print(word)
			self.isFindVarVal = False
		#Brackets
		elif self.isFindBracket:
			for x in range(tokenLocation, len(line)):
				word = word + line[x]
				if(word == "["):
					tokenLocation = x+1
					tokens.append(Token(word,OP))
				elif(word == "]"):
					print("bracket!")
					tokenLocation = x+1
					tokens.append(Token(word,OP))
				print(word)
			self.isFindBracket = False

		#print("Nexttoken " + str(line[tokenLocation]))
		try:
			if(line[tokenLocation] == '\n'):
				return 2
			print(line[tokenLocation])
		except IndexError:
			return 2
		return 0

if __name__ == "__main__":
	file = open(fileName, "r")
	l = Lexer(file)
	lines = file.readlines()
	running = True
	lineNum = 0
	while(running):
		result = l.get_next_token(lineNum)
		if(result == 1):
			#EOF
			running = False
			tokens.append(Token("EOF", EOF))
		elif(result == 2):
			#EOL
			lineNum = lineNum + 1
			tokenLocation = 0
		else:
			continue
			time.sleep(0.25)
	print(variables)
	print(tokens)