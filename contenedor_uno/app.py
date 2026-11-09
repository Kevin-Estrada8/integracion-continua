import json
import time
import urllib.request
import urllib.error

URL = "http://contenedor_dos:8000/mensaje"

mensaje = {
    "mensaje": "Hola desde el contenedor uno"
}

for intento in range(15):
    try:
        datos = json.dumps(mensaje).encode("utf-8")

        solicitud = urllib.request.Request(
            URL,
            data=datos,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        with urllib.request.urlopen(solicitud, timeout=5) as respuesta:
            resultado = json.loads(respuesta.read().decode())

            print("Respuesta del contenedor dos:")
            print(json.dumps(resultado, indent=4, ensure_ascii=False))

            if respuesta.status == 200 and resultado.get("estado") == "exitoso":
                print("PRUEBA DE COMUNICACION EXITOSA")
                break

            raise RuntimeError("Respuesta inesperada del servidor")

    except (urllib.error.URLError, TimeoutError, OSError) as error:
        print(f"Intento {intento + 1}: {error}")
        time.sleep(2)
else:
    raise SystemExit("ERROR: No fue posible comunicarse con el contenedor dos")