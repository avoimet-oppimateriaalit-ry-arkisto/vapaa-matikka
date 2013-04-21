# -*- coding: UTF-8 -*-

import kuva
from kuva import *
import kuvaaja

def pohja(a, b, n = 1, leveys = None, nimi = ""):
	"""Luo lukusuorapohja, jossa on 'n' lukusuoraa välille [a, b], kaikkien
	nimenä 'nimi'. Välin [a, b] pituudeksi tulee 'leveys' (oletuksena b - a)."""
	
	ret = AsetusPalautin()
	
	if n <= 0:
		raise ValueError("lukusuorapohja: Vaaditaan: n > 0.")
	if a >= b:
		raise ValueError("lukusuorapohja: Vaaditaan: a < b.")
	if leveys is None:
		leveys = b - a
	
	# Siirrytään lukusuorien koordinaatistoon.
	skaalaaX(float(leveys) / (b - a))
	skaalaaY(1.3)
	siirraY(0.5)
	
	# Pakotetaan bounding boxi ottamaan mukaan koko alue.
	alku = muunna((a, -0.5))
	loppu = muunna((a, n - 0.5))
	tila.out.write("\\draw[opacity=0] {} -- {};".format(tikzPiste(alku), tikzPiste(loppu)))
	
	# Tallennetaan asetuksiin ympäristön tiedot.
	tila.asetukset['lukusuora_n'] = n
	tila.asetukset['lukusuora_a'] = a
	tila.asetukset['lukusuora_b'] = b
	
	# Piirretään lukusuorat.
	for i in range(n):
		alku = vekSumma(muunna((a, i)), (-0.2, 0))
		loppu = vekSumma(muunna((b, i)), (0.6, 0))
		form = "\\draw[arrows=-triangle 45,line width=0.2mm] {} -- {} node[above] {{{}}}\n;"
		tila.out.write(form.format(tikzPiste(alku), tikzPiste(loppu), nimi))
	
	return ret

def piste(X, i = 1, nimi = ""):
	"""Piirrä ylhäältä lukien i:nteen lukusuoraan piste kohtaan 'X', nimellä 'nimi'.
	Jos i on None, piste piirretään kaikkiin lukusuoriin."""
	
	if i is None:
		for i in range(tila.asetukset['lukusuora_n']):
			piste(X, i + 1, nimi)
		return
	
	P = muunna((X, tila.asetukset['lukusuora_n'] - i))
	vari = tila.asetukset['piirtovari']
	
	tila.out.write("\\fill[color={}] {} circle (0.1);\n".format(vari, tikzPiste(P)))
	tila.out.write("\\draw[color={}] {} node[above] {{\\phantom{{$\\int$}}{}\\phantom{{$\\int$}}}};\n".format(vari, tikzPiste(P), nimi))

def kohta(X, i = 1, nimi = ""):
	"""Merkitse ylhäältä lukien i:nteen lukusuoraan kohta 'X' pienellä
	pystyviivalla, nimellä 'nimi'.
	Jos i on None, piste piirretään kaikkiin lukusuoriin."""
	
	if i is None:
		for i in range(tila.asetukset['lukusuora_n']):
			kohta(X, i + 1, nimi)
		return
	
	Y = tila.asetukset['lukusuora_n'] - i
	vari = tila.asetukset['piirtovari']
	
	keski = muunna((X, Y))
	alku = vekSumma(keski, (0, -0.1))
	loppu = vekSumma(keski, (0, 0.1))
	
	tila.out.write("\\draw[color={}, line width=1.2pt] {} -- {};\n".format(vari, alku, loppu))
	tila.out.write("\\draw[color={}] {} node[above] {{\\phantom{{$\\int$}}{}\\phantom{{$\\int$}}}};\n".format(vari, keski, nimi))

def piirraKuvaaja(f, i = 1):
	"""Piirrä i:nteen lukusuoraan funktion f (voi olla myös merkkijonokuvaus
	x:n funktiosta) kuvaaja. Vain alue, jossa f on välillä [-1, 1], piirretään."""
	
	with palautin():
		siirraY(tila.asetukset['lukusuora_n'] - i)
		skaalaaY(0.5)
		rajaa(minX = tila.asetukset['lukusuora_a'], maxX = tila.asetukset['lukusuora_b'], minY = -1, maxY = 1)
		kuvaaja.piirra(f)
