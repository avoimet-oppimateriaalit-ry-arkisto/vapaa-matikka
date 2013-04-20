# -*- coding: UTF-8 -*-

# LaTeX-koodin kirjoitusvirta.
out = None

# Datatiedostojen juokseva numerointi.
data_id = 0

# Nykyiset piirtoasetukset.
asetukset = {
	'minX': float("-inf"), # X-alaraja.
	'maxX': float("inf"), # X-yläraja.
	'minY': float("-inf"), # Y-alaraja.
	'maxY': float("inf"), # Y-yläraja.
	'xmuunnos': (1, 0), # X-koordinaatin muunnos (kulmakerroin, vakiotermi).
	'ymuunnos': (1, 0), # Y-koordinaatin muunnos (kulmakerroin, vakiotermi).
	'piirtovari': "black", # Piirrossa käytettävä TiKZ-väri.
	'piirtopaksuus': 1, # Piirrossa käytettävä viivan paksuus.
}

def haePaksuus():
	"""Hae nykyinen viivan paksuus pt:nä."""
	return asetukset['piirtopaksuus']