import re
import sys

from setuptools import setup, Extension

USE_CYTHON = False

if "--use-cython" in sys.argv:
    USE_CYTHON = True
    sys.argv.remove("--use-cython")

ext_modules = [Extension('kovit.citers', sources=['extensions/citers.cpp']),
               Extension('kovit.cjson', sources=['kovit/pjson.{}'.format('py' if USE_CYTHON else 'c')])]

if USE_CYTHON:
    from Cython.Build import cythonize

    ext_modules = cythonize(ext_modules)

version = ''
with open('kovit/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('version is not set')

readme = ''
with open('README.rst', 'r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='kovit',
    python_requires='>=3.5',
    version=version,
    packages=['kovit'],
    url='https://github.com/Teriks/kovit',
    license='BSD 3-Clause',
    author='Teriks',
    author_email='Teriks@users.noreply.github.com',
    description='Generic incrementally buildable Markov chains for text generation and other purposes.',
    long_description=readme,
    install_requires=['cffi', 'ijson', 'ujson'],
    ext_modules=ext_modules,
    classifiers=[
        'Development Status :: 2 - Pre Alpha',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
    ]
)
