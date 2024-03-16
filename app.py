from flask import Flask, request, jsonify
from datetime import datetime
import pytz

app = Flask(__name__)

from flask import Flask, request, jsonify
from datetime import datetime
import pytz

app = Flask(__name__)

# Constants
BASE_DELIVERY_FEE = 200 
SMALL_ORDER_THRESHOLD = 1000
ADDITIONAL_DISTANCE_FEE = 100
BULK_ORDER_THRESHOLD = 5
BULK_ORDER_SURCHARGE = 50
EXTRA_BULK_FEE = 120
MAX_DELIVERY_FEE = 1500
FREE_DELIVERY_THRESHOLD = 20000
FRIDAY_RUSH_MULTIPLIER = 1.2
FRIDAY_RUSH_START = 15
FRIDAY_RUSH_END = 19

@app.route('/')

def index():
    return "Welcome to the Delivery Fee Calculator API!"

def calculate_delivery_fee(cart_value, delivery_distance, number_of_items, time):

    delivery_fee = BASE_DELIVERY_FEE
    delivery_fee += calculate_small_order_surcharge(cart_value)
    delivery_fee += calculate_additional_distance_fee(delivery_distance)
    delivery_fee += calculate_bulk_order_surcharge(number_of_items)
    delivery_fee = apply_friday_rush_fee(delivery_fee, time)
    delivery_fee = min(delivery_fee, MAX_DELIVERY_FEE)
    if cart_value >= FREE_DELIVERY_THRESHOLD:
        return 0
    return delivery_fee

def calculate_small_order_surcharge(cart_value): # calculate surcharge for small orders
    if cart_value < SMALL_ORDER_THRESHOLD:
        return SMALL_ORDER_THRESHOLD - cart_value
    return 0

def calculate_additional_distance_fee(delivery_distance): # calculate surcharge for additional distance
    if delivery_distance > 1000:
        additional_distance = delivery_distance - 1000
        fee = (additional_distance // 500) * ADDITIONAL_DISTANCE_FEE
        if additional_distance % 500 > 0:
            fee += ADDITIONAL_DISTANCE_FEE
        return fee
    return 0

def calculate_bulk_order_surcharge(number_of_items): # calculate surcharge for a bulk order
    if number_of_items >= BULK_ORDER_THRESHOLD:
        additional_items = number_of_items - 4
        fee = additional_items * BULK_ORDER_SURCHARGE
        if number_of_items > 12:
            fee += EXTRA_BULK_FEE
        return fee
    return 0

def apply_friday_rush_fee(delivery_fee, time): # apply Friday rush multiplier 
    utc_time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.utc)
    if utc_time.weekday() == 4 and FRIDAY_RUSH_START <= utc_time.hour < FRIDAY_RUSH_END:
        return round(delivery_fee * FRIDAY_RUSH_MULTIPLIER)
    return delivery_fee


@app.route('/calculate_delivery_fee', methods=['POST'])

def calculate_fee():
    data = request.json
    fee = calculate_delivery_fee(
        cart_value=data['cart_value'], 
        delivery_distance=data['delivery_distance'], 
        number_of_items=data['number_of_items'], 
        time=data['time']
    )
    return jsonify({'delivery_fee': fee})

if __name__ == '__main__':
    app.run(debug=True)
