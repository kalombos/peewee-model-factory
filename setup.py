import os
from setuptools import setup, find_packages

dependencies = ["peewee", "pytz"]

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="peewee-model-factory",
    version="0.1.1",
    packages=find_packages(),
    install_requires=dependencies,
    author="Nikolay Gorshkov",
    author_email="nogamemorebrain@gmail.com",
    description="A library to create peewee model instances for testing.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/kalombos/peewee-model-factory",
    keywords="python testing fixture generator peewee model factory peewee fixtures",
    license="BSD",

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3'
    ]
)
