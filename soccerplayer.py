import argparse
from robotsoccer import SoccerClient

def parse_host_port():
    parser = argparse.ArgumentParser(description="A robotsoccer player")
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--port', type=int, default=1024)
    args = parser.parse_args()
    return args.host, args.port

print parse_host_port()
