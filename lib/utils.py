from google.cloud import firestore


def unpack_document(snap: firestore.DocumentSnapshot, data: dict):
    document = snap.to_dict()
    data["id"] = snap.id
    for field in document:
        if isinstance(document[field], firestore.DocumentReference):
            data[field] = {}
            unpack_document(document[field].get(), data[field])
        else:
            data[field] = document[field]