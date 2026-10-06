# Simple CoAP Weather Application

A simple CoAP-based weather application developed in Python using [aiocoap](https://github.com/chrysn/aiocoap) and the [OpenWeather API](https://openweathermap.org/api).

## Features

- CoAP server using `aiocoap`
- CoAP client
- GET current temperature
- POST city selection
- PUT city update
- DELETE/reset city
- Real-time weather data from OpenWeather
- Support for multiple predefined cities

## Technologies

- Python
- CoAP
- aiocoap
- Requests
- OpenWeather API

## How to Run

Install the required dependencies:

pip install aiocoap requests python-dotenv

Configure your OpenWeather API key using a `.env` file:


OPENWEATHER_API_KEY=your_api_key_here


Start the CoAP server:


python phome.py


Then, in another terminal, start the client:

python coap_cl.py

## CoAP Operations

| Operation | Description                 |
| --------- | --------------------------- |
| GET       | Get the current temperature |
| POST      | Select a city               |
| PUT       | Update the city             |
| DELETE    | Reset the city to GUELMA    |



