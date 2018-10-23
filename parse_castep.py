import numpy as np

def get_ev_from_line(line):
	return float(line.split("=")[1].split("e")[0])

def parse_castep(filename):
	contents = open(filename).read()
	ret = {}
	
	ret["0K energies"] = []
	ret["volumes"] = []

	for line in contents.split("\n"):
		line = line.lower()
		if "nb est. 0k energy" in line:
			ret["0K energies"].append(get_ev_from_line(line))
			continue
		if "total number of ions in cell" in line:
			ret["ions in cell"] = int(line.split("=")[1])
		if "lbfgs: final enthalpy" in line:
			ret["LBFGS final enthalpy"] = get_ev_from_line(line)
		if "cell volume" in line:
			ret["volumes"].append(float(line.split("=")[1].split("a")[0]))

	ret["final volume"] = ret["volumes"][-1]
	return ret

def parse_cell(filename):
	contents = open(filename).read()
	ret = {}
	
	pos_abs_start_index  = None
	pos_abs_end_index    = None
	pos_frac_start_index = None
	pos_frac_end_index   = None

	lines = [l.lower() for l in contents.split("\n")]
	for i in range(0,len(lines)):
		line = lines[i]
		if "%block" in line:
			if "lattice_cart" in line:
				if len(lines[i+1].split()) != 3:
					i += 1
				ret["lattice a"] = np.array([float(x) for x in lines[i+1].split()])
				ret["lattice b"] = np.array([float(x) for x in lines[i+2].split()])
				ret["lattice c"] = np.array([float(x) for x in lines[i+3].split()])
				continue
			if "positions_abs" in line:
				pos_abs_start_index = i+1
				continue
			if "positions_frac" in line:
				pos_frac_start_index = i+1
				continue

		if "%endblock" in line:
			if "positions_abs" in line:
				pos_abs_end_index = i
				continue
			if "positions_frac" in line:
				pos_frac_end_index = i
				continue
	
	atoms = []		
	if pos_abs_start_index != None:
		for i in range(pos_abs_start_index, pos_abs_end_index):
			a,x,y,z = lines[i].split()
			atoms.append([a,np.array([float(x),float(y),float(z)])])
	elif pos_frac_start_index != None:
		for i in range(pos_frac_start_index, pos_frac_end_index):
			a,x,y,z = lines[i].split()
			atoms.append([a,ret["lattice a"]*float(x) +
					ret["lattice b"]*float(y) +
					ret["lattice c"]*float(z)])
	ret["atoms"] = atoms
	return ret
