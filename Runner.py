
class Runner:

    def __init__(self, name, age, height, weight):
        self.name = name
        self.age = age
        self.height = height
        self. weight = weight


def stats(age, weight, height):

    if age > 55:
        ap_max = 185 - age
        ap_min = ap_max * 0.9
    elif age < 25:
        ap_max = 175 - age
        ap_min = ap_max * 0.9
    else:
        ap_max = 180 - age
        ap_min = ap_max * 0.9

    bmi = weight / (height * height)

    if bmi > 25:
        bmi_score = 1.1
    elif 25 > bmi > 20:
        bmi_score = 1.0
    else:
        bmi_score = 0.9

    return int(ap_min), ap_max, bmi_score
