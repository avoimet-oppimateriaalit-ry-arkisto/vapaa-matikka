# -*- coding: UTF-8 -*-

from kuva import *

def kuvaajapohja(minX, maxX, minY, maxY, leveys = None, korkeus = None, nimiX = "", nimiY = "", ruudukko = True):
	"""Luo kuvaajapohja kuvaajalle jossa X-koordinaatit ovat välillä [minX, maxX]
	ja Y-koordinaatit välillä [minY, maxY]. Kuvaajapohjan koko on
	'leveys' x 'korkeus'. Mikäli vain toinen parametreista 'leveys' ja 'korkeus'
	puuttuu, se lasketaan toisen perusteella säilyttäen kuvasuhteen. Mikäli
	molemmat puuttuvat, tehdään kuvaajapohjasta saman kokoinen kuin
	koordinaattialoista. On oltava minX <= 0 <= maxX ja minY <= 0 <= maxY.
	Kuvaajapohja rajoittaa piirron alueelle [minX, maxX] x [minY, maxY].
	nimiX:llä ja nimiY:llä voidaan nimetä akselit.
	Pohjaan piirretään ruudukko jos 'ruudukko' on True."""
	
	ret = AsetusPalautin()
	
	if minX > 0 or maxX < 0 or minY > 0 or maxY < 0:
		raise ValueError("kuvaajapohja: On oltava minX <= 0 <= maxX ja minY <= 0 <= maxY.")
	
	if minX == maxX or minY == maxY:
		raise ValueError("kuvaajapohja: On oltava minX < maxX ja minY < maxY.")
	
	if leveys is None and korkeus is None:
		leveys = maxX - minX
		korkeus = maxY - minY
	
	if leveys is None:
		leveys = (maxX - minX) * float(korkeus) / (maxY - minY)
	
	if korkeus is None:
		korkeus = (maxY - minY) * float(leveys) / (maxX - minX)
	
	leveys = float(leveys)
	korkeus = float(korkeus)
	
	# Siirrytään uuden kuvaajan koordinaatteihin.
	skaalaaX(leveys / (maxX - minX))
	skaalaaY(korkeus / (maxY - minY))
	
	siirraX(minX)
	siirraY(minY)
	
	# Piirretään ruudukko.
	if ruudukko:
		varit = ["black!30!white", "black!15!white", "black!8!white", "black!4!white", "black!2!white"]
		valit = [64.0, 32.0, 16.0, 8.0, 4.0, 2.0, 1.0, 0.5, 0.25, 0.125]
		rivit = []
		
		def piirraPystyViiva(X, vari):
			vari = varit[min(vari, len(varit) - 1)]
			
			alku = muunna((X, minY))
			loppu = muunna((X, maxY))
			rivit.append("\\draw[color={}] {} -- {};\n".format(vari, tikzPiste(alku), tikzPiste(loppu)));
		
		def piirraVaakaViiva(Y, vari):
			vari = varit[min(vari, len(varit) - 1)]
			
			alku = muunna((minX, Y))
			loppu = muunna((maxX, Y))
			rivit.append("\\draw[color={}] {} -- {};\n".format(vari, tikzPiste(alku), tikzPiste(loppu)));
		
		pvari = 0
		vvari = 0
		for vali in valit:
			if vali * tila.asetukset['xmuunnos'][0] >= 0.37:
				kaytetty = False
				X = vali
				while(X < maxX + 0.0001):
					kaytetty = True
					piirraPystyViiva(X, pvari)
					X += vali
				X = -vali
				while(X > minX - 0.0001):
					kaytetty = True
					piirraPystyViiva(X, pvari)
					X -= vali
				if kaytetty: pvari += 1
			
			if vali * tila.asetukset['ymuunnos'][0] >= 0.37:
				kaytetty = False
				Y = vali
				while(Y < maxY + 0.0001):
					kaytetty = True
					piirraVaakaViiva(Y, vvari)
					Y += vali
				Y = -vali
				while(Y > minY - 0.0001):
					kaytetty = True
					piirraVaakaViiva(Y, vvari)
					Y -= vali
				if kaytetty: vvari += 1
		
		rivit.reverse()
		for rivi in rivit:
			tila.out.write(rivi)
	
	# Piirretään pohjaristi.
	nuoli = "\\draw[arrows=-triangle 45, thick] {} -- {};\n"
	valku = vekSumma(muunna((minX, 0)), (-0.2, 0))
	vloppu = vekSumma(muunna((maxX, 0)), (0.6, 0))
	palku = vekSumma(muunna((0, minY)), (0, -0.2))
	ploppu = vekSumma(muunna((0, maxY)), (0, 0.6))
	tila.out.write("\\draw[arrows=-triangle 45, thick] {} -- {} node[above] {{{}}};\n".format(tikzPiste(valku), tikzPiste(vloppu), nimiX))
	tila.out.write("\\draw[arrows=-triangle 45, thick] {} -- {} node[right] {{{}}};\n".format(tikzPiste(palku), tikzPiste(ploppu), nimiY))
	
	# Piirretään asteikko.
	asteikkovalit = [1, 2, 4, 8, 16, 32, 64]
	
	def piirraXKohta(X):
		alku = vekSumma(muunna((X, 0)), (0, -0.09))
		kohta = vekSumma(muunna((X, 0)), (0.1, 0))
		loppu = vekSumma(muunna((X, 0)), (0, 0.09))
		tila.out.write("\\draw[line width=1.2pt] {} -- {};\n".format(tikzPiste(alku), tikzPiste(loppu)))
		tila.out.write("\\draw {} node[above] {{\\footnotesize {}}};\n".format(tikzPiste(kohta), X))
	
	def piirraYKohta(Y):
		alku = vekSumma(muunna((0, Y)), (-0.09, 0))
		kohta = muunna((0, Y))
		loppu = vekSumma(muunna((0, Y)), (0.09, 0))
		tila.out.write("\\draw[line width=1.2pt] {} -- {};\n".format(tikzPiste(alku), tikzPiste(loppu)))
		tila.out.write("\\draw {} node[right] {{\\footnotesize {}}};\n".format(tikzPiste(kohta), Y))
	
	for vali in asteikkovalit:
		if vali * tila.asetukset['xmuunnos'][0] >= 0.67:
			X = vali
			while X < maxX + 0.0001:
				piirraXKohta(X)
				X += vali
			
			X = -vali
			while X > minX - 0.0001:
				piirraXKohta(X)
				X -= vali
			
			break
	
	for vali in asteikkovalit:
		if vali * tila.asetukset['ymuunnos'][0] >= 0.67:
			Y = vali
			while Y < maxY + 0.0001:
				piirraYKohta(Y)
				Y += vali
			
			Y = -vali
			while Y > minY - 0.0001:
				piirraYKohta(Y)
				Y -= vali
			
			break
	
	# Rajaa piirto.
	rajaa(minX = minX, maxX = maxX, minY = minY, maxY = maxY)
	
	return ret

def parametrikuvaaja(x, y, a = 0, b = 1, nimi = "", kohta = None, suunta = (1, 0)):
	"""Piirrä parametrikäyrä (x(t), y(t)), kun t käy läpi välin [a, b].
	x ja y voivat olla funktioita tai merkkijonokuvauksia t:n funktiosta.
	Esimerkiksi paraabeli välillä [-1, 1] piirretään kutsulla
	piirraKayra(lambda t: t, lambda t: t**2, -1, 1) tai
	piirraKayra("t", "t**2", -1, 1).
	'nimi' kirjoitetaan kohtaan 'kohta' suuntaan 'suunta'. Mikäli kohtaa ei
	anneta, nimi kirjoitetaan käyrän viimeiseen pisteeseen. Mikäli kohta on
	yksi luku, nimi laitetaan käyrän arvoon parametrin arvolla 'kohta'. Muuten
	käytetään arvoa 'kohta' pisteenä."""
	
	x = funktioksi(x, "t")
	y = funktioksi(y, "t")
	
	a = float(a)
	b = float(b)
	if a >= b:
		raise ValueError("piirraKayra: alarajan on oltava pienempi kuin ylärajan.")
	
	t = a
	viim_t = a # Viimeinen sisäpuolella oleva t:n arvo.
	dt = (b - a) / 300
	
	paksuus = "{}pt".format(tikzLuku(tila.haePaksuus()))
	vari = tila.asetukset['piirtovari']
	
	datafp = [None]
	filename = [None]
	def lopetaTiedosto():
		if datafp[0] is not None:
			datafp[0].close()
			tila.out.write("\\draw[line width={}, color={}] plot[smooth] file{{{}}};\n".format(paksuus, vari, filename[0]))
		datafp[0] = None
		filename[0] = None
	
	def aloitaTiedosto():
		if datafp[0] is None:
			tila.data_id += 1
			filename[0] = "kuva-tmp-data{}.txt".format(tila.data_id)
			datafp[0] = open(filename[0], "w")
	
	while t <= b:
		P = (x(t), y(t))
		if onkoSisapuolella(P):
			viim_t = t
			X, Y = muunna(P)
			aloitaTiedosto()
			datafp[0].write("{} {}\n".format(tikzLuku(X), tikzLuku(Y)))
		else:
			lopetaTiedosto()
		
		t += dt
	lopetaTiedosto()
	
	# Kirjoitetaan nimi.
	if kohta is None:
		kohta = (x(viim_t), y(viim_t))
	elif isinstance(kohta, int) or isinstance(kohta, float):
		kohta = (x(kohta), y(kohta))
	
	nimeaPiste(kohta, nimi, suunta[0], suunta[1])

def kuvaaja(f, a = None, b = None, nimi = "", kohta = None, suunta = (1, 0)):
	"""Piirrä funktion f kuvaaja (f joko funktio tai x:n funktion
	merkkijonokuvaus). X-koordinaatti käy läpi välin [a, b], jos jompi kumpi
	jätetään pois, käytetään X-rajaa. Siis esimerkiksi kuvaajapohjassa ei yleensä
	erikseen tarvitse ilmoittaa väliä [a, b]. 'nimi', 'kohta' ja 'suunta'
	toimivat kuten parametrikäyrissä."""
	
	if a is None: a = tila.asetukset['minX']
	if b is None: b = tila.asetukset['maxX']
	
	if a == float("-inf"): raise ValueError("kuvaaja: X-alaraja puuttuu.")
	if b == float("inf"): raise ValueError("kuvaaja: X-yläraja puuttuu.")
	
	f = funktioksi(f, "x")
	parametrikuvaaja("t", f, a, b, nimi, kohta, suunta)
