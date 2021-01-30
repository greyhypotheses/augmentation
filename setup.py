import setuptools

NAME = 'augmentation'
VERSION = '0.0.1'
DESCRIPTION = 'Exploring image augmentation'
AUTHOR = 'greyhypotheses'
URL = 'https://github.com/greyhypotheses/augmentation'
PYTHON_REQUIRES = '=3.7.9'

with open('README.md') as f:
    readme_text = f.read()

setuptools.setup()(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=readme_text,
    author=AUTHOR,
    url=URL,
    python_requires=PYTHON_REQUIRES,
    package_dir={'': 'src'},
    packages=setuptools.find_packages('src', exclude=['docs', 'tests'])
)
