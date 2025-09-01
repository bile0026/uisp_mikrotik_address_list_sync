"""Basic test to verify imports work correctly."""
import pytest
import sys
import os

# Add the parent directory to the path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_imports():
    """Test that all modules can be imported."""
    try:
        from utils import str_to_bool, is_truthy
        from utils.uisp import UISPApi, UCRMApi
        from utils.mikrotik import MikroTikApi
        from classes.uisp import UISPClientAddress
        from classes.mikrotik import MikroTikClientAddress
        assert True
    except ImportError as e:
        pytest.fail(f"Import failed: {e}")


def test_str_to_bool():
    """Test the str_to_bool function."""
    from utils import str_to_bool
    
    assert str_to_bool("true") is True
    assert str_to_bool("false") is False
    assert str_to_bool("yes") is True
    assert str_to_bool("no") is False
