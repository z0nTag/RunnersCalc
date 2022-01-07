
import math


class Calculate:

    def __init__(self):
        pass


def calc_score(ap_max, bpm, score, distance_km, pace, time, spm, bmi_score):

    base_score = (math.sqrt(ap_max) / math.sqrt(bpm)) / math.sqrt(bpm) * score
    total_score = base_score * (distance_km / pace) * (distance_km / time) * (math.sqrt(spm) * bmi_score)
    final_score = math.sqrt(total_score)

    return final_score, total_score

