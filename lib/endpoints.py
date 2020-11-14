from flask import request
from flask_restful import Resource

from lib.utils import unpack_document
from lib.database import Database
db = Database()


class Errors:
    not_found = {"error": "Not found"}, 404
    wtf = {"error": "WTF just happened?"}, 500


class User(Resource):
    def get(self, user_id: str):
        data = {}
        doc = db.collection("users").document(user_id).get()
        unpack_document(doc, data)
        return data, 200

    def post(self):
        exists = list(db.collection("users").where("email", "==", f"{request.json['email']}").stream())
        if exists:
            data = {}
            unpack_document(exists[0], data)
            return data, 200

        try:
            data = {"email": request.json["email"],
                    "name": request.json["name"],
                    "avatar": request.json["avatar"],
                    "bio": "",
                    "contacts": "",
                    "skills": "",
                    "availability": ""}
            doc = db.collection("users").add(data)[1].get()
            data = {}
            unpack_document(doc, data)
            return data, 200
        except Exception:
            return Errors.wtf


class Project(Resource):
    def get(self, project_id: str):
        data = {}
        doc = db.collection("projects").document(project_id).get()
        unpack_document(doc, data)
        return data, 200

    def post(self):
        try:
            data = {"name": request.json["name"],
                    "description": request.json["description"],
                    "skills": request.json["skills"],
                    "availability": request.json["availability"],
                    "categories": request.json["categories"],
                    "owner": db.collection("users").document(request.json["owner"]),
                    "contributors": []}
            doc = db.collection("projects").add(data)[1].get()
            data = {}
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
            project = {}
            unpack_document(doc, project)
            data["projects"].append(project)
        return data, 200


class Search(Resource):
    def get(self, query: str):
        data = {"query": query,
                "projects": []}
        docs = db.collection("projects").stream()
        for doc in docs:
            print(doc.id)
            project = {}
            unpack_document(doc, project)
            if query.lower() in project["name"].lower():
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


class Category(Resource):
    def get(self, category: str):
        data = {"category": category,
                "projects": []}
        docs = db.collection("projects").where("categories", "array_contains", f"{category}").stream()
        # TODO: Case sensitive
        for doc in docs:
            project = {}
            unpack_document(doc, project)
            data["projects"].append(project)
        return data, 200