"""
 # nk-rt (www.github.com/nk-rt)
 # └── singleton_decorator/
 #   └── run_tests.py
 #
 # uncomplicated behavioral regression test runner evaluating singleton 
 # state, arguments, and descriptor attributes.
 #
 # (c) 2026. skyline rt, llc. zero rights reserved :')
"""

import sys
import inspect
from singleton.singleton import singleton


@singleton
class MultiPurposeService:
    """
    Mock target class exposing an initialization routine, mutable 
    attributes, and a classmethod.
    """

    def __init__(self, host="localhost", port=5432):
        """
        Mock target initialization routine that accepts arguments 
        and binds mutable instance attributes.
        """
        self.connected = True
        self.host = host
        self.port = port
        
    @classmethod
    def get_version(cls):
        """
        Mock target classmethod that returns a string containing the 
        runtime evaluated wrapped class name. 
        """
        return f"v1.0 running on {cls.__name__}"

class App:
    """
    Mock target class that binds and exposes the singleton wrapper 
    as a class attribute.
    """
    settings = MultiPurposeService()


def test_instance_identity():
    """
    Tests repeated instantiation of the singleton wrapper. Raises an 
    AssertionError if the returned instances are not identical.
    """
    srv1 = MultiPurposeService()
    srv2 = MultiPurposeService()
    assert srv1 is srv2

def test_class_method():
    """
    Tests the ability of the singleton wrapper to expose and execute 
    a classmethod that evaluates the wrapped class name. Raises an
    AssertionError if the returned string and expected value differ.
    """
    res_expected = "v1.0 running on MultiPurposeService"
    assert MultiPurposeService.get_version() == res_expected

def test_argument_immutability():
    """
    Tests argument retention and immutability by re-instantiating the 
    singleton wrapper with new, explicitly defined, non-default values.
    Raises an AssertionError if the returned instance's attributes fail
    to reflect the original, implicitly defined, default values.
    """
    srv_args = MultiPurposeService("production", port=8080)
    assert srv_args.host == "localhost"
    assert srv_args.port == 5432

def test_attribute_identity():
    """
    Tests the exposure of and access to the singleton wrapper's global 
    instance and its attributes via a foreign class attribute. Raises 
    an AssertionError if the foreign class attribute points to a local 
    instance of the singleton wrapper rather than the global instance.
    """
    srv = MultiPurposeService()
    app = App()
    assert app.settings is srv
    assert app.settings.connected is True

def run_tests():
    """
    The primary test runner. Dispatches behavioral regression tests 
    in a clean, isolated, and secure context and outputs incremental 
    and final progress reports to STDOUT.  
    """
    local = lambda: (f := sys._getframe(1)).f_locals.get(f.f_code.co_name)
    signature = lambda f: f"{f.__qualname__}{inspect.signature(f)}"

    print(f"{signature(run_tests)} starting...")

    print(f"BEGIN: {signature(test_instance_identity)}")
    test_instance_identity()
    print(f"[OK] {signature(test_instance_identity)} passed.")

    print(f"BEGIN: {signature(test_class_method)}")
    test_class_method()
    print(f"[OK] {signature(test_class_method)} passed.")

    print(f"BEGIN: {signature(test_argument_immutability)}")
    test_argument_immutability()
    print(f"[OK] {signature(test_argument_immutability)} passed.")

    print(f"BEGIN: {signature(test_attribute_identity)}")
    test_attribute_identity()
    print(f"[OK] {signature(test_attribute_identity)} passed.")

    print(f"[OK] {signature(run_tests)} completed with all tests passing.")

if __name__ == "__main__":
    run_tests()
