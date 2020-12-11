from collections import namedtuple
T = namedtuple('T', ( 'type', 'value' ))
LR = namedtuple('LR', ( 'expression', 'handler' ))
PR = namedtuple('PR', ( 'operator', 'val', 'handler' ))
OP = namedtuple('OP', ( 'associativity', 'operators' ))
class Lexer:
	class LexError(Exception):
		"""Input couldn't be lexed based on this gr."""
	def __init__(self, gr):
		self.gr = gr
	def lex(self, input):
		#Generate a series of tokens from an input string based on a grammar.
		while input:
			for r in self.gr:
				match = r.expression.match(input)
				if match:
					mT = match.group()
					tkn = r.handler(mT)
					if tkn:
						yield tkn
					input = input[len(mT):]
					break
			else:
				raise Lexer.LexError
class Parser:
	class ParseError(Exception):
		"""Input couldn't be parsed under these rs"""
		def __init__(self, memo):
			self.memo = memo
	def __init__(self, rs, pe):
		self.rs = rs
		self.pe = pe
	def opPrecedence(self, op):
		return next((prec for prec in enumerate(self.pe) if op in prec[1].operators), None)
	def parse(self, tks):
		memo = []
		while True:
			for r in self.rs:
				if len(memo) >= len(r.val) and all( a == b for a, b in zip(r.val, (t.type for t in memo[-len(r.val):]))):
					if r.operator and len(tks):
						memop = self.opPrecedence(r.operator)
						inP = self.opPrecedence(tks[0].type)
						if inP and memop and (
							(inP[0] > memop[0]) or
							(inP[0] == memop[0] and memop[1].associativity == 'right')
						):
							continue
					memo[-len(r.val):] = [r.handler(*memo[-len(r.val):])]
					break
			else:
				if len(tks):
					memo.append(tks[0])
					del tks[0]
				elif len(memo) <= 1:
					break
				else:
					raise Parser.ParseError(memo)
		return memo
if __name__ == "__main__":
	import doctest
	doctest.testmod(verbose=True)