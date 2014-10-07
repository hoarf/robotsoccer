# coding:utf-8
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

n_intensity_domain = np.arange(0,1,1.0/360.0)
intensity_L = fuzz.trimf(n_intensity_domain, [0,0,0.5])
intensity_H = fuzz.trimf(n_intensity_domain, [0.5,1,1])

R_Left = lambda ball_angle, target_angle, spin: reduce(np.fmax,[
    np.fmin(np.tile(np.min([E_input[ball_angle],E_input[target_angle]]),360),intensity_L),
    np.fmin(np.tile(np.min([E_input[ball_angle],F_input[target_angle]]),360),intensity_L),
    np.fmin(np.tile(np.min([E_input[ball_angle],D_input[target_angle]]),360),intensity_L),
    np.fmin(np.tile(np.min([F_input[ball_angle],E_input[target_angle]]),360),intensity_H),
    np.fmin(np.tile(np.min([F_input[ball_angle],F_input[target_angle]]),360),intensity_H),
    np.fmin(np.tile(np.min([F_input[ball_angle],D_input[target_angle]]),360),intensity_L),
    np.fmin(np.tile(np.min([D_input[ball_angle],E_input[target_angle]]),360),intensity_H),
    np.fmin(np.tile(np.min([D_input[ball_angle],F_input[target_angle]]),360),intensity_H),
    np.fmin(np.tile(np.min([D_input[ball_angle],D_input[target_angle]]),360),intensity_H),
    np.fmin(intensity_L[spin], intensity_H),
    np.fmin(intensity_H[spin], intensity_L)
])

R_Right = lambda ball_angle, target_angle, spin: reduce(np.fmax,[
    np.fmin(np.tile(np.min([E_input[ball_angle],E_input[target_angle]]),360),intensity_H),
    np.fmin(np.tile(np.min([E_input[ball_angle],F_input[target_angle]]),360),intensity_H),
    np.fmin(np.tile(np.min([E_input[ball_angle],D_input[target_angle]]),360),intensity_H),
    np.fmin(np.tile(np.min([F_input[ball_angle],E_input[target_angle]]),360),intensity_L),
    np.fmin(np.tile(np.min([F_input[ball_angle],F_input[target_angle]]),360),intensity_H),
    np.fmin(np.tile(np.min([F_input[ball_angle],D_input[target_angle]]),360),intensity_H),
    np.fmin(np.tile(np.min([D_input[ball_angle],E_input[target_angle]]),360),intensity_L),
    np.fmin(np.tile(np.min([D_input[ball_angle],F_input[target_angle]]),360),intensity_L),
    np.fmin(np.tile(np.min([D_input[ball_angle],D_input[target_angle]]),360),intensity_L),
    np.fmin(intensity_L[spin], intensity_H),
    np.fmin(intensity_H[spin], intensity_L)

])

def next_action(target_angle, ball_angle, spin):
  return fuzz.defuzz(n_intensity_domain, R_Left(ball_angle,target_angle, spin), 'centroid'), fuzz.defuzz(n_intensity_domain, R_Right(ball_angle,target_angle, spin), 'centroid')
