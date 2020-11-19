from flask import Flask
from flask_restful import Api


class Pages:
    @staticmethod
    def index():
        return "<h1>Assembee Server</h1>", 200


class Server:
    def __init__(self):
        self.app = Flask("Assembee")
        self.api = Api(self.app)
        self.base_url = "/"
        self.init()

    def init(self):
        try:
            import lib.endpoints as endpoints
            self.app.add_url_rule("/", "index", Pages.index)
            resources = [(endpoints.User,
                          f"{self.base_url}user/<string:user_id>",
                          f"{self.base_url}user"),
                         (endpoints.Project,
                          f"{self.base_url}project",
                          f"{self.base_url}project/<string:project_id>"),
                         (endpoints.Projects,
                          f"{self.base_url}projects/<string:user_id>"),
                         (endpoints.Search,
                          f"{self.base_url}search/<string:query>"),
                         (endpoints.Categories,
                          f"{self.base_url}categories"),
                         (endpoints.Category,
                          f"{self.base_url}category/<string:category>"),
                         (endpoints.Contributors,
                          f"{self.base_url}contributors/<string:project_id>/<string:user_id>"),
                         (endpoints.Notifications,
                          f"{self.base_url}notifications/<string:user_id>",
                          f"{self.base_url}notifications"),
                         (endpoints.Notification,
                          f"{self.base_url}notification/<string:notification_id>")
                         ]
            for resource in resources:
                self.api.add_resource(*resource)
        except Exception as error:
            print(error)
            raise

    def start(self, port: int = None, debug: bool = True):
        try:
            self.app.run(debug=debug, port=port)
        except Exception as error:
            print(error)
            raise
        

server = Server()
app = server.app  # Production WSGI server entry point

if __name__ == "__main__":
    server.start(6969)
