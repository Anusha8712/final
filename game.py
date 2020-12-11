from toy import *
class Calculator:
	from math import pow
	from re import compile
	gr = (
		LR(compile(r'\s+'), lambda match: None),
		LR(compile(r'(?:\.[0-9]+|[0-9]+(?:\.[0-9]+)?)'), lambda match: T('number', float(match))),
		LR(compile(r'\+'), lambda match: T('add', None)),
		LR(compile(r'-'), lambda match: T('subtract', None)),
		LR(compile(r'\*'), lambda match: T('multiply', None)),
		LR(compile(r'/'), lambda match: T('divide', None)),
		LR(compile(r'\^'), lambda match: T('pow', None)),
		LR(compile(r'\('), lambda match: T('(', None)),
		LR(compile(r'\)'), lambda match: T(')', None))
	)
	precedence = (
		OP('left', { 'add', 'subtract' }),
		OP('left', { 'multiply', 'divide' }),
		OP('right', { 'pow' })
	)
	expressions = (
		PR(None, ( 'number', ), lambda n: T('expression', n.value)),
		PR(None, ( '(', 'expression', ')' ), lambda l, ex, r: ex ),
		PR('add', ( 'expression', 'add', 'expression' ), lambda l, op, r: T('expression', l.value + r.value) ),
		PR('subtract', ( 'expression', 'subtract', 'expression' ), lambda l, op, r: T('expression', l.value - r.value) ),
		PR('multiply', ( 'expression', 'multiply', 'expression' ), lambda l, op, r: T('expression', l.value * r.value) ),
		PR('divide', ( 'expression', 'divide', 'expression' ), lambda l, op, r: T('expression', l.value / r.value) ),
		PR('pow', ( 'expression', 'pow', 'expression' ), lambda l, op, r: T('expression', pow(l.value, r.value)) )
	)
if __name__ == '__main__':
	import sys, readline
	parser = Parser(Calculator.expressions, Calculator.precedence)
	lexer = Lexer(Calculator.gr)
	while True:
		try:
			userinput = input('This is Your Calculator (Press Enter to Exit) >> ')
			if not userinput:
				break
                #press enter for breaking the loop
			tks = list(lexer.lex(userinput))
			print('Lexer results:')
			print(tks)
			print('')
			parsed = parser.parse(tks)
			print('Parser results:')
			print(parsed)
			if any(parsed):
				print('\nValue:')
				print(parsed[-1].value)
		except EOFError:
			print('')
			sys.exit()
		except Lexer.LexError:
			print('Couldn’t lex your input')
			continue
		except Parser.ParseError as e:
			print('Parse error. Stack:')
			print(e.memo)
		except:
			import traceback
			traceback.print_exc()