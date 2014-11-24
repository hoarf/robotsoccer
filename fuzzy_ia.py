# coding: utf-8
import random
import numpy as np
import skfuzzy as fuzz
import math

RESOLUTION = 360.0

"""
The Linespaces used in the fuzzy sets

    angle_dmn: angle in degrees domain of fuzzy sets
"""
angle_dmn = np.arange(-180,180,1)

"""
Fuzzy Sets Declarations
"""
L  = fuzz.trapmf(angle_dmn, [-180, -180, -180, 0])
F_narrow = fuzz.trimf(angle_dmn,  [-100, 0, 100])
F = fuzz.trimf(angle_dmn, [-180, 0, 180])
R = fuzz.trapmf(angle_dmn, [0, 180, 180, 180])

def fuzzy_and(t, b, fuzzy_set):
    """
    Calculates the 'AND' fuzzy operator, which is finding the minimum
    value on the sets and tiling it (making it a constant line)
    """
    candidates = []
    # if t: candidates.append(t)
    if b: candidates.append(b)
    if candidates:
        return np.fmin(np.tile(np.min(candidates), RESOLUTION), fuzzy_set)
    else:
        np.tile(.0, RESOLUTION)

"""
Output angle's transfer function
"""
output_function = lambda t, b, s: reduce(np.fmax,[
    fuzzy_and(L[angle_dmn == b],        L[angle_dmn == t],        F),
    fuzzy_and(L[angle_dmn == b],        F_narrow[angle_dmn == t], L),
    fuzzy_and(L[angle_dmn == b],        R[angle_dmn == t],        L),
    fuzzy_and(F_narrow[angle_dmn == b], L[angle_dmn == t],        R),
    fuzzy_and(F_narrow[angle_dmn == b], F_narrow[angle_dmn == t], F),
    fuzzy_and(F_narrow[angle_dmn == b], R[angle_dmn == t],        L),
    fuzzy_and(R[angle_dmn == b],        L[angle_dmn == t],        R),
    fuzzy_and(R[angle_dmn == b],        F_narrow[angle_dmn == t], R),
    fuzzy_and(R[angle_dmn == b],        R[angle_dmn == t],        F)
])

def next_action(t, b, s):
    """
    ¦  t: target angle
    ¦  b: ball angle
    ¦  s: spin
    """
    output = fuzz.defuzz(angle_dmn, output_function(t, b, s), 'centroid')
    outputrad = math.radians(output)
    cos_output = math.cos(outputrad)
    sin_output = math.sin(outputrad)
    return cos_output, sin_output

