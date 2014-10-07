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
    return args.host, args.port, args.ia

host, port, choice = parse_host_port()
print("Iniciando conexão com o host %s, na porta %s" %  (host,port))

sc = SoccerClient()
sc.connect(host, port)

def ball_angle():
    "Numerical manibulations on ball angle"
    return int(math.floor(math.degrees(sc.get_ball_angle())))

def target_angle():
    "Numerical manibulations on target angle"
    return int(math.floor(math.degrees(sc.get_target_angle())))

def spin():
    "Numerical manibulations on vehicle spin"
    print(sc.get_spin())
    return int(math.floor(math.degrees(sc.get_spin())))

IA = {
    'dummy': lambda: angle_to_left_right_force(random.uniform(-math.pi,math.pi)),
    'ball_freak': lambda: angle_to_left_right_force(sc.get_ball_angle()),
    'fuzzy': lambda: fuzzy_ia.next_action(target_angle(), ball_angle(), spin()),
    'fixed': lambda: (.5,1)
}

def angle_to_left_right_force(angle):
    return (math.cos(angle) - math.sin(angle), math.cos(angle)+math.sin(angle))

def unicycle_model(angle):
    print "Target angle: %s" % angle
    return (angle+180.0)/720.0,(-angle+180.0)/720.0

while True:
    ia_choice = IA[choice]()
    force_left_motor, force_right_motor = ia_choice
    sc.act(force_left_motor, force_right_motor)
