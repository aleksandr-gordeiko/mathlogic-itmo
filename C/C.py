# Copyright: Aleksandr Gordeiko 2020

from A.Node import Node
from Matcher import Matcher


class ProofMaker:

	def __init__(self):
		self.axiom_schemas = self.get_axiom_schemas()
		self.tenth_axiom_schema = Node("!!$1->$1")
		self.given = []
		self.prove = None
		self.causes, self.consequences = [], []
		self.in_lines = []
		self.out_lines = []

	@staticmethod
	def get_axiom_schemas():
		expressions = [
			"$1->$2->$1",
			"($1->$2)->($1->$2->$3)->($1->$3)",
			"$1->$2->$1&$2",
			"$1&$2->$1",
			"$1&$2->$2",
			"$1->$1|$2",
			"$2->$1|$2",
			"($1->$3)->($2->$3)->($1|$2->$3)",
			"($1->$2)->($1->!$2)->!$1"
		]
		schemas = list(map(Node, expressions))
		return schemas

	def run(self):
		self.read_first_line()
		self.read_proof()
		changed_first_line = ",".join(map(str, self.given)) + " |- !!(" + str(self.prove) + ")"
		return [changed_first_line] + self.out_lines

	def prove_common_axiom_or_given_double_negation(self, node: Node):
		with open("proof1.txt") as proof:
			line = proof.readline()
			while line:
				self.out_lines.append(line[:-1].replace("$1", node.get_expression()))
				line = proof.readline()

	def prove_tenth_axiom_double_negation(self, node: Node):
		with open("proof2.txt") as proof:
			line = proof.readline()
			while line:
				self.out_lines.append(line[:-1].replace("$1", node.get_expression()))
				line = proof.readline()

	def prove_modus_ponens_double_negation(self, idx: int):
		node1 = self.causes[idx]
		node2 = self.consequences[idx]
		with open("proof3.txt") as proof:
			line = proof.readline()
			while line:
				self.out_lines.append(line[:-1].replace("$1", node1.get_expression()).replace("$2", node2.get_expression()))
				line = proof.readline()

	def matches_axiom(self, expression: Node):
		for schema in self.axiom_schemas:
			if Matcher().matches(expression, schema):
				return True
		return False

	def matches_tenth_axiom(self, expression: Node):
		return Matcher().matches(expression, self.tenth_axiom_schema)

	def matches_given(self, expression: Node):
		for g in self.given:
			if expression == g:
				return True
		return False

	def matches_modus_ponens(self, node: Node):
		if node in self.consequences:
			idxs = [i for i, j in enumerate(self.consequences) if j == node]
			for idx in idxs:
				if self.causes[idx] in self.in_lines:
					return True, idx
		return False, 0

	def process_line(self):
		expr = self.in_lines[-1]

		if expr.sign == "->":
			self.causes.append(expr.left)
			self.consequences.append(expr.right)

		if self.matches_given(expr) or self.matches_axiom(expr):
			self.prove_common_axiom_or_given_double_negation(expr)
			return

		if self.matches_tenth_axiom(expr):
			self.prove_tenth_axiom_double_negation(expr.right)
			return

		matches_mp, idx = self.matches_modus_ponens(expr)
		if matches_mp:
			self.prove_modus_ponens_double_negation(idx)

	def read_proof(self):
		while True:
			inp = self.get_expression()
			self.in_lines.append(Node(inp))
			self.process_line()
			if Node(inp) == self.prove:
				return

	def read_first_line(self):
		line = self.get_expression().split("|-")
		self.given = list(map(Node, line[0].split(",")))
		self.prove = Node(line[1])

	@staticmethod
	def get_expression():
		inp = input()
		return inp.replace(" ", "").replace("\t", "").replace("\r", "")


if __name__ == "__main__":
	proof_lines = ProofMaker().run()
	for proof_line in proof_lines:
		print(proof_line)
