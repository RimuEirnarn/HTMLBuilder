from _core import _debugelementb, _debugelementa, _debugelementc, HTML, _p_like_element

"""
root = HTML()
root << _debugelementc(href='http://localhost')
root << _debugelementa(onclick='show()')
nested = _debugelementb(class_="div-like-class")
nested << _debugelementa()
nested1 = _debugelementc()
nested1 << _debugelementa()
nested2 = _p_like_element()
nested2 << "Hello, World!"
nested2 << _debugelementc()
nested2 << _debugelementa()
nested << nested1
nested << nested2
root << nested

print(root.compile())
"""
from elements import body, head, meta, div, p, span

root0 = HTML()
head0 = head()
body0 = body()
head0 << meta(charset="UTF-8")
head0 << meta(name="author", content="Archaent Nakasaki")
body_div0 = div(class_="container")
body_div0 << p("Hello, World!")
body_div0 << span("Here's Johnny!", style="display: none")
body0 << body_div0
root0 << head0
root0 << body0

print(root0.compile(), end='\n===\n')
print(body_div0.compile())