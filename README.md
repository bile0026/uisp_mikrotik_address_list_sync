# UISP to MikroTik Client Address List Sync Job

This job will take client IP addresses/Prefixes from UISP as assigned and sync them to MikroTik address lists for active and suspended services. These lists can then be used to do things like suspend services or block access based on service status.

This job utilizes the MikroTik RouterOS Rest API, so port 80/443 need to be allowed on the MikroTik from the source IP of the machine running this package. You will also need to enable `www` and `www-ssl` in `ip/services` in your MikroTik. It is strongly suggested to implement the `available from` field or `ip/firewall/filter` rules to restrict access. *DO NOT KEEP THIS OPEN TO THE INTERNET* You will also need to install a public certificate or generate a self-signed certificate for the REST API. See "MikroTik Configuration" section for more information.

It is simplest for permissions to do all this in your user directory, but keep in mind permissions and follow best practices for securing the .ini data since there will be sensitive credentials stored in it.

You can set this to run on a schedule with cron.

Always deploy from main branch, this should be considered stable. All other branches are not considered stable.

## Getting started

It is strongly advised to run this project in a python virtual environment to prevent conflicts. This project uses poetry to manage the dependencies and environment. 

## Run with Docker

Copy `uisp.ini.example` to `uisp.ini` and update the values as in the Job Configuration section. If you need to override any docker-compose values create a `docker-compose.override.yaml` and include the keys you want to override. Doing this will allow you to more easily pull changes from git without losing your customizations. 

Once your configuration is ready run `docker compose up -d --build` to start the project. The `interval` parameter in the .ini file will run the job each number of minutes specified.

## Run without Docker

If you don't want to run this without using poetry you can run `poetry export --output requirements.txt --without-hashes` to dump the python packages to a `requirements.txt` file, then create a virtual environment with `python -m venv .venv`. Run `source .venv/bin/activate` to activate the virtual environment. Then to install the dependencies run `pip install -r requirements.txt`.

After the virtual environment is created and dependencies installed. Take note of the path of the python executable in the virtual environment. You'll need this to setup the cron job.

* Before setting up to run as a cron job it would be best to run the job once with `python uisp_mikrotik_address_list_sync.py` (with the venv activated) to make sure you do not receive any errors.

## Debug

Run script with `--debug` to enable debug logging to troubleshoot sync issues. 

## Schedule Job to Run

To setup the job to run on a schedule run `crontab -e` to open the cron file. You can use a tool like [Cron Expression Generator](https://crontab.cronhub.io/) to help with the syntax. The entry should look something like the following (this will run the sync every 15 min):

```cron
*/15 * * * * /path/to/python/executable/in/venv uisp_mikrotik_address_list_sync.py
```

## Job Configuration

Copy the `uisp.ini.example` file to `uisp.ini`, and modify the values as necessary:

```config
[ADMIN]
send_health_check = False
healthcheck_io_id = 12345
interval = 15

[UISP]
server_fqdn = example.uisp.com
token = <uisp_token>
use_ssl = True

[MIKROTIK]
router_ip = 192.168.1.1
use_ssl = False
ssl_verify = False
disable_ssl_warning = False
username = admin
password = admin
```

## MikroTik Configuration

You will need to at least create a self-signed certificate for your router in order for the REST API to function. Adjust values per your environment.

```routeros
/certificate/add key-size=2048 trusted=yes organization=example-co days-valid=1000 name=ca-template common-name=routeros-test
/certificate/sign ca-template
/certificate add name=routeros-test common-name=hra-main-core subject-alt-name=IP:192.168.1.1 key-size=2048 days-valid=1000
/certificate/sign routeros-test ca=ca-template

/ip service
set www address="" disabled=no port=80 vrf=main
set www-ssl address="" certificate=routeros-test disabled=no port=443 tls-version=\
    any vrf=main
```

## Healthchecks

Can send healthchecks to [healthcheck.io](https://healthcheck.io) if you set the `send_health_check = True` and include the "guid" portion of the healthcheck in `health_check_id`.

## Notes

* Tested on python 3.8, 3.10
* Tested on RouterOS 7.6, 7.10.2

## To-Do

[X] Bulk API requests for MikroTik Create and Delete.

[] Validation of ip_address objects by making them `ip_address` objects from the `ipaddress` package.

[] Better error handling when a device doesn't have an IP address assigned in UISP.

[X] Add some kind of email/chat notification if script execution fails for some reason.

## Concurrent Operations

This project now supports concurrent operations for MikroTik address list management, significantly improving performance when syncing large numbers of addresses.

### Performance Benefits

- **Concurrent Execution**: Multiple API calls run in parallel using ThreadPoolExecutor
- **Improved Scalability**: Better performance with large address lists (100+ addresses)
- **Network Efficiency**: Minimized network overhead through connection reuse
- **Error Handling**: Individual error reporting for each address operation

### Performance Comparison

Run the performance comparison script to see the benefits:

```bash
python performance_comparison.py
```

Example results:
- Small datasets (10-100 addresses): Individual operations may be faster due to thread overhead
- Large datasets (500+ addresses): Concurrent operations show 68%+ performance improvement
- Real-world scenarios: Network latency makes concurrent operations even more beneficial

### Concurrent Operation Methods

The `MikroTikApi` class now includes these concurrent methods:

- `bulk_add_addresses_to_list(addresses_data)`: Add multiple addresses concurrently
- `bulk_remove_addresses_from_list(addresses_data)`: Remove multiple addresses concurrently
- `bulk_sync_address_list(list_name, addresses_to_add, addresses_to_remove)`: Complete sync operation
- `get_address_list_bulk(list_names=None)`: Get multiple address lists efficiently
- `get_entry_ids_bulk(addresses_to_remove)`: Get entry IDs for multiple addresses in one call

## Testing
Testing the app can be done with a few different commands. Passing tests are required before merging to main. 

```shell
# Run all tests
poetry run pytest tests/ -v --import-mode=importlib

# Run with coverage
poetry run pytest tests/ --cov=. --cov-report=term --import-mode=importlib

# Use the test runner
python run_tests.py --verbose

# Run specific test files
poetry run pytest tests/test_uisp_api.py -v --import-mode=importlib
```

## Contributions

Contributions welcome, just create a PR to develop or create an issue.
