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
	
	amigos, secretos, presentes, imagens, autoria = trans(amigos_secretos_presentes_imagens)
	
	p = []
	
	for amigo,oculto,presente,imagem in permutacao:
		
		r = [amigos[amigo]], [imagens[imagem]]
		p.append(r)
		if amigo == oculto:
			r[0].extend([verbos[1], presentes[presente]])
		else:	
			r[0].extend([verbos[0], presentes[presente], secretos[oculto]])
			
	return p, id, sequencia, permutacao		
		

		

def latex_pages (zine, id=None, seq=None, perm=None, pref='zine', size='', amigos_secretos_presentes_imagens = None): 	
	
	fila = []

	nomes = []	
	n = set()
	if amigos_secretos_presentes_imagens:
		for i in range(len(amigos_secretos_presentes_imagens)) if perm == None else [quad[-1] for quad in perm]:
			aut, inst = amigos_secretos_presentes_imagens[i][-1]
			if aut in n:
				continue 
			nomes.append(f'{aut} \\\\ {inst} \\\\ \hfill \\\\')
			n.add(aut)
	nomes.append('Akira Demenech (org.) \\\\ \\texttt{zine!.py} (desorg.)')		

	n = 0 if id == None else id
	pages = [([
		'\\centering jogo do amigo',
		['secreto','oculto'][n&1],
		['esquisito','delicado'][(n>>1)&1],
		str(id) * (id != None),
		'\\vfill'] + nomes,[])] + list(zine) + [([],[])] * (6 - len(perm)) + [([
		'Esta demonstração foi gerada em \\LaTeX, utilizando a fonte padrão',		
		('em tamanho ' + str(size)) * (size != None and (not size.isspace()) and len(size) > 0),
		f'\\\\ A semente sequencial é {seq}' * (seq != None),
		f'\\\\ A permutação correspondente é {perm}' * (perm != None),
		'\n\n { \n\n \\centering \n \\texttt{akirademenech.github.io} \n\n }'
	],['../../web/zine!.pdf'])]
	if perm != None:
		perm = [f'Cover {id}'] + list(perm) + ['blank'] * (6 - len(perm)) + [f'Back {seq} {perm}']
	
	for k in range(len(pages)):
		tex = f'{pref} {(str(id) + str(seq) + str(k)) if perm == None else perm[k]} '
		
		try:			
			with open(tex + '.tex','x',encoding='utf8') as arq:
				print('\\documentclass{article} \\usepackage{graphicx} \\usepackage[bottom=0.6cm, top=0.2cm, left=0.2in, right=0.4in, paperheight=105mm,paperwidth=74mm]{geometry} %http://ctan.org/pkg/geometry \n\\begin{document} \\thispagestyle{empty}', ('\\' + size) * (len(size) > 0 and not size.isspace()), '\\hfill \\vfill \n',file=arq)
				
				texto, figuras = pages[k]
				print('\t',*texto, sep='\n\t',file=arq)
				if figuras:
					print('\n\\vfill\n\t\\begin{figure}[hb]\n\t\t\\centering\n', file=arq)
					for fig in figuras:
						print(f'\t\t\\includegraphics[height={1/(1 + len(figuras))}\\textheight]{{{fig}}}',file=arq)
					print('\t\\end{figure}', file=arq)	
				
				print('\n\\end{document}', file=arq)
		except FileExistsError:
			print('\t',repr(tex),'já existe!')
		else:	
			fila.append(tex)
			# pdflatex -synctex=1 -interaction=nonstopmode "ARQUIVO".tex
		pages[k] = tex			
		
	return pages, fila		
	
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
	
def pdf (files, compiler = 'pdflatex -synctex=1 -interaction=nonstopmode', wait=6):
	s = []
	for f in files:
		sem = threading.Semaphore()
		com = f'{compiler} "{f}.tex"'
		print('\n\t',com)
		
		sem.acquire()
		threading.Thread(target=call_after,args=(os.system, [com]), kwargs={'callback':sem.release}).start()
		
		if wait:
			s.append(sem)
			if wait > 0 and len(s) >= wait:
				for sem in s:	
					sem.acquire()
				s.clear()	
	if len(s):		
		for sem in s:	
			sem.acquire()
		

fila = []		
pag = []

m = 0 

for amigos in [
	[
		['a Juju',	'da Juju',	'uma pedra',	'mpiccolo.isa.jpg',	('isabella maria píccolo','\\texttt{@mpiccolo.isa}')],
		['Tereza',	'de Tereza',	'uma toalha de banho',	'mpiccolo.isa2.jpeg',	('isabella maria píccolo','\\texttt{@mpiccolo.isa}')],
		['A Maria Eugênia',	'da Maria Eugênia',	'uma caixa de chocolate caribe (100 unidades)',	'laripntes.jpg',	('Larissa Pontes','\\texttt{@laripntes}')],
		['A Maria José',	'da Maria José',	'bala fini de gelatina em formato de minhocas',	'laripntes2.jpg',	('Larissa Pontes','\\texttt{@laripntes}')],
		['o corvo',	'do corvo',	'cachaça',	'Nocturne in B flat minor, Op. 9 no. 1_pages-to-jpg-0001.jpg',	('nathalia fante','\\texttt{@nfrtjt}')],		
		['a carpa',	'da carpa',	'a lua',	'Screenshot_20231021-113435_Photos-01.jpeg',	('nathalia fante','\\texttt{@nfrtjt}')]
	],
	[
		['Pedro Miguel Castelano de Oubrirres e Punha',	'de Pedro Miguel Castelano de Oubrirres e Punha',	'um pedaço de bolo',	'fabioalcover.jpg',	('Fábio Alcover','\\texttt{@fabioalcover}')],
		['Pitu',	'de Pitu',	'um jogo de chaves de fenda',	'fabioalcover2.jpg',	('Fábio Alcover','\\texttt{@fabioalcover}')],
		['a mãe do Pitu',	'da mãe do Pitu',	'uma roupa bem linda',	'fabioalcover3.jpg',	('Fábio Alcover','\\texttt{@fabioalcover}')],		
		['A Lagartinha',	'da Lagartinha',	'um pequeno violino',	'Anel2.png',	('Luana Bibiano de Melo','\\texttt{@luana.bibiano.m}')],
		['O Gilbertão',	'do Gilbertão',	'um bolo de queijo com goiabada',	'Bolo2.png',	('Luana Bibiano de Melo','\\texttt{@luana.bibiano.m}')],
		['Caju',	'da Caju',	'um anel da sorte (que na verdade dá azar)',	'Sapinho.png',	('Luana Bibiano de Melo','\\texttt{@luana.bibiano.m}')]		
	]
]: 
	permutacoes = []
	paginas = []

	while len(permutacoes) < 30:		

		n = m + len(permutacoes)

		if len(permutacoes) % 36 == 0:
			paginas.clear()
		
		while True:
			z = zine(amigos, ['ganhou','não podia ir, guardou pra si'], n, [random.randint(0,arranjo(len(amigos))-1) for k in range(4)])

			p = z[-1] 
			if p in permutacoes:
				print('Zine',p,'já gerado')
			else:	
				
				for q in p:
					
					if q in paginas:
						print('Página',q,'já gerada')
						break

				else:	
					paginas.extend(p)
					permutacoes.append(p)
					print('Gerado',p)
					break
		#	input()	
				


		 		
			
	#	print(z)		
				
		p,f = latex_pages(*z,pref=str(m),amigos_secretos_presentes_imagens=amigos)	
		pag.append(p)
		fila.extend(f)

	m += len(permutacoes)	

print('\a\b')
input('Pronto para gerar....')

pdf(fila)
print('\nPáginas geradas')
pdf(latex_dobra(pag)[1])

print('\a\b\t Concluído!')