from flask import request
from flask_restful import Resource
from google.cloud import firestore

from lib.utils import unpack_document
from lib.database import Database
db = Database()


class Errors:
    not_found = {"error": "Not found"}, 404
    wtf = {"error": "WTF just happened?"}, 500


class User(Resource):
    def get(self, username: str):
        data = {"username": username}
        return data, 200


class Project(Resource):
    def get(self, project_id: str):
        data = {"project_id": project_id}
        doc = db.collection("projects").document(project_id).get()
        unpack_document(doc, data)
        return data, 200

    def post(self):
        try:
            data = {"name": request.json["name"],
                    "description": request.json["description"],
                    "skills": request.json["skills"],
                    "availability": request.json["availability"],
                    "owner": db.collection("users").document(request.json["owner"]),
                    "contributors": []}
            doc = db.collection("projects").add(data)
            data = {"project_id": doc.id}
            unpack_document(doc, data)
            return data, 200
        except Exception:
            return Errors.wtf


class Projects(Resource):
    def get(self, user_id: str):
        data = {"user_id": user_id,
                "projects": []}
        docs = db.collection("projects").where("owner", "==", db.document(f"users/{user_id}")).stream()
        for doc in docs:
            project = {"project_id": doc.id}
            unpack_document(doc, project)
            data["projects"].append(project)
        return data, 200


class Categories(Resource):
    def get(self):
        data = {"categories": []}
        docs = db.collection("categories").stream()
        for doc in docs:
            category = {}
            unpack_document(doc, category)
            data["categories"].append(category)
        return data, 200