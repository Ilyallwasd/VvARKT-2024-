import matplotlib.pyplot as mtp


def GraphTimeMassa():
    mtp.xlabel("Время, c")
    mtp.ylabel("Масса, т")
    mtp.plot(time_ksp, massa_ksp, label='KSP', color=ksp_color)
    mtp.plot(time_mm, massa_mm, label='Math model', color=mm_color)
    Save("TimeMassa")

def GraphTimeHeight():
    mtp.xlabel("Время, с")
    mtp.ylabel("Высота, м")
    mtp.plot(time_ksp, height_ksp, label='KSP', color=ksp_color)
    mtp.plot(time_mm, height_mm, label='Math model', color=mm_color)
    Save("TimeHeight")

def GraphTimeSpeed():
    mtp.xlabel("Время, с")
    mtp.ylabel("Скорость, м/c")
    mtp.plot(time_ksp, speed_ksp, label='KSP', color=ksp_color)
    mtp.plot(time_mm, speed_mm, label='Math model', color=mm_color)
    Save("TimeSpeed")

def GraphHeightSpeed():
    mtp.xlabel("Высота, м")
    mtp.ylabel("Скорость, м/c")
    mtp.plot(height_ksp, speed_ksp, label='KSP', color=ksp_color)
    mtp.plot(height_mm, speed_mm, label='Math model', color=mm_color)
    Save("HeightSpeed")

def ErrorRate():
    mtp.title("Относительная погрешность")
    mtp.xlabel("Время, с")
    mtp.ylabel("Погрешность, %")
    time = min([time_ksp, time_mm])
    error_rate_massa = []
    error_rate_height = []
    error_rate_speed = []
    for i in range(10, len(time)):
        error_rate_massa.append(abs((massa_ksp[i] - massa_mm[i]) / massa_mm[i] * 100))
        error_rate_height.append(abs((height_ksp[i] - height_mm[i]) / height_mm[i] * 100))
        error_rate_speed.append(abs((speed_ksp[i] - speed_mm[i]) / speed_mm[i] * 100))
    mtp.plot(time[10::], error_rate_massa, label='Масса', color=massa_color)
    mtp.plot(time[10::], error_rate_height, label='Высота', color=height_color)
    mtp.plot(time[10::], error_rate_speed, label='Скорость', color=speed_color)
    Save("ErrorRate")

def Save(name):
    mtp.legend()
    mtp.savefig(f"Files/Data/Graphs_KSP/{name}.png")
    mtp.cla()

time_ksp = []
massa_ksp = []
height_ksp = []
speed_ksp = []
with open("Files/Data/KSP_Stats.txt", "r") as f:
    ss = f.read().split("\n")[1::]
    for i in range(len(ss)):
        ss[i] = ss[i].split(", ")
        time_ksp.append(float(ss[i][0]))
        massa_ksp.append(float(ss[i][1]) / 1000)
        height_ksp.append(float(ss[i][2]))
        speed_ksp.append(float(ss[i][3]))

time_mm = []
massa_mm = []
height_mm = []
speed_mm = []
with open("Files/Data/MathModel_Stats.txt", "r") as f:
    ss = f.read().split("\n")[1::]
    for i in range(len(ss) - 1):
        ss[i] = ss[i].split(", ")
        time_mm.append(float(ss[i][0]))
        massa_mm.append(float(ss[i][1]) / 1000)
        height_mm.append(float(ss[i][2]))
        speed_mm.append(float(ss[i][3]))


ksp_color = "#008000"
mm_color = "#ff0000"
massa_color = "#ff0000"
height_color = "#008000"
speed_color = "#0000ff"
GraphTimeMassa()
GraphTimeHeight()
GraphTimeSpeed()
GraphHeightSpeed()
ErrorRate()
print("Графики сохранены в Files/Data/Graphs_KSP")
