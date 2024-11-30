import json
from flask import Flask, render_template, jsonify
import sqlite3
import plotly.graph_objs as go
import plotly.io as pio
import plotly.utils

app = Flask(__name__)

DATABASE = 'device_number.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def get_device_data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM device_number WHERE date(timestamp) = date('now')")
    rows = cur.fetchall()
    conn.close()
    return rows

@app.route('/')
def index():
    data = get_device_data()
    timestamps = [row['timestamp'] for row in data]
    ap_down = [row['ap_down_number'] for row in data]
    switch_down = [row['switch_down_number'] for row in data]
    old_ont_down = [row['old_ont_down_number'] for row in data]
    new_ont_down = [row['new_ont_down_number'] for row in data]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=timestamps, y=ap_down, mode='lines+markers', name='AP Down'))
    fig.add_trace(go.Scatter(x=timestamps, y=switch_down, mode='lines+markers', name='Switch Down'))
    fig.add_trace(go.Scatter(x=timestamps, y=old_ont_down, mode='lines+markers', name='Old ONT Down'))
    fig.add_trace(go.Scatter(x=timestamps, y=new_ont_down, mode='lines+markers', name='New ONT Down'))

    fig.update_layout(title='设备在线情况', xaxis_title='时间', yaxis_title='在线数量')
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('index.html', graphJSON=graph_json)


@app.route('/data')
def data():
    data = get_device_data()
    timestamps = [row['timestamp'] for row in data]
    ap_down = [row['ap_down_number'] for row in data]
    switch_down = [row['switch_down_number'] for row in data]
    old_ont_down = [row['old_ont_down_number'] for row in data]
    new_ont_down = [row['new_ont_down_number'] for row in data]

    return jsonify({
        'timestamps': timestamps,
        'ap_down': ap_down,
        'switch_down': switch_down,
        'old_ont_down': old_ont_down,
        'new_ont_down': new_ont_down
    })

if __name__ == '__main__':
    app.run(debug=False)
