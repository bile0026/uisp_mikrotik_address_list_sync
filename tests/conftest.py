"""Pytest configuration and common fixtures."""
import pytest
import sys
import os
import requests
from unittest.mock import Mock

# Add the parent directory to the path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def mock_uisp_clients():
    """Mock UISP clients data."""
    return [
        {
            "id": 1,
            "firstName": "John",
            "lastName": "Doe",
            "status": 1
        },
        {
            "id": 2,
            "firstName": "Jane",
            "lastName": "Smith",
            "status": 1
        },
        {
            "id": 3,
            "firstName": "Bob",
            "lastName": "Johnson",
            "status": 2
        }
    ]


@pytest.fixture
def mock_uisp_services():
    """Mock UISP services data."""
    return [
        {
            "id": 101,
            "clientId": 1,
            "status": 1,
            "unmsClientSiteId": "site-1"
        },
        {
            "id": 102,
            "clientId": 2,
            "status": 1,
            "unmsClientSiteId": "site-2"
        },
        {
            "id": 103,
            "clientId": 3,
            "status": 2,
            "unmsClientSiteId": "site-3"
        }
    ]


@pytest.fixture
def mock_uisp_devices():
    """Mock UISP devices data."""
    return [
        {
            "id": "device-1",
            "identification": {
                "name": "Device-1",
                "site": {"id": "site-1"}
            },
            "ipAddress": "192.168.1.10/24"
        },
        {
            "id": "device-2",
            "identification": {
                "name": "Device-2",
                "site": {"id": "site-2"}
            },
            "ipAddress": "192.168.1.20/24"
        },
        {
            "id": "device-3",
            "identification": {
                "name": "Device-3",
                "site": {"id": "site-3"}
            },
            "ipAddress": "192.168.1.30/24"
        },
        {
            "id": "device-4",
            "identification": {
                "name": "Device-No-Site",
                "site": None
            },
            "ipAddress": "192.168.1.40/24"
        }
    ]


@pytest.fixture
def mock_mikrotik_address_lists():
    """Mock MikroTik address lists data."""
    return [
        {
            ".id": "1",
            "list": "clients_active",
            "address": "192.168.1.10",
            "comment": "John Doe"
        },
        {
            ".id": "2",
            "list": "clients_active",
            "address": "192.168.1.20",
            "comment": "Jane Smith"
        },
        {
            ".id": "3",
            "list": "clients_suspended",
            "address": "192.168.1.30",
            "comment": "Bob Johnson"
        },
        {
            ".id": "4",
            "list": "clients_all",
            "address": "192.168.1.10",
            "comment": "John Doe"
        },
        {
            ".id": "5",
            "list": "clients_all",
            "address": "192.168.1.20",
            "comment": "Jane Smith"
        },
        {
            ".id": "6",
            "list": "clients_all",
            "address": "192.168.1.30",
            "comment": "Bob Johnson"
        }
    ]


@pytest.fixture
def mock_config():
    """Mock configuration data."""
    return {
        "uisp_fqdn": "test.uisp.com",
        "uisp_nms_token": "test-nms-token",
        "uisp_crm_token": "test-crm-token",
        "uisp_use_ssl": True,
        "mt_ip": "192.168.1.1",
        "mt_username": "admin",
        "mt_password": "password",
        "mt_use_ssl": False,
        "ssl_verify": False
    }


@pytest.fixture
def mock_api_response():
    """Mock API response."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {"data": "test"}
    response.text = '{"data": "test"}'
    response.raise_for_status.return_value = None
    return response


@pytest.fixture
def mock_api_response_204():
    """Mock API response with 204 status."""
    response = Mock()
    response.status_code = 204
    response.text = ""
    response.raise_for_status.return_value = None
    return response


@pytest.fixture
def mock_api_error_response():
    """Mock API error response."""
    response = Mock()
    response.status_code = 401
    response.text = "Unauthorized"
    response.raise_for_status.side_effect = requests.exceptions.HTTPError("401 Client Error: Unauthorized")
    return response
