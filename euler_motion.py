import numpy as np
import matplotlib.pyplot as plt

# =========================
# PARAMETERS
# =========================
g = 9.81          # m/s^2
x0 = 0.0          # initial position (m)
v0 = 10.0         # initial velocity (m/s)

dt = 0.01         # time step (s)
t_max = 2.0       # simulation time (s)

# =========================
# TIME ARRAY
# =========================
t = np.arange(0, t_max + dt, dt)

# =========================
# ANALYTICAL SOLUTION
# =========================
x_exact = x0 + v0 * t - 0.5 * g * t**2

# =========================
# EULER METHOD
# =========================
x_euler = np.zeros_like(t)
v = v0

x_euler[0] = x0

for i in range(1, len(t)):
    v = v - g * dt
    x_euler[i] = x_euler[i-1] + v * dt

# =========================
# ERROR
# =========================
error_euler = np.abs(x_euler - x_exact)

# =========================
# PLOTS
# =========================
plt.figure()
plt.plot(t, x_exact, label="Analytical")
plt.plot(t, x_euler, "--", label="Euler")
plt.xlabel("Time (s)")
plt.ylabel("Position (m)")
plt.title("Free fall: Euler vs Analytical")
plt.grid(True)
plt.legend()

plt.figure()
plt.plot(t, error_euler, label="Euler error")
plt.xlabel("Time (s)")
plt.ylabel("Absolute error (m)")
plt.title("Euler method error growth")
plt.grid(True)
plt.legend()

plt.show()
