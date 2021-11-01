from flask import render_template, request, redirect, url_for, flash
from flask.helpers import url_for
import requests
from .forms import LoginForm, RegisterForm, EditProfileForm, PokemonForm
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required
from .import bp as auth


@auth.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = request.form.get("email").lower()
        password = request.form.get("password")
        u = User.query.filter_by(email=email).first()

        if u and u.check_hashed_password(password):
            login_user(u)
            flash('You have logged in', 'success')
            return redirect(url_for("main.index"))
        error_string = "Invalid Email password combo"
        return render_template('login.html.j2', error = error_string, form=form)
    return render_template('login.html.j2', form=form)


@auth.route('/logout')
@login_required
def logout():
    if current_user:
        logout_user()
        flash('You have logged out', 'danger')
        return redirect(url_for('login'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            new_user_data = {
                "first_name":form.first_name.data.title(),
                "last_name":form.last_name.data.title(),
                "email":form.email.data.lower(),
                "password": form.password.data,
                "icon":int(form.icon.data)
            }
            new_user_object = User()
            new_user_object.from_dict(new_user_data)
            new_user_object.save()
        except:
            error_string = "There was an unexpected Error creating your account. Please Try again."
            return render_template('register.html.j2',form=form, error = error_string) 
        return redirect(url_for('auth.login')) 
    return render_template('register.html.j2', form = form) 

@auth.route('/edit_profile',methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm()
    if request.method == 'POST' and form.validate_on_submit():
        new_user_data={
            "first_name":form.first_name.data.title(),
                "last_name":form.last_name.data.title(),
                "email":form.email.data.lower(),
                "password":form.password.data,
                "Icon":int(form.icon.data) if int(form.icon.data) != 9000 else current_user.icon
        }
        user=User.query.filter_by(email=form.email.data.lower()).first()
        if user and current_user.email != user.email:
            flash('Email already in use','danger')
            return redirect(url_for('auth.edit_profile'))
        try:
            current_user.from_dict(new_user_data)
            current_user.save()
            flash('Profile Updated', 'success')
        except:
            flash('There was an unexpected error', 'danger')
            return redirect(url_for('auth.edit_profile'))
    return render_template('auth/register.html.j2', form=form)

@auth.route('/pokemon', methods = ['GET', 'POST'])
@login_required
def pokemon():
    form = PokemonForm()
    if request.method == 'POST' and form.validate_on_submit():
        name = request.form.get('name')
        url = f'https://pokeapi.co/api/v2/pokemon/{name}/'
        response = requests.get(url)
        if response.ok:
            if not response.json()['stats']:
                return "We had an error loding your data"
            data = response.json()['stats']
            pokemon_stats=[]
            for pokemon in data:
                pokemon_dict={
                    'poke_name':pokemon['forms']['name'],
                    'base_hp':pokemon['stats'][0]['base_stat'],
                    'base_defense':pokemon['stats'][2]['base_stat'],
                    'base_attack':pokemon['stats'][1]['base_stat'],
                    }
                pokemon_stats.append(pokemon_dict)
            print(pokemon_stats)
            return render_template('pokemon.html.j2', pokemons=pokemon_stats)
        else:
            return "Houston we have a problem. Please try again"

    return render_template('pokemon.html.j2')
