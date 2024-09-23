from os import name
from flask import Flask

app = Flask(name)

@app.route('/')
def hello(): return 'Hola, mundo!'

if name == 'main': 
    app.run(debug=True) > app.py