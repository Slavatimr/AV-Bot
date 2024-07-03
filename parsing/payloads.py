data = {"year": "год", "price": "цену", "engine_capacity": "объем"}


class Payload:

    def __init__(self):
        self.transmission_type = self.year_min = self.year_max = self.price_min = self.price_max = None
        self.capacity_min = self.capacity_max = None
        self.result_payload = None

    def self_check(self):
        for key, value in self.result_payload.items():
            if value == "":
                self.result_payload[key] = None

    def payload(self):

        self.result_payload = {"transmission_type": self.transmission_type,
                               "year[min]": self.year_min,
                               "year[max]": self.year_max,
                               "price_usd[min]": self.price_min,
                               "price_usd[max]": self.price_max,
                               "engine_capacity[min]": self.capacity_min,
                               "engine_capacity[max]": self.capacity_max}

        self.self_check()
        return self.result_payload
