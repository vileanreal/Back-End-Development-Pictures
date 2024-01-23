from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if data:
        return jsonify(data), 200

    return {"message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    picture = next((picture for picture in data if picture["id"] == id), None)
    if picture:
        return jsonify(picture), 200
    else:
        return {"message": "Data not found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    try:
        # Extract picture data from the request body
        picture_data = request.json  # Assuming the request contains JSON data

        # Check if a picture with the same ID already exists
        existing_picture = next((picture for picture in data if picture["id"] == picture_data.get("id")), None)

        if existing_picture:
            return jsonify({"Message": f"picture with id {picture_data['id']} already present"}), 302

        # Append the new picture data to the data list
        data.append(picture_data)

        return jsonify(picture_data), 201
    except Exception as e:
        # Handle other exceptions if needed
        return jsonify({"Message": f"Error creating picture: {str(e)}"}), 500

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    # Extract picture data from the request body
    picture_data = request.json

    # Find the picture in the data list by id
    picture = next((picture for picture in data if picture["id"] == id), None)

    if picture:
        # Update the existing picture with the incoming request
        picture.update(picture_data)
        return jsonify({"message": "Picture updated successfully"}), 200
    else:
        return jsonify({"message": "Picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    # Find the picture in the data list by id
    picture = next((picture for picture in data if picture["id"] == id), None)

    if picture:
        # Delete the picture from the data list
        data.remove(picture)
        return "", 204  # Empty body with status code HTTP_204_NO_CONTENT
    else:
        return {"message": "Data not found"}, 404