import os
import krpc
import time
import numpy as np


os.system("cls")
print("Подключаюсь к кораблю")
conn = krpc.connect(name="Муна-25 1")
vessel = conn.space_center.active_vessel
kerbin = conn.space_center.bodies['Kerbin']

ss = "время, масса, высота, скорость"
t = 0
while vessel.orbit.periapsis_altitude < 200000:
    ss += f"\n{t}, {vessel.mass:.2f}, {vessel.flight(kerbin.reference_frame).mean_altitude:.2f}, {np.linalg.norm(vessel.velocity(kerbin.reference_frame)):.2f}"    
    t += 1
    time.sleep(1)

with open("Files/Data/KSP_Stats.txt", "w", encoding="UTF-8") as f:
    f.write(ss)
print("Файл сохранён")
