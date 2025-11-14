# tests/test_valves.py
from util.loader import load_config
from control_logic.controller import PLCController


def test_valve_opens_at_threshold():
    cfg = load_config()
    plc = PLCController(cfg)
    plc.set_sensor("PT101", 1.6)
    snap = plc.cycle()
    assert snap["valves"]["V1"] is True


def test_valve_stays_closed_below_threshold():
    cfg = load_config()
    plc = PLCController(cfg)
    plc.set_sensor("PT101", 1.4)
    snap = plc.cycle()
    assert snap["valves"]["V1"] is False
