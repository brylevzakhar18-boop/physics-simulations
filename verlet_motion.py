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
# VERLET METHOD
# =========================
x_verlet = np.zeros_like(t)
x_verlet[0] = x0

# first step from Taylor expansion
x_verlet[1] = x0 + v0 * dt - 0.5 * g * dt**2

for i in range(1, len(t) - 1):
    x_verlet[i+1] = 2*x_verlet[i] - x_verlet[i-1] - g * dt**2

# =========================
# ERRORS
# =========================
error_euler = np.abs(x_euler - x_exact)
error_verlet = np.abs(x_verlet - x_exact)

# =========================
# PLOTS
# =========================
plt.figure()
plt.plot(t, x_exact, label="Analytical")
plt.plot(t, x_euler, "--", label="Euler")
plt.plot(t, x_verlet, ":", label="Verlet")
plt.xlabel("Time (s)")
plt.ylabel("Position (m)")
plt.title("Free fall: Analytical vs Euler vs Verlet")
plt.grid(True)
plt.legend()

plt.figure()
plt.plot(t, error_euler, label="Euler error")
plt.plot(t, error_verlet, label="Verlet error")
plt.xlabel("Time (s)")
plt.ylabel("Absolute error (m)")
plt.title("Numerical error comparison")
plt.grid(True)
plt.legend()

plt.show()
