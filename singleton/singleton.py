"""
 # nk-rt (remote)
 # └── singleton-py/
 #   └── singleton/
 #     └── singleton.py
 #
 # pep 695 type-parameterized singleton decorator and descriptor 
 # implementation.
 #
 # (c) 2026. skyline rt, llc. zero rights reserved :')
"""

import sys
from typing import Any, Callable, Hashable


"""
  global::singleton() -> type[cls_T]:
    patches the class it decorates so the first instantiation wins: every later call returns
      ... that same cached instance and __init__ never runs again, so re-"constructing" a
      ... singleton cannot reset its state. its one argument is the class being decorated.
    returns type[cls_T]: the class itself, patched in place rather than wrapped, so isinstance
      ... checks, classmethods and annotations all behave as though it were undecorated.
"""
def singleton[cls_T](cls: type[cls_T]) -> type[cls_T]:
    original_new = cls.__new__
    original_init = cls.__init__
    instance: cls_T | None = None
    initialized = False

    def __new__(cls: type[cls_T], *args: Any, **kwargs: Any) -> cls_T:
        nonlocal instance
        if instance is None:
            if original_new is object.__new__:
                instance = original_new(cls)
            else:
                instance = original_new(cls, *args, **kwargs)
        return instance

    def __init__(self: cls_T, *args: Any, **kwargs: Any) -> None:
        nonlocal initialized
        if not initialized:
            original_init(self, *args, **kwargs)
            initialized = True

    cls.__new__ = staticmethod(__new__)
    cls.__init__ = __init__
    return cls


"""
  _MODULE/str: this module's own dotted name, used to skip the decorator's own frames when
    ... walking the stack out to whoever declared the instance.
"""
_MODULE = __name__


"""
  global::call_site() -> tuple[str, int]:
    the source location of the declaration being made, walking out past this module and past
      ... any constructor chain so a subclass of any depth still names the caller's own line.
    returns tuple[str, int]: the caller's filename and line number.
"""
def call_site() -> tuple[str, int]:
    depth = 1
    while True:
        frame = sys._getframe(depth)
        code = frame.f_code
        here = frame.f_globals.get("__name__") == _MODULE
        if not here and code.co_name != "__init__":
            return (code.co_filename, frame.f_lineno)
        depth += 1


"""
  global::singletons(key) -> Callable[[type[cls_T]], type[cls_T]]:
    patches the class it decorates so one instance exists per DECLARATION rather than per
      ... application: the same statement reached again returns what it returned before, and
      ... a different statement gets its own. its argument is the key to cache against.
      key/Callable[[], Hashable] | None: names the declaration, defaulting to the caller's own
        ... source location; a caller with a rule of its own supplies it, and may refuse. None.
    returns Callable[[type[cls_T]], type[cls_T]]: the decorator, patching in place so that
      ... isinstance checks, classmethods and annotations behave as though it were absent.
"""
def singletons[cls_T](
    key: Callable[[], Hashable] | None = None
) -> Callable[[type[cls_T]], type[cls_T]]:
    site = key if key is not None else call_site

    def decorate(cls: type[cls_T]) -> type[cls_T]:
        original_new = cls.__new__
        original_init = cls.__init__
        instances: dict[Hashable, cls_T] = {}
        cls.__sk_instances__ = instances

        def __new__(cls: type[cls_T], *args: Any, **kwargs: Any) -> cls_T:
            where = site()
            instance = instances.get(where)
            if instance is None:
                if original_new is object.__new__:
                    instance = original_new(cls)
                else:
                    instance = original_new(cls, *args, **kwargs)
                instances[where] = instance
                instance.__sk_declared__ = False
            return instance

        def __init__(self: cls_T, *args: Any, **kwargs: Any) -> None:
            if not self.__sk_declared__:
                original_init(self, *args, **kwargs)
                self.__sk_declared__ = True

        cls.__new__ = staticmethod(__new__)
        cls.__init__ = __init__
        return cls

    return decorate
