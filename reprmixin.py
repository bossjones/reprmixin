#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Easy repr, namedtuple-like.

>>> class CustomDescriptor(object):
...     def __get__(self, obj, _):
...         return obj.a
...     def __set__(self, obj, value):
...         obj.a = value

>>> class Titi(ReprMixin):
...     __slots__ = ['a', 'b', 'c']
...     clsvars = 'test'
...     def __init__(self, a, b):
...         self.a = a
...         self.b = b
...     def method(self):
...         return self.a
...     @property
...     def prop(self):
...         return self.b
...     @prop.setter
...     def prop(self, b):
...         self.b = b
...     custom_desc = CustomDescriptor()
...     @classmethod
...     def clsmethod(cls):
...         pass
...     @staticmethod
...     def static():
...         pass

>>> l = Titi(a=1, b='2')
>>> l.a
1
>>> l.b
'2'
>>> l.method()
1
>>> l.prop
'2'
>>> l.prop = 'g'
>>> l.prop
'g'
>>> l.custom_desc
1
>>> l.custom_desc = 2
>>> l.clsmethod()
>>> Titi.static()
>>> repr(l)
"Titi(a=2, b='g')"
"""

def _iter_attributes(obj):
    """Iterate over all attributes on objects.
    """
    if hasattr(obj, '__dict__'):
        names = sorted(obj.__dict__)
    else:
        names = obj.__slots__

    for name in names:
        # No private stuff, feel free to comment or change this to "__"
        if name.startswith('_'):
            continue
        # If __slots__ had elements undefined at __init__, getattr will fail
        if not hasattr(obj, name):
            continue
        yield name, repr(getattr(obj, name))


class ReprMixin(object):
    __slots__ = []

    def __repr__(self):
        return '{0}({1})'.format(
            self.__class__.__name__,
            ', '.join('{0}={1}'.format(*t) for t in _iter_attributes(self)))

