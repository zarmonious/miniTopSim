
#Georg Mikula
#e11902119

import mini_topsim.parameters as par
import sys

params = par.load_parameters(sys.argv[1]);

counter = 0
for item in dir(par):
	if item in params.keys():
		counter = counter + 1

if(len(params) != counter):
	print("Error not all params are available")

with open(sys.argv[1] + ".out", "w") as out_file:
	out_file.write("[Parameters]\n")
	for key, param in params.items():
		out_file.write(str(key) + " = " + str(param) + "\n")
		print(str(key) + " = " + str(param))


