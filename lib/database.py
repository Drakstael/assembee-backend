import os
import firebase_admin as firebase
from firebase_admin import credentials, firestore


class Singleton:
    def __init__(self, cls):
        self._cls = cls

    def instance(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._cls()
            return self._instance

    def __call__(self):
        return self.instance().get()

    def __instancecheck__(self, instance):
        return isinstance(instance, self._cls)


@Singleton
class Database:
    def __init__(self):
        cwd = os.getcwd()
        if cwd.split("\\")[-1] == "lib":
            creds = "../config/service_account_creds.json"
        else:
            creds = "config/service_account_creds.json"
        cert = credentials.Certificate(creds)
        firebase.initialize_app(cert)
        self._db = firestore.client()

    def get(self):
        return self._db


if __name__ == "__main__":
    db = Database()
    print(db.document("users/4k1TaKukA65kR99lpRSV").get().to_dict())