from flask import Flask, render_template
from .db import init_db
from .sensor import sensor_bp

def Create_app():
    server = Flask(__name__)
    init_db()
    server.register_blueprint(sensor_bp)
    return server
    
