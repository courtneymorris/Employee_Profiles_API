from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


# homework create own db model and have original columns
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False)
    DOB = db.Column(db.String(144), unique=False)
    start_date = db.Column(db.String(144), unique=False)
    position = db.Column(db.String(144), unique=False)
    pay_rate = db.Column(db.String(144), unique=False)

    def __init__(self, name, DOB, start_date, position, pay_rate):
        self.name = name
        self.DOB = DOB
        self.start_date = start_date
        self.position = position
        self.pay_rate = pay_rate


    def __repr__(self):
        return f'(name={self.name}, DOB={self.DOB}, start_date={self.start_date})'


class ProfileSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'DOB', 'start_date', 'position', 'pay_rate')


profile_schema = ProfileSchema()
profiles_schema = ProfileSchema(many=True)

# Endpoint to create a new profile
@app.route('/profile', methods=["POST"])
def add_profile():
    name = request.json['name']
    DOB = request.json['DOB']
    start_date = request.json['start_date']
    position = request.json['position']
    pay_rate = request.json['pay_rate']

    new_profile = Profile(name, DOB, start_date, position, pay_rate)

    db.session.add(new_profile)
    db.session.commit()

    profile = Profile.query.get(new_profile.id)

    return profile_schema.jsonify(profile)


# Endpoint to query all profiles
@app.route('/profiles', methods=['GET'])
def get_profiles():
    all_profiles = Profile.query.all()
    result = profiles_schema.dump(all_profiles)
    return jsonify(result)


# Endpoint for querying a single profile
@app.route('/profile/<id>', methods=['GET'])
def get_profile(id):
    profile = Profile.query.get(id)
    return profile_schema.jsonify(profile)


#Endpoint for updating a profile
@app.route('/profile/<id>', methods=['PUT'])
def profile_update(id):
    profile = Profile.query.get(id)
    name = request.json['name']
    DOB = request.json['DOB']
    start_date = request.json['start_date']
    position = request.json['position']
    pay_rate = request.json['pay_rate']

    profile.name = name
    profile.DOB = DOB
    profile.start_date = start_date
    profile.position = position
    profile.pay_rate = pay_rate

    db.session.commit()
    return profile_schema.jsonify(profile)


# Endpoint for deleting a profile
@app.route('/profile/<id>', methods=['DELETE'])   
def profile_delete(id):
    profile = Profile.query.get(id)
    db.session.delete(profile)
    db.session.commit()

    return profile_schema.jsonify(profile)


if __name__ == '__main__':
    app.run(debug=True)

