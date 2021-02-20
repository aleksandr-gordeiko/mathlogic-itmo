# Copyright: Aleksandr Gordeiko 2020

from A.Node import Node


class Matcher:

	def __init__(self):
		self.node_schema_expressions = {}

	def matches(self, node: Node, schema: Node):
		if schema.sign is None:
			try:
				ex = self.node_schema_expressions[schema.expr]
			except KeyError:
				self.node_schema_expressions[schema.expr] = node.expr
				return True

			if ex == node.expr:
				return True

			return False

		if node.sign is None or node.sign != schema.sign:
			return False

		if schema.sign in ["->", "|", "&"]:
			return self.matches(node.left, schema.left) and \
				self.matches(node.right, schema.right)
		elif schema.sign == "!":
			return self.matches(node.right, schema.right)
