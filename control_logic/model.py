from dataclasses import dataclass


@dataclass
class Sensor:
    name: str
    type: str
    unit: str
    value: float = 0.0
    min_value: float = 0.0
    max_value: float = 100.0


@dataclass
class Valve:
    name: str
    type: str
    pressure_required: float
    state: bool = False  # False = closed, True = open

    def update(self, pressure: float):
        """Open if pressure >= required, otherwise close."""
        self.state = pressure >= self.pressure_required


@dataclass
class Pump:
    name: str
    requires_valve_open: str
    min_pressure: float
    shutdown_pressure: float
    state: bool = False  # False = stopped, True = running

    def update(self, pressure: float, valve_open: bool):
        """
        Rules:
        - Stop immediately if pressure < shutdown_pressure.
        - Start only if valve is open and pressure >= min_pressure.
        """
        if pressure < self.shutdown_pressure:
            self.state = False
            return

        if valve_open and pressure >= self.min_pressure:
            self.state = True
        else:
            self.state = False
