import random
class Results:
    def __init__(self):
        self.history = []

    def generate_results(self, driver_name, car_name):
        won = random.random() < 0.8
        prize = 500 if won else 0
        car_damaged = not won and random.random() < 0.5
        
        result = {
            "driver": driver_name,
            "car": car_name,
            "won": won,
            "prize": prize,
            "car_damaged": car_damaged
        }
        self.history.append(result)
        return result

    def list_results(self):
        return self.history
