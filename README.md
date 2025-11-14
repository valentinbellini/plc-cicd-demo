# plc-cicd-demo

- PT101: Pressure Transmitter
- V1: Entry Valve
- P1: Transfer pump

R1 – Apertura de V1	V1 sólo puede abrir si PT101 >= 1.5 bar
R2 – Arranque de P1	P1 sólo puede arrancar si V1 está abierta y PT101 >= 1.5 bar
R3 – Seguridad	Si la presión cae por debajo de 0.5 bar, P1 debe pararse inmediatamente

plc-cicd-demo/
│
├── configs/
│   └── process.yaml --> YAML model of the industrial process
│
├── control_logic/
│   ├── __init__.py
│   ├── model.py
│   └── controller.py
│
├── tests/
│   ├── __init__.py
│   ├── test_valves.py
│   ├── test_pumps.py
│   └── test_sequences.py
│
├── ci/
│   ├── __init__.py
│   └── generate_report.py
│
├── util/
│   ├── __init__.py
│   └── loader.py
│
├── .github/
│   └── workflows/
│       └── cicd.yml
│
├── main.py
├── requirements.txt
└── README.md
