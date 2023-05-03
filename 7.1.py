import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt

#Константа периода измерений
T = 0.005

#Объявление GPIO портов и их настройка
dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [12, 20, 16, 12, 7, 8, 25, 24]
cmp = 4
troyka = 17

GPIO.setmode(GPIO.BCM)

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(leds, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(cmp, GPIO.IN)

#Функция dec2bin возвращает 8-значный битовый массив, являющийся двоичным представлением числа value
def dec2bin(value):
    return [int (element) for element in bin(value)[2:].zfill(8)]

#Функция set_leds выводит на светодиоды значения из битового массива data
def set_leds(data):
    for i in range(0, 8):
        GPIO.output(leds[i], data[i])

#Функция adc с помощью бинарного поиска находит текущее напряжение на Тройке
def adc():
    val = 0
    for i in range(7, -1, -1):
        val += 2**i
        GPIO.output(dac, dec2bin(val))
        time.sleep(T)
        comp = GPIO.input(cmp)
        if comp == 0:
            val -= 2**i
    return val

def print_voltage(cur):
    print("Current voltage: ", "{:.3f}".format(round(cur*3.3/256, 3)), " (", cur, "/256)", sep="")

try:
    data = []

    #Зарядная часть эксперимента
    GPIO.output(troyka, 1)
    t1 = time.time()
    cur = adc()
    while (cur < 8):
        data.append(cur)
        set_leds(dec2bin(cur))
        cur = adc()
        print_voltage(cur)

    #Разрядная часть эксперимента
    GPIO.output(troyka, 0)
    cur = adc()
    while (cur < 224):
        data.append(cur)
        set_leds(dec2bin(cur))
        cur = adc()
        print_voltage(cur)

    #Корректировка неисправности транзистора/нормальная разрядка
    GPIO.output(troyka, 1)
    cur = adc()
    while (cur > 66):
        data.append(cur)
        set_leds(dec2bin(cur))
        cur = adc()
        print_voltage(cur)

    #Расчёт времени эксперимента
    t2 = time.time()
    length = t2 - t1

    #Вывод графика по полученным данным
    plt.plot(data)
    plt.show()

    #Сохранение данных и настроек в файлы
    with open("data.txt", "w") as f1:
        for elem in data:
            f1.write(str(elem))
            f1.write("\n")

    with open("settings.txt", "w") as f2:
        f2.write(str(T))
        f2.write("\n")
        f2.write(str(3.3/256))

    #Вывод общих данных эксперимента
    print("\n\n\nЭксперимент завершён.")
    print("Время эксперимента: ", length, " с")
    print("Период одного измерения: ", T, " с")
    print("Средняя частота дискретизации: ", 1/T, " Гц")
    print("Шаг квантования АЦП: ", 3.3/256, " В")

#Обнуление всех пинов
finally:
    GPIO.output(dac, 0)
    GPIO.output(leds, 0)
    GPIO.cleanup()