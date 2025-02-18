import time
import numpy
import os


class Constats:
    # Физические и математические константы
    time_skip = 0.02
    count_skip = 10000
    multiply_skip = 100
    G = 6.67 * 10**(-11)
    P_0 = 101325
    M = 0.02898
    R = 8.314
    _R = 287.05
    T_0 = 288.2


    # Параметры связанный с Землёй
    massa_Earth = 5.29 * 10**22
    radius_Earth = 600000
    angular_velocity_Earth = 2.91 * 10**(-4)


    # Параметры связанные с ракетой
    dry_massa_first_stage = 6890
    massa_fuel_first_stage = 22800
    q_first_stage = 232.7
    F_1_first_stage = 644135
    F_0_first_stage = 677332
    I_1_first_stage = 285
    I_0_first_stage = 300

    dry_massa_second_stage = 8038
    massa_fuel_second_stage = 33200
    q_second_stage = 207.13
    F_1_second_stage = 568750
    F_0_second_stage = 650000
    I_1_second_stage = 280
    I_0_second_stage = 320

    dry_massa_third_stage = 2722
    massa_fuel_third_stage = 3993
    q_third_stage = 72.83
    F_1_third_stage = 64286
    F_0_third_stage = 250000
    I_1_third_stage = 90
    I_0_third_stage = 350

    other_massa = 9200
    C_d = 0.115
    A_eff = 1.77


class Math:
    def LengthVector(v):
        return (v[0] ** 2 + v[1] ** 2 + v[2] ** 2) ** 0.5
    
    def AngleVectors(v1, v2):
        if Math.LengthVector(v1) != 0 and Math.LengthVector(v2) != 0:
            return numpy.arccos(numpy.round((v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]) / (Math.LengthVector(v1) * Math.LengthVector(v2)), 5))
        return 0
    
    def MultiplyVectors(v1, v2):
        return Math.LengthVector(v1) * Math.LengthVector(v2) * numpy.cos(Math.AngleVectors(v1, v2))

    def ProectVV(v1, v2):
        # Проекция вектора v1 на вектор v2
        return [float(v2[0] * Math.MultiplyVectors(v1, v2) / Math.MultiplyVectors(v2, v2)),
                float(v2[1] * Math.MultiplyVectors(v1, v2) / Math.MultiplyVectors(v2, v2)),
                float(v2[2] * Math.MultiplyVectors(v1, v2) / Math.MultiplyVectors(v2, v2))]

    def ProectVPl(v1, v2):
        # Проекция вектора v1 на плоскость перпендикулярной вектору v2
        return [float(v1[0] - v2[0] * Math.LengthVector(v1) * numpy.cos(Math.AngleVectors(v1, v2)) / Math.LengthVector(v2)),
                float(v1[1] - v2[1] * Math.LengthVector(v1) * numpy.cos(Math.AngleVectors(v1, v2)) / Math.LengthVector(v2)),
                float(v1[2] - v2[2] * Math.LengthVector(v1) * numpy.cos(Math.AngleVectors(v1, v2)) / Math.LengthVector(v2)),]
    
    def RotateVector(v, angle):
        if v[2] < 0:
            alpha = numpy.arctan(v[0] / v[2]) - numpy.deg2rad(angle) + numpy.pi
        elif v[2] > 0:
            alpha = numpy.arctan(v[0] / v[2]) - numpy.deg2rad(angle)
        else:
            alpha = -numpy.deg2rad(angle)
        return [numpy.sin(alpha), 0, numpy.cos(alpha)]
    
    def FindAngle(v):
        if v[2] < 0:
            alpha = numpy.arctan(v[0] / v[2]) + numpy.pi
        elif v[2] > 0:
            alpha = numpy.arctan(v[0] / v[2])
        else:
            alpha = numpy.pi / 2
        return alpha


class Ship:
    _time = 0
    velocity = [0, 0, Constats.angular_velocity_Earth * Constats.radius_Earth]
    steering = 90
    position = [Constats.radius_Earth, 0, 0]
    throttle = 0
    stage = 0
    massa_fuel_first_stage = Constats.massa_fuel_first_stage
    massa_fuel_second_stage = Constats.massa_fuel_second_stage
    massa_fuel_third_stage = Constats.massa_fuel_third_stage
    stage_wait = 0
    wait = 0
    eta_apoapsis = 0

    def apoapsis_periapsis():
        def h():
            return Math.LengthVector(position) - Constats.radius_Earth

        def g():
            return Constats.G * Constats.massa_Earth / (Constats.radius_Earth + h()) ** 2

        def F_d():
            return 0.5 * p() * (U() ** 2) * Constats.C_d * Constats.A_eff

        def U():
            return Math.LengthVector([velocity[0] - velocity_point()[0], velocity[1] - velocity_point()[1], velocity[2] - velocity_point()[2]])

        def velocity_point():
            return [-numpy.cos(Math.FindAngle(position)) * Constats.angular_velocity_Earth * Constats.radius_Earth,
                    0,
                    numpy.sin(Math.FindAngle(position)) * Constats.angular_velocity_Earth * Constats.radius_Earth]

        def p():
            return P_a() / (Constats._R * T())

        def P_a():
            if h() <= 100000:
                return Constats.P_0 * numpy.e**(-Constats.M * g() * h() / Constats.R / T())
            else:
                return 0
        
        def T():
            if h() <= 11000:
                return Constats.T_0 - 6.5 * h() / 1000
            elif h() <= 20000:
                return Constats.T_0 - 71.5
            elif h() <= 50000:
                return Constats.T_0 - 71.5 + 54 * (h() - 20000) / 30000
            elif h() <= 80000:
                return Constats.T_0 - 17.5 - 72.1 * (h() - 50000) / 30000
            elif h() <= 100000:
                return Constats.T_0 - 89.6
            elif h() <= 150000:
                return Constats.T_0 - 89.6 + 429 * (h() - 100000) / 50000
            elif h() <= 200000:
                return Constats.T_0 + 339.4 + 226.8 * (h() - 150000) / 50000
            elif h() <= 300000:
                return Constats.T_0 + 566.2 + 116 * (h() - 200000) / 100000 
            elif h() <= 500000:
                return Constats.T_0 + 682.2 + 29.6 * (h() - 300000) / 200000
            return 1000

        position = Ship.position
        velocity = Ship.velocity
        m = Ship.m()
        time_skip = Constats.time_skip * Constats.multiply_skip
        height = []
        count = Constats.count_skip

        while count > 0 and h() > 0:
            old_velocity = velocity
            # Работа силы тяжести
            velocity = [velocity[0] - position[0] * g() * time_skip / Math.LengthVector(position),
                        velocity[1] - position[1] * g() * time_skip / Math.LengthVector(position),
                        velocity[2] - position[2] * g() * time_skip / Math.LengthVector(position)]
            
            # Сопротивление воздуха
            velocity = [velocity[0] - velocity[0] * F_d() * time_skip / Math.LengthVector(velocity) / m,
                        velocity[1] - velocity[1] * F_d() * time_skip / Math.LengthVector(velocity) / m,
                        velocity[2] - velocity[2] * F_d() * time_skip / Math.LengthVector(velocity) / m]

            #Обновляем координаты
            position = [position[0] + (velocity[0] + old_velocity[0]) * time_skip / 2,
                        position[1] + (velocity[1] + old_velocity[1]) * time_skip / 2,
                        position[2] + (velocity[2] + old_velocity[2]) * time_skip / 2]
            
            height.append(h())
            count -= 1
        if len(height) != 0:
            i = height.index(max(height))
            Ship.eta_apoapsis = Ship._time + i * time_skip
            return [max(height), min(height)]
        else:
            return[0, 0]

    def velocity_orbit():
        return [-numpy.cos(Math.FindAngle(Ship.position)) * Constats.angular_velocity_Earth * Math.LengthVector(Ship.position),
                0,
                numpy.sin(Math.FindAngle(Ship.position)) * Constats.angular_velocity_Earth * Math.LengthVector(Ship.position)]

    def stage_fuel():
        if Ship.stage == 0:
            return 4 * Ship.massa_fuel_first_stage
        elif Ship.stage == 1:
            return Ship.massa_fuel_second_stage
        elif Ship.stage == 2:
            return Ship.massa_fuel_third_stage

    def h():
        return Math.LengthVector(Ship.position) - Constats.radius_Earth

    def U():
        return Math.LengthVector([Ship.velocity[0] - Ship.velocity_orbit()[0], Ship.velocity[1] - Ship.velocity_orbit()[1], Ship.velocity[2] - Ship.velocity_orbit()[2]])

    def I():
        if Ship.stage == 0:
            return Constats.I_0_first_stage - (Constats.I_0_first_stage - Constats.I_1_first_stage) * Ship.P_a() / Constats.P_0
        elif Ship.stage == 1:
            return Constats.I_0_second_stage - (Constats.I_0_second_stage - Constats.I_1_second_stage) * Ship.P_a() / Constats.P_0
        elif Ship.stage == 2:
            return Constats.I_0_third_stage - (Constats.I_0_third_stage - Constats.I_1_third_stage) * Ship.P_a() / Constats.P_0

    def m():
        if Ship.stage == 0:
            return Ship.massa_fuel_first_stage * 4 + Ship.massa_fuel_second_stage + Ship.massa_fuel_third_stage +\
                   Constats.dry_massa_first_stage * 4 + Constats.dry_massa_second_stage +\
                   Constats.dry_massa_third_stage + Constats.other_massa
        elif Ship.stage == 1:
            return Ship.massa_fuel_second_stage + Ship.massa_fuel_third_stage + Constats.dry_massa_second_stage +\
                   Constats.dry_massa_third_stage + Constats.other_massa
        elif Ship.stage == 2:
            return Ship.massa_fuel_third_stage + Constats.dry_massa_third_stage + Constats.other_massa
        else:
            return Constats.other_massa

    def q():
        if Ship.stage == 0:
            return Constats.q_first_stage * Constats.I_0_first_stage / Ship.I()
        elif Ship.stage == 1:
            return Constats.q_second_stage * Constats.I_0_second_stage / Ship.I()
        elif Ship.stage == 2:
            return Constats.q_third_stage * Constats.I_0_third_stage / Ship.I()

    def F():
        if Ship.stage == 0:
            return 4 * Constats.F_0_first_stage - (Constats.F_0_first_stage - Constats.F_1_first_stage) * Ship.P_a() / Constats.P_0
        elif Ship.stage == 1:
            return Constats.F_0_second_stage - (Constats.F_0_second_stage - Constats.F_1_second_stage) * Ship.P_a() / Constats.P_0
        elif Ship.stage == 2:
            return Constats.F_0_third_stage - (Constats.F_0_third_stage - Constats.F_1_third_stage) * Ship.P_a() / Constats.P_0

    def F_d():
        return 0.5 * Ship.p() * (Ship.U() ** 2) * Constats.C_d * Constats.A_eff

    def p():
        return Ship.P_a() / (Constats._R * Ship.T())

    def g():
        return Constats.G * Constats.massa_Earth / (Constats.radius_Earth + Ship.h()) ** 2
    
    def P_a():
        if Ship.h() <= 100000:
            return Constats.P_0 * numpy.e**(-Constats.M * Ship.g() * Ship.h() / Constats.R / Ship.T())
        else:
            return 0
    
    def T():
        if Ship.h() <= 11000:
            return Constats.T_0 - 6.5 * Ship.h() / 1000
        elif Ship.h() <= 20000:
            return Constats.T_0 - 71.5
        elif Ship.h() <= 50000:
            return Constats.T_0 - 71.5 + 54 * (Ship.h() - 20000) / 30000
        elif Ship.h() <= 80000:
            return Constats.T_0 - 17.5 - 72.1 * (Ship.h() - 50000) / 30000
        elif Ship.h() <= 100000:
            return Constats.T_0 - 89.6
        elif Ship.h() <= 150000:
            return Constats.T_0 - 89.6 + 429 * (Ship.h() - 100000) / 50000
        elif Ship.h() <= 200000:
            return Constats.T_0 + 339.4 + 226.8 * (Ship.h() - 150000) / 50000
        elif Ship.h() <= 300000:
            return Constats.T_0 + 566.2 + 116 * (Ship.h() - 200000) / 100000 
        elif Ship.h() <= 500000:
            return Constats.T_0 + 682.2 + 29.6 * (Ship.h() - 300000) / 200000
        return 1000


class Update:
    def FixedUpdate():
        Ship._time += Constats.time_skip
        old_velocity = Ship.velocity

        #Обновляем скорость
        # Работа двигателей
        Ship.velocity = [Ship.velocity[0] + Math.RotateVector(Ship.position, 90 - Ship.steering)[0] * Ship.F() * Ship.throttle * Constats.time_skip / Ship.m(),
                         Ship.velocity[1] + Math.RotateVector(Ship.position, 90 - Ship.steering)[1] * Ship.F() * Ship.throttle * Constats.time_skip / Ship.m(),
                         Ship.velocity[2] + Math.RotateVector(Ship.position, 90 - Ship.steering)[2] * Ship.F() * Ship.throttle * Constats.time_skip / Ship.m(),]

        # Работа силы тяжести
        Ship.velocity = [Ship.velocity[0] - Ship.position[0] * Ship.g() * Constats.time_skip / Math.LengthVector(Ship.position),
                         Ship.velocity[1] - Ship.position[1] * Ship.g() * Constats.time_skip / Math.LengthVector(Ship.position),
                         Ship.velocity[2] - Ship.position[2] * Ship.g() * Constats.time_skip / Math.LengthVector(Ship.position)]
        
        # Сопротивление воздуха
        Ship.velocity = [Ship.velocity[0] - Ship.velocity[0] * Ship.F_d() * Constats.time_skip / Math.LengthVector(Ship.velocity) / Ship.m(),
                         Ship.velocity[1] - Ship.velocity[1] * Ship.F_d() * Constats.time_skip / Math.LengthVector(Ship.velocity) / Ship.m(),
                         Ship.velocity[2] - Ship.velocity[2] * Ship.F_d() * Constats.time_skip / Math.LengthVector(Ship.velocity) / Ship.m()]

        if Ship.h() <= 0:
            a = Math.ProectVV(Ship.velocity, Ship.position)
            if a[0] != 0:
                if Ship.position[0] / a[0] < 0:
                    Ship.velocity = Math.ProectVPl(Ship.velocity, Ship.position)


        #Обновляем координаты
        Ship.position = [Ship.position[0] + (Ship.velocity[0] + old_velocity[0]) * Constats.time_skip / 2,
                         Ship.position[1] + (Ship.velocity[1] + old_velocity[1]) * Constats.time_skip / 2,
                         Ship.position[2] + (Ship.velocity[2] + old_velocity[2]) * Constats.time_skip / 2]
        
        if Ship.h() < 0:
            Ship.position = [Ship.position[0] * Constats.radius_Earth / Math.LengthVector(Ship.position),
                             Ship.position[1] * Constats.radius_Earth / Math.LengthVector(Ship.position),
                             Ship.position[2] * Constats.radius_Earth / Math.LengthVector(Ship.position)]

        #Обновляем другие значения
        if Ship.stage == 0:
            Ship.massa_fuel_first_stage -= Ship.q() * Ship.throttle * Constats.time_skip
        elif Ship.stage == 1:
            Ship.massa_fuel_second_stage -= Ship.q() * Ship.throttle * Constats.time_skip
        elif Ship.stage == 2:
            Ship.massa_fuel_third_stage -= Ship.q() * Ship.throttle * Constats.time_skip
        
        if Ship.wait > 0:
            Ship.wait -= Constats.time_skip

    def Script():
        if Ship.stage_wait == 0:
            Ship.steering = 90
            Ship.throttle = 1

            if Ship.stage_fuel() > 0:
                Ship.steering = 90 - 70 * (Ship.h() / 50000)
                return

            Ship.steering = 20
            Ship.throttle = 0
            Ship.wait = 2
            Ship.stage_wait += 1
            return
        elif Ship.stage_wait == 1:
            if Ship.wait > 0:
                return
            Ship.stage += 1
            Ship.wait = 5
            Ship.stage_wait += 1
            return
        elif Ship.stage_wait == 2:
            if Ship.wait > 0:
                return
            
            Ship.throttle = 1

            if Ship.h() < 70000:
                return
            Ship.massa_fuel_second_stage -= 1000
            Ship.stage_wait += 1
            return
        elif Ship.stage_wait == 3:
            if Ship.apoapsis_periapsis()[0] < 202500:
                return
            
            Ship.throttle = 0
            Ship.wait = 1
            Ship.stage_wait += 1
            return
        elif Ship.stage_wait == 4:
            if Ship.wait > 0:
                return
            Ship.stage += 1
            Ship.stage_wait += 1
            return
        elif Ship.stage_wait == 5:
            Ship.steering = 0
            if Ship.eta_apoapsis - Ship._time > 20:
                return
            Ship.stage_wait += 1
            return
        elif Ship.stage_wait == 6:
            Ship.throttle = 1
            if Ship.apoapsis_periapsis()[1] < 200000:
                return

        global work
        work = False





ss = "время, масса, высота, скорость"
ss += f"\n{Ship._time:.0f}, {Ship.m():.2f}, {Ship.h():.2f}, {Ship.U():.2f}"
a = 0
work = True
while work:
    a += 1
    Update.FixedUpdate()
    Update.Script()
    if a == 50:
        apoapsis, periapsis = Ship.apoapsis_periapsis()
        os.system("cls")
        print(f"time: {Ship._time:.2f}")
        print(f"eta_apoapsis: {Ship.eta_apoapsis:.2f}")
        print(f"position: x: {Ship.position[0]:.2f}, y: {Ship.position[1]:.2f}, z: {Ship.position[2]:.2f}")
        print(f"height: {Ship.h():.2f}")
        print(f"velocity: x: {Ship.velocity[0]:.2f}, y: {Ship.velocity[1]:.2f}, z: {Ship.velocity[2]:.2f}")
        print(f"velocity_orbit: x: {Ship.velocity_orbit()[0]:.2f}, y: {Ship.velocity_orbit()[1]:.2f}, z: {Ship.velocity_orbit()[2]:.2f}")
        print(f"speed: {Ship.U():.2f}")
        print(f"throttle: {Ship.throttle:.2f}")
        print(f"steering: {Ship.steering:.2f}")
        print(f"massa: {Ship.m():.2f}")
        a = 0
        ss += f"\n{Ship._time:.0f}, {Ship.m():.2f}, {Ship.h():.2f}, {Ship.U():.2f}"



f = open("Files/Data/MathModel_Stats.txt", "w", encoding="UTF-8")
f.write(ss + "\n" +"5" * 9000)
print("Файл сохранён")
