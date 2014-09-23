# -*- coding:utf-8 -*-
import random
import numpy as np
import skfuzzy as fuzz
import math

RESOLUTION = 1 
SPAN = 360/RESOLUTION
n_domain = np.arange(-180,180,RESOLUTION)
print(SPAN)

E_input = fuzz.trimf(n_domain, [-180, -180, 0])
F_input = fuzz.trimf(n_domain, [-90, 0, 90])
D_input = fuzz.trimf(n_domain, [0, 180, 180])

n_force_domain = np.arange(0,1,1.0/360.0)
intensity_L = fuzz.trimf(n_force_domain, [0,0,0.5])
intensity_H = fuzz.trimf(n_force_domain, [0.5,1,1])

R_Left = lambda x1,x2: reduce(np.fmax,[
    np.fmin(np.tile(np.min([E_input[x1],E_input[x2]]),360),intensity_L),
    np.fmin(np.tile(np.min([E_input[x1],F_input[x2]]),360),intensity_L),
    np.fmin(np.tile(np.min([E_input[x1],D_input[x2]]),360),intensity_L),
    np.fmin(np.tile(np.min([F_input[x1],E_input[x2]]),360),intensity_H),
    np.fmin(np.tile(np.min([F_input[x1],F_input[x2]]),360),intensity_H),
    np.fmin(np.tile(np.min([F_input[x1],D_input[x2]]),360),intensity_L),
    np.fmin(np.tile(np.min([D_input[x1],E_input[x2]]),360),intensity_H),
    np.fmin(np.tile(np.min([D_input[x1],F_input[x2]]),360),intensity_H),
    np.fmin(np.tile(np.min([D_input[x1],D_input[x2]]),360),intensity_H)
])

R_Right = lambda x1,x2: reduce(np.fmax,[
    np.fmin(np.tile(np.min([E_input[x1],E_input[x2]]),360),intensity_H),
    np.fmin(np.tile(np.min([E_input[x1],F_input[x2]]),360),intensity_H),
    np.fmin(np.tile(np.min([E_input[x1],D_input[x2]]),360),intensity_H),
    np.fmin(np.tile(np.min([F_input[x1],E_input[x2]]),360),intensity_L),
    np.fmin(np.tile(np.min([F_input[x1],F_input[x2]]),360),intensity_H),
    np.fmin(np.tile(np.min([F_input[x1],D_input[x2]]),360),intensity_H),
    np.fmin(np.tile(np.min([D_input[x1],E_input[x2]]),360),intensity_L),
    np.fmin(np.tile(np.min([D_input[x1],F_input[x2]]),360),intensity_L),
    np.fmin(np.tile(np.min([D_input[x1],D_input[x2]]),360),intensity_L)
])

def decide(target_angle, ball_angle):
  target_angle = int(math.floor(target_angle))
  ball_angle = int(math.floor(ball_angle))
  return fuzz.defuzz(n_force_domain, R_Left(ball_angle,target_angle), 'centroid'), fuzz.defuzz(n_force_domain, R_Right(ball_angle,target_angle), 'centroid')
