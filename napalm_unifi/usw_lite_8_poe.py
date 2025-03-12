# napalm_unifi/usw_lite_8_poe.py

import json
from typing import Dict, Any

def get_interfaces_usw_lite_8_poe(netmiko_device) -> Dict[str, Dict[str, Any]]:
    """
    Specialized method to extract interface information from USW-Lite-8-PoE switches
    using mca-dump command.

    Args:
        netmiko_device: The established Netmiko connection to the device

    Returns:
        Dictionary of interfaces with their properties
    """
    interfaces = {}

    # Get mca-dump output
    mca_output = netmiko_device.send_command("mca-dump")
    mca_data = json.loads(mca_output)

    # Default MTU for all interfaces
    default_mtu = 1500

    # Process port_table to extract interface information
    port_table = mca_data.get("port_table", [])

    # Create a mapping of port_idx to port data for easier access
    port_map = {port.get("port_idx"): port for port in port_table if "port_idx" in port}

    # Ensure we have all 8 ports (USW-Lite-8-PoE has 8 ports)
    for port_idx in range(1, 9):
        # Get port data if available, otherwise use defaults
        port_data = port_map.get(port_idx, {})

        # Determine port name
        if port_idx == 1:
            port_name = "Uplink"
        else:
            port_name = f"Port {port_idx}"

        # Extract port information
        is_enabled = port_data.get("enable", False)
        is_up = port_data.get("up", False)
        speed = float(port_data.get("speed", -1))

        # Get MAC address if available
        mac_address = port_data.get("mac", None)

        # Create interface dictionary
        interfaces[port_name] = {
            "is_up": is_up,
            "is_enabled": is_enabled,
            "description": port_name,
            "last_flapped": float(-1),  # Not available in mca-dump
            "speed": speed,
            "mtu": default_mtu,
            "mac_address": mac_address,
            "type": "ether",
            "alias": "",
        }

    return interfaces
