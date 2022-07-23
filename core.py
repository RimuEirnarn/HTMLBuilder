try:
    import _core
    import elements
except ImportError:
    from . import _core
    from . import elements

class Document:
    def __init__(self):
        self._data = _core.HTML()
        self._data << elements.head()
        self._data << elements.body()
    
    @property
    def body(self):
        return self._data[1]
    
    @property
    def head(self):
        return self._data[0]
    
    def getElementById(self, idname):
        for x in self.body.iterchild():
            if isinstance(x, str):
                pass
            if x.id == idname:
                return x