# Modified version of the code featured at the given link
## {{{ http://code.activestate.com/recipes/473786/ (r1)
class AttrDict(dict):
    """A dictionary with attribute-style access. It maps attribute access to
    the real dictionary."""
    def __init__(self, init={}): super(AttrDict, self).__init__(init)
    def __getstate__(self): return self.__dict__.items()
    def __setstate__(self, items):
        for key, val in items: self.__dict__[key] = val
    def __repr__(self):
        return "{}({})".format(
            type(self).__name__,
            super(AttrDict, self).__repr__()
        )
    def __setitem__(self, key, value):
        return super(AttrDict, self).__setitem__(key, value)
    def __getitem__(self, name):
        return super(AttrDict, self).__getitem__(name)
    def __delitem__(self, name):
        return super(AttrDict, self).__delitem__(name)
    def __getattr__(self, name):
        # Basically, fall back on __getitem__ first
        # Try to access ourselves as a dict. Failing that, check for attributes
        # with the same name. Failing *that*, throw AttributeError to keep
        # other code happy.
        try: retval = self[name]
        except KeyError as err:
            try: retval = self.__dict__[name]
            except KeyError:
                # Raising KeyError here will confuse __deepcopy__, so don't do
                # that.
                raise AttributeError("No key/attr {!r}".format(name))
        return retval
    __setattr__ = __setitem__
    def __delattr__(self, name):
        try: del self[name]
        except KeyError as err:
            try: del self.__dict__[name]
            except KeyError:
                raise AttributeError(str(err))
    def copy(self): return type(self)(self)
    __copy__ = copy
## end of http://code.activestate.com/recipes/473786/ }}}

class DefAttrDict(AttrDict):
    def __init__(self, default_factory=None, *args, **kwargs):
        self.__dict__["default_factory"] = default_factory
        super(DefAttrDict, self).__init__(*args, **kwargs)
    def __repr__(self):
        return "%s(%r, %s)" % (
            type(self).__name__,
            self.default_factory,
            super(AttrDict, self).__repr__()
        )
    def __getitem__(self, name):
        try:
            return super(DefAttrDict, self).__getitem__(name)
        except KeyError:
            ##if self.default_factory is None: return None
            ##return self.default_factory()
            result = None
            if self.default_factory is not None:
                result = self.default_factory()
            self[name] = result
            return result
    __getattr__ = __getitem__
    def copy(self): return type(self)(self.default_factory, self)
