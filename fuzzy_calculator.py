import math

import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

min_value = 20
max_value = 90

# Tạo các biến mờ
traffic_d1 = ctrl.Antecedent(np.arange(0, 41, 1), 'traffic_d1')  # Lượng phương tiện từ 0 đến 40
light_duration_d1 = ctrl.Consequent(np.arange(0, 91, 1), 'light_duration_d1')  # Thời gian đèn từ 20 đến 90 giây

traffic_d2 = ctrl.Antecedent(np.arange(0, 41, 1), 'traffic_d2')
light_duration_d2 = ctrl.Consequent(np.arange(0, 91, 1), 'light_duration_d2')

# Tạo hàm liên thuộc cho biến đầu vào và đầu ra
# Direction 1
traffic_d1['very_low'] = fuzz.trapmf(traffic_d1.universe, [0, 0, 4, 8])
traffic_d1['low'] = fuzz.trapmf(traffic_d1.universe, [2, 6, 11.5, 16])
traffic_d1['medium'] = fuzz.gaussmf(traffic_d1.universe, 17, 3.4)
traffic_d1['high'] = fuzz.trapmf(traffic_d1.universe, [19, 22, 27, 30])
traffic_d1['very_high'] = fuzz.trapmf(traffic_d1.universe, [25, 32, 40, 40])

# Direction 2
traffic_d2['very_low'] = fuzz.trapmf(traffic_d2.universe, [0, 0, 4, 8])
traffic_d2['low'] = fuzz.trapmf(traffic_d2.universe, [2, 6, 11, 16])
traffic_d2['medium'] = fuzz.gaussmf(traffic_d2.universe, 17, 3.4)
traffic_d2['high'] = fuzz.trapmf(traffic_d2.universe, [19, 22, 27, 30])
traffic_d2['very_high'] = fuzz.trapmf(traffic_d2.universe, [25, 32, 40, 40])

# Light time 1
light_duration_d1['very_short'] = fuzz.trapmf(light_duration_d1.universe, [0, 0, 16, 24])
light_duration_d1['short'] = fuzz.trapmf(light_duration_d1.universe, [18, 20, 25, 41])
light_duration_d1['medium'] = fuzz.gaussmf(light_duration_d1.universe, 46, 5)
light_duration_d1['long'] = fuzz.trapmf(light_duration_d1.universe, [51, 56, 63, 72])
light_duration_d1['very_long'] = fuzz.trapmf(light_duration_d1.universe, [68, 75, 90, 90])

#light time 2
light_duration_d2['very_short'] = fuzz.trapmf(light_duration_d2.universe, [0, 0, 16, 24])
light_duration_d2['short'] = fuzz.trapmf(light_duration_d2.universe, [18, 20, 25, 41])
light_duration_d2['medium'] = fuzz.gaussmf(light_duration_d2.universe, 46, 5)
light_duration_d2['long'] = fuzz.trapmf(light_duration_d2.universe, [51, 56, 63, 72])
light_duration_d2['very_long'] = fuzz.trapmf(light_duration_d2.universe, [68, 75, 90, 90])

# Xây dựng cơ sở luật
rule1 = ctrl.Rule(traffic_d1['very_low'] & traffic_d2['very_low'],
                  (light_duration_d1['medium'], light_duration_d2['medium']))
rule2 = ctrl.Rule(traffic_d1['very_low'] & traffic_d2['low'], (light_duration_d1['long'], light_duration_d2['short']))
rule3 = ctrl.Rule(traffic_d1['very_low'] & traffic_d2['medium'],
                  (light_duration_d1['long'], light_duration_d2['short']))
rule4 = ctrl.Rule(traffic_d1['very_low'] & traffic_d2['high'],
                  (light_duration_d1['medium'], light_duration_d2['short']))
rule5 = ctrl.Rule(traffic_d1['very_low'] & traffic_d2['very_high'],
                  (light_duration_d1['very_long'], light_duration_d2['very_short']))

rule6 = ctrl.Rule(traffic_d1['low'] & traffic_d2['very_low'], (light_duration_d1['short'], light_duration_d2['long']))
rule7 = ctrl.Rule(traffic_d1['low'] & traffic_d2['low'], (light_duration_d1['medium'], light_duration_d2['medium']))
rule8 = ctrl.Rule(traffic_d1['low'] & traffic_d2['medium'], (light_duration_d1['long'], light_duration_d2['short']))
rule9 = ctrl.Rule(traffic_d1['low'] & traffic_d2['high'], (light_duration_d1['very_long'], light_duration_d2['short']))
rule10 = ctrl.Rule(traffic_d1['low'] & traffic_d2['very_high'],
                   (light_duration_d1['very_long'], light_duration_d2['very_short']))

rule11 = ctrl.Rule(traffic_d1['medium'] & traffic_d2['very_low'],
                   (light_duration_d1['short'], light_duration_d2['long']))
rule12 = ctrl.Rule(traffic_d1['medium'] & traffic_d2['low'], (light_duration_d1['short'], light_duration_d2['long']))
rule13 = ctrl.Rule(traffic_d1['medium'] & traffic_d2['medium'],
                   (light_duration_d1['medium'], light_duration_d2['medium']))
rule14 = ctrl.Rule(traffic_d1['medium'] & traffic_d2['high'], (light_duration_d1['long'], light_duration_d2['short']))
rule15 = ctrl.Rule(traffic_d1['medium'] & traffic_d2['very_high'],
                   (light_duration_d1['long'], light_duration_d2['short']))

rule16 = ctrl.Rule(traffic_d1['high'] & traffic_d2['very_low'],
                   (light_duration_d1['very_short'], light_duration_d2['very_long']))
rule17 = ctrl.Rule(traffic_d1['high'] & traffic_d2['low'], (light_duration_d1['very_short'], light_duration_d2['long']))
rule18 = ctrl.Rule(traffic_d1['high'] & traffic_d2['medium'], (light_duration_d1['short'], light_duration_d2['long']))
rule19 = ctrl.Rule(traffic_d1['high'] & traffic_d2['high'], (light_duration_d1['medium'], light_duration_d2['medium']))
rule20 = ctrl.Rule(traffic_d1['high'] & traffic_d2['very_high'],
                   (light_duration_d1['long'], light_duration_d2['short']))

rule21 = ctrl.Rule(traffic_d1['very_high'] & traffic_d2['very_low'],
                   (light_duration_d1['very_long'], light_duration_d2['very_short']))
rule22 = ctrl.Rule(traffic_d1['very_high'] & traffic_d2['low'],
                   (light_duration_d1['very_long'], light_duration_d2['very_short']))
rule23 = ctrl.Rule(traffic_d1['very_high'] & traffic_d2['medium'],
                   (light_duration_d1['short'], light_duration_d2['long']))
rule24 = ctrl.Rule(traffic_d1['very_high'] & traffic_d2['high'],
                   (light_duration_d1['short'], light_duration_d2['long']))
rule25 = ctrl.Rule(traffic_d1['very_high'] & traffic_d2['very_high'],
                   (light_duration_d1['medium'], light_duration_d2['medium']))

light_control = ctrl.ControlSystem(
    [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15,
     rule16, rule17, rule18, rule19, rule20, rule21, rule22, rule23, rule24, rule25])
light_duration_calc = ctrl.ControlSystemSimulation(light_control)


def fuzzy_calculate(traffic_d1, traffic_d2):
    print('Calculate triggerd: \ntraffic 1: ' + str(traffic_d1) + '\ntraffic 2: ' + str(traffic_d2))

    # Đưa vào giá trị lượng phương tiện và tính toán
    light_duration_calc.input['traffic_d1'] = traffic_d1
    light_duration_calc.input['traffic_d2'] = traffic_d2
    light_duration_calc.compute()

    # Lấy kết quả suy luận mờ
    light_d1 = light_duration_calc.output['light_duration_d1']
    light_d2 = light_duration_calc.output['light_duration_d2']

    # làm tròn
    light_d1 = math.ceil(light_d1)
    light_d2 = math.ceil(light_d2)

    # Áp trần

    if light_d1 > max_value:
        light_d1 = max_value
    if light_d1 < min_value:
        light_d1 = min_value
    if light_d2 > max_value:
        light_d2 = max_value
    if light_d2 < min_value:
        light_d2 = min_value

    return light_d1, light_d2


def estimate_light_time(traffic_r1, traffic_r2, traffic_r3, traffic_r4):
    traffic_d1 = traffic_r1 if traffic_r1 >= traffic_r3 else traffic_r3
    traffic_d2 = traffic_r2 if traffic_r2 >= traffic_r4 else traffic_r4
    light_time_d1, light_time_d2 = fuzzy_calculate(traffic_d1, traffic_d2)
    return light_time_d1, light_time_d2


def print_input_triangular_fuzzy_number():
    plt.figure()
    plt.plot(traffic_d1.universe, traffic_d1['very_low'].mf, 'b', linewidth=1.5, label='Rất ít')
    plt.plot(traffic_d1.universe, traffic_d1['low'].mf, 'g', linewidth=1.5, label='Ít')
    plt.plot(traffic_d1.universe, traffic_d1['medium'].mf, 'r', linewidth=1.5, label='Trung bình')
    plt.plot(traffic_d1.universe, traffic_d1['high'].mf, 'g', linewidth=1.5, label='Nhiều')
    plt.plot(traffic_d1.universe, traffic_d1['very_high'].mf, 'b', linewidth=1.5, label='Rất nhiều')
    plt.title('Hàm liên thuộc tập mờ mật độ xe D1/D2')
    plt.ylabel('Độ phụ thuộc (%)')
    plt.xlabel('Mật độ xe')
    plt.legend()
    plt.show()


def print_output_triangular_fuzzy_number():
    plt.figure()
    plt.plot(light_duration_d1.universe, light_duration_d1['very_short'].mf, 'b', linewidth=1.5, label='Rất ngắn')
    plt.plot(light_duration_d1.universe, light_duration_d1['short'].mf, 'g', linewidth=1.5, label='Ngắn')
    plt.plot(light_duration_d1.universe, light_duration_d1['medium'].mf, 'r', linewidth=1.5, label='Trung bình')
    plt.plot(light_duration_d1.universe, light_duration_d1['long'].mf, 'g', linewidth=1.5, label='Dài')
    plt.plot(light_duration_d1.universe, light_duration_d1['very_long'].mf, 'b', linewidth=1.5, label='Rất dài')
    plt.title('Hàm liên thuộc tập mờ thời gian đèn xanh D1/D2')
    plt.ylabel('Độ phụ thuộc (%)')
    plt.xlabel('Thời gian đèn xanh')
    plt.legend()
    plt.show()


l1, l2 = estimate_light_time(17, 20, 9, 16)
print('Direction1-3: ', l1)
print('Direction2-4: ', l2)

# print_input_triangular_fuzzy_number()
# print_output_triangular_fuzzy_number()
