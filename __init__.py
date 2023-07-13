"""Module declaration for uisp_mikrotik_address_list_sync."""
from configparser import ConfigParser


class UISPMikroTikSyncConfig:
    """configuration for uisp-mikrotik-sync module"""

    try:
        parser = ConfigParser()
        parser.read("uisp.ini")

        uisp_config = parser["UISP"]
        mikrotik_config = parser["MIKROTIK"]

        uisp_api_token = uisp_config["token"]
        uisp_fqdn = uisp_config["server_fqdn"]
        ssl_verify = mikrotik_config["ssl_verify"]
        mt_ip = mikrotik_config["router_ip"]
        mt_username = mikrotik_config["username"]
        mt_password = mikrotik_config["password"]
    except Exception as err:
        raise Exception(
            f"Error loading config from uisp.ini, ensure this file exists and has the proper variables. {err}"
        )
