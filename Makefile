run:
	python2 client.py dumpconfig.json
lint:
	python2 -m pylint --disable=superfluous-parens client.py
