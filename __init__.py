"""Module declaration for uisp_mikrotik_address_list_sync."""
from utils import str_to_bool
from configparser import ConfigParser
import logging

logger = logging.getLogger(__name__)


class UISPMikroTikSyncConfig:
    """configuration for uisp-mikrotik-sync module"""

    try:
        parser = ConfigParser(interpolation=None)
        parser.read("uisp.ini")

        admin_config = dict(parser["ADMIN"])
        uisp_config = dict(parser["UISP"])
        mikrotik_config = dict(parser["MIKROTIK"])

        send_health_check = str_to_bool(admin_config.get("send_health_check"))
        if send_health_check:
            health_check_id = admin_config.get("health_check_id")
        uisp_nms_token = uisp_config.get("nms_token")
        uisp_crm_token = uisp_config.get("crm_token")
        uisp_fqdn = uisp_config.get("server_fqdn")
        uisp_use_ssl = str_to_bool(uisp_config.get("use_ssl", "True"))
        ssl_verify = str_to_bool(mikrotik_config.get("ssl_verify"))
        mt_use_ssl = str_to_bool(mikrotik_config.get("use_ssl"))
        disable_ssl_warning = str_to_bool(mikrotik_config.get("disable_ssl_warning"))
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
