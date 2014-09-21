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

IA = {
    'dummy': lambda: random.uniform(-math.pi,math.pi),
    'ball_freak': lambda: sc.get_ball_angle(),
    'fuzzy': lambda: fuzzy_ia.decide(sc.get_target_angle(), sc.get_ball_angle())
}

def angle_to_left_right_force(angle):
    return (math.cos(angle) - math.sin(angle), math.cos(angle)+math.sin(angle))

while True:
    ia_choice = IA[choice]()
    print("B: %f, T: %f, angle: %f" % (
        math.degrees(sc.get_ball_angle()),
        math.degrees(sc.get_target_angle()),
        ia_choice))
    force_left_motor, force_right_motor = angle_to_left_right_force(ia_choice)
    sc.act(force_left_motor, force_right_motor)
