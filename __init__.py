"""Module declaration for uisp_mikrotik_address_list_sync."""
from configparser import ConfigParser
import logging

logger = logging.getLogger(__name__)


class UISPMikroTikSyncConfig:
    """configuration for uisp-mikrotik-sync module"""

    try:
        parser = ConfigParser()
        parser.read("uisp.ini")

        uisp_config = parser["UISP"]
        mikrotik_config = parser["MIKROTIK"]

        uisp_api_token = uisp_config.get("token")
        uisp_fqdn = uisp_config.get("server_fqdn")
        ssl_verify = mikrotik_config["ssl_verify"]
        disable_ssl_warning = mikrotik_config["disable_ssl_warning"]
        mt_ip = mikrotik_config.get("router_ip")
        mt_username = mikrotik_config.get("username")
        mt_password = mikrotik_config.get("password")
    except Exception as err:
        logger.error(
            f"Error loading config from uisp.ini, ensure this file exists and has the proper variables. {err}"
        )
        raise Exception(
            f"Error loading config from uisp.ini, ensure this file exists and has the proper variables. {err}"
        )
