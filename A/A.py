# Copyright: Aleksandr Gordeiko 2020

from Node import Node


def get_expression():
	inp = input()
	return inp.replace(" ", "").replace("\t", "").replace("\r", "")


if __name__ == "__main__":
	expression = get_expression()
	print(Node(expression))
