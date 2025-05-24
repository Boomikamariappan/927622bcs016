from flask import Flask, jsonify, request
import requests
import time
from collections import deque

app = Flask(_name_)


id = {'p', 'f', 'e', 'r'}
window_size= 10
api_url = "http://127.0.0.1:5001/test" 
number_window = deque(maxlen=window_size)

def average(nums):
    return round(sum(nums) / len(nums), 2) if nums else 0.0

def fetch_numbers(numberid):
    url = f"{api_url}/numbers/{numberid}"
    try:
        response = requests.get(url, timeout=0.5)
        response.raise_for_status()
        data = response.json()
        return data.get("numbers", [])
    except requests.RequestException:
        return []

@app.route("/numbers/<numberid>", methods=["GET"])
def numbers_handler(numberid):
    if numberid not in id:
        return jsonify({"error": "Invalid number ID"}), 400

    prev_state = list(number_window)
    start = time.time()
    fetched = fetch_numbers(numberid)
    elapsed = (time.time() - start) * 1000

  
    if elapsed > 500:
        return jsonify({"error": "Timeout while fetching numbers"}), 504

    
    for num in fetched:
        if num not in number_window:
            number_window.append(num)

    curr_state = list(number_window)

    return jsonify({
        "windowPrevState": prev_state,
        "windowCurrState": curr_state,
        "numbers": fetched,
        "avg": average(curr_state)
    })

if _name_ == "_main_":
    app.run(debug=True)