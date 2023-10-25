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
	
'''
def llc (g, e, a = None):	
	if not a in g:
		for a in g:
			break
			
	c = [a]
	i = 0
	for o in e:
		while not c[i] in g:
			i += 1
			if len(c) <= i:
				break
		else:		
			
			l = g[c.pop(i)]
			
			if type(o) == float:
				o = int(o * len(l))
			else:
				o %= len(l)
				
			c = c[:i] + list(l[o]) + c[i:]
			
			continue
		break		
	return c		

print(*llc({
	0: [('A Alice',1), ('O Bob',1), ('Um dragão',1)],
	1: [(' deu ',2)],
	2: [('um perfume ',3), ('palavras-cruzadas ',3), ('um adaptador VGA-HDMI com entrada de áudio P1 ',3)],
	3: [('pra Alice',), ('pro Bob',), ('pro dragão',)]
}, [0,1,2,2], 0))	
	
	#'''
	
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

def zine (amigos_secretos_presentes_imagens, verbos, id = None, sequencia = None, permutacao = None):	 
		
	if permutacao == None:	
		if sequencia == None:
			sequencia = 0,0,0,0
		permutacao = trans([perm(s,range(len(amigos_secretos_presentes_imagens))) for s in sequencia])
	elif sequencia == None:	
		sequencia = [seq(p,range(len(amigos_secretos_presentes_imagens))) for p in trans(permutacao)]
	
	amigos, secretos, presentes, imagens = trans(amigos_secretos_presentes_imagens)
	
	p = []
	
	for amigo,oculto,presente,imagem in permutacao:
		
		r = [amigos[amigo]], [imagens[imagem]]
		p.append(r)
		if amigo == oculto:
			r[0].extend([verbos[1], presentes[presente]])
		else:	
			r[0].extend([verbos[0], presentes[presente], secretos[oculto]])
			
	return p, id, sequencia, permutacao		
		

		

def latex_pages (zine, id=None, seq=None, perm=None, pref='zine', size='Huge'): 	
	
	fila = []
	pages = [(['\\centering $z_{ine}!$ Demo\n' + str(id) * (id != None) + '\\vfill \\hfill'],[])] + list(zine) + [([],[])] * (6 - len(perm)) + [([
		'Esta demonstração foi gerada em \\LaTeX, utilizando a fonte padrão',
		
		'em tamanho',
		'\\texttt{',
		size,		
		'}\\vfill',
		f'\nA semente sequencial é {seq}' * (seq != None),
		f'\nA permutação correspondente é {perm}' * (perm != None),
		'\\vfill { \\centering \\texttt{akirademenech.github.io}}'
	],[])]
	if perm != None:
		perm = [f'Cover {id}'] + list(perm) + ['blank'] * (6 - len(perm)) + [f'Back {seq} {perm}']
	
	for k in range(len(pages)):
		tex = f'{pref} {str(id) + str(seq) + str(k) if perm == None else perm[k]} '
		
		try:			
			with open(tex + '.tex','x',encoding='utf8') as arq:
				print('\\documentclass{article} \\usepackage{graphicx} \\usepackage{amsfonts} \\usepackage[margin=0.7in, paperheight=210mm,paperwidth=148mm]{geometry} %http://ctan.org/pkg/geometry \n\\begin{document} \\thispagestyle{empty}', '\\' + size, '\\hfill \\vfill \n',file=arq)
				
				texto, figuras = pages[k]
				print('\t',*texto,'\n\\vfill', sep='\n\t',file=arq)
				for fig in figuras:
					print(f'\\includegraphics[width={1/len(figuras)}\\textwidth]{{{fig}}}',file=arq)
				
				print('\n\\end{document}', file=arq)
		except FileExistsError:
			print('\t',repr(tex),'já existe!')
		else:	
			fila.append(tex)
			# pdflatex -synctex=1 -interaction=nonstopmode "ARQUIVO".tex
		pages[k] = tex			
		
	return pages, fila		
	
def latex_dobra (zines, file_name = 'dobra'):	
	
	with open(file_name + '.tex', 'x', encoding='utf8') as arq:	
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
	

def pdf (files, compiler = 'pdflatex -synctex=1 -interaction=nonstopmode'):
	for f in files:
		com = f'{compiler} "{f}.tex"'
		print('\n\t',com)
		os.system(com)

fila = []		
pag = []
for n in range(10):		
	z = zine([
		['A Alice',	'pra Alice',	'um perfume',	'caneca.png'],
		['O Bob',	'pro Bob',	'palavras-cruzadas',	'sudoku.png'],
		['Um dragão',	'para um dragão',	'um adaptador VGA-HDMI com entrada de áudio P1',	'hdmi-vga.jpg'],
		['Dona Aranha',	'para dona Aranha',	'um barco a vela',	'031.JPG'],
		['O Beto',	'pro Beto',	'a prova que $a^n + b^n = c^n$ não tem solução para $n > 2$ e $a,b,c,n \in \mathbb{Z}^*_+$',	'ipolon.jpg'],
		['O metal',	'pro metal',	'medo de consciência de classe',	'klein.png']
	], ['deu','não podia ir, guardou pra si'], n-0.3-(0.1*random.random()), [random.randint(0,arranjo(6)-1) for k in range(4)])
		
#	print(z)		
			
	p,f = latex_pages(*z)	
	pag.append(p)
	fila.extend(f)
pdf(fila + latex_dobra(pag)[1])