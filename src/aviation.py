import json
import logging
import os
import requests


def process_flight_data(data: list[dict]):
    """Process flight data from the AviationStack API response."""

    flights = []
    for record in data:

        # Handle codeshare flights
        if record["flight"]["codeshared"] is not None:
            airline_iata = record["flight"]["codeshared"]["airline_iata"]
            flight_number = record["flight"]["codeshared"]["flight_number"]
            flight_iata = record["flight"]["codeshared"]["flight_iata"]
        else:
            airline_iata = record["airline"]["iata"]
            flight_number = record["flight"]["number"]
            flight_iata = record["flight"]["iata"]

        if airline_iata is None:
            continue

        flight_info = {
            "flight_date": record["flight_date"],
            "flight_status": record["flight_status"],
            "airline_iata": airline_iata.upper(),
            "flight_number": flight_number.upper(),
            "flight_iata": flight_iata.upper(),
            "departure_iata": record["departure"]["iata"].upper(),
            "departure_scheduled": record["departure"]["scheduled"],
            "departure_actual": record["departure"]["actual"],
            "departure_actual_runway": record["departure"]["actual_runway"],
            "arrival_iata": record["arrival"]["iata"].upper(),
            "arrival_scheduled": record["arrival"]["scheduled"],
            "arrival_actual": record["arrival"]["actual"],
            "arrival_actual_runway": record["arrival"]["actual_runway"],
        }

        if flight_info["arrival_actual"] is None:
            continue

        flights.append(flight_info)
    return flights


def fetch_flight_data():

    url = f"https://api.aviationstack.com/v1/flights"
    params = {
        "access_key": os.getenv("AVIATION_API_KEY"),
        "dep_iata": "AUS",
        "flight_status": "landed",
        "offset": 0,
        "limit": 100,  # limit of free API plan
    }
    flights = []
    while True:
        logging.info(
            f"Fetching data {params['offset']} to {params['offset'] + params['limit']}"
        )
        r = requests.get(url, params=params).json()

        if len(r["data"]) == 0:
            break

        flights.extend(process_flight_data(r["data"]))
        params["offset"] += 100

    return flights

if __name__ == "__main__":
    flights = fetch_flight_data()
    with open("response.json", "w") as file:
        json.dump(flights, file, indent=4)