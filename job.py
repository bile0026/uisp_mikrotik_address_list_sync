# job.py
import configparser
import schedule
import time
import logging
from uisp_mikrotik_address_list_sync import sync_addresses

config = configparser.ConfigParser()
config.read("uisp.ini")
interval = int(config["ADMIN"]["interval"])

# Setup logging if needed
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("UISP to Mikrotik Address List Sync app started successfully...")
print("UISP to Mikrotik Address List Sync app started successfully...")

# Schedule the job every 5 minutes
schedule.every(interval).minutes.do(sync_addresses)

logging.info("Starting scheduler...")

# Keep the script running to execute scheduled tasks
while True:
    schedule.run_pending()
    time.sleep(1)
