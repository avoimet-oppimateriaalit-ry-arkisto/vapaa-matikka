# -*- coding: UTF-8 -*-

# LaTeX-koodin kirjoitusvirta.
_out = None

# Datatiedostojen juokseva numerointi.
_data_id = 0

def aloitaKuva():
	"""Aloita kuvan piirtäminen. Kutsuttava aina ennen muita operaatioita, 
	lopetettava kutsumalla lopeta(). LaTeX-ympäristö kutsuu yleensä aloitaKuva-
	ja lopetaKuva-funktioita automaattisesti."""
	
	global _out
	_out = open("kuva-tmp.out", "w")
	
	_out.write("\\begin{tikzpicture}\n")

def lopetaKuva():
	"""Lopeta kuvan, joka aloitettiin kutsulla aloita(), piirtäminen.
	LaTeX-ympäristö kutsuu yleensä aloitaKuva- ja lopetaKuva-funktioita
	automaattisesti."""
	
	_out.write("\\end{tikzpicture}\n")
	
	_out.close()

def piirraKayra(x, y, a = 0, b = 1):
	"""Piirrä käyrä (x(t), y(t)), kun t käy läpi välin [a, b].
	Esimerkiksi paraabeli välillä [-1, 1] piirretään kutsulla
	piirraKayra(lambda t: t, lambda t: t**2, -1, 1)."""
	
	a = float(a)
	b = float(b)
	if a >= b: raise ValueError("piirraKayra: alarajan on oltava pienempi kuin ylärajan.")
	
	t = a
	dt = (b - a) / 300
	
	global _data_id
	_data_id += 1
	filename = "kuva-data-tmp{}.out".format(_data_id)
	
	with open(filename, "w") as datafp:
		while t <= b:
			datafp.write("{:.10f} {:.10f}\n".format(x(t), y(t)))
			
			t += dt
	
	_out.write("\draw plot file{{{}}};\n".format(filename))
	