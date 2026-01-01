# the mock "API" that connects to the robots (M-patrol units)
# and mimics the "MCP" or API layer to check live data
import json
import random

# mock database (the live fleet)
# In production, this would be an API call to the Microspot backend
FLEET_DB = {
    "unit_alpha": {
        "status": "Patrolling",
        "battery": 42,
        "location": "Sector 4 (North Gate)",
        "last_seen": "10 seconds ago"
    },
    "unit_beta": {
        "status": "Charging",
        "battery": 98,
        "location": "HQ Docking Station",
        "last_seen": "Online"
    },
    "unit_gamma": {
        "status": "Maintenance",
        "battery": 0,
        "location": "Workshop",
        "last_seen": "Offline (Error E-404)"
    }
}

def get_fleet_status(unit_name: str):
    """
    Simulates an API call to get real-time telemetry.
    """
    # normalize the name (handle "alpha", "unit alpha", "Alpha")
    key = "unit_" + unit_name.lower().split(" ")[-1]
    
    data = FLEET_DB.get(key)
    if data:
        return json.dumps(data)
    else:
        return json.dumps({"error": "Unit ID not found in active fleet."})

def dispatch_unit(unit_name: str, location: str):
    """
    Simulates sending a command to the robot.
    """
    # In a real system, this would POST to the robot's API
    return json.dumps({
        "status": "SUCCESS", 
        "message": f"Command Sent: {unit_name} is rerouting to {location}."
    })