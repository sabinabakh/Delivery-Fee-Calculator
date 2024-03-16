# Delivery Fee Calculator API

This Python project is an HTTP API developed using Flask. It calculates the delivery fee for an online grocery shop based on the cart value, the number of items in the cart, the time of the order, and the delivery distance.


Features
Calculation of delivery fee based on cart value, item count, order time, and delivery distance.
Implementation of surcharges for small orders and bulk orders.
Special pricing adjustments during Friday rush hours.
Limitations on maximum delivery fee and free delivery for large cart values.

## Technologies
* Python 3.9.18 or later
* Flask 3.0.1
* pytz 2023.4

## Setup

1. Set up a virtual environment in the root directory of the project and activate it:
    
    For Windows:
    ``` sh
    python -m venv venv
    venv\Scripts\activate
    ```
    For macOS and Linux:
    ``` sh
    python3 -m venv venv
    source venv/bin/activate
    ```

2. Install dependencies:

    ``` sh
    pip install -r requirements.txt
    ```  

## Runing the Application

1. Start the Flask application:
    
    ``` sh
    python app.py
    ```  

2. Access the API:

    After starting the Flask application the API should be accessible at http://127.0.0.1:5000/.
    You can interact with the API endpoints using tools like Postman or cURL from the command line. The primary endpoint for calculating delivery fees is /calculate_delivery_fee.

    Sending a POST request to /calculate_delivery_fee via command line:

    ``` sh
    curl -X POST http://127.0.0.1:5000/calculate_delivery_fee \
    -H "Content-Type: application/json" \
    -d '{"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-15T13:00:00Z"}'
    ```  



## Testing

Run the tests to ensure the application is working as expected:

``` sh
python -m unittest
```  


