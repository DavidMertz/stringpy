from collections.abc import Iterable, Collection, Mapping


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

    def __getattr__(self, attr):
        if self._lazy:
            return (getattr(item, attr)() for item in self._it)
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
