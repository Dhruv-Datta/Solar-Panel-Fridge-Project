import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

# Constants
solar_panel_power = 350  # Watts
sunlight_hours = 5  # Hours
fridge_total_power = 100  # Watts
fridge_standby_power = 5 # Watts
startup_power = 500  # Watts
startup_duration = 5 / 3600  # hours
startups_per_day = 20  # Estimated number of compressor starts per day
fridge_hours = 24  # Hours
energy_loss = 0.8 # Percentage
duty_cycle = 0.4 # Percentage

steady_energy_consumed = ( (fridge_total_power * duty_cycle) + (fridge_standby_power * (1 - duty_cycle)) ) * fridge_hours  # Wh

startup_energy_consumed = startup_power * startup_duration * startups_per_day  # Wh

energy_consumed = steady_energy_consumed + startup_energy_consumed

# Simulation Parameters
total_days = 3
total_hours = total_days * 24
initial_battery_charge = 100  # Percent
battery_capacity = 1500  # Wh

# Battery charge over time
battery_charge = [initial_battery_charge]
battery_energy = (initial_battery_charge / 100) * battery_capacity  # Wh
net_change = []

# Generate a realistic sunlight (peak at noon)
sunlight_start = 10  # 10 AM
sunlight_end = 15  # 3 PM
peak_hour = (sunlight_start + sunlight_end) / 2
sunlight_profile = [
    max(0, np.exp(-0.5 * ((hour - peak_hour) / 1.75) ** 2) * solar_panel_power)
    for hour in range(24)
]

# Simulate battery charge
def get_energy_at_hour(hour):
    hour_of_day = hour % 24
    solar_energy = sunlight_profile[hour_of_day] * energy_loss
    net_energy = solar_energy - (energy_consumed / 24)
    return net_energy

for hour in range(1, total_hours + 1):
    net_energy = get_energy_at_hour(hour)
    net_change.append(net_energy)
    battery_energy += net_energy
    # Clamp battery energy within 0 and maximum capacity
    battery_energy = max(0, min(battery_energy, battery_capacity))
    # Convert to percentage
    battery_charge.append((battery_energy / battery_capacity) * 100)

# Visualization
start_time = datetime(2025, 1, 1, 0, 0)
hours = [start_time + timedelta(hours=i) for i in range(total_hours + 1)]
formatted_hours = [hour.strftime("%I:%M %p") for hour in hours]

# Plot battery charge with zoom-in functionality
plt.figure(figsize=(12, 6))
plt.plot(hours, battery_charge, label="Battery Charge", color="blue")
plt.axhline(100, color='green', linestyle='--', label="Full Charge")
plt.axhline(0, color='red', linestyle='--', label="Empty Battery")
plt.title(f"Battery Charge Over {total_days} Day(s)")
plt.xlabel("Time")
plt.ylabel("Battery Charge (%)")
plt.xticks(hours[::1], formatted_hours[::1], rotation=90)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 6))
plt.plot(hours[:-1], net_change, label="Net Energy Change", color="orange")
plt.axhline(0, color='black', linestyle='--', label="No Change")

# Add vertical lines for sunlight hours
for day in range(total_days):
    sunlight_start_time = start_time + timedelta(hours=(day * 24) + sunlight_start)
    sunlight_end_time = start_time + timedelta(hours=(day * 24) + sunlight_end)
    plt.axvline(sunlight_start_time, color='green', linestyle='--', label="Sunlight Start" if day == 0 else "")
    plt.axvline(sunlight_end_time, color='red', linestyle='--', label="Sunlight End" if day == 0 else "")

plt.title(f"Net Energy Change Over {total_days} Day(s)")
plt.xlabel("Time")
plt.ylabel("Net Energy Change (Wh)")
plt.xticks(hours[::1], formatted_hours[::1], rotation=90)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.show()


# Calculate positive and negative area under the net change to find out the total energy gained and lost
# over the simulation period, helping determine whether the battery will sustain its charge or eventually deplete.

positive_area = 0
negative_area = 0

for i in range(1, len(net_change)):
    # Trapezoidal area for each segment (between i-1 and i)
    area = (net_change[i] + net_change[i-1]) / 2
    time_diff = (hours[i] - hours[i-1]).total_seconds() / 3600
    
    if area > 0:
        positive_area += area * time_diff
    elif area < 0:
        negative_area += area * time_diff

cumulative_area = positive_area + negative_area

print(f"Total Positive Area: {positive_area:.2f} Wh")
print(f"Total Negative Area: {negative_area:.2f} Wh")
print(f"Total Area (Positive + Negative): {cumulative_area:.2f} Wh")

if cumulative_area < 0:
    print(f'The battery will eventually die.')
else:
    print(f'The battery will not die!\n')

# Debugging
print(f'Fridge Energy Consumed: {energy_consumed:.2f} Wh')


