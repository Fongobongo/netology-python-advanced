class Stack:
	def __init__(self, string):
		self.stack = list(string)

	def __str__(self):
		is_balanced = True
		opening_brackets = ['[', '(', '{']
		closing_brackets = [']', ')', '}']
		check_stack = Stack('')
		while self.size() > 0 and is_balanced:
			element = self.peek()
			if element in closing_brackets:
				check_stack.push(self.pop())
			elif element in opening_brackets:
				if opening_brackets.index(element) == closing_brackets.index(check_stack.peek()):
					self.pop()
					check_stack.pop()
				else:
					is_balanced = False
		if is_balanced and check_stack.is_empty():
			return 'Сбалансированно'
		else:
			return 'Небалансированно'

	def is_empty(self):
		return self.stack == []

	def push(self, element):
		self.stack.append(element)

	def pop(self):
		return self.stack.pop()

	def peek(self):
		return self.stack[-1]

	def size(self):
		return len(self.stack)


if __name__ == '__main__':
	print(Stack("(((([{}]))))"))
	print(Stack("[([])((([[[]]])))]{()}"))
	print(Stack("{{[()]}}"))
	print(Stack("}{}"))
	print(Stack("{{[(])]}}"))
	print(Stack("[[{())}]"))
