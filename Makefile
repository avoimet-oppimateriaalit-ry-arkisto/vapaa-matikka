pdf:
	pdflatex --shell-escape book.tex
clean:
	rm -f *~ *.aux *.toc *.log
