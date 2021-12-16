from app import db
from flask_login import UserMixin
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash
from app import login

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poke_name = db.column(db.String(150))
    base_hp = db.Column(db.Integer)
    base_attack = db.Column(db.Integer)
    base_defense = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f'<id: {self.id} | {self.poke_name}>'

    def to_dict(self):
        data={
            'id': self.id,
            'poke_name': self.poke_name,
            'base_hp': self.base_hp,
            'base_attack': self.base_attack,
            'base_defense': self.base_defense,
        }
        return data
    def catch(self):
        db.session.add(self)
        db.session.commit()

    def release(self):
        db.session.delete(self)
        db.session.commit()
    
    def save(self):
        db.session.add(self)
        db.session.commit() 
    

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200))
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'))


    def __repr__(self):
        return f'<User: {self.id} | {self.email}>'

    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data["email"]
        self.password = self.hash_password(data['password'])
        self.save()


    def hash_password(self, original_password):
        return generate_password_hash(original_password)

    
    def check_hashed_password(self, login_password):
        return check_password_hash(self.password, login_password)

    
    def save(self):
        db.session.add(self)
        db.session.commit() 


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    