run:
	python2 client.py
lint:
	python2 -m pylint --disable=superfluous-parens client.py dumpconfig.py
