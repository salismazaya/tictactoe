# coded by: salism3
# 26 - 02 - 2020

import os, random, time, sqlite3, sys

class Tictactoe:
	def __init__(self):
		self.col = list(range(1,10))
		self.response = ""
		self.p1 = None
		self.p2 = "AI"
		
	def show(self):
		os.system("cls" if os.name == "nt" else "clear")
		# print(self.response)
		# print(self.getEmptyColoums())
		for_format = str(self.col).replace("[", "").replace("]", "")
		data = """\x1b[1;33m      ╔═══╦═══╦═══╗
      ║ {} \x1b[1;33m║ {} \x1b[1;33m║ {} \x1b[1;33m║
      ╠═══╣═══╣═══╣
      ║ {} \x1b[1;33m║ {} \x1b[1;33m║ {} \x1b[1;33m║
      ╠═══╣═══╣═══╣
      ║ {} \x1b[1;33m║ {} \x1b[1;33m║ {} \x1b[1;33m║
      ╚═══╩═══╩═══╝\x1b[1;39m"""
		data = eval("data.format({})".format(for_format))
		print(data)
	
	def p1_select(self, x):
		if self.col[x - 1] != "X" and self.col[x - 1] != "O" and x > 0 and x < 10:
			self.col[x - 1] = "O"

	def p2_select(self, x):
		if self.col[x - 1] != "O" and self.col[x - 1] != "X" and x > 0 and x < 10:
			self.col[x - 1] = "X"
	
	def who_win(self):
		col = self.col
		win = [("X", "X", "X"), ("O", "O", "O")]
		rules = [(0,1,2), (3,4,5), (6,7,8)]
		rules += [(0,3,6), (1,4,7), (2,5,8)]
		rules += [(0,4,8), (2,4,6)]
		for x in rules:
			w = tuple([col[i] for i in x])
			if w in win:
				return "AI" if "X" in w else "You"
		if len(self.getEmptyColoums()) == 0:
			return "Draw"

	def getEmptyColoums(self):
		return [x for x in self.col if x != "O" and x != "X"]

	def getMoveList(self):
		db = sqlite3.connect("data.db")
		cur = db.cursor()
		cur.execute("select * from move")
		return cur.fetchall()

	def ai_move(self):
		col = self.col
		for x in self.getMoveList():
			move = [int(y) for y in list(str(x[0]))]
			response = x[1]
			m1 = move[0] - 1
			m2 = move[1] - 1
			if (col[m1], col[m2]) == ("X", "X"):
				if col[response - 1] not in ("O", "X"):
					return response
		for x in self.getMoveList():
			move = [int(y) for y in list(str(x[0]))]
			response = x[1]
			m1 = move[0] - 1
			m2 = move[1] - 1
			if (col[m1], col[m2]) == ("O", "O"):
				if col[response - 1] not in ("O", "X"):
					return response
		else:
			return random.choice(self.getEmptyColoums())

			

def main():
	gas = Tictactoe()
	p1 = True
	gas.show()
	while True:
		if p1:
			awal = len(gas.getEmptyColoums())
			gas.p1_select(int(input("Your Turn: ")))
			if awal != len(gas.getEmptyColoums()):
				p1 = False
		else:
			p1 = True
			for i in range(1,4):
				sys.stdout.write("\rAI Turn " + "." * i)
				time.sleep(0.3)
				sys.stdout.flush()
			gas.p2_select(gas.ai_move())
		gas.show()
		if gas.who_win() in ["You", "AI"]:
			print("Winner: " + gas.who_win())
			break
		elif gas.who_win() == "Draw":
			print("Draw")
			break
	
main()