import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.colors as mcolors
from matplotlib.widgets import Slider, Button, TextBox

# Физические параметры
size = 200
dx = 0.01
base_dt = 0.01

# Материалы
materials = {
    0: {'density': 8960, 'specific_heat': 385, 'conductivity': 401},
    1: {'density': 2700, 'specific_heat': 900, 'conductivity': 237}
}

# Инициализация сеток
initial_grid = np.full((size, size), 293.15)
material_mask = np.full((size, size), -1)
thermal_diffusivity = np.zeros((size, size))


def create_body(x, y, w, h, material_idx):
    material_mask[x:x + w, y:y + h] = material_idx
    alpha = materials[material_idx]['conductivity'] / (
            materials[material_idx]['density'] * materials[material_idx]['specific_heat'])
    thermal_diffusivity[x:x + w, y:y + h] = alpha


create_body(50, 50, 40, 40, 0)
create_body(120, 80, 60, 80, 1)

initial_grid[50:90, 50:90] = 373.15
initial_grid[120:180, 80:160] = 283.15


class Simulation:
    def __init__(self):
        self.reset()

    def reset(self):
        self.grid = initial_grid.copy()
        self.time = 0.0

    def step(self, dt):
        laplacian = (np.roll(self.grid, 1, 0) + np.roll(self.grid, -1, 0) +
                     np.roll(self.grid, 1, 1) + np.roll(self.grid, -1, 1) - 4 * self.grid) / dx ** 2
        self.grid += thermal_diffusivity * laplacian * dt
        self.time += dt


sim = Simulation()

# Настройка интерфейса
fig, ax = plt.subplots(figsize=(12, 10))
plt.subplots_adjust(left=0.1, right=0.8, bottom=0.25)

cmap = plt.cm.viridis
im = ax.imshow(sim.grid.T - 273.15, cmap=cmap, vmin=0, vmax=100,
               interpolation='bilinear', origin='lower')
cbar = plt.colorbar(im, ax=ax, label='Температура (°C)')

# Элементы управления
ax_time = plt.axes([0.1, 0.1, 0.65, 0.03])
time_slider = Slider(ax_time, 'Время (с)', 0, 1000, valinit=0)

ax_speed = plt.axes([0.1, 0.15, 0.65, 0.03])
speed_slider = Slider(ax_speed, 'Скорость', 0.1, 10, valinit=1)

ax_text = plt.axes([0.8, 0.1, 0.15, 0.05])
time_text = TextBox(ax_text, 'Время (с)', initial='0')

# Состояние анимации
paused = False
update_lock = False


def safe_update(func):
    def wrapper(*args, **kwargs):
        global update_lock
        if update_lock:
            return []
        update_lock = True
        try:
            result = func(*args, **kwargs)
        finally:
            update_lock = False
        return result

    return wrapper


@safe_update
def update(frame):
    if not paused:
        actual_dt = base_dt * speed_slider.val
        sim.step(actual_dt)
        time_slider.set_val(sim.time)
        time_text.set_val(f"{sim.time:.2f}")

    im.set_data(sim.grid.T - 273.15)
    return [im]


@safe_update
def update_time(val):
    target_time = float(val)

    if target_time < sim.time:
        sim.reset()

    while sim.time < target_time:
        sim.step(base_dt)

    time_text.set_val(f"{sim.time:.2f}")
    im.set_data(sim.grid.T - 273.15)
    return [im]


def set_time(text):
    try:
        new_time = float(text)
        time_slider.set_val(new_time)
    except:
        pass


def toggle_pause(event):
    global paused
    paused = not paused


time_slider.on_changed(update_time)
time_text.on_submit(set_time)

ax_pause = plt.axes([0.8, 0.2, 0.1, 0.05])
pause_button = Button(ax_pause, 'Пауза')
pause_button.on_clicked(toggle_pause)

ani = FuncAnimation(
    fig,
    update,
    interval=50,
    blit=True,
    cache_frame_data=False,
    save_count=0
)

plt.show()
