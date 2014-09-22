# -*- coding:utf-8 -*-
import argparse
import time
import math
import random
import fuzzy_ia
from robotsoccer import SoccerClient

def parse_host_port():
    parser = argparse.ArgumentParser(description="A robotsoccer player")
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--port', type=int, default=1024)
    parser.add_argument('--ia', default='dummy')
    args = parser.parse_args()
    global choice
    choice = args.ia
    return args.host, args.port

host, port = parse_host_port()
print("Iniciando conexão com o host %s, na porta %s" %  (host,port))

sc = SoccerClient()
sc.connect(host, port)

def normalize(angle):
    if angle < -math.pi:
        angle += 2*math.pi
    elif angle > math.pi:
        angle -= 2*math.pi
    elif angle < -math.pi/2:
        angle = -math.pi/2
    elif angle > math.pi/2:
        angle = math.pi/2
    return angle


def ball_angle():
    n= math.degrees(normalize(sc.get_ball_angle()))
    return n

def target_angle():
    n=  math.degrees(normalize(sc.get_target_angle()))
    return n

IA = {
    'dummy': lambda: angle_to_left_right_force(random.uniform(-math.pi,math.pi)),
    'ball_freak': lambda: angle_to_left_right_force(sc.get_ball_angle()),
    'fuzzy': lambda: unicycle_model(fuzzy_ia.decide(target_angle(), ball_angle())),
    'fixed': lambda: (.5,1)
}

def angle_to_left_right_force(angle):
    return (math.cos(angle) - math.sin(angle), math.cos(angle)+math.sin(angle))

def unicycle_model(angle):
    angle = math.radians(angle)/4.0
    print angle
    return 0.5, 0.5+angle

while True:
    ia_choice = IA[choice]()
    force_left_motor, force_right_motor = ia_choice
    sc.act(force_left_motor, force_right_motor)
