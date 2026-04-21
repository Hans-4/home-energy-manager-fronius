import requests


class FroniusSymoApi:
    def __init__(self, ip, feed_in_tariff):
        self.ip = ip
        self.feed_in_tariff = feed_in_tariff #Feed in tariff in cent
        self.last_values = {}
        self.solar_values = []

    @staticmethod
    def get_nested_value(data, *keys):
        for key in keys:
            if isinstance(data, dict) and key in data:
                data = data[key]
            else:
                return None
        return data

    def _revenue_calculation(self, power_value):
        if power_value is None:
            return "0.00"
        revenue = (float(power_value) / 1000) * self.feed_in_tariff
        return f"{revenue:.2f}"

    def get_data(self, data):
        #get the data in watts
        values = {
            'current_production': self.get_nested_value(data, 'Body', 'Data', 'Inverters', '1', 'P'),
            'daily_production': self.get_nested_value(data, 'Body', 'Data', 'Inverters', '1', 'E_Day'),
            'yearly_production': self.get_nested_value(data, 'Body', 'Data', 'Inverters', '1', 'E_Year'),
            'total_production': self.get_nested_value(data, 'Body', 'Data', 'Inverters', '1', 'E_Total'),
            'current_grid_usage': self.get_nested_value(data, 'Body', 'Data', 'Site', 'P_Grid'),
            'current_load': self.get_nested_value(data, 'Body', 'Data', 'Site', 'P_Load')
        }

        current_production = values['current_production'] if values['current_production'] is not None else 0
        current_grid_usage = values['current_grid_usage'] if values['current_grid_usage'] is not None else 0
        current_load = values['current_load'] if values['current_load'] is not None else 0
        daily_production = values['daily_production'] if values['daily_production'] is not None else 0
        yearly_production = values['yearly_production'] if values['yearly_production'] is not None else 0
        total_production = values['total_production'] if values['total_production'] is not None else 0

        daily_revenue = self._revenue_calculation(daily_production)
        yearly_revenue = self._revenue_calculation(yearly_production)
        total_revenue = self._revenue_calculation(total_production)

        self.solar_values = [
            current_production,
            current_grid_usage,
            current_load,
            daily_production,
            float(daily_revenue),
            yearly_production,
            float(yearly_revenue),
            total_production,
            float(total_revenue),
        ]

    def run_fronius(self):
        if not self.ip:
            print("FRONIUS_SOLAR_SYSTEM_IP is not set")
            return []

        url = f'http://{self.ip}/solar_api/v1/GetPowerFlowRealtimeData.fcgi'

        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.get_data(data)
                return self.solar_values
            else:
                print(f"Error fetching data: {response.status_code}")
                return []
        except requests.exceptions.RequestException as e:
            print(f"Connection error: {e}")
            return []