from flask import Flask, request, session, render_template, g, redirect, url_for, flash
import model
import jinja2
import os

app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
app.jinja_env.undefined = jinja2.StrictUndefined

@app.route("/")
def index():
    """This is the 'cover' page of the ubermelon site"""
    return render_template("index.html")

@app.route("/melons")
def list_melons():
    """This is the big page showing all the melons ubermelon has to offer"""
    melons = model.get_melons()
    return render_template("all_melons.html",
                           melon_list = melons)

@app.route("/melon/<int:id>")
def show_melon(id):
    """This page shows the details of a given melon, as well as giving an
    option to buy the melon."""
    melon = model.get_melon_by_id(id)
    print melon
    return render_template("melon_details.html",
                  display_melon = melon)

@app.route("/cart")
def shopping_cart():
    """TODO: Display the contents of the shopping cart. The shopping cart is a
    list held in the session that contains all the melons to be added. Check
    accompanying screenshots for details."""
    if session.get('cart') == None:
        session['cart'] = {}
        current_cart = []
        total = 0.00
        return render_template("cart.html", current_cart=current_cart, total=total)
    else:
        current_cart = []
        melon_ids = session['cart'].keys()
        for melon_id in melon_ids:
            temp_melon = model.get_melon_by_id(melon_id)
            temp_quantity = session['cart'][melon_id]
            temp_melon_total = temp_melon.price * temp_quantity
            temp_melon_total = "$%.2f" % temp_melon_total
            current_cart.append((temp_melon, temp_quantity, temp_melon_total))

            print current_cart
        total = 0
        for tup in current_cart:
            total = total + tup[0].price * float(tup[1])
        total = float(total)
        pretty_total = "$%.2f" %total
        return render_template("cart.html", current_cart=current_cart, total=pretty_total)

@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    # session['test'] = 'this is a test'
    # """TODO: Finish shopping cart functionality using session variables to hold
    # cart list.

    # Intended behavior: when a melon is added to a cart, redirect them to the
    # shopping cart page, while displaying the message"""
    if session.get('cart') == None:
        session['cart'] = {str(id): 1}
        flash("Successfully added to cart") 
    else:
        session['cart'][str(id)] = session['cart'].get(str(id), 0) + 1
        flash("successfully added to cart")

    print session['cart']

    return redirect("/cart")


@app.route("/login", methods=["GET"])
def show_login():
    if session.get('email') != None:
        session.clear()
        flash("Successfully logged out!")     
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """TODO: Receive the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session."""
    email = request.form.get("email")
    password = request.form.get("password")
    if model.get_customer_by_email(email) == None:
        flash("Please contact ubermelon to sign up!")
    else:
        session['email'] = model.get_customer_by_email(email).email
        print session['email']
        flash("Successfully logged in!")
    

    return redirect("/melons")


@app.route("/checkout")
def checkout():
    """TODO: Implement a payment system. For now, just return them to the main
    melon listing page."""
    flash("Sorry! Checkout will be implemented in a future version of ubermelon.")
    return redirect("/melons")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
