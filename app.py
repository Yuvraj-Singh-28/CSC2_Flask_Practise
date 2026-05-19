import json
from flask import Flask, render_template, request, session, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = 'mysecretkey'


def load_data():
    with open('data/flower.json') as file:
        return json.load(file)


def load_addons():
    with open('data/addons.json') as file:
        return json.load(file)


@app.route('/')
def index():
    flowers = load_data()
    addons = load_addons()
    cart = session.get('cart', {})

    return render_template(
        'index.html',
        flowers=flowers,
        addons=addons,
        cart=cart
    )

@app.route("/remove_from_cart")
def remove_from_cart():
    return render_template("test.html")

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    flower = request.form['flower']
    quantity = int(request.form['quantity'])

    flowers = load_data()
    cart = session.get('cart', {})

    if flower not in flowers:
        flash("Invalid flower selected.")
        return redirect(url_for('index'))

    if flower in cart:
        cart[flower]['quantity'] += quantity
    else:
        cart[flower] = {
            'price': flowers[flower]['price'],
            'quantity': quantity
        }

    session['cart'] = cart
    session.modified = True

    flash(f"{quantity} {flower}(s) added to cart.")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)