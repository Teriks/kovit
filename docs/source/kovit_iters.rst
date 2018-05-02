kovit.iters package
===================

Module Contents
---------------

.. function:: iter_window(items, window_size=1)

    Iterate over tuples of (start_item, (trailing, ..))

    Each item in the sequence is visited as a **start_item**, **window_size** items
    are accumulated after it and returned.

    This is used to produce dense chains where the probabilities of every sequence of length **N**
    coming after after a start item is always known. Even when the trailing sequence is a
    string of multiple items from the source data, as shown below.

    Every item in the sequence will be considered a start item, and the next **N** items will
    be a sequence that is probable to trail that item.

    This produces a very large and accurate Markov chain.

    .. code-block:: python

        items = [1, 2, 3, 4, 5, 6, 7, 8]

        windowed = list(kovit.iters.iter_window(items, 4))

        windowed == [
            (1, (2, 3, 4, 5)),
            (2, (3, 4, 5, 6)),
            (3, (4, 5, 6, 7)),
            (4, (5, 6, 7, 8)),
            (5, (6, 7, 8)),
            (6, (7, 8)),
            (7, (8,)),
            (8, ())]

    :param items: items
    :type items: iterable

    :param window_size: Trailing window size
    :type window_size: int


.. function:: iter_runs(items, run_size=1)

    Iterate over tuples of (start_item, (trailing, ..))

    A **start_item** is taken, and then the next **N** items are considered a trailing
    sequence. The last item in the trailing sequence becomes the new **start_item**.

    This results in a chain that discards the trailing item probabilities inside
    of each trailing sequence of size **N** except for the last.

    Only the last element of the trailing sequence will become a **start_item**.

    Below for instance, the probability of (3,4,5,6) coming after 2 will be unknown in the chain.

    This produces a smaller chain which could be adequate enough for random text generation given
    a particular **run_size**, but one which is does not perfectly model the probability of the next item
    occurring in a sequence.


    .. code-block:: python

        items = [1, 2, 3, 4, 5, 6, 7, 8]

        runs = list(kovit.iters.iter_runs(items, 4))

        runs == [(1, (2, 3, 4, 5)), (5, (6, 7, 8)), (8, ())]

    :param items: items
    :type items: iterable

    :param window_size: Trailing run size
    :type window_size: int