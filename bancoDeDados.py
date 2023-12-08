from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="clinicaMedica"
)
