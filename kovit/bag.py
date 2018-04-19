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
from collections import namedtuple

Item = namedtuple('Item', ['value', 'count'])


class _NoItem:
    pass


class ProbabilityBag:

    @staticmethod
    def from_iterable_counts(i):
        r = ProbabilityBag()
        i = iter(i)
        for value, count in zip(i, i):
            r._items[value] = Item(value, count)
            r._count += count

    def __init__(self, items=None):
        self._items = {}
        self._count = 0
        if items:
            for i in items:
                self.add(i)

    def __len__(self):
        return self._count

    def get(self, item, default=None):
        return self._items.get(item, default)

    def merge(self, other):
        for value, count in other.choices():
            self.add(value, count)

    def add(self, item, count=1):
        i = self.get(item, default=_NoItem)

        if i is _NoItem:
            self._items[item] = Item(item, count)
        else:
            self._items[item] = Item(item, i.count + count)

        self._count += count

    @property
    def count(self):
        return self._count

    @property
    def unique_count(self):
        return len(self._items)

    def choices_weights(self):
        for i in self._items.values():
            yield (i.value, i.count / len(self))

    def choices(self):
        for i in self._items.values():
            yield (i.value, i.count)

    def values(self):
        return (v.value for v in self._items.values())

    def __eq__(self, other):
        if not isinstance(other, ProbabilityBag):
            raise ValueError('Cannot compare ProbabilityBag to "{}"'.format(type(other).__name__))

        if self.unique_count != other.unique_count or self.count != other.count:
            return False

        for value, count in self.choices():
            o_item = other.get(value, None)
            if o_item is None or o_item.count != count:
                return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def choose(self):
        r = random.uniform(0, self._count)
        up_to = 0
        for item in self._items.values():
            if up_to + item.count >= r:
                return item.value
            up_to += item.count

    def __str__(self):
        return str(self._items)

    def __repr__(self):
        return self.__str__()
