# Copyright (c) 2018, Teriks
# All rights reserved.
#
# kovit is distributed under the following BSD 3-Clause License
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import random
from collections import defaultdict

try:
    import kovit.json as _kovit_json
except ImportError:
    import kovit.pjson as _kovit_json

from kovit.bag import ProbabilityBag


class _NoItem:
    pass


def _tuplefy(items):
    return ((i,) if not isinstance(i, tuple) else i for i in items)


class Chain:
    def __init__(self):
        self._c = {}

    def __contains__(self, start):
        return start in self._c

    def __getitem__(self, start):
        return self._c.__getitem__(start)

    def __setitem__(self, start, next_items):
        self._c.__setitem__(start, ProbabilityBag(_tuplefy(next_items)))

    def __delitem__(self, start):
        self._c.__delitem__(start)

    def __len__(self):
        return len(self._c)

    def get_bag(self, start, default=None):
        return self._c.get(start, default)

    def set_bag(self, start, bag):
        if not isinstance(bag, ProbabilityBag):
            raise ValueError("bag must be of type ProbabilityBag")

        self._c[start] = bag

    def __eq__(self, other):
        if not isinstance(other, Chain):
            raise ValueError('Cannot compare Chain to "{}"'.format(type(other).__name__))

        if len(self) != len(other):
            return False

        for start, bag in self.items():
            o_bag = other.get_bag(start, default=None)
            if o_bag is None:
                return False
            if o_bag != bag:
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def build_frequency_dict(self):
        d = defaultdict(int)
        for start, bag in self._c.items():
            d[start] += 1
            for items, cnt in bag.choices():
                for item in items:
                    d[item] += 1
        return d

    def add_to_bag(self, start, next_items, count=1):
        """
        Cumulatively add a sequential run of items that may follow a starting word.

        The items are added into a :py:type:`markovchain.ProbabilityBag` if one exists
        for the start item, otherwise a bag is created and then they are added.


        :param start: Start item
        :param next_items: An iterable run of items that may follow the start item in order
        :param count: Number of occurrences to add
        """
        next_items = tuple(next_items)

        entry = self.get_bag(start, _NoItem)

        if entry is _NoItem:
            new_bag = ProbabilityBag()
            new_bag.add(next_items, count=count)
            self.set_bag(start, new_bag)
        else:
            entry.add(next_items, count=count)

    def starts(self):
        return self._c.keys()

    def items(self):
        return self._c.items()

    def random_start(self):
        return random.choice(tuple(self.starts()))

    def walk(self, max_items=0, start=None, repeat=False, start_chooser=None, next_chooser=None):

        if start_chooser is None:
            start_chooser = self.random_start

        if next_chooser is None:
            def next_chooser(bag):
                return bag.choose()

        if start is None:
            start = (start_chooser(),)
        else:
            start = (start,)

        cnt = 0

        while True:
            assert type(start) is tuple

            for start_next in start:
                if max_items == 0 or cnt < max_items:
                    yield start_next
                    cnt += 1
                else:
                    return

            if len(start):
                while True:
                    # start_next will be set to the last item
                    # iterated to above if any iteration happened
                    bag = self.get_bag(start_next, default=None)
                    if bag is not None:
                        break
                    if not repeat:
                        return
                    start_next = start_chooser()
                start = next_chooser(bag)
            elif repeat:
                start = (start_chooser(),)
            else:
                return

    def __str__(self):
        return str(self._c)

    def __repr__(self):
        return self.__str__()

    def dump_json(self, file, frequency_compress=True, large_file=False):
        if large_file:
            _kovit_json.dump_json_big(self, file, frequency_compress=frequency_compress)
        else:
            _kovit_json.dump_json_small(self, file, frequency_compress=frequency_compress)

    def load_json(self, file, merge=False, large_file=False):
        if large_file:
            _kovit_json.load_json_big(self, file, merge=merge)
        else:
            _kovit_json.load_json_small(self, file, merge=merge)

    def clear(self):
        self._c.clear()