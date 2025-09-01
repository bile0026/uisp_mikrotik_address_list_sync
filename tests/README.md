# Test Suite for UISP MikroTik Address List Sync

This directory contains comprehensive tests for the UISP MikroTik Address List Sync application.

## Test Structure

### `conftest.py`
Contains pytest fixtures and mock data used across all tests:
- `mock_uisp_clients`: Mock UISP client data
- `mock_uisp_services`: Mock UISP service data  
- `mock_uisp_devices`: Mock UISP device data
- `mock_mikrotik_address_lists`: Mock MikroTik address list data
- `mock_config`: Mock configuration data
- `mock_api_response*`: Mock API response objects

### `test_uisp_api.py`
Tests for UISP API functionality:
- UISPApi class initialization and SSL configuration
- UCRMApi class initialization and SSL configuration
- API method calls (get_devices, get_clients, get_services)
- Error handling for API failures
- URL validation

### `test_mikrotik_api.py`
Tests for MikroTik API functionality:
- MikroTikApi class initialization and SSL configuration
- Address list operations (get, add, remove)
- Authentication header encoding
- Error handling for API failures
- URL validation

### `test_utils.py`
Tests for utility functions:
- Lookup functions (client IP, service ID, service status)
- Object manipulation functions
- Boolean conversion functions
- Edge cases and error conditions

### `test_classes.py`
Tests for data classes:
- UISPClientAddress class
- MikroTikClientAddress class
- Object comparison and set operations

### `test_integration.py`
Integration tests for the main sync functionality:
- Complete sync process with mocked APIs
- Error handling scenarios
- Sync logic validation

## Running Tests

### Using pytest directly:
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_uisp_api.py

# Run tests with coverage
pytest --cov=. --cov-report=html
```

### Using the test runner script:
```bash
# Run all tests
python run_tests.py

# Run unit tests only
python run_tests.py --type unit

# Run integration tests only
python run_tests.py --type integration

# Run with coverage
python run_tests.py --coverage

# Run with verbose output
python run_tests.py --verbose
```

### Using poetry:
```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=. --cov-report=html
```

## Test Categories

### Unit Tests
- Individual function and method testing
- Mocked dependencies
- Fast execution
- Marked with `@pytest.mark.unit`

### Integration Tests
- End-to-end functionality testing
- API interaction testing
- Slower execution
- Marked with `@pytest.mark.integration`

### Slow Tests
- Tests that take longer to execute
- May involve network calls or complex operations
- Marked with `@pytest.mark.slow`

## Mock Data

The test suite uses realistic mock data that simulates:
- UISP client information with various statuses
- UISP services with different configurations
- UISP devices with site assignments and IP addresses
- MikroTik address lists with different states
- API responses with various status codes

## Coverage

The test suite aims for high code coverage, testing:
- ✅ All API classes and methods
- ✅ All utility functions
- ✅ All data classes
- ✅ Error handling paths
- ✅ Edge cases and boundary conditions
- ✅ SSL configuration scenarios
- ✅ Authentication mechanisms

## Best Practices

1. **Mock External Dependencies**: All API calls are mocked to ensure tests are fast and reliable
2. **Realistic Test Data**: Mock data closely resembles real API responses
3. **Comprehensive Coverage**: Tests cover both success and failure scenarios
4. **Clear Test Names**: Test names clearly describe what is being tested
5. **Isolated Tests**: Each test is independent and doesn't rely on other tests
6. **Fast Execution**: Tests run quickly to encourage frequent execution

## Adding New Tests

When adding new functionality:

1. Add unit tests for individual functions/methods
2. Add integration tests for end-to-end functionality
3. Update mock data in `conftest.py` if needed
4. Ensure proper error handling is tested
5. Add appropriate test markers
6. Update this README if adding new test categories
