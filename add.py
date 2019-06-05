from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,
                                                                    'dbsqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
database = SQLAlchemy(app)
# Init ma
marshmallow = Marshmallow(app)


# Child Class/Model
class Child(database.Model):

    id = database.Column(database.Integer, primary_key=True)
    age = database.Column(database.Integer, unique=True)
    weight = database.Column(database.Integer)
    height = database.Column(database.Integer)

    def __init__(self, age, weight,height):
        self.age = age
        self.weight = weight
        self.height = height

    # Child Schema

class ChildSchema(marshmallow.Schema):
    class Meta:
        fields = ('id', 'age', 'weight', 'height')



# Init schema
child_children = ChildSchema(strict=True)
child_schema = ChildSchema(many=True, strict=True)


# Create a child
@app.route('/child', methods=['POST'])
def add_child():
    age = request.json['age']
    weight = request.json['weight']
    height = request.json['height']

    new_child = Child(age, weight, height)

    database.session.add(new_child)
    database.session.commit()

    return child_schema.jsonify(new_child)


# Get all child
@app.route('/child', methods=['GET'])
def get_all_child():
    all_child = Child.query.all()
    result = child_children.dump(all_child)
    return jsonify(result.data)

# Get one child
@app.route('/child/<id>', methods=['GET'])
def get_child(id):
    child = Child.children.get(id)
    return child_schema.jsonify(child)

# Update a child
@app.route('/child/<id>', methods=['PUT'])
def update_child(id):
    child = Child.query.get(id)

    age = request.json["age"]
    weight = request.json["weight"]
    height = request.json["height"]

    child.age = age
    child.weight = weight
    child.height = height

    database.session.commit()

    return child_schema.jsonify(child)

# Delete child
@app.route('/child/<id>', methods=['DELETE'])
def delete_child(id):
    child = Child.query.get(id)
    database.session.delete(child)
    database.session.commit()
    return child_schema.jsonify(child)


database.create_all()
# Run Server
if __name__ == '__main__':
    app.run(debug=True)