-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Crime reported on Humphrey Street on 7/28/2021

SELECT description FROM crime_scene_reports WHERE year = 2021 AND month = 7 AND day = 28 AND street = "Humphrey Street";

-- interviews on 7/28/2021 inluding "bakery"

SELECT transcript FROM interviews WHERE year = 2021 AND month = 7 AND day = 28 AND transcript LIKE "%bakery%";

-- get names from matching transcripts

SELECT name FROM people JOIN bakery_security_logs ON bakery_security_logs.license_plate = people.license_plate WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25 AND activity = "exit";

-- Suspects: Vanessa, Bruce, Barry, Luca, Sofia, Iman, Diana, Kelsey

-- get names from atm transactions

SELECT name FROM people JOIN bank_accounts ON bank_accounts.person_id = people.id JOIN atm_transactions.account_number = bank_accounts.account_number WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = "Leggett Street" AND transaction_type = "withdraw";

-- New Suspects: Bruce, Diana, Brooke, Kenny, Iman, Luca, Taylor, Benista

-- Common suspects: Bruce, Luca, Iman, Diana

-- get names for passengers on first fligth out tomorrow

SELECT name FROM people JOIN passengers ON passengers.passport_number = people.passport_number WHERE flight_id = (SELECT id FROM flights WHERE year = 2021 AND nmonth = 7 AND day = 29 AND origin_airport_id = (SELECT id FROM airports WHERE city = "Fiftyville") ORDER BY hour, minute LIMIT 1);

-- new suspects: Doris, Sofia, Bruce, Edward, Kelsey, Taylor, Kenny, Luca

-- commone suspects: Bruce, Luca

-- get calls matching person

SELECT name FROM people JOIN phone_calls ON phone_calls.caller = people.phone_number WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60;

-- new suspects: Sofia, Kelsey, Bruce, Kelsey, Taylor, Diana, Carina, Kenny, Benista

-- common: Bruce

-- get destination city

SELECT city FROM airports WHERE id = (SELECT destination_airport_id FROM flights WHERE year = 2021 AND month = 7 AND day = 29 AND origin_airport_id = (SELECT id FROM airports WHERE city = "Fiftyville") ORDER BY hour, minute LIMIT 1);

-- city: New York City

-- get accomplice name

-- Bruce phone number

SELECT phone_number FROM people WHERE name = "Bruce";

-- Bruce # = (367)555-5533

SELECT name FROM people WHERE phone_number = (SELECT receiver FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60 AND caller = "(367) 555-5533");

-- accomplice: ROBIN