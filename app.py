from flask import Flask, render_template, request, jsonify
from qiskit import QuantumCircuit, Aer, transpile, assemble
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

# Global variables
number_counts = {}
total_generated = 0


def generate_random_number(min_value, max_value):
    global total_generated

    if min_value > max_value:
        raise ValueError("Invalid range: Minimum value should be less than or equal to the maximum value")

    num_bits = len(bin(max_value)) - 2

    circuit = QuantumCircuit(num_bits, num_bits)
    circuit.h(range(num_bits))
    circuit.measure(range(num_bits), range(num_bits))

    backend = Aer.get_backend('qasm_simulator')
    result = backend.run(assemble(transpile(circuit, backend=backend))).result()
    counts = result.get_counts(circuit)

    random_number = int(list(counts.keys())[0], 2)

    # Ensure that the generated number is within the specified range
    random_number = min(max(random_number, min_value), max_value)

    # Update the count of the generated number in the dictionary
    number_counts[random_number] = number_counts.get(random_number, 0) + 1
    total_generated += 1

    return random_number


def generate_numbers(min_value, max_value, num_samples=1):
    global total_generated

    if min_value > max_value:
        raise ValueError("Invalid range: Minimum value should be less than or equal to the maximum value")

    num_bits = len(bin(max_value)) - 2
    backend = Aer.get_backend('qasm_simulator')

    generated_numbers = []

    for _ in range(num_samples):
        circuit = QuantumCircuit(num_bits, num_bits)
        circuit.h(range(num_bits))
        circuit.measure(range(num_bits), range(num_bits))

        result = backend.run(assemble(transpile(circuit, backend=backend))).result()
        counts = result.get_counts(circuit)

        random_number = int(list(counts.keys())[0], 2)

        # Ensure that the generated number is within the specified range
        random_number = min(max(random_number, min_value), max_value)

        # Update the count of the generated number in the dictionary
        number_counts[random_number] = number_counts.get(random_number, 0) + 1
        total_generated += 1

        generated_numbers.append(random_number)

    return generated_numbers


def plot_bar_chart():
    plt.bar(number_counts.keys(), number_counts.values())
    plt.xlabel('Number')
    plt.ylabel('Occurrences')
    plt.title('Distribution of Numbers')
    plt.grid(axis='y')
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return base64.b64encode(img.getvalue()).decode()


@app.route('/', methods=['GET', 'POST'])
def home():
    random_number = None
    error_message = None

    if request.method == 'POST':
        try:
            min_value = int(request.form['min_value'])
            max_value = int(request.form['max_value'])
            if 'generate_100' in request.form:
                generated_numbers = generate_numbers(min_value, max_value, num_samples=100)
                return render_template('index.html', generated_numbers=generated_numbers, number_counts=number_counts, total_generated=total_generated)
            else:
                random_number = generate_random_number(min_value, max_value)
        except ValueError as e:
            error_message = str(e)

    return render_template('index.html', random_number=random_number, number_counts=number_counts, total_generated=total_generated, error_message=error_message)


@app.route('/generate_100_numbers', methods=['POST'])
def generate_100_numbers_route():
    try:
        min_value = int(request.form['min_value'])
        max_value = int(request.form['max_value'])
        generated_numbers = generate_numbers(min_value, max_value, num_samples=100)
        return render_template('index.html', generated_numbers=generated_numbers, number_counts=number_counts, total_generated=total_generated)
    except ValueError as e:
        return jsonify({'error': str(e)})


@app.route('/clear')
def clear_numbers():
    global number_counts, total_generated
    number_counts = {}
    total_generated = 0
    return render_template('index.html', random_number=None, number_counts=number_counts, total_generated=total_generated)


@app.route('/generate_graph')
def generate_graph():
    plot = plot_bar_chart()
    return render_template('index.html', plot=plot, random_number=None, number_counts=number_counts, total_generated=total_generated)


if __name__ == '__main__':
    app.run(debug=True)
