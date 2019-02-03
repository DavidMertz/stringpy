from collections.abc import Iterable, Collection, Mapping
# from itertools import chain


class Vector(object):
    def __init__(self, it):
        # Either concrete collection or iterable
        self._lazy = False
        self._it = it

        if not isinstance(it, Iterable):
            raise TypeError("Vector can only be initialized with an iterable")
        elif not isinstance(it, Collection):
            self._lazy = True
        elif isinstance(it, Mapping):
            raise TypeError("Ambiguity vectorizing a map, perhaps try "
                            "it.keys(), it.values(), or it.items()")

    def __iter__(self):
        return iter(self._it)

    def __contains__(self, x):
        if self._lazy:
            raise TypeError("Iterators cannot test membership. "
                            "Vector.concretize() will create a collection")
        return x in self._it

    def __getattr__(self, attr):
        if self._lazy:
            def method(*args, **kws):
                def _nested(*args, **kws):
                    for item in self._it:
                        elem_method = getattr(type(item), attr)
                        yield elem_method(item, *args, **kws)
                return Vector(_nested(*args, **kws))
            return method

        else:
            def method(*args, **kws):
                cast = type(self._it)
                items = []
                for item in self._it:
                    elem_method = getattr(type(item), attr)
                    items.append(elem_method(item, *args, **kws))
                return Vector(cast(items))
            return method

    def __str__(self):
        return "<Vector of %s>" % str(self._it)

    def __repr__(self):
        return "<Vector of %s>" % repr(self._it)

    def __len__(self):
        if self._lazy:
            raise TypeError("Iterators do not have a length. "
                            "Vector.concretize() will create a collection")
        return len(self._it)

    def concretize(self):
        if self._lazy:
            self._it = list(self._it)
            self._lazy = False
        return self
