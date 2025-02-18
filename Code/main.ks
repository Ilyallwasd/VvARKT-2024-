function WaitBeforeStart {
    clearscreen.
    set timer to 10.
    until timer = 0 {
        print timer.
        set timer to timer - 1.
        wait 1.
        clearscreen.
    }
    print "ПОЕХАЛИ!".
    wait 1.
}

function FirstStage {
    clearscreen.

    print "Набираем высоту".
    lock steering to heading(90, 90).
    lock throttle to 1.
    stage.

    until stage:liquidfuel < 1 {
        lock steering to heading(90, 90 - 70 * (ship:altitude / 50000)).
        wait 0.2.
    }

    lock steering to heading(90, 20).
    print "У первой ступени закончилось топливо, начинаю отстыковку".
    lock throttle to 0.
    wait 2.
    stage.
    wait 5.
}

function SecondStage {
    clearscreen.

    print "Произвожу запуск второй ступени".
    lock throttle to 1.

    wait until ship:altitude > 70000.
    print "Вышли за пределы орбиты Земли. Произвожу сброс обтекателей".
    stage.

    wait until ship:apoapsis > 202500.
    lock throttle to 0.
    wait 1.
    stage.
}

function CircleOrbit {
    clearscreen.

    print "Выходим на апоцентр в 200км".
    lock steering to heading(90, 0).
    until eta:apoapsis < 20 {
        clearscreen.
        print "Выходим на апоцентр в 200км".
        print "До апоцентра осталось: " + eta:apoapsis + " секунд".
        wait 0.2.
    }

    lock throttle to 1.
    until ship:periapsis > 200000 {
        clearscreen.
        print "Апоцентр: " + ship:apoapsis + " метров".
        print "Перицентр: " + ship:periapsis + " метров".
        wait 0.2.
    }
    
    lock throttle to 0.
    wait 3.
    stage.
    wait 3.
}

function GoToMoon {
    clearscreen.

    print "Подлетаем к точке отлёта".
    wait until CheckCanGoToMoon.
    
    print "Начинаем полёт к Луне".
    lock steering to prograde.
    wait 3.
    
    until orbit:apoapsis > body("Mun"):altitude {
        lock throttle to 1 - 0.9 * orbit:apoapsis / body("Mun"):altitude.
        wait 0.2.
    }

    lock throttle to 0.
}

function OnTheMoon {
    clearscreen.

    print "Летим к Луне".
    wait until ship:body = body("Mun").
    print "Вошли в орбиту Луны".
    wait 10.
    stage.
    
    if ship:periapsis > 1000 {
        print "Сбились с курса, начинаю выравнивание".
        lock steering to heading(90, 0).
        
        until ship:periapsis < 1000 {
            lock throttle to 1.
            print "Перицентр: " + ship:periapsis + "метров".
            wait 0.2.
            clearscreen.
        }
        wait 5.

        lock throttle to 0.
        print "Направление выравнено, готовлюсь к посадке".
    }

    wait until ship:altitude < 100000.
    print "Начинаем посадку".
    
    lock steering to ship:velocity:surface * -1.
    legs on.
    wait 5.

    until ship:bounds:bottomaltradar < 1 {
        lock throttle to 1 * FindX.
        wait 0.2.
    }

    unlock steering.
    lock throttle to 0.
    clearscreen.
    print "Посадка совершена, миссия успешна!".
    wait until false.
}


// Дополнительные функции
function CheckCanGoToMoon {
    set Vector_Kerbin_Mun to body("Mun"):position - body("Kerbin"):position.
    set Vector_Kerbin_ship to Ship:position - body("Kerbin"):position.

    set angle_ship_Moon to VANG(Vector_Kerbin_Mun, Vector_Kerbin_ship).
    if (VANG(VXCL(ship:up:vector, ship:velocity:orbit), body("Mun"):position - ship:position) > 90) {
		set angle_ship_Moon to -angle_ship_Moon.
	}

    set a1 to (Vector_Kerbin_Mun:mag + ship:altitude + body("Kerbin"):radius) / 2.
	set a2 to Vector_Kerbin_Mun:mag.
	set angle_true to 180 * (1 - (a1/a2) ^ 1.5).

    clearscreen.
    print "Текущий угол: " + angle_ship_Moon + "°".
    print "Необходимый угол: " + angle_true + "°".
    return abs(angle_ship_Moon - angle_true) < 3.
}

function FindX {
    clearscreen.

    set b1 to ship:mass / ship:maxthrust.
    set b2 to (ship:velocity:surface:mag ^ 2) / (2 * ship:bounds:bottomaltradar).
    set g to (6.67 * (10 ^ (-11))) * ((9.76 * (10 ^ 20)) / ((200000 + ship:bounds:bottomaltradar) ^ 2)).

    set true_force to b1 * (b2 + g).
    set work_force to true_force.
    if true_force > 0.5 {
        set work_force to 0.5 + (true_force - 0.5) * 3.
    }
    if work_force > 1 {
        set work_force to 1.
    }
    set t to ship:velocity:surface:mag / (ship:maxthrust * true_force / ship:mass - g).
    print "Начинаем посадку".
    print "Скорость: " + ship:velocity:surface:mag + " м/с".
    print "Высота: " + ship:bounds:bottomaltradar + " м".
    print "Масса корабля: " + (ship:mass * 1000) + " кг".
    print "Воздействие гравитации: " + g + " м/с²".
    print "Необходимая работа двигателей: " + true_force * 100 + "%".
    print "Работа двигателей: " + work_force * 100 + "%".
    print "Ориентировочно посадка через: " + t + " с".

    return work_force.
}


WaitBeforeStart.
FirstStage.
SecondStage.
CircleOrbit.
GoToMoon.
OnTheMoon.
