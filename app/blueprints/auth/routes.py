from flask import render_template, request, redirect, url_for, flash
from flask.helpers import url_for
import requests
from .forms import LoginForm, RegisterForm, EditProfileForm, PokemonForm
from app.models import User, Pokemon
from flask_login import login_user, current_user, logout_user, login_required
from .import bp as auth
from sqlalchemy import and_


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
        return redirect(url_for('auth.login'))


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
                #"icon":int(form.icon.data)
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
    return render_template('register.html.j2', form=form)

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
            pokemon = response.json()
            new_pokemon=[]
            pokemon_dict={
                'poke_name':pokemon['name'],
                'base_hp':pokemon['stats'][0]['base_stat'],
                'base_defense':pokemon['stats'][2]['base_stat'],
                'base_attack':pokemon['stats'][1]['base_stat'],
            }
            new_pokemon.append(pokemon_dict)
            pokemon_count = Pokemon.query.filter(Pokemon.user_id == current_user.id).count()
        if pokemon_count>= 5:
            flash(f'You can not have more than 5 Pokemon', 'danger')
            return redirect(url_for('auth.pokemon'))
        elif new_pokemon == pokemon:
                flash(f'You can not add the same Pokemon twice', 'danger')
                return redirect(url_for('auth.pokemon'))
        else:
            new_poke = Pokemon(user_id = current_user.id, poke_name=pokemon_dict['poke_name'], base_hp = pokemon_dict['base_hp'], base_defense = pokemon_dict['base_defense'], base_attack = pokemon_dict['base_attack'])
            new_poke.save()
            flash(f'You caught {pokemon_dict["poke_name"]}', 'success')
        print(new_pokemon)
        return render_template('pokemon.html.j2', name=new_pokemon, form=form)
    else:
        error_string = "Houston we have a problem. Please try again"
        return render_template('pokemon.html.j2', error = error_string, form=form)


@auth.route('/release_pokemon/<name>', methods=['GET', 'POST'])
@login_required
def release_pokemon(name):
    pokemon_to_delete = Pokemon.query.get(id)
    if current_user.id==Pokemon.user_id:
        pokemon_to_delete.release()
        flash('Your Pokemon has been released','info')
    else:
        flash('You do not have access to do that')
    return redirect(url_for('main.profile'))

@auth.route('/mypokemon', methods = ['GET'])
@login_required
def mypokemon():
    p = Pokemon.query.filter_by(user_id=current_user.id)
    print(p)
    return render_template('profile.html.j2', pokemons=p)



@auth.route('/battle', methods=['GET', 'POST'])
@login_required
def battle_pokemon(name, base_attack, base_hp, base_defense):
    pokemon_user = Pokemon.query.filter_by(user_id=current_user.id)
    pokemon_defend = Pokemon.query.filter_by(user_id=User.id)
    