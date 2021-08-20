# example script to just develop a parameter sweeping script

from sys import argv
import os

def main():
	s, m, l = argv[1:]
	print(s, m, l)
	# print("!")

if __name__ == '__main__':
	main()