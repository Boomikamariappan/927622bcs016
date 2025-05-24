from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import numpy as np

app = Flask(_name_)


def fetch_stock_price_history(ticker):
    now = datetime.utcnow()
    example_data = {
        "NVDA": [
            {"price": 231.95296, "lastUpdatedAt": (now - timedelta(minutes=35)).isoformat()},
            {"price": 124.95156, "lastUpdatedAt": (now - timedelta(minutes=30)).isoformat()},
            {"price": 459.09558, "lastUpdatedAt": (now - timedelta(minutes=20)).isoformat()},
            {"price": 998.27924, "lastUpdatedAt": (now - timedelta(minutes=10)).isoformat()},
        ],
        "PYPL": [
            {"price": 688.59766, "lastUpdatedAt": (now - timedelta(minutes=40)).isoformat()},
            {"price": 450.0, "lastUpdatedAt": (now - timedelta(minutes=30)).isoformat()},
            {"price": 300.0, "lastUpdatedAt": (now - timedelta(minutes=15)).isoformat()},
        ],
    }
    return example_data.get(ticker.upper(), [])

def parse_iso_datetime(s):
    return datetime.fromisoformat(s)

def filter_prices_last_mins(price_history, minutes):
    cutoff = datetime.utcnow() - timedelta(minutes=minutes)
    filtered = [
        p for p in price_history if parse_iso_datetime(p["lastUpdatedAt"]) >= cutoff
    ]
    return filtered

def average_price(prices):
    if not prices:
        return 0.0
    return round(sum(p["price"] for p in prices) / len(prices), 6)

def align_price_series(prices1, prices2):
    
    dict1 = {p["lastUpdatedAt"]: p["price"] for p in prices1}
    dict2 = {p["lastUpdatedAt"]: p["price"] for p in prices2}
    common_times = sorted(set(dict1.keys()) & set(dict2.keys()))
    aligned1 = [dict1[t] for t in common_times]
    aligned2 = [dict2[t] for t in common_times]
    return aligned1, aligned2

@app.route("/stocks/<ticker>")
def average_stock_price(ticker):
    minutes = request.args.get("minutes", type=int)
    aggregation = request.args.get("aggregation", default="average")

    if minutes is None or minutes <= 0:
        return jsonify({"error": "Invalid or missing 'minutes' query parameter"}), 400
    if aggregation != "average":
        return jsonify({"error": f"Aggregation '{aggregation}' not supported"}), 400

    price_history = fetch_stock_price_history(ticker)
    filtered_history = filter_prices_last_mins(price_history, minutes)
    avg = average_price(filtered_history)

    return jsonify({
        "averageStockPrice": avg,
        "priceHistory": filtered_history
    })

@app.route("/stockcorrelation")
def stock_correlation():
    minutes = request.args.get("minutes", type=int)
    tickers = request.args.getlist("ticker")

    if minutes is None or minutes <= 0:
        return jsonify({"error": "Invalid or missing 'minutes' query parameter"}), 400
    if len(tickers) != 2:
        return jsonify({"error": "Exactly two 'ticker' query parameters required"}), 400

    t1, t2 = tickers
    ph1 = filter_prices_last_mins(fetch_stock_price_history(t1), minutes)
    ph2 = filter_prices_last_mins(fetch_stock_price_history(t2), minutes)

    aligned1, aligned2 = align_price_series(ph1, ph2)

    if len(aligned1) < 2:
        return jsonify({"error": "Not enough overlapping data points for correlation"}), 400

    correlation = np.corrcoef(aligned1, aligned2)[0, 1]
    correlation = round(float(correlation), 4)

    response = {
        "correlation": correlation,
        "stocks": {
            t1.upper(): {
                "averagePrice": average_price(ph1),
                "priceHistory": ph1
            },
            t2.upper(): {
                "averagePrice": average_price(ph2),
                "priceHistory": ph2
            }
        }
    }

    return jsonify(response)

if _name_ == "_main_":
    app.run(debug=True)