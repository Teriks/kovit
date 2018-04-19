import re

from setuptools import setup, Extension
from Cython.Build import cythonize

ext_modules = [Extension('kovit.citers', sources=['extensions/citers.cpp']),
               Extension('kovit.cjson',  sources=['kovit/pjson.py'])]

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
    description='Generic incrementally build-able Markov chains for text generation and other purposes.',
    long_description=readme,
    install_requires=['cffi', 'ijson', 'ujson'],
    ext_modules=cythonize(ext_modules),
    classifiers=[
        'Development Status :: 2 - Pre Alpha',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
    ]
)
