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
from thetoolkit import Table, BulletList
"""
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
"""

root0 = HTML()
d = {
    "Name": ["Archaent", 'RimuEirnarn', "Shirou"],
    "UID": [1000, 0, 65283017499284],
    "Age": [8671, -1, 16]
}
k = {
    "key0": ["Value0", "Value1", "Value2"],
    "key1": ["Value3", "Value4"],
    "key2": ['Value5']
}
l = ["Python", "C", "C++"]
root0 << Table(d).body
root0 << BulletList(*l).body
root0 << Table(k).body
print(root0.compile())

with open("_coretester.html", 'w') as f:
    f.write(root0.compile())