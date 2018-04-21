.. |codecov| image:: https://codecov.io/gh/Teriks/kovit/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/Teriks/kovit

.. |Master Documentation Status| image:: https://readthedocs.org/projects/kovit/badge/?version=latest
    :target: http://kovit.readthedocs.io/en/latest/?badge=latest

.. |pypi| image:: https://badge.fury.io/py/kovit.svg
    :target: https://badge.fury.io/py/kovit

About kovit
===========

|pypi| |Master Documentation Status| |codecov|

kovit is a generic markov chain library that allows for easy incremental chain building.

kovit comes with fast iterator utilities written in C/C++ which can be used to build a
markov chain from a stream of objects produced by a python iterable or generator.

Random chain walks based on trailing item probability are implemented for easy sequence generation.

See: `Quotes Example <https://github.com/Teriks/kovit/blob/master/examples/quotes/main.py>`_



