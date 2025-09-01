"""Tests for utility functions."""
import pytest
import sys
import os
import random
from unittest.mock import patch

# Add the parent directory to the path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import (
    lookup_client_ip,
    lookup_service_id,
    lookup_service_status,
    get_objects_by_key_value,
    find_missing_items,
    str_to_bool,
    is_truthy
)
from classes.uisp import UISPClientAddress
from classes.mikrotik import MikroTikClientAddress


class TestLookupFunctions:
    """Test lookup utility functions."""

    def test_lookup_service_id_found(self, mock_uisp_services):
        """Test lookup_service_id when service is found."""
        result = lookup_service_id(mock_uisp_services, 1)
        assert result == 101

    def test_lookup_service_id_not_found(self, mock_uisp_services):
        """Test lookup_service_id when service is not found."""
        result = lookup_service_id(mock_uisp_services, 999)
        assert result is None

    def test_lookup_service_status_found(self, mock_uisp_services):
        """Test lookup_service_status when service is found."""
        result = lookup_service_status(mock_uisp_services, 1)
        assert result == 1

    def test_lookup_service_status_not_found(self, mock_uisp_services):
        """Test lookup_service_status when service is not found."""
        result = lookup_service_status(mock_uisp_services, 999)
        assert result is None

    def test_lookup_client_ip_found(self, mock_uisp_devices, mock_uisp_services):
        """Test lookup_client_ip when IP is found."""
        with patch('utils.random.randint', return_value=100):
            result = lookup_client_ip(mock_uisp_devices, mock_uisp_services, 1)
            assert result == "192.168.1.10"

    def test_lookup_client_ip_not_found(self, mock_uisp_devices, mock_uisp_services):
        """Test lookup_client_ip when IP is not found."""
        with patch('utils.random.randint', return_value=100):
            result = lookup_client_ip(mock_uisp_devices, mock_uisp_services, 999)
            assert result is None

    def test_lookup_client_ip_device_no_site(self, mock_uisp_devices, mock_uisp_services):
        """Test lookup_client_ip with device that has no site assignment."""
        # Add a service for a device with no site
        services_with_no_site = mock_uisp_services + [{
            "id": 104,
            "clientId": 4,
            "status": 1,
            "unmsClientSiteId": "site-4"
        }]
        
        with patch('utils.random.randint', return_value=100):
            result = lookup_client_ip(mock_uisp_devices, services_with_no_site, 4)
            # When no matching device is found, the function returns None
            assert result is None

    def test_lookup_client_ip_device_no_ip(self, mock_uisp_devices, mock_uisp_services):
        """Test lookup_client_ip with device that has no IP address."""
        # Create a device without IP address
        devices_no_ip = mock_uisp_devices.copy()
        devices_no_ip[0]["ipAddress"] = None
        
        with patch('utils.random.randint', return_value=100):
            result = lookup_client_ip(devices_no_ip, mock_uisp_services, 1)
            assert result == "192.0.0.100"


class TestObjectFunctions:
    """Test object manipulation utility functions."""

    def test_get_objects_by_key_value_found(self):
        """Test get_objects_by_key_value when objects are found."""
        objects = [
            UISPClientAddress("192.168.1.10", "John Doe", 1, 101, "active"),
            UISPClientAddress("192.168.1.20", "Jane Smith", 2, 102, "active"),
            UISPClientAddress("192.168.1.30", "Bob Johnson", 3, 103, "suspended")
        ]
        
        result = get_objects_by_key_value(objects, "service_status", "active")
        assert len(result) == 2
        assert all(obj.service_status == "active" for obj in result)

    def test_get_objects_by_key_value_not_found(self):
        """Test get_objects_by_key_value when no objects are found."""
        objects = [
            UISPClientAddress("192.168.1.10", "John Doe", 1, 101, "active"),
            UISPClientAddress("192.168.1.20", "Jane Smith", 2, 102, "active")
        ]
        
        result = get_objects_by_key_value(objects, "service_status", "suspended")
        assert len(result) == 0

    def test_find_missing_items(self):
        """Test find_missing_items function."""
        objects1 = [
            UISPClientAddress("192.168.1.10", "John Doe", 1, 101, "active"),
            UISPClientAddress("192.168.1.20", "Jane Smith", 2, 102, "active"),
            UISPClientAddress("192.168.1.30", "Bob Johnson", 3, 103, "suspended")
        ]
        
        objects2 = [
            MikroTikClientAddress("192.168.1.10", "clients_active", "John Doe", "active", "1"),
            MikroTikClientAddress("192.168.1.20", "clients_active", "Jane Smith", "active", "2")
        ]
        
        missing = find_missing_items(objects1, objects2)
        assert len(missing) == 1
        assert missing[0].ip_address == "192.168.1.30"

    def test_find_missing_items_none_ip(self):
        """Test find_missing_items with objects that have None IP addresses."""
        objects1 = [
            UISPClientAddress("192.168.1.10", "John Doe", 1, 101, "active"),
            UISPClientAddress(None, "Jane Smith", 2, 102, "active")
        ]
        
        objects2 = [
            MikroTikClientAddress("192.168.1.10", "clients_active", "John Doe", "active", "1")
        ]
        
        missing = find_missing_items(objects1, objects2)
        assert len(missing) == 0  # Objects with None IP should be ignored


class TestBooleanFunctions:
    """Test boolean conversion utility functions."""

    def test_str_to_bool_true_values(self):
        """Test str_to_bool with true values."""
        assert str_to_bool("true") is True
        assert str_to_bool("True") is True
        assert str_to_bool("yes") is True
        assert str_to_bool("Yes") is True
        assert str_to_bool("1") is True

    def test_str_to_bool_false_values(self):
        """Test str_to_bool with false values."""
        assert str_to_bool("false") is False
        assert str_to_bool("False") is False
        assert str_to_bool("no") is False
        assert str_to_bool("No") is False
        assert str_to_bool("0") is False
        assert str_to_bool("random") is False

    def test_is_truthy_true_values(self):
        """Test is_truthy with true values."""
        assert is_truthy("y") is True
        assert is_truthy("yes") is True
        assert is_truthy("t") is True
        assert is_truthy("true") is True
        assert is_truthy("on") is True
        assert is_truthy("1") is True
        assert is_truthy(True) is True

    def test_is_truthy_false_values(self):
        """Test is_truthy with false values."""
        assert is_truthy("n") is False
        assert is_truthy("no") is False
        assert is_truthy("f") is False
        assert is_truthy("false") is False
        assert is_truthy("off") is False
        assert is_truthy("0") is False
        assert is_truthy(False) is False

    def test_is_truthy_invalid_value(self):
        """Test is_truthy with invalid value."""
        with pytest.raises(ValueError):
            is_truthy("invalid")
