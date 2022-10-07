# -*- coding=UTF-8; tab-width: 4 -*-
# Heavily modified version of the code featured at the given link
## {{{ http://code.activestate.com/recipes/473786/ (r1)
class AttrDict(dict):
    """A dictionary with attribute-style access. It maps attribute access to
    the real dictionary.

    Note that accesses to preexisting (e.g. class inherited) or reserved
    attributes are handled as they would be normally, and will not be
    overwritten.
    Overload _is_reserved if you want to change this."""

    def __init__(self, init={}):
        super(AttrDict, self).__init__(init)

    def __getstate__(self):
        return list(self.__dict__.items())

    def __setstate__(self, items):
        for key, val in items:
            self.__dict__[key] = val

    def __repr__(self):
        return "{0}({1})".format(type(self).__name__, super(AttrDict, self).__repr__())

    def __setitem__(self, name, value):
        return super(AttrDict, self).__setitem__(name, value)

    def __getitem__(self, name):
        return super(AttrDict, self).__getitem__(name)

    def __delitem__(self, name):
        return super(AttrDict, self).__delitem__(name)

    def __getattr__(self, name):
        # NOTE: __getattr__ is called if the code has already failed to access
        # an attribute on this object. The rest of this code reflects this.
        # We could override __getattribute__ to bypass this, but that's not
        # worthwhile.

        # We don't do any special handling for reserved names.
        if self._is_reserved(name):
            # Fall back to normal handling, by force.
            return object.__getattribute__(self, name)

        try:
            # Try to __getitem__.
            result = self[name]
        except (KeyError, AttributeError):
            # Raising KeyError here will confuse __deepcopy__, so don't do
            # that.
            # Throw a custom error.
            raise AttributeError("No key/attr {0!r}".format(name))
        return result

    def __setattr__(self, name, value):
        # Set to the attribute first if it's defined.
        # (NOTE: This isn't subject to the same checking as __getattr__.)
        # Using dir() also checks non-instance definitions, so things defined
        # on a class can be easily set on an instance this way.

        # Detect special/reserved names.
        if name in dir(self) or self._is_reserved(name):
            # Set it if it's 'special' because we aren't supposed to touch any
            # of that - too many potential implementation issues.
            #
            # Apparently we're also not supposed to set our own dict directly
            # in this particular function?...
            return object.__setattr__(self, name, value)
        else:
            return super(AttrDict, self).__setitem__(name, value)

    def __delattr__(self, name):
        # We very *specifically* use self.__dict__ here, because we couldn't
        # possibly delete a value that doesn't yet *exist* in our instance's
        # namespace yet!
        # This shouldn't be a problem, since this type should never have
        # __slots__.
        if name in self.__dict__:
            # See __setattr__.
            return object.__delattr__(self, name)
        else:
            try:
                del self[name]
            except KeyError as err:
                raise AttributeError(str(err))

    @staticmethod
    def _is_reserved(name):
        """Check if an attribute name is reserved for system use."""
        # A very simple method.
        result = name[:2] == name[-2:] == "__"
        return result

    def copy(self):
        return type(self)(self)

    __copy__ = copy


## end of http://code.activestate.com/recipes/473786/ }}}


class DefAttrDict(AttrDict):
    default_factory = None

    def __init__(self, default_factory=None, *args, **kwargs):
        self.default_factory = default_factory
        super(DefAttrDict, self).__init__(*args, **kwargs)

    def __repr__(self):
        return "{0}({1!r}, {2})".format(
            type(self).__name__,
            self.default_factory,
            # We skip normal processing here, since AttrDict provides basic
            # repr for classes in general, which we don't want.
            dict.__repr__(self),
        )

    def __getitem__(self, name):
        try:
            result = super(DefAttrDict, self).__getitem__(name)
        except KeyError:
            result = None
            if self.default_factory is not None:
                result = self.default_factory()
            self[name] = result
        return result

    def __getattr__(self, name):
        try:
            result = super(DefAttrDict, self).__getattr__(name)
        except AttributeError:
            # Detect special/reserved names.
            if self._is_reserved(name):
                # We shouldn't automatically fill these in.
                # Pass this along.
                raise
        return result

    def copy(self):
        return type(self)(self.default_factory, self)

    __copy__ = copy


# vim: set autoindent ts=4 sts=4 sw=4 textwidth=79 expandtab:
