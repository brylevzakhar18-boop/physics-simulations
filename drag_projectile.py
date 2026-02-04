import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ---------------- SETTINGS ----------------
MODE = "ANIM"            # "STATIC" or "ANIM"
v0 = 20.0                # m/s
g = 9.81                 # m/s^2

angles_deg = [30, 45, 60]   # for STATIC
anim_angle_deg = 45         # for ANIM
N = 300                     # points/frames
# ------------------------------------------


def compute_trajectory(v0, angle_deg, g, N):
    theta = np.deg2rad(angle_deg)

    t_flight = 2 * v0 * np.sin(theta) / g
    t = np.linspace(0, t_flight, N)

    x = v0 * np.cos(theta) * t
    y = v0 * np.sin(theta) * t - 0.5 * g * t**2

    range_x = v0 * np.cos(theta) * t_flight
    y_max = (v0**2 * np.sin(theta)**2) / (2 * g)

    return t, x, y, t_flight, range_x, y_max


def plot_angles(v0, angles_deg, g, N):
    plt.figure()

    for angle in angles_deg:
        t, x, y, t_flight, range_x, y_max = compute_trajectory(v0, angle, g, N)
        plt.plot(x, y, label=f"{angle}° (R={range_x:.2f} m)")

    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.title("Projectile trajectories for different angles")
    plt.legend()
    plt.grid(True)
    plt.show()


def animate(v0, angle_deg, g, N):
    t, x, y, t_flight, range_x, y_max = compute_trajectory(v0, angle_deg, g, N)

    print(f"Angle = {angle_deg}°")
    print(f"Time of flight = {t_flight:.3f} s")
    print(f"Range = {range_x:.3f} m")
    print(f"Max height = {y_max:.3f} m")

    fig, ax = plt.subplots()
    ax.set_xlim(0, max(x) * 1.05)
    ax.set_ylim(0, max(y) * 1.10)
    ax.set_title(f"2D Projectile Motion ({angle_deg}°)")
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.grid(True)

    point, = ax.plot([], [], "ro")
    trail, = ax.plot([], [], "-", lw=2)

    def init():
        point.set_data([], [])
        trail.set_data([], [])
        return point, trail

    def update(frame):
        point.set_data([x[frame]], [y[frame]])
        trail.set_data(x[:frame+1], y[:frame+1])
        return point, trail

    _ = FuncAnimation(fig, update, frames=len(t), init_func=init, interval=30, blit=True)
    plt.show()


if __name__ == "__main__":
    if MODE == "STATIC":
        plot_angles(v0, angles_deg, g, N)
    elif MODE == "ANIM":
        animate(v0, anim_angle_deg, g, N)
    else:
        print("Unknown MODE. Use 'STATIC' or 'ANIM'.")
