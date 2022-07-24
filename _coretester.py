from _core import HTML
from thetoolkit import Table, BulletList


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