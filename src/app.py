import json
from flask import Flask, jsonify, request, Response
import psycopg2
import os
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(host=os.environ['POSTGRES_HOST'],
        database=os.environ['POSTGRES_DB'],
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD'])
    return conn

@app.route("/")
def hello():
    return "hello world!"

@app.route("/sensors", methods=["GET"])
def get_sensors():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM sensors;')
    sensors = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(sensors)

@app.route("/sensors/<id>", methods=["GET"])
def get_sensor_by_id(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute('SELECT * FROM sensors where id = %s;',id)
        sensors = cur.fetchone()
        cur.close()
        conn.close()      
        if (sensors == None):
            return Response(status=404)
        return jsonify(sensors)
    except TypeError as e:
        return Response(status=500)

@app.route("/sensors", methods=["POST"])
def save_sensor():
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO sensors (name, description, token)'
            'VALUES (%(name)s, %(description)s, %(token)s) RETURNING ID',
            data
            )
    id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    data['id'] = id
    return jsonify(data)

@app.route("/sensors/<id>", methods=["PUT"])
def update_sensor(id):
    data = request.get_json()
    data['id'] = id
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE sensors SET name = %(name)s, description = %(description)s, token = %(token)s WHERE id = %(id)s',
            data
            )
    cur.close()
    conn.commit()
    conn.close()
    data['id'] = id
    return jsonify(data)

@app.route("/sensors/<id>", methods=["DELETE"])
def delete_sensor(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM sensors WHERE id = %s',
            id
            )
    cur.close()
    conn.commit()
    conn.close()
    return Response(status=200)

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")

