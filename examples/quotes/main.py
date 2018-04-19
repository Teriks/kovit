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

import time
import timeit

import os

try:
    import ujson as json
except ImportError:
    import json

import re
import textwrap

from kovit import Chain
from kovit.iters import iter_window

import itertools


def get_quotes():
    with open('quotes.json', 'r', encoding='utf-8') as f:
        obj = json.load(f)
        for q in obj:
            yield [i for i in re.split('\s+', q['quoteText'].strip())]


chain = Chain()
chain2 = Chain()


def read():
    for sentence in itertools.chain(get_quotes()):
        for start, next_items in iter_window(sentence, 5):
            chain.add_to_bag(start, next_items)


def dump():
    with open('model.json', 'w') as f:
        chain.dump_json(f)


def load():
    with open('model.json', 'rb') as f:
        chain2.load_json(f, large_file=True)


print("Build Time: {}".format(timeit.timeit(read, number=1)))
print("Dump Time: {}".format(timeit.timeit(dump, number=1)))
print("Load Time: {}".format(timeit.timeit(load, number=1)))

print("Chains Equal: {}".format(chain == chain2))


def gen():
    val = textwrap.fill(' '.join(chain.walk(max_items=300)))
    print(val+os.linesep)


print('--------------')

while True:
    print("Gen Time: {}".format(timeit.timeit(gen, number=1)), os.linesep + "==============")
    time.sleep(5)
