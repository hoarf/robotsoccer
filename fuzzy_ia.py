# coding: utf-8
import random
import numpy as np
import skfuzzy as fuzz
import math

RESOLUTION = 360.0
angle_dmn = np.arange(-180,180,1)
intensity_dmn = np.arange(0,1,1.0/RESOLUTION)

left_set = fuzz.trapmf(angle_dmn, [-180, -180, -100, 0])
front_set = fuzz.trimf(angle_dmn, [-60, 0, 60])
right_set = fuzz.trapmf(angle_dmn, [0, 100, 180, 180])
v_low_set = fuzz.trapmf(intensity_dmn, [0, 0, .1, .3])
v_high_set = fuzz.trapmf(intensity_dmn, [.7, .9, 1, 1])
med_set = fuzz.trimf(intensity_dmn, [.3,.5,.7])
low_set = fuzz.trimf(intensity_dmn, [.2,.3,.4])
high_set = fuzz.trimf(intensity_dmn, [.6,.7,.8])


def fuzzy_and(t, b, fuzzy_set):
    candidates = []
    if t: candidates.append(t)
    if b: candidates.append(b)
    if candidates:
        return np.fmin(np.tile(np.min(candidates), RESOLUTION), fuzzy_set)
    else:
        np.tile(0.0, RESOLUTION)

# left motor transfer function
left_tf = lambda t, b, s: reduce(np.fmax,[
    fuzzy_and(left_set[angle_dmn == b], left_set[angle_dmn == t], v_low_set),
    fuzzy_and(left_set[angle_dmn == b], front_set[angle_dmn == t], v_low_set),
    fuzzy_and(left_set[angle_dmn == b], right_set[angle_dmn == t], low_set),
    fuzzy_and(front_set[angle_dmn == b], left_set[angle_dmn == t], low_set),
    fuzzy_and(front_set[angle_dmn == b], front_set[angle_dmn == t], v_high_set),
    fuzzy_and(front_set[angle_dmn == b], right_set[angle_dmn == t], high_set),
    fuzzy_and(right_set[angle_dmn == b], left_set[angle_dmn == t], v_high_set),
    fuzzy_and(right_set[angle_dmn == b], front_set[angle_dmn == t], v_high_set),
    fuzzy_and(right_set[angle_dmn == b], right_set[angle_dmn == t], v_high_set)
])

# right motor transfer function
right_tf = lambda t, b, spin: reduce(np.fmax,[
    fuzzy_and(left_set[angle_dmn == b], left_set[angle_dmn == t], v_high_set),
    fuzzy_and(left_set[angle_dmn == b], front_set[angle_dmn == t], v_high_set),
    fuzzy_and(left_set[angle_dmn == b], right_set[angle_dmn == t], v_high_set),
    fuzzy_and(front_set[angle_dmn == b], left_set[angle_dmn == t], high_set),
    fuzzy_and(front_set[angle_dmn == b], front_set[angle_dmn == t], v_high_set),
    fuzzy_and(front_set[angle_dmn == b], right_set[angle_dmn == t], high_set),
    fuzzy_and(right_set[angle_dmn == b], left_set[angle_dmn == t], v_low_set),
    fuzzy_and(right_set[angle_dmn == b], front_set[angle_dmn == t], v_low_set),
    fuzzy_and(right_set[angle_dmn == b], right_set[angle_dmn == t], v_low_set)
])

def next_action(t, b, s):
    """
       t: target angle
       b: ball angle
       s: spin
    """
    intensity_left = fuzz.defuzz(intensity_dmn, left_tf(t, b, s), 'dcentroid')
    intensity_right = fuzz.defuzz(intensity_dmn, right_tf(t, b, s), 'dcentroid')
    return intensity_left, intensity_right
