# -*- coding: UTF-8 -*-

import kuva
from kuva import *
import kuvaaja

def pohja(a, b, leveys = None, nimi = "", n = 1, varaa_tila = True):
	"""Luo lukusuorapohja, jossa on 'n' lukusuoraa välille [a, b], kaikkien
	nimenä 'nimi'. Välin [a, b] pituudeksi tulee 'leveys' (oletuksena b - a).
	Jos varaa_tila on True, lukusuorien ympärille varataan heti suurin
	mahdollinen tila."""
	
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
	if varaa_tila:
		alku = muunna((a, -0.5))
		loppu = muunna((a, n - 0.5))
		tila.out.write("\\draw[opacity=0] {} -- {};".format(tikzPiste(alku), tikzPiste(loppu)))
	
	# Tallennetaan asetuksiin ympäristön tiedot.
	tila.asetukset['lukusuora_n'] = n
	tila.asetukset['lukusuora_a'] = a
	tila.asetukset['lukusuora_b'] = b
	tila.asetukset['lukusuora_alkux'] = vekSumma(muunna((a, 0)), (-0.2, 0))[0]
	tila.asetukset['lukusuora_loppux'] = vekSumma(muunna((b, 0)), (0.6, 0))[0]
	
	# Piirretään lukusuorat.
	for i in range(n):
		alku = vekSumma(muunna((a, i)), (-0.2, 0))
		loppu = vekSumma(muunna((b, i)), (0.6, 0))
		form = "\\draw[arrows=-triangle 45,line width=0.2mm] {} -- {} node[above] {{{}}}\n;"
		tila.out.write(form.format(tikzPiste(alku), tikzPiste(loppu), nimi))
	
	return ret

def nimio(X, nimi = "", i = 0, nimi_ylos = True):
	"""Merkitse ylhäältä lukien i:nteen lukusuoraan kohtaan 'X' teksti 'nimi'.
	Jos i on 0, piste piirretään kaikkiin lukusuoriin."""
	
	if nimi_ylos:
		suunta = "above"
	else:
		suunta = "below"
	
	if i is None or i == 0:
		for i in range(tila.asetukset['lukusuora_n']):
			nimio(X, nimi, i + 1, nimi_ylos)
		return
	
	Y = tila.asetukset['lukusuora_n'] - i
	vari = tila.asetukset['piirtovari']
	
	keski = muunna((X, Y))
	
	tila.out.write("\\draw[color={}] {} node[{}] {{\\phantom{{$\\int$}}{}\\phantom{{$\\int$}}}};\n".format(vari, tikzPiste(keski), suunta, nimi))

def piste(X, nimi = "", i = 0, nimi_ylos = True):
	"""Piirrä ylhäältä lukien i:nteen lukusuoraan piste kohtaan 'X', nimellä 'nimi'.
	Jos i on 0, piste piirretään kaikkiin lukusuoriin."""
	
	if i is None or i == 0:
		for i in range(tila.asetukset['lukusuora_n']):
			piste(X, nimi, i + 1, nimi_ylos)
		return
	
	P = muunna((X, tila.asetukset['lukusuora_n'] - i))
	vari = tila.asetukset['piirtovari']
	
	tila.out.write("\\fill[color={}] {} circle (0.1);\n".format(vari, tikzPiste(P)))
	
	nimio(X, nimi, i, nimi_ylos)

def kohta(X, nimi = "", i = 0, nimi_ylos = True):
	"""Merkitse ylhäältä lukien i:nteen lukusuoraan kohta 'X' pienellä
	pystyviivalla, nimellä 'nimi'.
	Jos i on 0, piste piirretään kaikkiin lukusuoriin."""
	
	if i is None or i == 0:
		for i in range(tila.asetukset['lukusuora_n']):
			kohta(X, nimi, i + 1, nimi_ylos)
		return
	
	Y = tila.asetukset['lukusuora_n'] - i
	vari = tila.asetukset['piirtovari']
	
	keski = muunna((X, Y))
	alku = vekSumma(keski, (0, -0.1))
	loppu = vekSumma(keski, (0, 0.1))
	
	tila.out.write("\\draw[color={}, line width=1.2pt] {} -- {};\n".format(vari, tikzPiste(alku), tikzPiste(loppu)))
	
	nimio(X, nimi, i, nimi_ylos)

def piirraKuvaaja(f, i = 1):
	"""Piirrä i:nteen lukusuoraan funktion f (voi olla myös merkkijonokuvaus
	x:n funktiosta) kuvaaja. Vain alue, jossa f on välillä [-1, 1], piirretään."""
	
	with palautin():
		siirraY(tila.asetukset['lukusuora_n'] - i)
		skaalaaY(0.7)
		rajaa(minX = tila.asetukset['lukusuora_a'], maxX = tila.asetukset['lukusuora_b'], minY = -1, maxY = 1)
		kuvaaja.piirra(f)

def vali(a = None, b = None, a_kuuluu = False, b_kuuluu = False, a_nimi = "", b_nimi = "", i = 1, nimi_ylos = True):
	"""Piirrä i:nteen lukusuoraan väli kohdasta 'a' kohtaan 'b'. Välin
	päätepisteen pois jättäminen tarkoittaa rajoittamatonta väliä.
	Päätepisteet voidaan saada mukaan muuttamalla a_kuuluu tai b_kuuluu Trueksi.
	Alku- ja loppupisteelle voidaan antaa nimet a_nimi ja b_nimi."""
	
	if nimi_ylos:
		suunta = "above"
	else:
		suunta = "below"
	
	Y = tila.asetukset['lukusuora_n'] - i
	
	if a is None:
		ap = (tila.asetukset['lukusuora_alkux'], muunna((0, Y))[1])
	else:
		ap = muunna((a, Y))
	
	if b is None:
		bp = (tila.asetukset['lukusuora_loppux'] - 0.24, muunna((0, Y))[1])
	else:
		bp = muunna((b, Y))
	
	vari = tila.asetukset['piirtovari']
	
	tila.out.write("\\draw[color={},line width=0.6mm] {} -- {}\n;".format(vari, tikzPiste(ap), tikzPiste(bp)))
	
	nimiformat = "\\draw[color={}] {} node[{}] {{\phantom{{$\\int$}}{}\phantom{{$\\int$}}}};\n"
	
	if a is not None:
		tila.out.write("\\fill[color={}] {} circle (0.1)\n;".format(vari, tikzPiste(ap)))
		if not a_kuuluu:
			tila.out.write("\\fill[color=white] {} circle (0.08)\n;".format(tikzPiste(ap)))
		tila.out.write(nimiformat.format(vari, tikzPiste(ap), suunta, a_nimi))
	
	if b is not None:
		tila.out.write("\\fill[color={}] {} circle (0.1)\n;".format(vari, tikzPiste(bp)))
		if not b_kuuluu:
			tila.out.write("\\fill[color=white] {} circle (0.08)\n;".format(tikzPiste(bp)))
		tila.out.write(nimiformat.format(vari, tikzPiste(bp), suunta, b_nimi))

def nuoli(a, b, a_i = 1, b_i = 1):
	"""Piirrä nuoli lukusuoran 'a_i' kohdasta 'a' lukusuoran 'b_i' kohtaan 'b'."""
	
	a_Y = tila.asetukset['lukusuora_n'] - a_i
	b_Y = tila.asetukset['lukusuora_n'] - b_i
	
	ap = muunna((a, a_Y))
	bp = muunna((b, b_Y))
	
	vari = tila.asetukset['piirtovari']
	
	if a_i != b_i:
		nuoliformat = "\\draw[arrows=-triangle 45,thick,color={}] {} -- {};\n"
		tila.out.write(nuoliformat.format(vari, ap, bp))
	else:
		ac = vekSumma(vekSumma(vekSkaalaa(ap, 0.8), vekSkaalaa(bp, 0.2)), (0, -0.7))
		bc = vekSumma(vekSumma(vekSkaalaa(ap, 0.2), vekSkaalaa(bp, 0.8)), (0, -0.7))
		nuoliformat = "\\draw[arrows=-triangle 45,thick,color={}] {} .. controls {} and {} .. {};\n"
		tila.out.write(nuoliformat.format(vari, ap, ac, bc, bp))
		
	