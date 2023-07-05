#!/usr/bin/env python3

# Review:
# API Fundamentals
# RESTful Routing
# Serialization
# Postman

# Set Up:
# Run in terminal:
# cd server
# export FLASK_APP=app.py
# export FLASK_RUN_PORT=5555
# flask db init
# flask db revision --autogenerate -m "Create table <table name>"
# flask db upgrade
# pipenv install flask_restful (if not done already)

# Double check the database to verify the migration worked as expected

# RESTful routing examples

# |  HTTP Verb  |      Path       |      Description      |
# |-------------|-----------------|-----------------------|
# | GET         |  /services      | READ all resources    |
# | GET         |  /services/:id  | READ one resource     |
# | POST        |  /services      | CREATE one resource   |
# | PATCH/PUT   |  /services/:id  | UPDATE one resource   |
# | DELETE      |  /services/:id  | DESTROY one resource  |
# |-------------|-----------------|-----------------------|

# Status code reference: https://httpstatusdogs.com/

from flask import Flask, jsonify, make_response, request
from flask_migrate import Migrate

# 1. Import `Api` and `Resource` from `flask_restful`
from flask_restful import Api, Resource

from models import db, Service, Show

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False  # configures JSON responses to print on indented lines

migrate = Migrate(app, db)
db.init_app(app)

# 2. Initialize the Api
# api = Api(app)

api = Api(app)

# 3. Create a Service class that inherits from Resource

# 4. Create a GET (all) Route (aka "index" route)
# 4.1 Make a `get` method that takes `self` as a param
# 4.2 Create a `services` list
# 4.3 Query for ALL services. For each service, create a dictionary
#     containing all attributes, then append to the services list.
# 4.4 Create a `response` variable (using make_response), jsonify our services list, add a 200 status code
# 4.5 Return `response`
# 4.6 Test in browser


class Services(Resource):
    def get(self):
        # services_list = [
        #     {"name": service.name, "price": service.price}
        #     for service in Service.query.all()
        # ]

        services_list = [service.to_dict() for service in Service.query.all()]

        response = make_response(services_list, 200)

        return response

    def post(self):
        # get the data from the form
        request_json = request.get_json()
        new_service = Service(name=request_json["name"], price=request_json["price"])

        # add the new data to the database
        db.session.add(new_service)

        # commit
        db.session.commit()

        # return a response

        return make_response(new_service.to_dict(), 201)


# 5. Add the new route to our api - `api.add_resource`

api.add_resource(Services, "/services")


class Shows(Resource):
    def get(self):
        shows_list = [show.to_dict() for show in Show.query.all()]

        response = make_response(shows_list, 200)

        return response

    def post(self):
        request_json = request.get_json()
        new_show = Show(
            name=request_json["name"],
            seasons=request_json["seasons"],
            service_id=request_json["service_id"],
        )

        db.session.add(new_show)

        db.session.commit()

        return make_response(new_show.to_dict(), 201)


api.add_resource(Shows, "/shows")
# 6. Serialization
# steps 6-9 in models.py

# 10. Use our serializer to return a cleaner response
# 10.1 Query all Services, convert them to a dictionary with `to_dict`, then append to a list (or use list comprehension!)
# 10.2 Invoke `make_response`, pass it the list of services along with a status of 200
# 10.3 Return the response
# 10.4 Test in browser

# 11. Create a GET (one) route
# 11.1 Build a class called ServiceByID that inherits from `Resource`
# 11.2 Create a `get` method and pass in the id along with `self`
# 11.3 Make a query for a service by the `id` and build a response to send to the browser/client


class ServiceById(Resource):
    def get(self, id):
        service = Service.query.filter(Service.id == id).first()

        return make_response(service.to_dict(), 200)


# 12. Add the new route to our api - `api.add_resource`

api.add_resource(ServiceById, "/services/<int:id>")


class ShowById(Resource):
    def get(self, id):
        show = Show.query.filter(Show.id == id).first()

        return make_response(show.to_dict(), 200)


api.add_resource(ShowById, "/shows/<int:id>")

# 13. Create a POST Route
# We'll use Postman to create a POST request. In the `Body` tab, select `form-data` and fill out the body
# with a service we want to create

# Create the POST route
# review the request object

# 13.1 Create a `post` method and pass `self` as a parameter
# 13.2 Create a new service from the `request` object, using `get_json()`
# 13.3 Add and commit the new service to the database
# 13.4 Convert the new production to a dictionary (to_dict)
# 13.5 Use `make_response` to create our response object, this time with status code 201 (created)
# 13.6 Test the route using Postman
