import os
import sys
import unittest

import kovit.piters as python_iters
import kovit_citers as native_iters

script_dir = os.path.dirname(os.path.realpath(__file__))

sys.path.insert(1, os.path.abspath(
    os.path.join(script_dir, os.path.join('..', '..'))))


class NamespaceTest(unittest.TestCase):

    def test_missing_params(self):

        for i in native_iters.iter_window([1, 2, 3, 4, 5]):
            pass

        with self.assertRaises(TypeError):
            for i in native_iters.iter_window():
                pass

        for i in native_iters.iter_runs([1, 2, 3, 4, 5]):
            pass

        with self.assertRaises(TypeError):
            for i in native_iters.iter_runs():
                pass

        # ===

        for i in python_iters.iter_window([1, 2, 3, 4, 5]):
            pass

        with self.assertRaises(TypeError):
            for i in python_iters.iter_window():
                pass

        for i in python_iters.iter_runs([1, 2, 3, 4, 5]):
            pass

        with self.assertRaises(TypeError):
            for i in python_iters.iter_runs():
                pass

    def test_iter_equivalence(self):

        # random
        seq = [94,
               20,
               15,
               64,
               8,
               55,
               87,
               30,
               50,
               54,
               37,
               6,
               56,
               83,
               72,
               29,
               91,
               76,
               92,
               77,
               2,
               99,
               9,
               46,
               66,
               47,
               10,
               68,
               86,
               69,
               45,
               40]

        for i in range(1, len(seq)):
            r1 = list(python_iters.iter_window(seq, i))
            r2 = list(native_iters.iter_window(seq, i))
            self.assertSequenceEqual(r1, r2)

            r1 = list(python_iters.iter_runs(seq, i))
            r2 = list(native_iters.iter_runs(seq, i))
            self.assertSequenceEqual(r1, r2)

        r1 = list(python_iters.iter_window(seq))
        r2 = list(native_iters.iter_window(seq))
        self.assertSequenceEqual(r1, r2)

        r1 = list(python_iters.iter_runs(seq))
        r2 = list(native_iters.iter_runs(seq))
        self.assertSequenceEqual(r1, r2)
