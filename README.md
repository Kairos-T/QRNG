# Quantum Random Number Generator

This project is an implementation of a quantum random number generator using the Qiskit integrated into a Flask web application. It includes a simple web interface allowing users to generate random numbers and visualise the distribution through a graph plot using Matplotlib.

## Getting Started

1. Clone this repository:
```bash
git clone https://github.com/Kairos-T/QRNG
cd QRNG
```

2. (Optional) Create a virtual environment:
```bash
sudo python3 -m venv venv
source venv/bin/activate
```

3. Install the dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python3 app.py
```

5. Open the application in your browser at http://localhost:5000

## Features
- Entering a specified range
- Generating a single random number
- Generating 100 random numbers
- Clearing the generated numbers
- Visualising the distribution of the generated numbers using a bar chart

## Usage
1. Enter the minimum and maximum values.
2. Click on the "Generate" button to generate a single random number, or the "Generate 100 Numbers" button to generate 100 random numbers.
3. Click on the "Generate Graph" button to visualise the distribution of the generated numbers.
4. Click on the "Clear" button to clear the generated numbers and the graph.

## Screenshots
1. Landing Page
![Landing Page](screenshots/QRNG.png)

2. Generate random number
![Generate random number](screenshots/Gen.png)

3. Generate 100 random numbers
![Generate 100 random numbers](screenshots/Gen100.png)

4. Visualise distribution
![Visualise distribution](screenshots/Plt.png)

## Limitations
- **Simulation** - The `qasm_simulator` is simply a classical simulator for quantum circuits, and has limitations in simulating quantum systems. Hence, there might be outliers and in the distribution of the generated numbers, as can be seen in the screenshot above.

