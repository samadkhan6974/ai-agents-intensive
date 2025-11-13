# Makefile for Day 3: Agent with Memory

run:
	python agent_with_memory.py

clean:
	rm -f memory.json

setup:
	pip install -r requirements.txt
