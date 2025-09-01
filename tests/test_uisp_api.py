"""Tests for UISP API functionality."""
import pytest
import sys
import os
from unittest.mock import patch, Mock
import requests

# Add the parent directory to the path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.uisp import UISPApi, UCRMApi


class TestUISPApi:
    """Test UISPApi class."""

    def test_uisp_api_init_with_ssl(self):
        """Test UISPApi initialization with SSL enabled."""
        api = UISPApi(
            base_url="test.uisp.com",
            api_version="v2.1",
            token="test-token",
            use_ssl=True
        )
        
        assert api.base_url == "https://test.uisp.com/nms/api/v2.1/"
        assert api.headers["x-auth-token"] == "test-token"
        assert api.headers["Content-Type"] == "application/json"
        assert api.token == "test-token"

    def test_uisp_api_init_without_ssl(self):
        """Test UISPApi initialization with SSL disabled."""
        api = UISPApi(
            base_url="test.uisp.com",
            api_version="v2.1",
            token="test-token",
            use_ssl=False
        )
        
        assert api.base_url == "http://test.uisp.com/nms/api/v2.1/"

    def test_uisp_api_get_devices_success(self, mock_uisp_devices, mock_api_response):
        """Test successful get_devices call."""
        mock_api_response.json.return_value = mock_uisp_devices
        
        with patch('utils.base.requests.request', return_value=mock_api_response):
            api = UISPApi(
                base_url="test.uisp.com",
                api_version="v2.1",
                token="test-token"
            )
            
            result = api.get_devices()
            
            assert result == mock_uisp_devices

    def test_uisp_api_get_devices_error(self, mock_api_error_response):
        """Test get_devices call with API error."""
        with patch('utils.base.requests.request', return_value=mock_api_error_response):
            api = UISPApi(
                base_url="test.uisp.com",
                api_version="v2.1",
                token="test-token"
            )
            
            with pytest.raises(Exception, match="Error communicating to the API: 401 Client Error: Unauthorized"):
                api.get_devices()

    def test_uisp_api_get_sites_success(self, mock_api_response):
        """Test successful get_sites call."""
        mock_sites = [{"id": "site-1", "name": "Site 1"}]
        mock_api_response.json.return_value = mock_sites
        
        with patch('utils.base.requests.request', return_value=mock_api_response):
            api = UISPApi(
                base_url="test.uisp.com",
                api_version="v2.1",
                token="test-token"
            )
            
            result = api.get_sites()
            
            assert result == mock_sites

    def test_uisp_api_url_validation(self):
        """Test URL validation in UISPApi."""
        api = UISPApi(
            base_url="test.uisp.com",
            api_version="v2.1",
            token="test-token"
        )
        
        # Test with trailing slash in base_url
        api.base_url = "https://test.uisp.com/nms/api/v2.1/"
        result = api.validate_url("devices")
        assert result == "https://test.uisp.com/nms/api/v2.1/devices"
        
        # Test without trailing slash in base_url
        api.base_url = "https://test.uisp.com/nms/api/v2.1"
        result = api.validate_url("devices")
        assert result == "https://test.uisp.com/nms/api/v2.1/devices"


class TestUCRMApi:
    """Test UCRMApi class."""

    def test_ucrm_api_init_with_ssl(self):
        """Test UCRMApi initialization with SSL enabled."""
        api = UCRMApi(
            base_url="test.uisp.com",
            api_version="v2.1",
            token="test-token",
            use_ssl=True
        )
        
        assert api.base_url == "https://test.uisp.com/crm/api/v2.1/"
        assert api.headers["x-auth-app-key"] == "test-token"
        assert api.headers["Content-Type"] == "application/json"
        assert api.token == "test-token"

    def test_ucrm_api_init_without_ssl(self):
        """Test UCRMApi initialization with SSL disabled."""
        api = UCRMApi(
            base_url="test.uisp.com",
            api_version="v2.1",
            token="test-token",
            use_ssl=False
        )
        
        assert api.base_url == "http://test.uisp.com/crm/api/v2.1/"

    def test_ucrm_api_get_clients_success(self, mock_uisp_clients, mock_api_response):
        """Test successful get_clients call."""
        mock_api_response.json.return_value = mock_uisp_clients
        
        with patch('utils.base.requests.request', return_value=mock_api_response):
            api = UCRMApi(
                base_url="test.uisp.com",
                api_version="v2.1",
                token="test-token"
            )
            
            result = api.get_clients()
            
            assert result == mock_uisp_clients

    def test_ucrm_api_get_services_success(self, mock_uisp_services, mock_api_response):
        """Test successful get_services call."""
        mock_api_response.json.return_value = mock_uisp_services
        
        with patch('utils.base.requests.request', return_value=mock_api_response):
            api = UCRMApi(
                base_url="test.uisp.com",
                api_version="v2.1",
                token="test-token"
            )
            
            result = api.get_services()
            
            assert result == mock_uisp_services

    def test_ucrm_api_get_clients_error(self, mock_api_error_response):
        """Test get_clients call with API error."""
        with patch('utils.base.requests.request', return_value=mock_api_error_response):
            api = UCRMApi(
                base_url="test.uisp.com",
                api_version="v2.1",
                token="test-token"
            )
            
            with pytest.raises(Exception, match="Error communicating to the API: 401 Client Error: Unauthorized"):
                api.get_clients()

    def test_ucrm_api_url_validation(self):
        """Test URL validation in UCRMApi."""
        api = UCRMApi(
            base_url="test.uisp.com",
            api_version="v2.1",
            token="test-token"
        )
        
        # Test with trailing slash in base_url
        api.base_url = "https://test.uisp.com/crm/api/v2.1/"
        result = api.validate_url("clients")
        assert result == "https://test.uisp.com/crm/api/v2.1/clients"
        
        # Test without trailing slash in base_url
        api.base_url = "https://test.uisp.com/crm/api/v2.1"
        result = api.validate_url("clients")
        assert result == "https://test.uisp.com/crm/api/v2.1/clients"
