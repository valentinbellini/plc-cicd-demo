# PLC Simulation + CI/CD Pipeline (Python)

This repository implements a simplified industrial control loop (PLC scan cycle) using Python, combined with a full CI/CD pipeline using GitHub Actions.
The goal is to understand how automation logic can be versioned, tested, and automatically validated.

## Purpose of the Project

The project simulates the interaction between:
- Sensors
- Actuators (Valve, Pump)
- A PLC controller running a cyclic scan

and demonstrates how:

- Control logic can be modeled in Python
- Inputs can be loaded from external files
- The system can be validated with automated tests
- CI/CD ensures correctness on every commit or pull request

## How the Simulation Works

### models/model.py

Defines the "physical" elements of the process: *Sensor, Valve, Pump*. These classes store state but do not implement control logic.

### controller/controller.py

Represents the PLC and its scan cycle:

1) Read sensor values

2) Apply control logic

3) Update actuators

4) Return a snapshot of system state

The **snapshot** is a dictionary used for:

- Debugging
- Historical logs
- Unit testing
- CI/CD validation

### loader.py

Loads sets of input data (pressure values in this case) from JSON or CSV so tests and simulations are deterministic and repeatable.

### main.py

Allows manual, local execution without CI/CD. Useful to visualize the cycle-by-cycle behavior.

### tests/

Contains unit tests using pytest to ensure:

- The pump activates/deactivates correctly
- The valve opens/closes under the right conditions

Testing is crucial for CI/CD: every **push** triggers these tests automatically.


### GitHub Actions CI/CD (cicd.yml)

The pipeline:

- Sets up a Python environment
- Installs dependencies
- Runs tests
- Reports success/failure

Every change must be verified automatically before being accepted.

## How CI/CD Works

Every time you do a **git push** -> GitHub will automatically:

- Clone the repository
- Install Python dependencies
- Run all tests
- Fail or succeed the pipeline

A failing test will block the pipeline — exactly how industrial control software is validated in modern workflows.