from flask import Flask, jsonify, render_template
import csv

app = Flask(__name__)


def read_data():
    data = []
    # read the data from csv file and return as dictionary
    with open('shipdata.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        for row in csv_reader:
            data.append(row)

    return data

def calculate_aggregated_values_by_ship(data):
    aggregated_data = []
    ag = {}

    for value in data:
        if value['imo'] in ag:
            ag[value['imo']].append(value)
        else:
            ag[value['imo']] = [value]

    for key, group in ag.items():
        sum_mainEngineConsumption = sum(float(entry['mainEngineConsumption']) for entry in group)
        sum_DistanceOverGround = sum(float(entry['DistanceOverGround']) for entry in group)
        sum_Speed = sum(float(entry['Speed']) for entry in group)
        avg_mainEngineConsumption = sum_mainEngineConsumption / len(group)
        avg_DistanceOverGround = sum_DistanceOverGround / len(group)
        avg_Speed = sum_Speed / len(group)
        aggregated_data.append({
            'imo': key,
            'name': group[0]['name'],
            'sum_mainEngineConsumption': sum_mainEngineConsumption,
            'sum_DistanceOverGround': sum_DistanceOverGround,
            'sum_Speed': sum_Speed,
            'avg_mainEngineConsumption': avg_mainEngineConsumption,
            'avg_DistanceOverGround': avg_DistanceOverGround,
            'avg_Speed': avg_Speed
        })

    return aggregated_data


@app.route("/api/data", methods=['GET'])
def get_data():
    return jsonify({'data': read_data()})

@app.route('/api/aggregated-data', methods=['GET'])
def get_aggregated_data():
    raw_data = read_data()
    return jsonify({'data': calculate_aggregated_values_by_ship(raw_data)})


@app.route('/data')
def display_data():
    return render_template('table.html', title="Data Grid")

@app.route('/aggregated-data')
def display_aggregated_data():
    return render_template('calculated_table.html', title="Aggregated Data")

if __name__ == '__main__':
    app.run(port=8000, debug=True)