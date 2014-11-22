# coding: utf-8
import argparse
import math
import random
import fuzzy_ia
import csv
from robotsoccer import SoccerClient


def ball_angle():
    """
    Numerical manipulations on ball angle
    """
    return -int(math.floor(math.degrees(sc.get_ball_angle())))


def target_angle():
    """
    Numerical manipulations on target angle
    """
    return int(math.floor(math.degrees(sc.get_target_angle())))


def int_repr(i):
    """
    String representation of force instensity
    """
    return '*' * int(math.floor(i / .1))


def angle_repr(angle):
    """
    String representation of angle
    """
    if angle < 0: return '<'
    elif angle > 0: return '>'
    else: return '^'


def parse_host_port():
    """
    Command line argument parser
    """
    parser = argparse.ArgumentParser(description="A robotsoccer player")
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--port', type=int, default=1024)
    parser.add_argument('--ia', default='fuzzy')
    args = parser.parse_args()
    return args.host, args.port, args.ia


def save_output(*data):
    """
    Writes output to a file
    """
    with open('output.csv', 'w') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(data)


host, port, choice = parse_host_port()
print("Iniciando conexão com o host %s, na porta %s" %  (host,port))

sc = SoccerClient()
sc.connect(host, port)

IA = {
    'fuzzy': lambda t, b, s: fuzzy_ia.next_action(t, b, s),
    'spin': lambda t, b, s: (2., -2.),
    'str8': lambda t, b, s: (0., 0.),
    'crazy': lambda t, b, s: (1., 1.),
}

def print_info(l, r):
    print("raw_target_angle: %f raw_ball_angle: %f" % (sc.get_target_angle(),
                                                       sc.get_ball_angle()))
    print("target_angle: %d ball_angle: %d left: %f right: %f" % (target_angle(),
                                                                  ball_angle(),
                                                                  l, r))
    print("left: [%s], right: [%s]" % (int_repr(l), int_repr(r)))
    print("target: [%s], ball: [%s]" % (angle_repr(target_angle()),
          angle_repr(ball_angle())))

while True:
    l, r = IA[choice](target_angle(), ball_angle(), None)
    print_info(l,r)
    save_output(target_angle(), ball_angle(), l ,r)
    sc.act(l, r)
