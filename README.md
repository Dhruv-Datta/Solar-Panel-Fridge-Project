# Solar-Panel-Fridge-Project

I wanted to understand how the power generation and consumption would work with the solar panel cooling system. To do this I simulated the energy dynamics of a solar-powered fridge system over a given period, tracking the charge of the battery as it is impacted by solar energy generation and energy consumption by the fridge. Here is the details of how it works:

Energy Generation: The solar panel system generates energy based on its power rating (in my example it is 350W), the number of sunlight hours available per day (5 hours is standard), and efficiency losses (20%). The energy produced by the solar panel each day is calculated using the formula:

Energy Generated = Solar Panel Power × Sunlight Hours × Efficiency Loss

Energy Consumption: The fridge consumes energy at a varying rate due to its duty cycle, where the compressor runs for a certain percentage of the time (40% in this case), and the rest of the time it draws standby power. The total energy consumed by the fridge, including startup energy from the compressor, is calculated as:

Energy Consumed = ( ( Total Power Consumption × Duty Cycle ) + ( Standby Power Consumption × ( 1 − Duty Cycle) ) ) × Hours of Use

Battery Charge Simulation: The code simulates the change in the battery's charge over time. It keeps track of the energy generated by the solar panel and the energy consumed by the fridge. The battery charge is updated hourly, and its energy content is clamped within the range of 0% to 100% to ensure the system does not exceed its capacity or discharge too far.

Sunlight Profile: The energy generated by the solar panel is modeled to vary throughout the day, with higher output around noon (using a Gaussian-like curve), which provides a more realistic representation of solar energy availability.

Net Energy Change: The net energy change is calculated for each hour by subtracting the energy consumed from the energy generated by the solar panel. This allows us to see whether the system is charging the battery or discharging it during different times of the day.

Visualization: The results are plotted to visualize the battery charge over time and the net energy change over the simulation period. This helps understand how effectively the solar panel is charging the battery and whether the system is sustainable over the period in question.

Energy Balance and Decision: Lastly, the code calculates the positive and negative areas under the net energy curve (representing energy gained and lost, respectively). If the cumulative area is negative, it indicates the battery will eventually be depleted, meaning the system is not self-sustaining. If it is positive, the system is viable, and the battery will stay charged.

This code is essential for evaluating whether a solar-powered fridge system can be sustainable and off-grid by accounting for energy generation, consumption, and the dynamics of battery charging. It helps optimize the design by considering factors like duty cycles, sunlight variability, and energy losses.

