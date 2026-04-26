.PHONY: install ingest graph query lint serve

install:
	python -m pip install -e "."

ingest:
	python tools/ingest.py $(SRC)

graph:
	python tools/build_graph.py $(ARGS)

query:
	python tools/query.py $(Q) $(ARGS)

lint:
	python tools/lint.py $(ARGS)

serve:
	python -m sermon_insight_wiki.app
