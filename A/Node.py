# Copyright: Aleksandr Gordeiko 2020

import re


class Node:

	def __init__(self, expr):
		self.expr = expr
		self.sign = None
		self.right = None
		self.left = None
		self.__parse()

	def __parse(self):
		if len(self.expr) == 0:
			return

		bounds = self.__get_brackets_bounds(self.expr)
		cons = self.__find_not_in_brackets("->", self.expr, bounds, False)
		orr = self.__find_not_in_brackets("|", self.expr, bounds, True)
		andd = self.__find_not_in_brackets("&", self.expr, bounds, True)
		nott = self.__find_not_in_brackets("!", self.expr, bounds, False)

		if cons != -1:
			self.sign = "->"
			self.right = Node(self.expr[cons + 2:])
			self.left = Node(self.expr[:cons])
		elif orr != -1:
			self.sign = "|"
			self.right = Node(self.expr[orr + 1:])
			self.left = Node(self.expr[:orr])
		elif andd != -1:
			self.sign = "&"
			self.right = Node(self.expr[andd + 1:])
			self.left = Node(self.expr[:andd])
		elif nott != -1:
			self.sign = "!"
			self.right = Node(self.expr[1:])
		elif self.expr[0] == "(" and self.expr[-1] == ")":
			self.expr = self.expr[1:-1]
			self.__parse()

	'''def __str__(self):
		if self.sign in ["->", "|", "&"]:
			return "({},{},{})".format(self.sign, self.left, self.right)
		elif self.sign == "!":
			return "(!{})".format(self.right)
		else:
			return self.expr'''

	def __str__(self):
		return self.expr

	def __eq__(self, other):
		if (self.sign is None) and (self.left is None) and (self.right is None):
			return self.expr == other.expr
		return (self.sign == other.sign) and (self.left == other.left) and (self.right == other.right)

	def get_expression(self):
		return "(" + self.expr + ")"

	@staticmethod
	def __get_brackets_bounds(expr):
		c = 0
		indexes = []
		bounds = []
		for i in range(len(expr)):
			if expr[i] == "(":
				c += 1
				if c == 1:
					indexes.append(i)
			if expr[i] == ")":
				c -= 1
				if c == 0:
					indexes.append(i)
		for i in range(0, len(indexes), 2):
			bounds.append([indexes[i], indexes[i + 1]])
		return bounds

	@staticmethod
	def __find_not_in_brackets(sign, expr, bounds, reverse):

		def is_in_brackets(i, _bounds):
			for b in _bounds:
				if b[0] < i < b[1]:
					return True
			return False

		idxs = [g.start() for g in re.finditer(re.escape(sign), expr)]

		if reverse:
			idxs.reverse()

		for j in idxs:
			if not is_in_brackets(j, bounds):
				return j
		return -1
