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

class BulletList(BaseToolkit):
    def __init__(self, *items, classList=None, **kwargs):
        item = [elements.li(item_) for item_ in items if item_]
        self.body = elements.ul(*item, **kwargs)
        if classList is not None and isinstance(classList, (tuple, list, set)):
            self.body.class_ = " ".join(classList)

# Create some class to 'auto' create some elements to create some fascinating stuff like table, etc.