import unittest
import json
from app import app

class test_delivery_fee_for_additional_distance(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_additonal_distance_1(self):
        response = self.app.post('/calculate_delivery_fee', data=json.dumps({
            'cart_value': 1000,
            'delivery_distance': 1499, 
            'number_of_items': 3, 
            'time': '2024-01-15T13:00:00Z'
        }), content_type='application/json')

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['delivery_fee'], 300)  # 2€ base fee + 1€ for the additional 500 m
    
    def test_additional_distance_2(self):
        response = self.app.post('/calculate_delivery_fee', data=json.dumps({
            'cart_value': 1000, 
            'delivery_distance': 1500, 
            'number_of_items': 2, 
            'time': '2024-01-15T13:00:00Z'
        }), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['delivery_fee'], 300)  # 2€ base fee + 1€ for the additional 500 m

    def test_additional_distance_3(self):
        response = self.app.post('/calculate_delivery_fee', data=json.dumps({
            'cart_value': 1000,
            'delivery_distance': 1501, 
            'number_of_items': 1, 
            'time': '2024-01-15T13:00:00Z'
        }), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['delivery_fee'], 400)  # 2€ base fee + 1€ for the first 500 m + 1€ for the second 500 m 

    def test_additional_distance_complex_1(self):
        response = self.app.post('/calculate_delivery_fee', data=json.dumps({
            'cart_value': 800,
            'delivery_distance': 1500, 
            'number_of_items': 1, 
            'time': '2024-01-15T13:00:00Z'
        }), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['delivery_fee'], 500)  # 2€ base fee + 1€ for the first 500 m + 2€ surcharge
    
    def test_additional_distance_complex_2(self):
        response = self.app.post('/calculate_delivery_fee', data=json.dumps({
            'cart_value': 888,
            'delivery_distance': 2000, 
            'number_of_items': 5, 
            'time': '2024-01-15T13:00:00Z'
        }), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['delivery_fee'], 562)  # 2€ base fee + 1€ for the first 500 m + 1€ for the second 500 m + 50 cent surcharge + 1.12€ surcharge


class test_basic_delivery_fee(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_basic_deivery_fee_1(self):
        response = self.app.post('/calculate_delivery_fee', data=json.dumps({
            'cart_value': 1500, 
            'delivery_distance': 900, 
            'number_of_items': 3, 
            'time': '2024-01-15T13:00:00Z'
        }), content_type='application/json')

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['delivery_fee'], 200)  # €2 base fee
    
    def test_basic_deivery_fee_2(self):
        response = self.app.post('/calculate_delivery_fee', data=json.dumps({
            'cart_value': 2000, 
            'delivery_distance': 200, 
            'number_of_items': 3, 
            'time': '2024-01-15T13:00:00Z'
        }), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['delivery_fee'], 200)  # 2€ base fee


class test_small_order_delivery_fee(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_small_order_fee_1(self):
        response = self.app.post('/calculate_delivery_fee', data=json.dumps({
            'cart_value': 890, 
            'delivery_distance': 1000, 
            'number_of_items': 3, 
            'time': '2024-01-15T13:00:00Z'
        }), content_type='application/json')

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['delivery_fee'], 310)  # €2 base fee + 1.10€ surcharge
    
    def test_small_order_fee_2(self):
        response = self.app.post('/calculate_delivery_fee', data=json.dumps({
            'cart_value': 800, 
            'delivery_distance': 1000, 
            'number_of_items': 3, 
            'time': '2024-01-15T13:00:00Z'
        }), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['delivery_fee'], 400)  # 2€ base fee + 2€ surcharge

    def test_small_order_fee_complex(self):
        response = self.app.post('/calculate_delivery_fee', data=json.dumps({
            'cart_value': 733,
            'delivery_distance': 1500, 
            'number_of_items': 13, 
            'time': '2024-01-15T13:00:00Z'
        }), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['delivery_fee'], 1137)  # 2€ base fee + 2.67€ surcharge + 1€ for the first 500 m + 5,70€ surcharge


class test_bulk_order_delivery_fee(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_bult_order_1(self):
        response = self.app.post('/calculate_delivery_fee', data=json.dumps({
            'cart_value': 1000, 
            'delivery_distance': 1000, 
            'number_of_items': 5, 
            'time': '2024-01-15T13:00:00Z'
        }), content_type='application/json')

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['delivery_fee'], 250)  # 2€ base fee + 50 cent surcharge

    def test_bult_order_2(self):
        response = self.app.post('/calculate_delivery_fee', data=json.dumps({
            'cart_value': 1000, 
            'delivery_distance': 1000, 
            'number_of_items': 4, 
            'time': '2024-01-15T13:00:00Z'
        }), content_type='application/json')

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['delivery_fee'], 200)  # 2€ base fee + no surcharge

    def test_bult_order_3(self):
        response = self.app.post('/calculate_delivery_fee', data=json.dumps({
            'cart_value': 1000, 
            'delivery_distance': 1000, 
            'number_of_items': 10, 
            'time': '2024-01-15T13:00:00Z'
        }), content_type='application/json')

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['delivery_fee'], 500)  # 2€ base fee + 3€ surcharge
    
    def test_delivery_fee_for_more_than_12_items_1(self):
        response = self.app.post('/calculate_delivery_fee', data=json.dumps({
            'cart_value': 1000, 
            'delivery_distance': 1000, 
            'number_of_items': 13, 
            'time': '2024-01-15T13:00:00Z'
        }), content_type='application/json')

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['delivery_fee'], 770)  # 2€ base fee + 5,70€ surcharge
   
    def test_delivery_fee_for_more_than_12_items_2(self):
        response = self.app.post('/calculate_delivery_fee', data=json.dumps({
            'cart_value': 1000, 
            'delivery_distance': 1000, 
            'number_of_items': 14, 
            'time': '2024-01-15T13:00:00Z'
        }), content_type='application/json')

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['delivery_fee'], 820)  # 2€ base fee + 6,20€ surcharge


class test_maximum_delivery_fee(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_maximum_fee_1(self):
        response = self.app.post('/calculate_delivery_fee', data=json.dumps({
            'cart_value': 200,
            'delivery_distance': 2000, 
            'number_of_items': 10, 
            'time': '2024-01-15T16:00:00Z'
        }), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['delivery_fee'], 1500)  # (2€ base fee + 1€ for the first 500 m + 1€ for the second 500 m + 3€ surcharge + 8€ surcharge) * 1.2
    
    def test_maximum_fee_2(self):
        response = self.app.post('/calculate_delivery_fee', data=json.dumps({
            'cart_value': 200,
            'delivery_distance': 2000, 
            'number_of_items': 10, 
            'time': '2024-01-15T13:00:00Z'
        }), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['delivery_fee'], 1500)  # 2€ base fee + 1€ for the first 500 m + 1€ for the second 500 m + 3€ surcharge + 8€ surcharge


class test_free_delivery(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_free_delivery(self):
        response = self.app.post('/calculate_delivery_fee', data=json.dumps({
            'cart_value': 20000, 
            'delivery_distance': 2235, 
            'number_of_items': 4, 
            'time': '2024-01-15T13:00:00Z'
        }), content_type='application/json') 

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['delivery_fee'], 0)  # Expected delivery fee

class test_Friday_rush(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_Friday_rush(self):
        response = self.app.post('/calculate_delivery_fee', data=json.dumps({
            'cart_value': 1000, 
            'delivery_distance': 1000, 
            'number_of_items': 4, 
            'time': '2024-01-26T15:00:00Z'
        }), content_type='application/json') 

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['delivery_fee'], 240)  # 2€ base fee * 1.2

    def test_Friday_rush_complex_1(self):
        response = self.app.post('/calculate_delivery_fee', data=json.dumps({
            'cart_value': 800, 
            'delivery_distance': 1000, 
            'number_of_items': 4, 
            'time': '2024-01-26T15:00:00Z'
        }), content_type='application/json') 

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['delivery_fee'], 480)  # (2€ base fee + 2€ surcharge) * 1.2

    def test_Friday_rush_complex_2(self):
        response = self.app.post('/calculate_delivery_fee', data=json.dumps({
            'cart_value': 1000, 
            'delivery_distance': 1499, 
            'number_of_items': 4, 
            'time': '2024-01-26T17:00:00Z'
        }), content_type='application/json') 

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['delivery_fee'], 360)  # (2€ base fee + 1€ for the additional 500 m) * 1.2

    def test_Friday_rush_complex_3(self):
        response = self.app.post('/calculate_delivery_fee', data=json.dumps({
            'cart_value': 700, 
            'delivery_distance': 1499, 
            'number_of_items': 4, 
            'time': '2024-01-26T16:00:00Z'
        }), content_type='application/json') 

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['delivery_fee'], 720)  # (2€ base fee + 1€ for the additional 500 m + 3€ surcharge) * 1.2

    def test_Friday_rush_complex_4(self):
        response = self.app.post('/calculate_delivery_fee', data=json.dumps({
            'cart_value': 664, 
            'delivery_distance': 1499, 
            'number_of_items': 4, 
            'time': '2024-01-26T15:00:00Z'
        }), content_type='application/json') 

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['delivery_fee'], 763)  # (2€ base fee + 1€ for the additional 500 m + 3,36€ surcharge) * 1.2 


if __name__ == '__main__':
    unittest.main()
