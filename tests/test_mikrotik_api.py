"""Tests for MikroTik API functionality."""
import pytest
import sys
import os
from unittest.mock import patch, Mock
import base64

# Add the parent directory to the path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.mikrotik import MikroTikApi


class TestMikroTikApi:
    """Test MikroTikApi class."""

    def test_mikrotik_api_init_with_ssl(self):
        """Test MikroTikApi initialization with SSL enabled."""
        api = MikroTikApi(
            base_url="192.168.1.1",
            username="admin",
            password="password",
            use_ssl=True
        )
        
        assert api.base_url == "https://192.168.1.1/rest/"
        assert api.username == "admin"
        assert api.password == "password"
        expected_auth = base64.b64encode(b"admin:password").decode("utf-8")
        assert api.headers["Authorization"] == f"Basic {expected_auth}"
        assert api.headers["Accept"] == "*/*"

    def test_mikrotik_api_init_without_ssl(self):
        """Test MikroTikApi initialization with SSL disabled."""
        api = MikroTikApi(
            base_url="192.168.1.1",
            username="admin",
            password="password",
            use_ssl=False
        )
        
        assert api.base_url == "http://192.168.1.1/rest/"

    def test_mikrotik_api_get_address_list_all(self, mock_mikrotik_address_lists, mock_api_response):
        """Test get_address_list without specific list name."""
        mock_api_response.json.return_value = mock_mikrotik_address_lists
        
        with patch('utils.base.requests.request', return_value=mock_api_response):
            api = MikroTikApi(
                base_url="192.168.1.1",
                username="admin",
                password="password"
            )
            
            result = api.get_address_list()
            
            assert result == mock_mikrotik_address_lists

    def test_mikrotik_api_get_address_list_specific(self, mock_mikrotik_address_lists, mock_api_response):
        """Test get_address_list with specific list name."""
        # Filter for active list only
        active_addresses = [addr for addr in mock_mikrotik_address_lists if addr["list"] == "clients_active"]
        mock_api_response.json.return_value = active_addresses
        
        with patch('utils.base.requests.request', return_value=mock_api_response):
            api = MikroTikApi(
                base_url="192.168.1.1",
                username="admin",
                password="password"
            )
            
            result = api.get_address_list(list_name="clients_active")
            
            assert result == active_addresses

    def test_mikrotik_api_get_address_list_item_id(self, mock_api_response):
        """Test get_address_list_item_id."""
        mock_item = [{"id": "1", "address": "192.168.1.10"}]
        mock_api_response.json.return_value = mock_item
        
        with patch('utils.base.requests.request', return_value=mock_api_response):
            api = MikroTikApi(
                base_url="192.168.1.1",
                username="admin",
                password="password"
            )
            
            result = api.get_address_list_item_id("clients_active", "192.168.1.10")
            
            assert result == mock_item

    def test_mikrotik_api_add_address_to_list(self, mock_api_response):
        """Test add_address_to_list."""
        mock_api_response.status_code = 200
        
        with patch('utils.base.requests.request', return_value=mock_api_response):
            api = MikroTikApi(
                base_url="192.168.1.1",
                username="admin",
                password="password"
            )
            
            # Should not raise an exception
            api.add_address_to_list("192.168.1.10", "clients_active", "Test Comment")

    def test_mikrotik_api_remove_address_from_list(self, mock_api_response_204):
        """Test remove_address_from_list."""
        with patch('utils.base.requests.request', return_value=mock_api_response_204):
            api = MikroTikApi(
                base_url="192.168.1.1",
                username="admin",
                password="password"
            )
            
            # Should not raise an exception
            api.remove_address_from_list("1")

    def test_mikrotik_api_get_address_list_error(self, mock_api_error_response):
        """Test get_address_list with API error."""
        with patch('utils.base.requests.request', return_value=mock_api_error_response):
            api = MikroTikApi(
                base_url="192.168.1.1",
                username="admin",
                password="password"
            )
            
            with pytest.raises(Exception, match="Error communicating to the API"):
                api.get_address_list()

    def test_mikrotik_api_authentication_header(self):
        """Test that authentication header is properly encoded."""
        api = MikroTikApi(
            base_url="192.168.1.1",
            username="admin",
            password="password123"
        )
        
        # Test that the auth header is properly base64 encoded
        expected_credentials = "admin:password123"
        expected_auth = base64.b64encode(expected_credentials.encode("utf-8")).decode("utf-8")
        assert api.headers["Authorization"] == f"Basic {expected_auth}"

    def test_mikrotik_api_url_validation(self):
        """Test URL validation in MikroTikApi."""
        api = MikroTikApi(
            base_url="192.168.1.1",
            username="admin",
            password="password"
        )
        
        # Test with trailing slash in base_url
        api.base_url = "https://192.168.1.1/rest/"
        result = api.validate_url("ip/firewall/address-list")
        assert result == "https://192.168.1.1/rest/ip/firewall/address-list"
        
        # Test without trailing slash in base_url
        api.base_url = "https://192.168.1.1/rest"
        result = api.validate_url("ip/firewall/address-list")
        assert result == "https://192.168.1.1/rest/ip/firewall/address-list"

    def test_mikrotik_api_ssl_verify_disabled(self):
        """Test that SSL verification can be disabled."""
        api = MikroTikApi(
            base_url="192.168.1.1",
            username="admin",
            password="password",
            ssl_verify=False
        )
        
        assert api.verify is False

    def test_bulk_add_addresses_to_list(self, mock_api_response):
        """Test bulk_add_addresses_to_list method."""
        mock_api_response.status_code = 200
        
        with patch('requests.Session') as mock_session_class:
            mock_session = Mock()
            mock_session.put.return_value = mock_api_response
            mock_session_class.return_value = mock_session
            
            api = MikroTikApi(
                base_url="192.168.1.1",
                username="admin",
                password="password"
            )
            
            addresses_data = [
                {
                    "ip_address": "192.168.1.10",
                    "list_name": "clients_active",
                    "comment": "John Doe"
                },
                {
                    "ip_address": "192.168.1.20",
                    "list_name": "clients_active",
                    "comment": "Jane Smith"
                }
            ]
            
            # Should not raise an exception
            api.bulk_add_addresses_to_list(addresses_data)

    def test_bulk_add_addresses_to_list_empty(self):
        """Test bulk_add_addresses_to_list with empty data."""
        api = MikroTikApi(
            base_url="192.168.1.1",
            username="admin",
            password="password"
        )
        
        # Should handle empty list gracefully
        api.bulk_add_addresses_to_list([])

    def test_bulk_remove_addresses_from_list(self, mock_api_response):
        """Test bulk_remove_addresses_from_list method."""
        mock_api_response.status_code = 200
        
        with patch('requests.Session') as mock_session_class:
            mock_session = Mock()
            mock_session.delete.return_value = mock_api_response
            mock_session_class.return_value = mock_session
            
            api = MikroTikApi(
                base_url="192.168.1.1",
                username="admin",
                password="password"
            )
            
            addresses_data = [
                {
                    "entry_id": "1",
                    "ip_address": "192.168.1.10",
                    "list_name": "clients_active"
                },
                {
                    "entry_id": "2",
                    "ip_address": "192.168.1.20",
                    "list_name": "clients_active"
                }
            ]
            
            # Should not raise an exception
            api.bulk_remove_addresses_from_list(addresses_data)

    def test_bulk_remove_addresses_from_list_empty(self):
        """Test bulk_remove_addresses_from_list with empty data."""
        api = MikroTikApi(
            base_url="192.168.1.1",
            username="admin",
            password="password"
        )
        
        # Should handle empty list gracefully
        api.bulk_remove_addresses_from_list([])

    def test_bulk_sync_address_list(self, mock_api_response):
        """Test bulk_sync_address_list method."""
        mock_api_response.status_code = 200
        
        with patch('requests.Session') as mock_session_class:
            mock_session = Mock()
            mock_session.put.return_value = mock_api_response
            mock_session.delete.return_value = mock_api_response
            mock_session_class.return_value = mock_session
            
            api = MikroTikApi(
                base_url="192.168.1.1",
                username="admin",
                password="password"
            )
            
            addresses_to_add = [
                {
                    "ip_address": "192.168.1.10",
                    "list_name": "clients_active",
                    "comment": "John Doe"
                }
            ]
            
            addresses_to_remove = [
                {
                    "entry_id": "1",
                    "ip_address": "192.168.1.20",
                    "list_name": "clients_active"
                }
            ]
            
            # Should not raise an exception
            api.bulk_sync_address_list(
                list_name="clients_active",
                addresses_to_add=addresses_to_add,
                addresses_to_remove=addresses_to_remove
            )

    def test_bulk_sync_address_list_empty(self):
        """Test bulk_sync_address_list with empty data."""
        api = MikroTikApi(
            base_url="192.168.1.1",
            username="admin",
            password="password"
        )
        
        # Should handle empty lists gracefully
        api.bulk_sync_address_list(
            list_name="clients_active",
            addresses_to_add=[],
            addresses_to_remove=[]
        )

    def test_get_address_list_bulk_all(self, mock_mikrotik_address_lists, mock_api_response):
        """Test get_address_list_bulk method for all lists."""
        mock_api_response.json.return_value = mock_mikrotik_address_lists
        
        with patch('utils.base.requests.request', return_value=mock_api_response):
            api = MikroTikApi(
                base_url="192.168.1.1",
                username="admin",
                password="password"
            )
            
            result = api.get_address_list_bulk()
            
            # Should return a dictionary with list names as keys
            assert isinstance(result, dict)
            assert "clients_active" in result
            assert "clients_suspended" in result
            assert "clients_all" in result

    def test_get_address_list_bulk_specific(self, mock_mikrotik_address_lists, mock_api_response):
        """Test get_address_list_bulk method for specific lists."""
        # Filter for active list only
        active_addresses = [addr for addr in mock_mikrotik_address_lists if addr["list"] == "clients_active"]
        mock_api_response.json.return_value = active_addresses
        
        with patch('utils.base.requests.request', return_value=mock_api_response):
            api = MikroTikApi(
                base_url="192.168.1.1",
                username="admin",
                password="password"
            )
            
            result = api.get_address_list_bulk(list_names=["clients_active"])
            
            # Should return a dictionary with only the requested list
            assert isinstance(result, dict)
            assert "clients_active" in result
            assert len(result) == 1

    def test_get_entry_ids_bulk(self, mock_mikrotik_address_lists, mock_api_response):
        """Test get_entry_ids_bulk method."""
        mock_api_response.json.return_value = mock_mikrotik_address_lists
        
        with patch('utils.base.requests.request', return_value=mock_api_response):
            api = MikroTikApi(
                base_url="192.168.1.1",
                username="admin",
                password="password"
            )
            
            addresses_to_remove = [
                {
                    "ip_address": "192.168.1.10",
                    "list_name": "clients_active"
                },
                {
                    "ip_address": "192.168.1.30",
                    "list_name": "clients_suspended"
                }
            ]
            
            result = api.get_entry_ids_bulk(addresses_to_remove)
            
            # Should return list with entry IDs added
            assert len(result) == 2
            assert all('entry_id' in addr for addr in result)
            assert result[0]['entry_id'] == '1'  # From mock data
            assert result[1]['entry_id'] == '3'  # From mock data

    def test_get_entry_ids_bulk_empty(self):
        """Test get_entry_ids_bulk with empty data."""
        api = MikroTikApi(
            base_url="192.168.1.1",
            username="admin",
            password="password"
        )
        
        result = api.get_entry_ids_bulk([])
        assert result == []

    def test_get_entry_ids_bulk_not_found(self, mock_mikrotik_address_lists, mock_api_response):
        """Test get_entry_ids_bulk with addresses not found."""
        mock_api_response.json.return_value = mock_mikrotik_address_lists
        
        with patch('utils.base.requests.request', return_value=mock_api_response):
            api = MikroTikApi(
                base_url="192.168.1.1",
                username="admin",
                password="password"
            )
            
            addresses_to_remove = [
                {
                    "ip_address": "192.168.1.999",  # Not in mock data
                    "list_name": "clients_active"
                }
            ]
            
            result = api.get_entry_ids_bulk(addresses_to_remove)
            
            # Should return empty list for not found addresses
            assert len(result) == 0
