# Home Control Dashboard

A simple web dashboard that reads temperature and humidity data from the Home Monitoring System and displays it in the browser.

## How It Works

Arduino sends sensor data over serial port. A Python script reads this data, saves it to a MySQL database, and serves it to the browser. The dashboard fetches new data every 3 seconds.

## Files

- index.html — main page
- style.css — styles
- app.js — fetches data and updates the page
- server.py — reads serial port, saves to MySQL, serves data

