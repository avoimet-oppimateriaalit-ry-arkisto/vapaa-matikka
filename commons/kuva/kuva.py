# -*- coding: UTF-8 -*-

import tila
from util import *

def muunna(P):
	"""Muunna piirrettävä piste (2-tuple) pisteeksi kuvapinnalla."""
	x, y = P
	a1, b1 = tila.asetukset['xmuunnos']
	a2, b2 = tila.asetukset['ymuunnos']
	
	return (a1 * x + b1, a2 * y + b2)

def onkoSisapuolella(P):
	"""Onko piste 'P' rajojen sisäpuolella?"""
	
	X, Y = P
	
	ret = True
	ret &= X >= tila.asetukset['minX']
	ret &= X <= tila.asetukset['maxX']
	ret &= Y >= tila.asetukset['minY']
	ret &= Y <= tila.asetukset['maxY']
	
	return ret

def aloitaKuva():
	"""Aloita kuvan piirtäminen. Kutsuttava aina ennen muita operaatioita, 
	lopetettava kutsumalla lopeta(). LaTeX-ympäristö kutsuu yleensä aloitaKuva-
	ja lopetaKuva-funktioita automaattisesti."""
	
	tila.out = open("kuva-tmp-output.txt", "w")
	
	tila.out.write("\\begin{tikzpicture}\n")

def lopetaKuva():
	"""Lopeta kuvan, joka aloitettiin kutsulla aloita(), piirtäminen.
	LaTeX-ympäristö kutsuu yleensä aloitaKuva- ja lopetaKuva-funktioita
	automaattisesti."""
	
	tila.out.write("\\end{tikzpicture}\n")
	
	tila.out.close()

def nimeaPiste(P, nimi, vaaka = 1, pysty = -1):
	"""Kirjoita LaTeX-koodina annettu 'nimi' pisteen P viereen, suunnilleen
	suuntaan (vaaka, pysty)."""
	
	nodepos = ""
	
	if pysty < 0:
		nodepos += "below "
	elif pysty > 0:
		nodepos += "above "
	
	if vaaka < 0:
		nodepos += "left "
	elif vaaka > 0:
		nodepos += "right "
	
	nodepos = nodepos[:-1]
	
	if pysty and vaaka:
		nodepos += "=-0.07cm"
	
	tila.out.write("\draw[color={}] {} node[{}] {{{}}};\n".format(tila.asetukset['piirtovari'], tikzPiste(muunna(P)), nodepos, nimi))

class AsetusPalautin:
	"""Tallentaa konstruktorissaan asetukset ja palauttaa ne __exit__-funktiossaan."""
	
	def __init__(self):
		self.asetukset = tila.asetukset.copy()
	
	def __enter__(self):
		pass
	
	def __exit__(self, type, value, traceback):
		tila.asetukset = self.asetukset

# Funktiot piirtoasetusten muuttamiseen. Kaikkia funktioita voi käyttää
# with-lauseessa, jolloin with-blokin jälkeen asetukset palaavat ennalleen.

def skaalaaX(kerroin):
	"""Skaalaa X-koordinaatteja kertoimella 'kerroin'."""
	
	ret = AsetusPalautin()
	kerroin = float(kerroin)
	
	a, b = tila.asetukset['xmuunnos']
	tila.asetukset['xmuunnos'] = (kerroin * a, b)
	
	tila.asetukset['minX'] /= kerroin
	tila.asetukset['maxX'] /= kerroin
	
	return ret

def skaalaaY(kerroin):
	"""Skaalaa Y-koordinaatteja kertoimella 'kerroin'."""
	
	ret = AsetusPalautin()
	kerroin = float(kerroin)
	
	a, b = tila.asetukset['ymuunnos']
	tila.asetukset['ymuunnos'] = (kerroin * a, b)
	
	tila.asetukset['minY'] /= kerroin
	tila.asetukset['maxY'] /= kerroin
	
	return ret

def siirraX(siirto):
	"""Siirrä X-koordinaatteja."""
	
	ret = AsetusPalautin()
	
	a, b = tila.asetukset['xmuunnos']
	tila.asetukset['xmuunnos'] = (a, b + siirto)
	
	return ret

def siirraY(siirto):
	"""Siirrä Y-koordinaatteja."""
	
	ret = AsetusPalautin()
	
	a, b = tila.asetukset['ymuunnos']
	tila.asetukset['ymuunnos'] = (a, b + siirto)
	
	return ret

def skaalaa(kerroin):
	"""Skaalaa koordinaatteja kertoimella 'kerroin'."""
	ret = AsetusPalautin()
	
	skaalaaX(kerroin)
	skaalaaY(kerroin)
	
	return ret

def rajaa(minX = None, maxX = None, minY = None, maxY = None):
	"""Aseta X- tai Y-koordinaattien piirtoja rajaavia ala- ja ylärajoja."""
	
	ret = AsetusPalautin()
	
	if minX is not None:
		tila.asetukset['minX'] = minX
	
	if maxX is not None:
		tila.asetukset['maxX'] = maxX
	
	if minY is not None:
		tila.asetukset['minY'] = minY
	
	if maxY is not None:
		tila.asetukset['maxY'] = maxY
	
	return ret

def vari(uusivari):
	"""Aseta piirrossa käytettävä väri annettuun TiKZ-värikuvaukseen."""
	
	ret = AsetusPalautin()
	tila.asetukset['piirtovari'] = uusivari
	return ret

def paksuus(kerroin):
	"""Aseta käyrien viivanpaksuus alkuperäiseen paksuuteen kerrottuna
	luvulla 'kerroin'."""
	
	ret = AsetusPalautin()
	tila.asetukset['piirtopaksuus'] = kerroin
	return ret
	
def muutaPaksuus(kerroin):
	"""Kerro nykyistä käyrien viivan paksuutta luvulla 'kerroin'."""
	
	ret = AsetusPalautin()
	tila.asetukset['piirtopaksuus'] *= kerroin
	return ret

def piste(P, nimi = "", suunta = (1, 0)):
	"""Piirrä piste 'P' kuvaan. Nimi laitetaan suuntaan 'suunta' (ks. nimeaPiste)."""
	
	vari = tila.asetukset['piirtovari']
	tila.out.write("\\fill[color={}] {} circle (0.07);\n".format(vari, tikzPiste(muunna(P))))
	
	nimeaPiste(P, nimi, suunta[0], suunta[1])
