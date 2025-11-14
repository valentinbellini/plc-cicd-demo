# main.py
from util.loader import load_config, load_inputs
from control_logic.controller import PLCController
import time
from pathlib import Path


def demo_sequence():
    # Load config and create PLC controller
    cfg = load_config()  # configs/process.yaml
    plc = PLCController(cfg)

    # Try to load pressures from data/inputs.json; if missing, fallback to default list
    default_pressures = [0.0, 0.4, 1.0, 1.6, 2.0, 0.3]
    pressures = default_pressures
    try:
        # prefer data/inputs.json if exists
        pfile = Path("data/inputs.json")
        if pfile.exists():
            pressures = load_inputs(str(pfile))
        else:
            print("Warning: data/inputs.json not found — using default pressures.")
    except Exception as ex:
        print(f"Warning loading inputs.json: {ex}\nUsing default pressures.")
        pressures = default_pressures

    print("Starting demo sequence (pressure -> states):")
    for p in pressures:
        # Set sensor value and run one PLC scan
        plc.set_sensor("PT101", p)
        snap = plc.cycle()

        # Print
        valve_state = "OPEN" if snap["valves"]["V1"] else "CLOSED"
        pump_state = "RUN" if snap["pumps"]["P1"] else "STOP"
        print(f"P={p:4.2f} bar | V1={valve_state} | P1={pump_state}")

        time.sleep(0.3)


if __name__ == "__main__":
    demo_sequence()
