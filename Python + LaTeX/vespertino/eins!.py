import threading
import random	
import os	


	

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
		print('Utilizados todos os',x,'de',n)
		nomes.pop(n)
	return n,x,e

from eins import dados 

dir = 'à direita'
esq = 'à esquerda'

sujeito = 's'
predicado = 'p'
lugar = 'l'

Sujeito = sujeito.upper()
Predicado = predicado.upper()
Lugar = lugar.upper()

coluna = lugar, sujeito, predicado
largura = 4

teste = [list(coluna) for c in range(largura)]

pos = []
for c in range(len(teste)):
	for h in range(len(teste[c])):
		pos.insert(random.randint(0,len(pos)),(c,h))

while len(pos):	
	ac,ah = pos.pop()
	a = teste[ac][ah]

	bc,bh = pos.pop()	
	b = teste[bc][bh]

	d = ac - bc

	print(d, '\t', a, ac,ah, '\t', b, bc,bh)

	a,b,c = escolher(dados,a,b,d)
	print(a,c,b,'\n')

	teste[ac][ah] = a
	teste[bc][bh] = b

print(teste)	