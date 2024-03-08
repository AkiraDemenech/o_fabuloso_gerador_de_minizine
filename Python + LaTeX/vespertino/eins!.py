import threading
import random	
import os	
import sys 

def creditar (nomes, n):
	if not n in nomes:
		nomes[n] = 0
	nomes[n] += 1	

	
def concordar (*f):	
	r = []	
	c = None



	for aut,form,trecho in f:

		if type(trecho) != str:
			if len(trecho) == 2:
				trecho, c = trecho # concorda com a última expressão definidora 
			r.append([aut,form,trecho])	
		else:		
			r.append((aut,form,trecho))	

	if c != None:
		for t in r:			
			if type(t[-1]) != str:
				t[-1] = t[-1][c]

	return r 			

def escolher (partes, x, y = None, d = None):
	if y != None:
		lado = ''

		y = y.lower()
		x = x.lower()
		
		X = x.upper()
		Y = y.upper()

		if d:
			if d < 0:
				lado = 'à esquerda'
			else:	
				lado = 'à direita'
			
			if X != Predicado or y != lugar:
				y = X.lower()
			x = Y.lower()	
				
		return escolher(partes, X + y), escolher(partes, x + Y), lado
	
	nomes = partes[x]	
	n = list(nomes)[random.randint(0, len(nomes) - 1)]

	e = nomes[n].pop(random.randint(0, len(nomes[n]) - 1)) 	
	if not len(nomes[n]):
		print('%Utilizados todos os',x,'de',n)
		nomes.pop(n)
	return n,x,e

import eins  

dir = 'à direita'
esq = 'à esquerda'

sujeito = 's'
predicado = 'p'
lugar = 'l'

Sujeito = sujeito.upper()
Predicado = predicado.upper()
Lugar = lugar.upper()

programa = sys.argv[0].split('\\')[-1].split('/')[-1]  

def gerar (largura = 4, coluna = (lugar, sujeito, predicado), dados = eins.dados):

	# cópia
	dados = {k: {n: list(dados[k][n]) for n in dados[k]} for k in dados} 

	# matriz
	teste = [list(coluna) for c in range(largura)]
	frases = []
	aut = {}

	# sortear  
	pos = []
	for c in range(len(teste)):
		for h in range(len(teste[c])):
			pos.insert(random.randint(0,len(pos)),(c,h))

	# pares 
	while len(pos):	
		ac,ah = pos.pop()
		a = teste[ac][ah]

		bc,bh = pos.pop()	
		b = teste[bc][bh]
		
		d = ac - bc

		print('%', d, '\t', a, ac,ah, '\t', b, bc,bh)

		a,b,c = escolher(dados,a,b,d) # trechos 

		a,b = concordar(a,b) # flexão 

		print('%',a[1],a[0],'\n%',b[1],b[0],sep='\t')
		print('%',a[-1],c,b[-1],'\n')

		creditar(aut, a[0])
		creditar(aut, b[0])

		teste[ac][ah] = a
		teste[bc][bh] = b

		frases.append((a,b,c))

	return frases, aut, teste	


	

def gerar_um_latex (frases, aut, id=None, escrever=print):
	escrever('''\\ttfamily % monoespaçada
\\pagenumbering{gobble}

	\\ 
	\\vfill
	\\begin{turn}{180}	
		\\begin{minipage}{\\textwidth}
			\\centering
			{\\Huge 2e-2}
		  
			\hfill
		  
			''')	
	
	for n in aut:
		escrever('\n\n\\textit{' + n + '}\n\t\ ' + str((aut[n] * 50) // len(frases)) + ' \%')

	escrever('\n\n\\bigskip\n\n' + programa) 

	if id != None:
		escrever('\n0x%04x\n\n' %id)	

	escrever('''
		\\end{minipage}	
	\\end{turn}
	\\vfill
	\\

\\pagebreak

	\\begin{turn}{180}	
		\\begin{minipage}{\textwidth}
				
		\\end{minipage}	
	\\end{turn} 

\\pagebreak
\\sffamily
\\large

	\\begin{enumerate}
''')	
	
	escrever('''
	\\end{enumerate}
''')

	for a,b,c in frases:
		print(a,b,c)
		escrever('\n\n\\vfill \\item\n' + a[-1] + '\t%' + a[1] + '\t' + a[0] + '\n' + c + '\n' + b[-1] + '\t%' + b[1] + '\t' + b[0])
gerar_um_latex(*gerar()[:2],0)