FILENAME = CHEP_2021_proposal

date = $(shell date +%Y-%m-%d)
output_file = draft_$(date).pdf

figure_src = $(wildcard figures/*.tex figures/*/*.tex)
figure_list = $(figure_src:.tex=.pdf)

LATEX = pdf #pdflatex
# LATEX = xelatex
# LATEX = lualatex

BIBTEX = bibtex
# BIBTEX = biber

default: document copy_draft

all: default

figures: $(figure_list)

# Target assumes figure source is in same directory as expected figure path
figures/%.pdf: figures/%.tex
	latexmk -$(LATEX) -interaction=nonstopmode -halt-on-error $(basename $@)
	mv $(notdir $(basename $@)).pdf $(basename $@).pdf
	rm $(notdir $(basename $@)).*

text:
	latexmk -$(LATEX) -logfilewarnings -halt-on-error $(FILENAME)

document: figures text

copy_draft:
	rsync $(FILENAME).pdf $(output_file)

clean:
	rm -f *.aux *.bbl *.blg *.dvi *.idx *.lof *.log *.lot *.toc \
		*.xdy *.nav *.out *.snm *.vrb *.mp \
		*.synctex.gz *.brf *.fls *.fdb_latexmk \
		*.glg *.gls *.glo *.ist *.alg *.acr *.acn

clean_figures:
	rm -f $(figure_list)

clean_drafts:
	rm -f draft_*.pdf

realclean: clean clean_figures
	rm -f *.ps *.pdf

lint:
	grep -E --color=always -r -i --include=\*.tex --include=\*.bib "(\b[a-zA-Z]+) \1\b" || true

final:
	if [ -f *.aux ]; then \
		$(MAKE) clean; \
	fi
	$(MAKE) figures
	$(MAKE) abstract
	$(MAKE) text
	$(MAKE) clean
	$(MAKE) lint
