from fastapi import FastAPI, Depends, HTTPException
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel

import psutil

app = FastAPI()

@app.get('/fastapi')
def fastapi_url():
    return {'message': 'This is first API'}


def getSystemHealth():
    # CPU Usage
    cpu_usage = psutil.cpu_percent(interval=1)

    # Memory Usage
    memory_usage = psutil.virtual_memory().percent

    # Disk Usage
    disk_usage = psutil.disk_usage('/').percent

    # Network Usage
    net_info = psutil.net_io_counters()
    bytes_sent = net_info.bytes_sent
    bytes_received = net_info.bytes_recv

    # Battery Information (if applicable)
    try:
        battery_info = psutil.sensors_battery()
        battery_percent = battery_info.percent
        power_plugged = battery_info.power_plugged
        # Sensor Information (Temperature, Voltage, Fans)
        sensor_info = psutil.sensors_temperatures()
    except AttributeError:
        battery_percent = None
        power_plugged = None
        sensor_info = None

    # System Uptime
    uptime = psutil.boot_time()

    # Disk Partition Information
    partitions = psutil.disk_partitions()
    disk_partitions = {}
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_partitions[partition.device] = {
                "total": usage.total,
                "used": usage.used,
                "free": usage.free
            }
        except PermissionError:
            # Handle the case where the disk is not ready or accessible
            disk_partitions[partition.device] = {
                "total": None,
                "used": None,
                "free": None
            }

    swap_info = psutil.swap_memory()

    num_logical_cores = psutil.cpu_count()
    num_physical_cores = psutil.cpu_count(logical=False)

    system_health = {
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage,
        "disk_usage": disk_usage,
        "network": {
            "bytes_sent": bytes_sent,
            "bytes_received": bytes_received
        },
        "battery": {
            "percent": battery_percent,
            "power_plugged": power_plugged
        },
        "sensors": sensor_info,
        "uptime": uptime,
        "disk_partitions": disk_partitions,
        "swap_memory": {
            "total": swap_info.total,
            "used": swap_info.used,
            "free": swap_info.free
        },
        "cpu_cores": {
            "logical": num_logical_cores,
            "physical": num_physical_cores
        }
    }

    return system_health


@app.get('/health', response_model=dict)
def health_check(system_health: dict = Depends(getSystemHealth)):
    return system_health