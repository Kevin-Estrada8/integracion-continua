from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class Servidor(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(
                json.dumps({"estado": "activo"}).encode()
            )
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/mensaje":
            longitud = int(self.headers.get("Content-Length", 0))
            datos = self.rfile.read(longitud)

            mensaje = json.loads(datos.decode())

            print("Mensaje recibido:", mensaje)

            respuesta = {
                "estado": "exitoso",
                "mensaje": "Mensaje recibido correctamente",
                "origen": mensaje.get("mensaje")
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(json.dumps(respuesta).encode())
        else:
            self.send_response(404)
            self.end_headers()


servidor = HTTPServer(("0.0.0.0", 8000), Servidor)

print("Servidor escuchando en el puerto 8000...")

servidor.serve_forever()
