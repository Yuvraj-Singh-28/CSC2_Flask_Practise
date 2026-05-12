import json
from flask import Flask, render_template, request, redirect, url_for,session, flash

app = Flask(__name__)
app.secret_key = 'mysecretkey'

def load_data():
    with open('data/flower.json') as file:
     flowers = json.load(file)
     return flowers
 
def load_addons():
    with open('data/addons.json') as file:
     addons = json.load(file)
     return addons

@app.route('/')
def index():
    flowers = load_data()
    addons = load_addons()
    return render_template('index.html', flowers=flowers, addons=addons)


# This is the last line of the code.

if __name__ == '__main__':
    app.run(debug=True)
    
# last line ends.    
    