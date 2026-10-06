import asyncio
import requests
import os

from aiocoap import Context, Message, resource
from aiocoap.numbers.codes import Code


# ============================================================
# CONFIGURATION
# ============================================================

HOST = "127.0.0.1"
PORT = 5683

API_KEY = os.getenv("OPENWEATHER_API_KEY")

DEFAULT_CITY = "GUELMA"


# ============================================================
# CITY COORDINATES
# ============================================================

CITY_COORDINATES = {
    "GUELMA": {
        "lat": 36.4621,
        "lon": 7.4261
    },

    "ANNABA": {
        "lat": 36.9000,
        "lon": 7.7667
    },

    "ALGIERS": {
        "lat": 36.7538,
        "lon": 3.0588
    },

    "ORAN": {
        "lat": 35.6971,
        "lon": -0.6308
    }
}


# ============================================================
# TEMPERATURE RESOURCE
# ============================================================

class TemperatureResource(resource.Resource):

    def __init__(self):
        super().__init__()

        self.city = DEFAULT_CITY

    # ========================================================
    # GET
    # ========================================================

    async def render_get(self, request):

        print("GET request received")

        temperature = self.get_temperature(self.city)

        if temperature is None:

            return Message(
                code=Code.INTERNAL_SERVER_ERROR,
                payload=b"Error getting temperature"
            )

        message = f"{self.city}: {temperature:.2f} C"

        print(message)

        return Message(
            payload=message.encode("utf-8")
        )

    # ========================================================
    # POST
    # ========================================================

    async def render_post(self, request):

        new_city = request.payload.decode("utf-8").strip().upper()

        print(f"POST request: {new_city}")

        if new_city not in CITY_COORDINATES:

            return Message(
                code=Code.BAD_REQUEST,
                payload=b"City not supported"
            )

        self.city = new_city

        message = f"City changed to {new_city}"

        return Message(
            code=Code.CREATED,
            payload=message.encode("utf-8")
        )

    # ========================================================
    # PUT
    # ========================================================

    async def render_put(self, request):

        new_city = request.payload.decode("utf-8").strip().upper()

        print(f"PUT request: {new_city}")

        if new_city not in CITY_COORDINATES:

            return Message(
                code=Code.BAD_REQUEST,
                payload=b"City not supported"
            )

        self.city = new_city

        message = f"City changed to {new_city}"

        return Message(
            code=Code.CHANGED,
            payload=message.encode("utf-8")
        )

    # ========================================================
    # DELETE
    # ========================================================

    async def render_delete(self, request):

        print("DELETE request received")

        self.city = DEFAULT_CITY

        return Message(
            code=Code.DELETED,
            payload=b"City reset to GUELMA"
        )

    # ========================================================
    # OPENWEATHER - ONE CALL API 4.0
    # ========================================================

    def get_temperature(self, city):

        if city not in CITY_COORDINATES:
            print(f"Unknown city: {city}")
            return None

        lat = CITY_COORDINATES[city]["lat"]
        lon = CITY_COORDINATES[city]["lon"]

        url = (
            "https://api.openweathermap.org/data/2.5/weather"
            f"?lat={lat}"
            f"&lon={lon}"
            f"&appid={API_KEY}"
            "&units=metric"
        )

        print(f"Requesting weather for {city}")
        print(f"Coordinates: {lat}, {lon}")
        print(f"URL: {url.replace(API_KEY, 'HIDDEN_KEY')}")

        try:

            print("Sending HTTP request...")

            response = requests.get(
                url,
                timeout=60,
                headers={
                    "User-Agent": "Mozilla/5.0"
                }
            )

            print("HTTP response received!")
            print("Status code:", response.status_code)

            response.raise_for_status()

            data = response.json()

            print("JSON received:")
            print(data)

            print("Temperature found:", data["main"]["temp"])

            return data["main"]["temp"]

        except requests.exceptions.Timeout:

            print("ERROR: Weather API request timed out.")
            return None

        except requests.exceptions.RequestException as e:

            print("ERROR: Weather API request failed:")
            print(e)
            return None

        except KeyError as e:

            print("ERROR: Temperature key not found:")
            print(e)
            print("Received data:")
            print(data)
            return None

        except Exception as e:

            print("ERROR:", e)
            return None


# ============================================================
# COAP SERVER
# ============================================================

async def main():

    root = resource.Site()

    root.add_resource(
        ["temperature"],
        TemperatureResource()
    )

    await Context.create_server_context(
        root,
        bind=(HOST, PORT)
    )

    print()
    print("========================================")
    print("        CoAP TEMPERATURE SERVER")
    print("========================================")
    print()
    print(
        f"Server: coap://{HOST}:{PORT}/temperature"
    )
    print()
    print("Weather API: OpenWeather One Call 4.0")
    print()
    print("Supported operations:")
    print("  GET")
    print("  POST")
    print("  PUT")
    print("  DELETE")
    print()
    print("Waiting for requests...")
    print("Press CTRL+C to stop.")
    print()

    await asyncio.get_running_loop().create_future()


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    try:

        asyncio.run(main())

    except KeyboardInterrupt:

        print()
        print("Server stopped.")