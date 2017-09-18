def fungsi (tipe,x,y):
	try:
		if (tipe == 'ADD'):
			return int(x)+int(y)
		elif (tipe == 'SUB'):
			return int(x)-int(y)
		elif (tipe == 'MUL'):
			return int(x)*int(y)
		elif (tipe == 'DIV'):
			return int(x)/int(y)
		else:
			return 'ERR'
	except ValueError:
		return 'ERROR'

