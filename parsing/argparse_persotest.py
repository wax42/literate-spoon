import argparse

parser = argparse.ArgumentParser()

# default : valuer par default
# choices : restreindre les choix possible
# nargs : nombre de choix
# action='store_tue' | no argument after
# required=True | obligatoire

parser.add_argument('-f', nargs=1, help="input file", required=True)
parser.add_argument('-e', '--heuristique', nargs=1, choices=['coucou', 'john', 'her'], default="coucou", help='choose an heuristique')
parser.add_argument('--save', nargs=1, help='save in file data result')
parser.add_argument('--stats', action='store_true', help="show stats")
parser.add_argument('--graphics', action='store_true', help="launch graphic mode(tkinter)")
#parser.add_argument('--foo', nargs=2)#

args = parser.parse_args()

print(args)
print(args.f)
