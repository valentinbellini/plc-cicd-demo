from control_logic.model import Sensor, Valve, Pump


class PLCController:
    def __init__(self, config: dict):
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

        self.valves = {}
        for name, props in config.get("valves", {}).items():
            self.valves[name] = Valve(
                name=name,
                type=props.get("type", "normally_closed"),
                pressure_required=float(
                    props.get("pressure_required", 0.0)
                ),
            )

        self.pumps = {}
        for name, props in config.get("pumps", {}).items():
            self.pumps[name] = Pump(
                name=name,
                requires_valve_open=props.get("requires_valve_open"),
                min_pressure=float(props.get("min_pressure", 0.0)),
                shutdown_pressure=float(
                    props.get("shutdown_pressure", 0.0)
                ),
            )

    def set_sensor(self, sensor_name: str, value: float):
        if sensor_name in self.sensors:
            self.sensors[sensor_name].value = value

    def cycle(self):
        # Read pressure
        pressure = 0.0
        if "PT101" in self.sensors:
            pressure = float(self.sensors["PT101"].value)

        # Update valves
        for valve in self.valves.values():
            valve.update(pressure)

        # Update pumps
        for pump in self.pumps.values():
            valve_name = pump.requires_valve_open
            valve_open = False

            if valve_name and valve_name in self.valves:
                valve_open = self.valves[valve_name].state

            pump.update(pressure, valve_open)

        # Return snapshot
        snapshot = {
            "sensor_pressure": pressure,
            "valves": {
                name: valve.state
                for name, valve in self.valves.items()
            },
            "pumps": {
                name: pump.state
                for name, pump in self.pumps.items()
            },
        }

        return snapshot
