#!/bin/bash
rm -r ./dist
rm -r ./build
rm -r ./peewee_model_factory.egg-info
python setup.py sdist bdist_wheel
python -m twine upload dist/*