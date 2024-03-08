import threading
import random	
import os	




	
		
	




	
	









def escolher (partes, x, y = None):
	

from eins import dados 

		
	
	
	
		
			
		
dir = 'à direita'
esq = 'à esquerda'

		
coluna = 'lsp'
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

			
					
				
		
	
	
		
		
		

		
			
	print(ac - bc, '\t', a, ac,ah, '\t', b, bc,bh)