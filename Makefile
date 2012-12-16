pdf:
	pdflatex -shell-escape book.tex
index: pdf
	makeindex book
	pdflatex -shell-escape book.tex
clean:
	rm -f *~ *.aux *.toc *.log *.idx *.ind *.ilg
