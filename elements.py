"""HTML Elements

No need to tell; this consist (atleast) all HTML elements.
To make your own element, do atleast these:

class <name>(HTML, name='<name>', **<your options here>):
    '''Your documentation'''
"""

from pickletools import optimize


try:
    from ._core import _HTML
except (ImportError, ModuleNotFoundError):
    from _core import HTML


class head(HTML, name='head', decrease_level=True):
    pass


class body(HTML, name='body', decrease_level=True):
    pass


class a(HTML, name='a', canonical_names=['href']):
    pass


class meta(HTML, name='meta', canonical_names=['charset', 'name', 'content'], require_close=False, nochild=True):
    pass


class title(HTML, name='title'):
    """Title of your page."""


class style(HTML, name='style'):
    pass


class link(HTML, name='link', canonical_names=['href', 'rel'], require_close=False, nochild=True):
    pass


class script(HTML, name="script", canonical_names=['type', 'src']):
    pass


class img(HTML, name="img", canonical_names=['href', 'alt', 'src']):
    pass


class p(HTML, name="p", newlineoncompile=False):
    pass


class abbr(HTML, name="abbr", newlineoncompile=False):
    pass

class address(HTML, name="address"):
    pass

class area(HTML, name='area', require_close=False):
    pass

class map(HTML, name="map"):
    pass

class pre(HTML, name="pre"):
    pass


class span(HTML, name="span", newlineoncompile=False):
    pass


class div(HTML, name='div'):
    pass


class button(HTML, name="button", newlineoncompile=False):
    pass

class input(HTML, name="input"):
    pass

class form(HTML, name='form', canonical_names=['action', 'href']):
    pass

class br(HTML, name="br", require_close=False):
    pass

class hr(HTML, name="hr", require_close=False):
    pass

class blockquote(HTML, name='blockquote'):
    pass

class canvas(HTML, name='canvas', newlineoncompile=False):
    pass

class caption(HTML, name='caption', newlineoncompile=False):
    pass

class ul(HTML, name='ul'):
    pass

class li(HTML, name='li', optimize_child=True):
    pass