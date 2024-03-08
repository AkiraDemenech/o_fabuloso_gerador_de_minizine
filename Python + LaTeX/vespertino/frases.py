import csv 

h = None

arq_dados = '2e-2.csv'
arq_resultado = '2e-2.py'

nome = ''

dados = {}

for ln in csv.reader(open(arq_dados, 'r', encoding='utf-8')):
	cols = [col.strip() for col in ln]
	if not sum(len(col) for col in cols):
		continue 

	if not h:
		h = cols 
		print(h)

		for t in h:
			if t:
				dados[t] = {}
		continue 

	for c in range(min(len(h), len(cols))):
		if not cols[c]:
			continue 

		t = tuple(cols[c].split())
		col = ('%s '*len(t)).strip() %t

		if h[c]: # frase
			if h[c].upper() in ('SP','PS'):
				col = (col,)
				if 'P' in h[c]:
					col *= 4	

			print(nome, '\t', h[c], '\t', col)
			if not nome in dados[h[c]]:
				dados[h[c]][nome] = []
			dados[h[c]][nome].append(col)			
		#	dados[h[c]].append((nome, col))

		else:	# nome
			nome = col
			print('\n', nome)


with open(arq_resultado,'w',encoding='utf-8') as res:
	print('f=',False,file=res)
	print('m=',True,file=res)
	
	print('F=',2,file=res)
	print('M=',3,file=res)


	print('\ndados=', str(dados).replace('),','),\n\t\t').replace('],','],\n\t').replace('},','},\n').replace('{','{\n\t'), file=res)		