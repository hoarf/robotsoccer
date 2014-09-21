# -*- coding:utf-8 -*-
import random
import numpy as np
import skfuzzy as fuzz
import math

RESOLUTION = .5
SPAN = 360/RESOLUTION
n_domain = np.arange(-180,180,RESOLUTION)

E_input = fuzz.trimf(n_domain, [-180, -180, 0])
F_input = fuzz.trimf(n_domain, [-90, 0, 90])
D_input = fuzz.trimf(n_domain, [0, 180, 180])

E_output = fuzz.trimf(n_domain, [-180, -180, 0])
F_output = fuzz.trimf(n_domain, [-180, 0, 180])
D_output = fuzz.trimf(n_domain, [0, 180, 180])

rel = lambda x1,x2: reduce(np.fmax,[
        np.fmin(np.tile(np.min([E_input[x1],E_input[x2]]),SPAN),F_output),
        np.fmin(np.tile(np.min([E_input[x1],F_input[x2]]),SPAN),E_output),
        np.fmin(np.tile(np.min([E_input[x1],D_input[x2]]),SPAN),E_output),
        np.fmin(np.tile(np.min([F_input[x1],E_input[x2]]),SPAN),D_output),
        np.fmin(np.tile(np.min([F_input[x1],F_input[x2]]),SPAN),F_output),
        np.fmin(np.tile(np.min([F_input[x1],D_input[x2]]),SPAN),E_output),
        np.fmin(np.tile(np.min([D_input[x1],E_input[x2]]),SPAN),D_output),
        np.fmin(np.tile(np.min([D_input[x1],F_input[x2]]),SPAN),D_output),
        np.fmin(np.tile(np.min([D_input[x1],D_input[x2]]),SPAN),F_output)

])

def decide(target_angle, ball_angle):
    target_angle = math.floor(target_angle)
    ball_angle = math.floor(ball_angle)
    return fuzz.defuzz(n_domain, rel(ball_angle,target_angle), 'centroid')
