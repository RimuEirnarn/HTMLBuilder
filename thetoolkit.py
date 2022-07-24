try:
    import _core
    import elements
except ImportError:
    from . import _core
    from . import elements


class BaseToolkit:
    def __init__(self, *args, **kwargs):
        self.body = elements.HTML(*args, **kwargs)

    def __lshift__(self, other):
        self.body << other

    def __getitem__(self, other):
        self.body[other]

    def compile(self, level=1):
        return self.body.compile(level)


class BulletList(BaseToolkit):
    def __init__(self, *items, classList=None, **kwargs):
        item = [elements.li(item_) for item_ in items if item_]
        self.body = elements.ul(*item, **kwargs)
        if classList is not None and isinstance(classList, (tuple, list, set)):
            self.body.class_ = " ".join(classList)

    def push(self, item):
        self.body.append(elements.li(item))

    def remove(self, item):
        k = None
        for n in self.body.iterchild():
            if n[0] == item:
                k = n
        if k is not None:
            self.body.remove(k)

    def insert(self, index: int, item):
        self.body.insert(index, item)

# Create some class to 'auto' create some elements to create some fascinating stuff like table, etc.


class Table(BaseToolkit):
    def __init__(self, object: dict[str, list[str]]):
        for n in object.items():
            if not isinstance(n[1], (list, tuple, set)):
                raise Exception(
                    "Cannot mark the table data. Invalid child types.")
        self.body = elements.table()
        self._object = object
        self._update()

    def _update(self):
        object = self._object
        itemed = tuple(object.items())
        root = elements.tr()
        na = list()
        for i,k in enumerate(itemed):
            root << elements.th(k[0])
            nroot = elements.tr()
            for i_ in range(len(k[1])):
                try:
                    nroot << elements.td(itemed[i_][1][i])
                except IndexError:
                    nroot << elements.td("null") # Occurred when supposed-length is not satisfied.
            na.append(nroot)

        self.body << root
        [self.body << a for a in na]

    def update(self, new_dict):
        self.body.clearchild()
        self._object.update(new_dict)
        self._update()