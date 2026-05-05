from os import name

from flask import Flask, render_template, request, redirect, url_for,session, flash

app = Flask(__name__)
app.secret_key = 'mysecretkey'

if name == 'main':
    app.run(debug=True)
    
    @app.route('/')
    def index():
        return render_template('index.html')