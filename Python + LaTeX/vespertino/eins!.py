import threading
import random	
import os	

def arranjo (n, p = 0):
	c = 1
	while n > p:
		c *= n
		n -= 1
	return c	

def seq (t, s):
	i = 0
	s = list(s)
	for k in range(len(t)):
		p = s.index(t[k])
		s.pop(p)
		i += p * arranjo(len(s))
	return i

def perm (i, s):
	t = []
	s = list(s)
	while len(s):
		a = arranjo(len(s) - 1)
		p = i // a
		t.append(s.pop(p))
		i %= a
	return t

def	num (s): 
	if type(s) == str and len(s) == 1: 
		return int(s)   	
	return [num(c) for c in s]	
	
def trans (m):
	i = 0
	t = []
	while True:
		u = []
		col = True
		for ln in m:
			if i < len(ln):
				col = False
				u.append(ln[i])
			else:	
				u.append(0)
		i += 1		
		if col:	
			break
		t.append(u)	
	return t		
		
	
def maga (i, n):	
	if type(n) == int:
		n = range(n)
	return [perm(k, n) for k in i]

LUGAR = 0
SUJEITO = 1
PREDICADO = 2

NADA = None
PREP_EM = -1
PREP_DE = -2
ART = -3

ESQUERDA = 'esquerda'
DIREITA = 'direita'
LADO = ESQUERDA, DIREITA

CONECTIVOS = {
	(LUGAR,LUGAR): (
		(), 
		(ART,PREP_DE, 'fica à %s')),
	
	(LUGAR,SUJEITO): (
		(PREP_EM,ART, ''), 
		(ART,ART, 'fica à %d de onde')
	),
	
	(LUGAR,PREDICADO): (
		(PREP_EM,NADA, ''),
		(ART,NADA, 'fica à %d de onde')
	),


	(SUJEITO,LUGAR): (
		(ART,PREP_EM, ''),
		(ART,PREP_DE, 'à %d')
	),

	(SUJEITO,SUJEITO): (
		(),
		(ART,PREP_DE, 'mora à %s')),

	(SUJEITO,PREDICADO): (
		(ART,NADA, ''),
		(ART,NADA, 'mora à %d de onde alguém')
	),	


	(PREDICADO,LUGAR): (
		(NADA,PREP_EM, ''),
		(NADA,PREP_DE, 'à %d')
	),

	(PREDICADO,SUJEITO): (
		(NADA,ART, ''),
		(NADA,ART, 'à %d de')
	),

	(PREDICADO,PREDICADO): (
		(),
		(NADA,ART, 'à %s de onde'))
}

FRASES = {
	(LUGAR, LUGAR):	'%s %s %s',	# 1 2
	(LUGAR, SUJEITO):	'%s %s mora %s',	# 3 4
	(LUGAR, PREDICADO):	'%s %s alguém %s',	# 5 6
	
	(SUJEITO, LUGAR):	'%s mora %s %s',	# 7 8 
	(SUJEITO, SUJEITO):	'%s %s %s',	# 9 10
	(SUJEITO, PREDICADO):	'%s %s %s',	# 11 12

	(PREDICADO, LUGAR):	'Alguém %s %s %s',	# 13 14
	(PREDICADO, SUJEITO):	'Alguém %s %s onde mora %s',	# 15 16
	(PREDICADO, PREDICADO):	'Alguém %s %s alguém %s'	# 17 18
}

		
		sequencia = [seq(p,range(len(amigos_secretos_presentes_imagens))) for p in trans(permutacao)]
	
	
	
		
			
		

		

	


	
		
				
			# pdflatex -synctex=1 -interaction=nonstopmode "ARQUIVO".tex
		
	
def latex_dobra (zines, file_name = 'dobra'):	
	
	with open(file_name + '.tex', 'w', encoding='utf8') as arq:	
		print('''\\documentclass{article}
\\usepackage[margin=0mm,	paperheight=210mm,paperwidth=297mm]{geometry} %http://ctan.org/pkg/geometry
\\usepackage{graphicx}

\\newcommand{\\zine}[8]{%
	\\thispagestyle{empty}		
	\\centering
	\\includegraphics[width=0.24\\textwidth,angle=180]{#1} % página 1
	\\hfill
	\\includegraphics[width=0.24\\textwidth,angle=180]{#8} % página 8
	\\hfill
	\\includegraphics[width=0.24\\textwidth,angle=180]{#7} % página 7
	\\hfill
	\\includegraphics[width=0.24\\textwidth,angle=180]{#6} % página 6
	%\\vfill
	\\includegraphics[width=0.24\\textwidth]{#2} % página 2
	\\hfill
	\\includegraphics[width=0.24\\textwidth]{#3} % página 3
	\\hfill
	\\includegraphics[width=0.24\\textwidth]{#4} % página 4
	\\hfill
	\\includegraphics[width=0.24\\textwidth]{#5} % página 5
}%

\\begin{document}''', file=arq)
		for pages in zines:
			print(file=arq,end='\n\t\\zine')
			
			if len(pages) != 8:
				if not len(pages):
					continue
					
				pages = list(pages)
				pages.extend(pages * (8 // len(pages)))
				
			for a in pages:
				print(file=arq,end='{' + str(a) + '.pdf}')
		print('\n\\end{document}',file=arq)
		
	return pages, [file_name]	
	
def call_after (target, args=[], kwargs={}, callback = print):
	target(*args, **kwargs)
	callback()
	
def pdf (files, compiler = 'pdflatex -synctex=1 -interaction=nonstopmode', wait=True):
	s = []
	for f in files:
		sem = threading.Semaphore()
		com = f'{compiler} "{f}.tex"'
		print('\n\t',com)
		s.append(sem)
		sem.acquire()
		threading.Thread(target=call_after,args=(os.system, [com]), kwargs={'callback':sem.release}).start()
		
	for sem in s:	
		sem.acquire()
		
		

fila = []		
pag = []
		
			
pdf(fila)
print('\nPáginas geradas')
pdf(latex_dobra(pag)[1])