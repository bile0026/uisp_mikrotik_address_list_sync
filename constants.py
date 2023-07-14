"""Constant values for uisp_mikrotik_address_list_sync."""


service_status_map = {
    0: "prepared",
    1: "active",
    2: "ended",
    3: "suspended",
    4: "prepared blocked",
    5: "obsolete",
    6: "deferred",
    7: "quoted",
    8: "inactive",
}

service_status_map_reverse = {
    "prepared": 0,
    "active": 1,
    "ended": 2,
    "suspended": 3,
    "prepared blocked": 4,
    "obsolete": 5,
    "deferred": 6,
    "quoted": 7,
    "inactive": 8,
}

uisp_api_version = "v2.1"
ucrm_api_version = "v1.0"

active_list_name = "clients_active"
suspended_list_name = "clients_suspended"
all_list_name = "clients_all"
