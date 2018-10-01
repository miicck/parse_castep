def get_ev_from_line(line):
	return float(line.split("=")[1].split("e")[0])

def parse(contents):
	ret = {}
	
	ret["0K energies"] = []

	for line in contents.split("\n"):
		if "NB est. 0K energy" in line:
			ret["0K energies"].append(get_ev_from_line(line))
			continue
		if "Total number of ions in cell" in line:
			ret["ions in cell"] = int(line.split("=")[1])
		if "LBFGS: Final Enthalpy" in line:
			ret["LBFGS final enthalpy"] = get_ev_from_line(line)

	return ret
