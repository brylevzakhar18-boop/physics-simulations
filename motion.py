"""
Kinematic Motion Simulation
Models 1D motion with constant acceleration.
"""

g = 9.81      # acceleration (m/s^2)
dt = 0.05     # time step
t = 0

velocity = 0
position = 0

time_data = []
position_data = []
velocity_data = []

while t <= 10:
    time_data.append(t)
    position_data.append(position)
    velocity_data.append(velocity)

    velocity += g * dt
    position += velocity * dt
    t += dt

print("Simulation finished.")
print("Final position:", round(position, 2), "meters")
