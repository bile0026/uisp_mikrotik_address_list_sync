"""Constant values for uisp_mikrotik_address_list_sync."""


service_status_map = {
    "0": "prepared",
    "1": "active",
    "2": "ended",
    "3": "suspended",
    "4": "prepared blocked",
    "5": "obsolete",
    "6": "deferred",
    "7": "quoted",
    "8": "inactive",
}

uisp_api_version = "v2.1"
ucrm_api_version = "v1.0"

active_list_name = "clients_active"
suspended_list_name = "clients_suspended"
all_list_name = "clients_all"
