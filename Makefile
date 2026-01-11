# Makefile for automation

PYTHON = python
PIP = pip

.PHONY: setup train test clean

setup:
	$(PIP) install -r requirements.txt

train:
	$(PYTHON) -m src.model

test:
	PYTHONPATH=. pytest tests/

clean:
	rm -rf __pycache__
	rm -rf src/__pycache__
	rm -rf tests/__pycache__
	rm -rf results/*.png
	rm -rf logs/*.log
