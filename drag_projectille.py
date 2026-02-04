import numpy as np
import matplotlib.pyplot as plt

# -----------------------
# SETTINGS
# -----------------------
g = 9.81

v0 = 25.0               # m/s
angle_deg = 45.0        # degrees

dt = 0.002              # time step (smaller = smoother, slower)
t_max = 20.0            # safety cap

k_quad = 0.020          # quadratic drag strength (1/m)
# попробуй 0.005, 0.01, 0.02, 0.05

# -----------------------
# Helpers
# -----------------------
def simulate_no_drag(v0, angle_deg, dt):
    theta = np.deg2rad(angle_deg)
    vx0 = v0 * np.cos(theta)
    vy0 = v0 * np.sin(theta)

    x, y = 0.0, 0.0
    vx, vy = vx0, vy0

    xs, ys, ts, speeds = [x], [y], [0.0], [np.hypot(vx, vy)]

    t = 0.0
    while t < t_max:
        # update
        x += vx * dt
        y += vy * dt
        vy += -g * dt
        t += dt

        xs.append(x)
        ys.append(y)
        ts.append(t)
        speeds.append(np.hypot(vx, vy))

        if y < 0 and t > dt:
            break

    xs = np.array(xs); ys = np.array(ys); ts = np.array(ts); speeds = np.array(speeds)
    return ts, xs, ys, speeds


def simulate_quadratic_drag(v0, angle_deg, k, dt):
    theta = np.deg2rad(angle_deg)
    vx = v0 * np.cos(theta)
    vy = v0 * np.sin(theta)

    x, y = 0.0, 0.0

    xs, ys, ts, speeds = [x], [y], [0.0], [np.hypot(vx, vy)]

    t = 0.0
    while t < t_max:
        v = np.hypot(vx, vy)

        # acceleration with quadratic drag: a = -k * |v| * v_vector
        ax = -k * v * vx
        ay = -g - k * v * vy

        # Euler step
        vx += ax * dt
        vy += ay * dt
        x += vx * dt
        y += vy * dt

        t += dt

        xs.append(x)
        ys.append(y)
        ts.append(t)
        speeds.append(np.hypot(vx, vy))

        if y < 0 and t > dt:
            break

    xs = np.array(xs); ys = np.array(ys); ts = np.array(ts); speeds = np.array(speeds)
    return ts, xs, ys, speeds


def flight_stats(ts, xs, ys):
    # estimate landing (when y crosses 0)
    # last point may be below 0 -> interpolate for better range/time
    if len(ys) < 2:
        return 0.0, 0.0, 0.0

    y1, y2 = ys[-2], ys[-1]
    x1, x2 = xs[-2], xs[-1]
    t1, t2 = ts[-2], ts[-1]

    if y2 == y1:
        t_land, x_land = t2, x2
    else:
        alpha = (0 - y1) / (y2 - y1)   # between 0..1
        alpha = np.clip(alpha, 0, 1)
        t_land = t1 + alpha * (t2 - t1)
        x_land = x1 + alpha * (x2 - x1)

    y_max = float(np.max(ys))
    return float(x_land), float(t_land), y_max


# -----------------------
# Run simulations
# -----------------------
ts0, xs0, ys0, sp0 = simulate_no_drag(v0, angle_deg, dt)
tsd, xsd, ysd, spd = simulate_quadratic_drag(v0, angle_deg, k_quad, dt)

R0, T0, H0 = flight_stats(ts0, xs0, ys0)
Rd, Td, Hd = flight_stats(tsd, xsd, ysd)

print("=== RESULTS ===")
print(f"No drag:     range={R0:.2f} m, flight time={T0:.2f} s, max height={H0:.2f} m")
print(f"Quad drag k={k_quad:.3f}: range={Rd:.2f} m, flight time={Td:.2f} s, max height={Hd:.2f} m")

# -----------------------
# Plots
# -----------------------
plt.figure()
plt.plot(xs0, ys0, label="No drag")
plt.plot(xsd, ysd, label=f"With drag (QUAD), k={k_quad:.3f}")
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.title(f"Projectile trajectory (v0={v0:.1f} m/s, angle={angle_deg:.1f}°)")
plt.grid(True)
plt.legend()
plt.show()

plt.figure()
plt.plot(ts0, sp0, label="No drag")
plt.plot(tsd, spd, label=f"With drag (QUAD), k={k_quad:.3f}")
plt.xlabel("time (s)")
plt.ylabel("speed |v| (m/s)")
plt.title("Speed vs time")
plt.grid(True)
plt.legend()
plt.show()
