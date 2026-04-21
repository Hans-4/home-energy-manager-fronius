# Energy Manager Fronius

**Python package for reading from Fronius devices**

## Supported devices

| Device          | Verification              | Script  | Url |
|-----------------|---------------------------|---------|-----|
| Symo 10.0-3-M   | self tested               | symo.py | /   |
| Symo 3.0 - 20.0 | should work / not testet  | symo.py | /   |

## Installation

```bash
pip install home-energy-manager-fronius
```

## Usage

```python
from fronius.symo import FroniusSymoApi

device = FroniusSymoApi(ip="192.168.178.20", feed_in_tariff=0.12)

current_production, current_grid_usage, current_load, daily_production, daily_revenue, yearly_production, yearly_revenue, total_production, total_revenue = device.run_fronius()

print(current_production, current_grid_usage, current_load, daily_production, daily_revenue, yearly_production, yearly_revenue, total_production, total_revenue)
```