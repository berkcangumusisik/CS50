-- I wanted to get some information about the crime scene to see if i can find anything useful.
SELECT description
FROM   crime_scene_reports
WHERE  day = 28
       AND month = 7
       AND year = 2020
       AND street = 'Chamberlin Street';

-- I'm looking for any clue in interviews that recorded on crime day and contains 'courthouse'.
SELECT name, transcript
FROM   interviews
WHERE  day = 28
       AND month = 7
       AND year = 2020
       AND transcript LIKE '%courthouse%';

-- With the clue that i found, i can now search for a plate numbers and with the plate numbers i found, i can find the people that exit between given time.
SELECT name
FROM   people
       JOIN courthouse_security_logs
         ON people.license_plate = courthouse_security_logs.license_plate
WHERE  day = 28
       AND month = 7
       AND year = 2020
       AND hour = 10
       AND minute BETWEEN 15 AND 25
       AND activity = 'exit';

-- trying to find people that use ATM on 28th. (list: Ernest, Danielle, Elizabeth, Russel)
SELECT DISTINCT name
FROM   people
       JOIN bank_accounts
         ON people.id = bank_accounts.person_id
       JOIN atm_transactions
         ON bank_accounts.account_number = atm_transactions.account_number
WHERE  day = 28
       AND month = 7
       AND year = 2020
       AND transaction_type = 'withdraw'
       AND atm_location = 'Fifer Street';

-- Trying to find the person who took the first flight on 29th day. (list: Ernest, Danielle)
SELECT name
FROM   people
       JOIN passengers
         ON people.passport_number = passengers.passport_number
WHERE  flight_id = (SELECT id
                    FROM   flights
                    WHERE  day = 29
                           AND month = 7
                           AND year = 2020
                    ORDER  BY hour,
                              minute
                    LIMIT  1);

-- The first flight of the day.
SELECT city
FROM   airports
WHERE  id = (SELECT destination_airport_id
             FROM   flights
             WHERE  day = 29
                    AND month = 7
                    AND year = 2020
             ORDER  BY hour,
                       minute
             LIMIT  1);

-- I'm looking for the people that make a phone call shorter than a minute. (Ernest)
SELECT name
FROM   people
       JOIN phone_calls
         ON people.phone_number = phone_calls.caller
WHERE  day = 28
       AND month = 7
       AND year = 2020
       AND duration < 60;

-- With the phone log, i can find the accomplice
SELECT name
FROM   people
       JOIN phone_calls
         ON people.phone_number = phone_calls.receiver
WHERE  day = 28
       AND month = 7
       AND year = 2020
       AND duration < 60
       AND caller = (SELECT phone_number
                     FROM   people
                     WHERE  name = 'Ernest');