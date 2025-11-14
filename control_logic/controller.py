# Import models
from control_logic.model import Sensor, Valve, Pump

# Simulated PLC
class PLCController:
    def __init__(self, config: dict):
        # create sensors
        self.sensors = {}
        for name, props in config.get("sensors", {}).items():
            self.sensors[name] = Sensor(
                name=name,
                type=props.get("type", "generic"),
                unit=props.get("unit", ""),
                min_value=props.get("min_value", 0.0),
                max_value=props.get("max_value", 100.0),
                value=props.get("default", 0.0),
            )
        # create valves
        self.valves = {}
        for name, props in config.get("valves", {}).items():
            self.valves[name] = Valve(
                name=name,
                type=props.get("type", "normally_closed"),
                pressure_required=float(props.get("pressure_required", 0.0)),
            )
        # create pumps
        self.pumps = {}
        for name, props in config.get("pumps", {}).items():
            self.pumps[name] = Pump(
                name=name,
                requires_valve_open=props.get("requires_valve_open"),
                min_pressure=float(props.get("min_pressure", 0.0)),
                shutdown_pressure=float(props.get("shutdown_pressure", 0.0)),
            )

    # Method to set pressure value.
    def set_sensor(self, sensor_name: str, value: float):
        if sensor_name in self.sensors:
            self.sensors[sensor_name].value = value

    # Scan cycle.
    def cycle(self):
        """Simulate one PLC scan: read sensors -> evaluate valves -> evaluate pumps -> output state snapshot"""
        
        # read pressure
        pressure = 0.0
        if "PT101" in self.sensors:
            pressure = float(self.sensors["PT101"].value)

        # update valves
        for v in self.valves.values():
            v.update(pressure)

        # update pumps (need valve states)
        for p in self.pumps.values():
            valve_name = p.requires_valve_open
            valve_open = False
            if valve_name and valve_name in self.valves:
                valve_open = self.valves[valve_name].state
            p.update(pressure, valve_open)

        # return snapshot
        snapshot = {
            "sensors": {k: v.value for k, v in self.sensors.items()},
            "valves": {k: v.state for k, v in self.valves.items()},
            "pumps": {k: p.state for k, p in self.pumps.items()},
        }
        return snapshot
