from flask import Blueprint,request,jsonify
from .db import get_connections
from datetime import datetime
import os
from flask import render_template

sensor_bp = Blueprint("sensor",__name__)

@sensor_bp.route("/send-data",methods=["POST"])
def send_data():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error":"NO DATA FOUND"})
        
        if "temperature" not in data or "humidity" not in data:
            return jsonify({"error":"NO TEMPERATURE OR HUMIDITY FOUND"})
        try:
            temperature = data["temperature"]
            humidity = data["humidity"]
        except(TypeError,ValueError):
            return jsonify({"error":"INVALID DATA TYPE"})
        
        timestamp = datetime.now().isoformat()

        try:
            connect = get_connections()
            cursor = connect.cursor()

            print("DB path:", os.path.abspath("sensor_data.db"))

            cursor.execute("INSERT INTO sensor_data(temperature,humidity,received_at) VALUES (?,?,?)",(temperature,humidity,timestamp))

            connect.commit()

        finally:
            connect.close()

        return jsonify({
            "message":"Data sent successfully",
            "RECEIVED DATA":{
            "temperature":temperature,
            "humidity":humidity,
            "timestamp":timestamp
            }
        })
    except Exception as err:
        return jsonify({"error":str(err)})
    

@sensor_bp.route("/get-data",methods = ["GET"])

def get_data():
    try:
        connect = get_connections()
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM sensor_data ORDER BY received_at DESC")
        rows = cursor.fetchall()
        connect.close()
        result = []

        for row in rows:
            result.append({
                "temperature":row[1],
                "humidity":row[2],
                "timestamp":row[3]
                })
            
        return jsonify({
            "total":len(result),
            "data":result,
            "message":"Data retrieved successfully"
            })
    except Exception as err:
        return jsonify({"error":str(err)})
    
@sensor_bp.route("/realtime")
def realtime_view():
    return render_template("realtime.html")