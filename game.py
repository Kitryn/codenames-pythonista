# coding: utf-8

import ui
import random

BG_CELL = (0.9, 0.9, 0.9, 1.0)
BG_BOARD = (0.9, 0.85, 0.8, 1.0)

class Board (ui.View):
	def __init__(self):
		self.width = 1024
		self.height = 700
		
		self.background_color = BG_BOARD
	
	def add_cell(self, text, col, row, touch_handler):
		x_pos = ((self.width / 5) * col) - (self.width / 10)
		y_pos = ((self.height / 5) * row) - (self.height / 10)
		
		cell = Cell(text, x_pos, y_pos, touch_handler)
		self.add_subview(cell)


class Cell (ui.View):
	def __init__(self, text, x, y, touch_handler):
		#self.multitouch_enabled = False
		self.is_clicked = False
		
		self.name = text
		
		self.background_color = BG_CELL
		self.border_width = 1.0
		self.border_color = 0.3
		self.width = 200
		self.height = 100
		#self.flex = 'WH'
		self.corner_radius = 5
		
		self.center = (x, y)
		
		label = ui.Label(name=text)
		#label.flex = 'LRT'
		label.font = ('<system-bold>', 24)
		label.text = text
		label.alignment = ui.ALIGN_CENTER
		label.size_to_fit()
		label.center = (self.width / 2, self.height / 2)
		#label.line_break_mode = ui.LB_CLIP
		#label.number_of_lines = 1
		
		self.add_subview(label)
		self.label = label
		
		self.touch_handler = touch_handler
		self.last_ended_time = 0
	
	def touch_ended(self, touch):
		# touch ended outside view, ignore it
		if not 0 < touch.location[0] < self.width:
			return
		
		if not 0 < touch.location[1] < self.height:
			return
		
		# doubleclick checker
		if touch.timestamp - self.last_ended_time <= 0.2:
			for subview in self.superview.subviews:
				subview.background_color = BG_CELL
				subview.label.text_color = 'black'
			self.superview.background_color = BG_BOARD
			return
		
		self.last_ended_time = touch.timestamp
		
		# register as a proper click
		self.touch_handler(self)
	
	def turn_red(self):
		self.background_color = (1.0, 0, 0, 1)
		self.label.text_color = 'white'
	
	def turn_blue(self):
		self.background_color = (0, 0, 1.0, 1)
		self.label.text_color = 'white'
	
	def turn_grey(self):
		self.background_color = (0.5, 0.5, 0.5, 1)
		self.label.text_color = 'white'
	
	def turn_black(self):
		self.background_color = (0, 0, 0, 1)
		self.label.text_color = 'white'


def touch_handler(cell):
	global red_words, blue_words
	global red_revealed, blue_revealed
	if cell.name in red_words:
		cell.turn_red()
		red_revealed += 1
	elif cell.name in blue_words:
		cell.turn_blue()
		blue_revealed += 1
	elif cell.name in assassin:
		cell.turn_black()
	else:
		cell.turn_grey()


WORDLIST = []
with open("wordlist.txt", 'r') as f:
	WORDLIST = f.readlines()

red_index = random.randint(8,9)
blue_index = 17 - red_index
words = random.sample(WORDLIST, 25)
assassin = words[0]
red_words = words[1:red_index+1]
blue_words = words[red_index+1:18]
red_revealed = 0
blue_revealed = 0

v = Board()

random.shuffle(words)
col = 1
row = 1
for word in words:
	v.add_cell(word, col, row, touch_handler)
	col += 1
	if col == 6:
		col = 1
		row += 1

for cell in v.subviews:
	touch_handler(cell)

if len(red_words) > len(blue_words):
	v.background_color = '#ffaaaa'
else:
	v.background_color = '#aac8ff'


v.present('full_screen')
