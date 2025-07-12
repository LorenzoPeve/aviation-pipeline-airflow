DROP TABLE IF EXISTS austin_flights;

CREATE TABLE austin_flights (
    flight_date DATE,
    flight_status TEXT,

    -- Flight Info - Operating Carrier not ticketing carrier
    airline_iata VARCHAR(10), -- e.g., "AA" for American Airlines
    flight_number VARCHAR(10), -- e.g., "100" for American Airlines flight 100
    flight_iata VARCHAR(10), -- e.g., "AA100" for American Airlines flight 100

    -- Departure Info
    departure_iata VARCHAR(8), -- IATA code of the departure location/airport (e.g., "AUS" for Austin-Bergstrom International Airport)
    departure_scheduled TIMESTAMP, -- scheduled departure timestamp in RFC3339 (ISO8601)
    departure_actual TIMESTAMP, -- actual departure timestamp in RFC3339 (ISO8601)
    departure_actual_runway TIMESTAMP, -- actual runway timestamp. when the aircraft actually takes off from the runway as opposed to when it leaves the gate

    -- Arrival Info
    arrival_iata VARCHAR(8),
    arrival_scheduled TIMESTAMP,
    arrival_actual TIMESTAMP,
    arrival_actual_runway TIMESTAMP,

    PRIMARY KEY (flight_date, flight_iata),
    CONSTRAINT chk_flight_aus CHECK (departure_iata = 'AUS' OR arrival_iata = 'AUS')
);
