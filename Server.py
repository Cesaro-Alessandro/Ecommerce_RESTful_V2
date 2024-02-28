from http.server import BaseHTTPRequestHandler, HTTPServer
import Product
import json
import DBManager

hostName = "localhost"
serverPort = 8888


class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        id = path.split("/")[-1]
        db = DBManager.Database()
        if db._connection == None:
            self.send_response(500)
            self.send_header("Content-type", "text/html")
            self.end_headers()
        else:
            if path == "/products":
                products = Product.Product.get_All()
                json_temp2 = []
                for p in products:
                    json_temp = {
                        "type": "products",
                        "id": p["id"],
                        "attributes": {
                            "nome": p["name"],
                            "marca": p["brand"],
                            "prezzo": p["price"],
                        },
                    }
                    json_temp2.append(json_temp)
                json_s = {"data": json_temp2}
                json_s = json.dumps(json_s)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json_s.encode(encoding="utf-8"))
            elif path == "/products/{}".format(id):
                product = Product.Product.get_By_Id(id)
                if product:
                    product = json.dumps(
                        {
                            "data": {
                                "type": "products",
                                "id": product["id"],
                                "attributes": {
                                    "nome": product["name"],
                                    "marca": product["brand"],
                                    "prezzo": product["price"],
                                },
                            }
                        },
                        indent=2,
                    )
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(product.encode(encoding="utf-8"))
                else:
                    self.send_response(404, message="Not found")
                    self.send_header("Content-type", "text/html")
                    self.end_headers()

    def do_DELETE(self):
        path = self.path
        id = path.split("/")[-1]
        db = DBManager.Database()
        if db._connection == None:
            self.send_response(500)
            self.send_header("Content-type", "text/html")
            self.end_headers()
        else:
            if path == "/products/{}".format(id):
                product = Product.Product.delete_By_Id(id)
                if product:
                    self.send_response(204)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                else:
                    self.send_response(404, message="Not found")
                    self.send_header("Content-type", "text/html")
                    self.end_headers()

    def do_POST(self):
        db = DBManager.Database()
        if db._connection == None:
            self.send_response(500)
            self.send_header("Content-type", "text/html")
            self.end_headers()
        else:
            try:
                self.send_response(201)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                content_len = int(self.headers.get("content-length", 0))
                post_body = self.rfile.read(content_len)
                json_s = json.loads(post_body)
                params = [
                    json_s["data"]["attributes"]["nome"],
                    json_s["data"]["attributes"]["marca"],
                    json_s["data"]["attributes"]["prezzo"],
                ]
                product = Product.Product.create(params)
                product_j = json.dumps(
                    {
                        "data": {
                            "type": "products",
                            "id": product["id"],
                            "attributes": {
                                "nome": product["name"],
                                "marca": product["brand"],
                                "prezzo": product["price"],
                            },
                        }
                    },
                    indent=2,
                )
                self.wfile.write(product_j.encode("utf-8"))
                print(json_s)
            except:
                self.send_response(404)
                self.send_header("Content-type", "application/json")
                self.end_headers()

    def do_PATCH(self):
        path = self.path
        id = path.split("/")[-1]
        db = DBManager.Database()
        if db._connection == None:
            self.send_response(500)
            self.send_header("Content-type", "text/html")
            self.end_headers()
        else:
            if path == "/products/{}".format(id):
                product = Product.Product.get_By_Id(id)
                if product:
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    content_len = int(self.headers.get("content-length", 0))
                    post_body = self.rfile.read(content_len)
                    json_f = json.loads(post_body)
                    params = [
                        id,
                        json_f["data"]["attributes"]["nome"],
                        json_f["data"]["attributes"]["marca"],
                        json_f["data"]["attributes"]["prezzo"],
                    ]
                    product = Product.Product.update(params)
                    product = json.dumps(
                        {
                            "data": {
                                "type": "products",
                                "id": product["id"],
                                "attributes": {
                                    "nome": product["name"],
                                    "marca": product["brand"],
                                    "prezzo": product["price"],
                                },
                            }
                        },
                        indent=2,
                    )
                    self.wfile.write(product.encode("utf-8"))
                else:
                    self.send_response(404, message="Not found")
                    self.send_header("Content-type", "text/html")
                    self.end_headers()


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), Server)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

