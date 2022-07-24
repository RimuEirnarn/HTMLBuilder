"""Core of HTMLBuilder

There's also a good note here, the << and >> are translated to append/push and pop"""

from typing import Any, Callable, List, NoReturn, Protocol, Union

from string import whitespace, punctuation
from re import compile as re_compile, escape as re_escape


class ListLike(Protocol):
    def append(__obj: Any) -> NoReturn:
        ...

    def remove(__obj: Any) -> NoReturn:
        ...

    def pop(index: int) -> Any:
        ...


class ArrayLike(Protocol):
    def push(__obj: Any) -> NoReturn:
        ...

    def remove(__obj: Any) -> NoReturn:
        ...

    def pop(index: int) -> Any:
        ...


try:
    from . import config
except ImportError:
    import config


class ShiftedObject:
    def __init__(self, parent, temp):
        self._parent: Union[ArrayLike, ListLike] = parent
        self._temp = temp

    @staticmethod
    def _getmeth(other) -> Callable[[Any], NoReturn]:
        method = None
        for name in config._shiftable_methods:
            if (method := getattr(other, name, _sentinel)) is not _sentinel:
                if not callable(method):
                    method = None
                break
        if method is None:
            raise AttributeError(
                f"{other} cannot be appended. (See config.py on shiftable methods)")

    def __lshift__(self, other):
        method = self._getmeth(other)
        return method(self._temp)

    def __rshift__(self, other):
        method = self._getmeth(other)
        return method(self._parent.pop(self._parent.index(self._temp)))

    def __getattr__(self, name):
        if (meth := getattr(super(self), name, _sentinel)) is _sentinel:
            return getattr(self._temp, name)
        return meth


_element_openings = "<{name}{values}>"
_element_autoclose = "<{name}{values}/>"
_element_closing = "</{name}>"
_sentinel = object()
_notallowednames = re_compile("["+re_escape(punctuation.replace('_', ''))+"\\s]+" +
                              "[A-Za-z0-9]+["+re_escape(punctuation.replace('_', ''))+"\\s]+")
_notallowedchars = re_compile("["+re_escape(punctuation)+"\\s]+")


class ShiftableArray:
    def __init__(self, *init):
        if len(init) == 1 and isinstance(init[0], (tuple, list)):
            init = init[0]
        self._values = init.copy()

    def __getitem__(self, key):
        return ShiftedObject(self, self._values[key])

    def __lshift__(self, other):
        self._values.append(other)

    def __getattr__(self, name: str):
        if (x := getattr(self, name, _sentinel)) is _sentinel:
            if (x := getattr(self._values, name, _sentinel)) is _sentinel:
                raise AttributeError(f"{name} is undefined")
            return x
        return x


class _BaseElement:
    """Base Element for all HTML elements"""
    _rootnode = None
    _nodes = []
    _nodes_by_name = {}

    # final
    def __init_subclass__(cls, name: str = None, isroot=False, autoclose=False, decrease_level=False, require_close=True, nochild=False, newlineoncompile=True, optimize_child=False, canonical_names: List[str] = None, header=None) -> None:
        if name is None:
            name = cls.__name__
        if name.lower() in _BaseElement._nodes_by_name:
            raise Exception(f"The name of {name} already exists")
        if canonical_names is None:
            canonical_names = ()
        if _notallowedchars.match(name) is not None:
            raise Exception(
                "Name of the elements must not contain invalid characters")
        cls._name = name.lower()
        if _BaseElement._rootnode is not None and isroot is True:
            raise Exception(f"Root has already been assigned to \
                {_BaseElement._rootnode}")
        if isroot is True:
            _BaseElement._rootnode = cls

        def base_fget(name: str):
            def fget(self):
                return self._names[name]

            def fset(self, value: Any):
                self._names[name] = value
            return fget, fset
        init_dict = {}

        for cname in canonical_names:
            if _notallowednames.match(cname) is None:
                g, s = base_fget(cname)
                setattr(cls, cname, property(g, s))
                init_dict[cname] = None

        def __init__(self, *args, **kwargs):
            self._name = name
            self._autoclose = autoclose
            self._newlineoncompile = newlineoncompile
            self._require_close = require_close
            self._decrease_level = decrease_level
            self._nochild = nochild
            self._optimize_child = optimize_child
            self._data = init_dict.copy()
            self._data.update(kwargs)
            self._elements = list(args)
            self._header = header if isroot is True else None

        def finalise(self):
            raise Exception("This class is final")

        if isroot is not True:
            cls.__init_subclass__ = finalise
        cls.__init__ = __init__
        _BaseElement._nodes.append(cls)
        _BaseElement._nodes_by_name[name.lower()] = cls
        return cls

    def __init__(self, *args, **kwargs):
        self._name = None
        self._autoclose = False
        self._data = kwargs.copy()
        self._elements = list(args)

    def _checkElement(self, element):
        if not issubclass(type(element), _BaseElement) and not isinstance(element, str):
            return False
        return True

    def _parseNames(self) -> str:
        a = ""
        for k, v in self._data.items():
            if v is None:
                v = ''
            if v == '':
                continue
            a += f"{k.replace('_','')}={repr(v)} "
        return a[:-1]

    def _nullify(self):
        n = {}
        for k, v in self._data.items():
            if v is None or v == '':
                continue
            n[k] = v
        return n

    def __getitem__(self, index: int):
        return self._elements[index]

    def __getattr__(self, name: str):
        try:
            return object.__getattr__(self, name)
        except Exception:
            if name in self._data:
                return self._data[name]
        raise AttributeError(f"{name} not found")

    def append(self, element):
        if self._checkElement(element):
            self._elements.append(element)
            return

        raise TypeError(f"{element} is not a valid element")

    def iterchild(self):
        return self._elements.__iter__()

    def itervars(self):
        return self._data.items()

    def push(self, element):
        self.append(element)

    def remove(self, element):
        self._elements.remove(element)
    
    def clearchild(self):
        self._elements.clear()
    
    def insert(self, index, element):
        self._elements.insert(index, element)

    def pop(self, index):
        return self._elements.pop(index)

    def __lshift__(self, other):
        if other.__class__ is not _BaseElement._rootnode:
            self.append(other)
            return
        raise Exception("Cannot left shifting root object")

    def __rshift__(self, other):
        method = ShiftedObject._getmeth(other)
        if self.__class__ is not _BaseElement._rootnode:
            return method(self)
        raise Exception("Cannot right shifting root object")

    def __str__(self):
        # "name required"
        return _element_openings.format(name=self._name, values=f"{' ' if len(self._nullify()) != 0 else ''}{self._parseNames()}") if self._autoclose is not True else _element_autoclose.format(name=self._name, values=f"{' ' if self._data else ''}{self._parseNames()}")

    def compile(self, level=1) -> str:
        if self._autoclose is True:
            return str(self)
        x = level if self._decrease_level is False else level-1
        indent = config.COMPILE_NEWLINE_INDENT if x == 1 else config.COMPILE_NEWLINE_INDENT * \
            (x)
        a = '\n'+indent if self._newlineoncompile is True else ""
        _a = '\n' if self._newlineoncompile is True else ""
        indent_b = config.COMPILE_NEWLINE_INDENT*(x-1)
        _b = '\n'+indent_b if self._newlineoncompile is True else ''
        n = str(self)
        if self._header is not None:
            n = self._header+'\n'+n
        if self._require_close is True and self._nochild is True:
            return n
        if len(self._elements) == 0:
            return n+(_element_closing.format(name=self._name) if self._require_close is True else "")
        for val in self._elements:
            if len(self._elements) == 1 and self._optimize_child is True:
                a = ''
                _a = ''
                _b = ""
            if isinstance(val, str):
                n += val
                continue
            if not hasattr(val, "compile") and not hasattr(val, "_parseNames"):
                n += str(val)
                continue
            if hasattr(val, '_decrease_level'):
                val._decrease_level = True if type(self) in (
                    _BaseElement, _BaseElement._rootnode) else False
            n += (a if (type(self) in (_BaseElement, _BaseElement._rootnode))
                  is not True else _a)+(val.compile(x+1) if hasattr(val, 'compile') else str(val))
        return n+(_a if x == 1 else _b)+(_element_closing.format(name=self._name) if self._require_close is True else "")

    def __repr__(self):
        n = str(self)
        if self._autoclose is True:
            return n
        if len(self._elements) > 0:
            n += '...'
        return n+(_element_closing.format(name=self._name) if self._require_close is True else "")


class _debugelementa(_BaseElement, name='debuga', autoclose=True):
    pass


class _debugelementb(_BaseElement, name='debugb'):
    pass


class _debugelementc(_BaseElement, name='debugc', canonical_names=['href', 'onclick']):
    pass


class _p_like_element(_BaseElement, name='debugd', newlineoncompile=False):
    pass


class HTML(_BaseElement, name="html", isroot=True, header="<!DOCTYPE html>"):
    pass
