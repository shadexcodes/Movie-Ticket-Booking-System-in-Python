from flask import Flask, render_template, request, jsonify
import random
import time

app = Flask(__name__)

# --- ORIGINAL DATA STRUCTURES ---
movies = {
    1: {"title": "Interstellar",      "genre": "Sci-Fi",   "duration": "2h 49m", "rating": "PG-13"},
    2: {"title": "The Dark Knight",   "genre": "Action",   "duration": "2h 32m", "rating": "PG-13"},
    3: {"title": "Inception",         "genre": "Thriller", "duration": "2h 28m", "rating": "PG-13"},
    4: {"title": "Avengers: Endgame", "genre": "Action",   "duration": "3h 01m", "rating": "PG-13"},
}

show_timings = ["10:00 AM", "1:30 PM", "4:45 PM", "8:00 PM", "11:15 PM"]

seat_prices = {"Silver": 150, "Gold": 220, "Platinum": 350}

ROWS = ["A", "B", "C", "D", "E", "F", "G", "H"]
SEATS_PER_ROW = 10

# Initialize booked_seats exactly like your script
booked_seats = {mid: {t: set() for t in show_timings} for mid in movies}

def get_tier(row):
    if row in ["A", "B", "C"]: return "Silver"
    elif row in ["D", "E", "F"]: return "Gold"
    return "Platinum"

@app.route('/')
def index():
    return render_template('index.html', movies=movies, timings=show_timings, rows=ROWS, spr=SEATS_PER_ROW)

@app.route('/get_seats', methods=['POST'])
def get_seats():
    data = request.json
    mid, timing = int(data['mid']), data['timing']
    # Convert set to list for JSON compatibility
    return jsonify(list(booked_seats[mid][timing]))

@app.route('/book', methods=['POST'])
def book():
    data = request.json
    mid, timing = int(data['mid']), data['timing']
    selected = data['seats'] # List of seat IDs
    
    # 90% Success Rate Simulation
    success = random.randint(1, 10) <= 9
    if not success:
        return jsonify({"status": "fail", "message": "Payment Gateway Timeout!"})

    # Mark seats as booked
    for s in selected:
        booked_seats[mid][timing].add(s)
        
    booking_id = "BK" + str(random.randint(100000, 999999))
    return jsonify({"status": "success", "id": booking_id})

if __name__ == '__main__':
    app.run(debug=True)