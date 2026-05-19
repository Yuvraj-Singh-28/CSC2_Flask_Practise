import json
from flask import Flask, render_template, request, session, flash, redirect, url_for

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

def load_data():
    with open('data/flower.json') as file:
        flowers = json.load(file)
        return flowers
    



@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    flower = request.form['flower']  # get selected flower name
    quantity = int(request.form['quantity'])  # convert quantity to a number
    flowers = load_data()  # get flower data from file
    cart = session.get('cart', {})  # get cart from session or start fresh

    if flower not in flowers:
        flash("Invalid flower selected.")
        return redirect(url_for('index'))

    if flower in cart:
        cart[flower]['quantity'] += quantity  # add existing quantity
    else:
        cart[flower] = {
            'price': flowers[flower]['price'],
            'quantity': quantity
        }

    session['cart'] = cart  # update session
    session.modified = True  # force Flask to save it
    flash(f"{quantity} {flower}(s) added to cart.")
    return redirect(url_for('index'))

# This is the last line of the code.

if __name__ == '__main__':
    app.run(debug=True)
    
# last line ends.    
    