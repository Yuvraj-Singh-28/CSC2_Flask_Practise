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


def calculate_cart_totals(cart):
    subtotal = sum(details['price'] * details['quantity'] for details in cart.values())

    return {
        'subtotal': subtotal,
        'total': subtotal
    }


@app.route('/')
def index():
    flowers = load_data()
    addons = load_addons()
    cart = session.get('cart', {})
    totals = calculate_cart_totals(cart)

    return render_template(
        'index.html',
        flowers=flowers,
        addons=addons,
        cart=cart,
        totals=totals
    )

@app.route('/remove_from_cart/<item>')
def remove_item_from_cart(item):
    cart = session.get('cart', {})
    
    if item in cart:
        del cart[item]
        session['cart'] = cart
        session.modified = True
        flash(f"{item} removed from cart.")
    else:
        flash(f"{item} not found in cart.")
    return redirect(url_for('index'))

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    flower = request.form.get('flower')
    addon = request.form.get('addon')
    selected_addons = request.form.getlist('addons')
    quantity = int(request.form.get('quantity', 1))

    flowers = load_data()
    addons = load_addons()
    cart = session.get('cart', {})

    if flower:
        if flower not in flowers:
            flash("Invalid flower selected.")
            return redirect(url_for('index'))

        item_name = flower
        item_price = flowers[flower]['price']
    elif addon:
        if addon not in addons:
            flash("Invalid add-on selected.")
            return redirect(url_for('index'))

        item_name = addon
        item_price = addons[addon]['price']
    elif selected_addons:
        invalid_addons = [addon for addon in selected_addons if addon not in addons]
        if invalid_addons:
            flash("Invalid add-on selected.")
            return redirect(url_for('index'))

        for selected_addon in selected_addons:
            if selected_addon in cart:
                cart[selected_addon]['quantity'] += quantity
            else:
                cart[selected_addon] = {
                    'price': addons[selected_addon]['price'],
                    'quantity': quantity
                }

        session['cart'] = cart
        session.modified = True
        flash(f"{len(selected_addons)} add-on(s) added to cart.")
        return redirect(url_for('index'))
    else:
        flash("Please choose an item to add.")
        return redirect(url_for('index'))

    if item_name in cart:
        cart[item_name]['quantity'] += quantity
    else:
        cart[item_name] = {
            'price': item_price,
            'quantity': quantity
        }

    session['cart'] = cart
    session.modified = True

    flash(f"{quantity} {item_name}(s) added to cart.")
    return redirect(url_for('index'))


@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    session.pop('cart', None)
    session.modified = True
    flash("Cart cleared.")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
