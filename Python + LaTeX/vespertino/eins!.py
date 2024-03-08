#import threading
import random	
#import os	
import sys 
from matplotlib import pyplot 

def imagem (v, l, h):
	fig = [[(255,)*3 for j in range(h*l)] for i in range(l*h)]
	coord = [(i, j) for j in range(h) for i in range(l)]				
	Coord = [(i * h, j * l) for i, j in coord]

	g = (random.randint(0,125),) * 3

	u = None
	linhas = []
	
	for c in range(len(v)):
		x,y = Coord[v[c] % (l*h)]
		w,z = coord[c]

		x += z 
		y += w

		if u == None:
			u = x, y
		else:	
			linhas.append((u, (x, y)))
			u = None

	for a,b in linhas:		
		x,y = a
		w,z = b

		c = max(abs(x - w), abs(y - z))
		dx = (w - x) / c
		dy = (z - y) / c
		for k in range(c + 1):
			fig[x][y] = g
			x = int(x + dx)
			y = int(y + dy)

	ext = 'pdf'
	arq = str(v) + '.' + ext

	pyplot.imshow(fig) 
	pyplot.savefig(arq, format=ext)
	pyplot.clf()
#	pyplot.show()
	return arq

sorteados = []

def sortear (i, j = None):

	if j == None:
		j = i
		i = 0

	k = random.randint(i,j)
	sorteados.append((i, j, k))

	return k

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
	n = list(nomes)[sortear(0, len(nomes) - 1)]

	e = nomes[n].pop(sortear(0, len(nomes[n]) - 1)) 	
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
	seq = []
	for c in range(len(teste)):
		for h in range(len(teste[c])):
			q = sortear(0, len(pos))
			seq.append(q)
			pos.insert(q,(c,h))

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

	sorteios = list(sorteados)	
	sorteados.clear()

	figura = imagem(seq,largura,len(coluna))
	#contrafigura = imagem(sorteios,largura,len(coluna))

	return frases, aut, teste, sorteios, figura 	


	

def gerar_um_latex (frases, aut, matriz, sorte=None, img=None, id=None, escrever=print):
	escrever('''\n\n\\pagebreak			
			\\pagenumbering{gobble} % nenhuma numeração

	\\ 
	\\vfill
	\\begin{turn}{180}	
		\\begin{minipage}{\\textwidth}
		  	\\ttfamily % monoespaçada
			\\centering
			{\\Huge 2e-2}
		  
			\hfill
		  
			''')	
	
	for n in aut:
		escrever('\n\n\\textit{\\small ' + n + '}\n\t%\ ' + str(aut[n]))

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
		\\begin{minipage}{\\textwidth}		  
		% texto 
		  Documento gerado com \\LaTeX			
		  
		  \\texttt{akirademenech.github.io}

		% qr code
		  \\includegraphics[height=0.3\\textheight]{2e-2.pdf}

		\\end{minipage}	
	\\end{turn}  
		  
		\\vfill  
		  ''')
	
	if sorte != None:
	#	escrever('\n\\begin{minipage}{0.7\\textwidth}')
		escrever('\n{')
		for i,j,k in sorte:
			escrever(f'\n\t{k}\t% {i} {j}')
			if i == 0 and j == 0:
				escrever('\n')
		escrever('\n}')  
	#	escrever('\\end{minipage}\n')
		  
	escrever('''	  
		    	

		 

\\pagebreak


	\\begin{enumerate}
		  \\sffamily % sem serifa
		  \\large % grande 
''')			

	for a,b,c in frases:
		print('%',a,b,c,sep='\t')
		escrever('\n\n\\vfill \\item\n' + a[-1] + '\t%' + a[1] + '\t' + a[0] + (('\n' + c) if c else '') + '\n' + b[-1] + '\t%' + b[1] + '\t' + b[0])

	escrever('''
	\\end{enumerate}
		  
		  \\hfill

		  \\vfill
	% ilustração''')

	if img != None:
		escrever('\n\n\\includegraphics[width=\\textwidth]{' + img + '}\n\n')	  
		  
	escrever('''
	\hfill	  	  
''')
	
	escrever('\n\t%' + str(matriz))

def abrir_latex (escrever=print):
	escrever('''\\documentclass[12pt]{article}

\\usepackage[a6paper, left=0.3in, right=0.7in, top=1cm]{geometry}
\\usepackage{rotating}

%\\usepackage[T1]{fontenc}
%\\usepackage[brazil]{babel}

\\begin{document}
		  ''')
	
def fechar_latex (escrever=print):	
	escrever('\n\n\\end{document}')

with open(programa + '.tex', 'w', encoding='utf8') as tex:
	abrir_latex(tex.write)
	for num in range(32,64):	
		gerar_um_latex(*gerar(),num,tex.write)
	fechar_latex(tex.write)