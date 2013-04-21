# -*- coding: UTF-8 -*-

from math import *

def funktioksi(funktio, muuttuja):
	"""Jos funktio on merkkijono, tulkitse se muuttujan funktioksi.
	Muussa tapauksessa palautetaan alkuperäinen funktio."""
	if isinstance(funktio, str):
		return eval("lambda {}: {}".format(muuttuja, funktio))
	else:
		return funktio

def tikzLuku(luku):
	"""Muotoile luku niin ettei TiKZ huuda 'Dimension too large.'"""
	return "{:.10f}".format(float(luku))

def tikzPiste(P):
	"""Muotoile piste (kahden koordinaatin tuple) oikein TiKZille."""
	X, Y = P
	
	return "({}, {})".format(tikzLuku(X), tikzLuku(Y))

def vekSumma(P, V):
	"""Laske 2D-pistetuplejen P ja V summa."""
	
	X1, Y1 = P
	X2, Y2 = V
	
	return (X1 + X2, Y1 + Y2)

def vekSkaalaa(V, c):
	"""Laske vektori V skaalattuna kertoimella c."""
	
	return (c * V[0], c * V[1])