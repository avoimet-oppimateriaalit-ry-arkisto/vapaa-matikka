# -*- coding: utf-8 -*-
import sys
import os
import re

#filename = sys.argv[1]
#doc = open(filename, 'r')

directory = sys.argv[1]
os.chdir(directory)

replaces = [(r'\\begin{enumerate}[\[a\)\]]*', r'\\begin{alakohdat}'),
			('\\end{enumerate}', '\\end{alakohdat}'),
			(r'(\s+)\\item\s([^*\n]*)', r'\1\\alakohta{ \2 }'),
			(r'\\begin{itemize}[\[a\)\]]*',r'\\begin{alakohdat}'),
			(r'\\end{itemize}',r'\\end{alakohdat}')]

for filename in os.listdir("."):
	if filename.endswith(".tex"):
		doc = open(filename, 'r')

		doc_mod = ''
		for line in doc.readlines():
			line_mod = line
			for r in replaces:
				p = re.compile(r[0], re.VERBOSE)
				line_mod = p.sub(r[1], line_mod)
			
			doc_mod += line_mod + '\n'

		output = open(filename+'.mod', 'w')
		output.write(doc_mod)

