
.PHONY: tar clean

all : article.pdf slides.pdf

article.pdf: article.tex biblio.bib Makefile
	pdflatex $^
	bibtex article
	pdflatex $^
	pdflatex $^

slides.pdf: slides.tex Makefile
	pdflatex $^
	pdflatex $^

clean:
	rm -f *.toc *.aux *.log *.bbl *.blg *.dvi *.nav *.out *.snm *.lof *.vrb

# Run 'make zip' to produce the final archive
# You can also add .mlw and .pl files and generated datafiles
zip: \
 25ARIA.pdf \
 25RAISER.pdf \
 23efcs.pdf \
 25SATsym-sps.pdf \
 22combi.pdf\
 14saw.pdf \
 article.tex article.pdf biblio.bib \
 slides.tex slides.pdf \
 measure.pl valid.sh write_swi.pl util.pl write_swi \
 Makefile
	zip groupeTPnomEquipe2526.zip $^

enum: permut.pl
	swipl -s permut.pl

