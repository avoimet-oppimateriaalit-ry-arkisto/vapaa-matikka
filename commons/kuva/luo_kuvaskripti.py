# -*- coding: UTF-8 -*-

"""Lisää skriptin alkuun ja loppuun tarvittavat rivit kuvan luomiseen. Ottaa
parametreina syöte- ja tulostetiedostojen nimet."""

import sys

if __name__ == '__main__':
	infile = open(sys.argv[1])
	outfile = open(sys.argv[2], "w")
	
	outfile.write("from math import *\n")
	outfile.write("import sys\n")
	outfile.write("sys.path.append(\"../commons/kuva/\")\n")
	outfile.write("from kuva import *\n")
	outfile.write("aloitaKuva()\n")
	outfile.write("if True:\n")
	for line in infile:
		outfile.write(" " + line)
	outfile.write("\nlopetaKuva()\n")
	outfile.close()
	