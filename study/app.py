# -*- coding: utf-8 -*-

from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello world'

@app.route('/add', methods=['GET'])
def add():
    a = int(request.args.get('a'))
    b = int(request.args.get('b'))
   
    return(f"The sum of {a} and {b} is {a+b}")

@app.route('/login', methods=['GET'])
def login():
    username = request.args.get('username')
    password= request.args.get('password')
    return (f"user: {username} <br/> password: {password}")

