# tests/test_pumps.py
from util.loader import load_config
from control_logic.controller import PLCController

# Automatic tests ejecution when push:

def test_pump_does_not_start_without_valve():
    cfg = load_config()
    plc = PLCController(cfg)
    # set pressure high but we will force valve closed by setting pressure slightly below requirement
    plc.set_sensor("PT101", 1.4)  # valve will be closed
    snap = plc.cycle()
    assert snap["valves"]["V1"] is False
    assert snap["pumps"]["P1"] is False

def test_pump_starts_when_conditions_met():
    cfg = load_config()
    plc = PLCController(cfg)
    plc.set_sensor("PT101", 1.6)
    snap = plc.cycle()
    assert snap["valves"]["V1"] is True
    assert snap["pumps"]["P1"] is True

def test_pump_stops_on_low_pressure():
    cfg = load_config()
    plc = PLCController(cfg)
    plc.set_sensor("PT101", 1.6)
    snap = plc.cycle()
    assert snap["pumps"]["P1"] is True
    # now drop pressure below shutdown_pressure
    plc.set_sensor("PT101", 0.3)
    snap2 = plc.cycle()
    assert snap2["pumps"]["P1"] is False
