import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.colors as mcolors
from matplotlib.widgets import Slider, Button, TextBox

# Физические константы
k_B = 1.380649e-23  # Постоянная Больцмана (Дж/К)

# Параметры моделирования
size = 200  # Разрешение сетки
dx = 0.01  # Размер ячейки (м)
base_dt = 0.01  # Базовый шаг времени (с)

# Материалы
materials = {
    0: {
        'name': 'copper',
        'density': 8960,
        'specific_heat': 385,
        'conductivity': 401
    },
    1: {
        'name': 'aluminum',
        'density': 2700,
        'specific_heat': 900,
        'conductivity': 237
    }
}

# Инициализация сеток
initial_grid = np.full((size, size), 293.15, dtype=np.float64)  # Начальная температура
material_mask = np.full((size, size), -1, dtype=int)
thermal_diffusivity = np.zeros((size, size))


def create_rectangle(mask, x, y, w, h, material_idx):
    mask[x:x + w, y:y + h] = material_idx
    mat_props = materials[material_idx]
    alpha = mat_props['conductivity'] / (mat_props['density'] * mat_props['specific_heat'])
    thermal_diffusivity[x:x + w, y:y + h] = alpha


# Создание объектов
create_rectangle(material_mask, 50, 50, 40, 40, 0)
create_rectangle(material_mask, 120, 80, 60, 80, 1)

# Начальные условия
initial_grid[50:90, 50:90] = 373.15  # 100°C
initial_grid[120:180, 80:160] = 283.15  # 10°C


class SimulationState:
    def __init__(self):
        self.reset()

    def reset(self):
        self.grid = initial_grid.copy()
        self.time = 0.0
        self.steps = 0

    def step(self, dt):
        laplacian = (np.roll(self.grid, 1, 0) + np.roll(self.grid, -1, 0) +
                     np.roll(self.grid, 1, 1) + np.roll(self.grid, -1, 1) - 4 * self.grid) / dx ** 2
        self.grid += thermal_diffusivity * laplacian * dt
        self.time += dt
        self.steps += 1


# Инициализация симуляции
sim = SimulationState()

# Настройка визуализации
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111)
plt.subplots_adjust(left=0.1, right=0.8, bottom=0.25)

cmap = plt.cm.viridis
im = ax.imshow(sim.grid.T - 273.15, origin='lower', cmap=cmap,
               norm=mcolors.Normalize(vmin=0, vmax=100),
               interpolation='bilinear')
cbar = plt.colorbar(im, ax=ax, label='Температура (°C)')
ax.set_title("Теплопередача между телами")

# Элементы управления
ax_time = plt.axes([0.1, 0.1, 0.65, 0.03])
time_slider = Slider(ax_time, 'Время (с)', 0, 1000, valinit=0)

ax_speed = plt.axes([0.1, 0.15, 0.65, 0.03])
speed_slider = Slider(ax_speed, 'Скорость', 0.1, 10, valinit=1)

ax_text = plt.axes([0.8, 0.1, 0.15, 0.05])
time_text = TextBox(ax_text, 'Время (с)', initial='0')

# Состояние анимации
paused = False


def update(frame):
    global sim
    if not paused:
        actual_dt = base_dt * speed_slider.val
        sim.step(actual_dt)
        time_slider.set_val(sim.time)
        time_text.set_val(f"{sim.time:.2f}")

    im.set_data(sim.grid.T - 273.15)
    im.set_clim(vmin=0, vmax=100)
    return im,


def update_time(val):
    global sim
    target_time = float(val)

    if target_time < sim.time:
        # Перезапуск симуляции при перемотке назад
        sim.reset()

    # Выполняем шаги до достижения целевого времени
    while sim.time < target_time:
        sim.step(base_dt)

    time_text.set_val(f"{sim.time:.2f}")
    im.set_data(sim.grid.T - 273.15)


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

ani = FuncAnimation(fig, update, interval=50, blit=True)

plt.show()
