# install GNU make to run make
MAKE = make

help:
	@echo "make <OPTIONS>"
	@echo OPTIONS:
	@echo "  help"
	@echo "  test"
	@echo "  docclean"
	@echo "  docapidoc"
	@echo "  dochtml"
	@echo "  clean"
	@echo "  setup"
	@echo "  build"
	@echo "  testupload"
	@echo "  upload"

.PHONY = help, test, docclean, docapidoc, dochtml, clean, setup, build, testupload, upload, tox

test:
	pytest -s -v  tests/

docclean:
	$(MAKE) -C docs clean

docapidoc:
	sphinx-apidoc -o ./docs/source -e ./src/lxmlutil
	$(MAKE) dochtml

dochtml:
	$(MAKE) docclean
	$(MAKE) -C docs html

clean:
	rm -rf "dist"
	rm -rf .tox
	rm -rf src/lxml_util.egg-info

setup:
	pip install -e .[docs,tests,dists]
	pip uninstall -y lxml-util

build:
	$(MAKE) clean
	python -m build

testupload:
	twine upload -r testpypi dist/*

upload:
	twine upload dist/* --verbose

tox:
	$(MAKE) clean
	tox