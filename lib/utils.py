from google.cloud import firestore
from datetime import datetime



def unpack_document(snap: firestore.DocumentSnapshot, data: dict, depth: int = -1):
    document = snap.to_dict()
    data["id"] = snap.id

    if depth == 0:
        return

    for field in document:
        if isinstance(document[field], firestore.DocumentReference):
            data[field] = {}
            unpack_document(document[field].get(), data[field], depth-1)

        elif isinstance(document[field], list) and isinstance(document[field][0], firestore.DocumentReference):
            data[field] = []
            for item in document[field]:
                array_data = {}
                unpack_document(item.get(), array_data, depth-1)
                data[field].append(array_data)

        elif isinstance(document[field], datetime):
            data[field] = document[field].strftime("%m-%d-%YT%H:%M:%S")

        else:
            data[field] = document[field]