import json

import flask
from flask_login import login_user, current_user, logout_user

from receipt_tracker.flask import app, repo, session, bcrypt, login_manager
from receipt_tracker.repo.models import Buyer, Receipt, Seller, User
from receipt_tracker.flask.forms import (BusinessForm, ClientForm, LoginForm,
                                         ReceiptForm, RegistrationForm)
from receipt_tracker.use_cases import list_uc


@app.route("/")
@app.route("/home")
def home():
    return flask.render_template('home.html')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed_password)
        session.add(user)
        session.commit()
        flask.flash(f'Account created for {form.username.data}!', 'success')
        return flask.redirect(flask.url_for('home'))

    return flask.render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flask.flash(f'Welcome back {user.username}', 'success')
            next_page = flask.request.args.get('next')
            return flask.redirect(next_page) if next_page else flask.redirect(flask.url_for('home'))
        else:
            flask.flash('Login Unsuccessful. Please check email and password', 'danger')
    return flask.render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return flask.redirect(flask.url_for('home'))


# STATS ############################################################################
@app.route("/view_buyers")
def view_buyers():
    table = list_uc.create_table(repo, Buyer)
    return flask.render_template('stats.html', table=table, title="Buyers")


@app.route("/view_sellers")
def view_sellers():
    table = list_uc.create_table(repo, Seller)
    return flask.render_template('stats.html', table=table, title="Sellers")


@app.route("/view_receipts")
def view_receipts():
    table = list_uc.create_table(repo, Receipt, fields=['id', 'date', 'buyer_name', 'seller_name', 'total', 'description'])
    return flask.render_template('stats.html', table=table, title="Receipts")


# ADD NEW ##########################################################################
@app.route("/add_new", methods=['GET', 'POST'])
def add_new():
    """
    Main route to add_new page for all three buyer, seller, receipt add forms.

    Implemented using first solution by Grey Li (Update version).
    See: https://stackoverflow.com/questions/18290142/multiple-forms-in-a-single-page-using-flask-and-wtforms

    """
    client_form = ClientForm()
    business_form = BusinessForm()
    receipt_form = ReceiptForm()

    return flask.render_template('add_new.html',
                                 client_form=client_form,
                                 business_form=business_form,
                                 receipt_form=receipt_form
                                 )


@app.route("/add_client", methods=['GET', 'POST'])
def add_client():
    client_form = ClientForm()
    business_form = BusinessForm()
    receipt_form = ReceiptForm()

    if client_form.validate_on_submit():
        client = Buyer(name=client_form.client_name.data)
        session.add(client)
        session.commit()
        flask.flash(f'New buyer {client_form.client_name.data} added!', 'success')
        return flask.redirect(flask.url_for('add_new'))

    return flask.render_template('add_new.html',
                                 client_form=client_form,
                                 business_form=business_form,
                                 receipt_form=receipt_form
                                 )


@app.route("/add_business", methods=['GET', 'POST'])
def add_business():
    client_form = ClientForm()
    business_form = BusinessForm()
    receipt_form = ReceiptForm()

    if business_form.validate_on_submit():
        seller = Seller(name=business_form.business_name.data)
        session.add(seller)
        session.commit()
        flask.flash(f'New seller {business_form.business_name.data} added!', 'success')
        return flask.redirect(flask.url_for('add_new'))

    return flask.render_template('add_new.html',
                                 client_form=client_form,
                                 business_form=business_form,
                                 receipt_form=receipt_form
                                 )


@app.route("/add_receipt", methods=['GET', 'POST'])
def add_receipt():
    client_form = ClientForm()
    business_form = BusinessForm()
    receipt_form = ReceiptForm()

    if receipt_form.validate_on_submit():
        buyer = Buyer.query.filter_by(name=receipt_form.buyer.data).first()
        seller = Seller.query.filter_by(name=receipt_form.seller.data).first()
        receipt = Receipt(date=receipt_form.date.data,
                          buyer_id=buyer.id,
                          seller_id=seller.id,
                          total=receipt_form.total.data,
                          description=receipt_form.description.data
                          )
        session.add(receipt)
        session.commit()
        flask.flash(f'New receipt added!', 'success')
        return flask.redirect(flask.url_for('add_new'))

    return flask.render_template('add_new.html',
                                 client_form=client_form,
                                 business_form=business_form,
                                 receipt_form=receipt_form
                                 )


@app.route('/_autocomplete_buyer', methods=['GET'])
def autocomplete_buyer():
    """Helper route for jQuery autocomplete function."""
    return flask.Response(json.dumps(list_uc.get_entities(repo, Buyer, 'name')),
                          mimetype='application/json')


@app.route('/_autocomplete_seller', methods=['GET'])
def autocomplete_seller():
    """Helper route for jQuery autocomplete function."""
    return flask.Response(json.dumps(list_uc.get_entities(repo, Seller, 'name')),
                          mimetype='application/json')
