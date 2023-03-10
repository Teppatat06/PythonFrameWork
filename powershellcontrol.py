import subprocess

def check_license(software_exe):
	license_check = True
	while license_check:
			processes = subprocess.check_output(['tasklist']).decode()
			if software_exe in processes:
				pass
			else:
				license_check = False
				print(f'{software_exe} license software is available.')


def icem_duct_in(number_of_blade):
	for n_blade in number_of_blade:
		duct_in_dir = f'{parent_dir}\\ductIn\\macroduct_in{n_blade}.rpl'
		subprocess.Popen(f'"C:\\Program Files\\ANSYS Inc\\v201\\icemcfd\\win64_amd\\bin\\med_batch.exe" -batch -script "{duct_in_dir}"')
		check_license("med_batch.exe")

def icem_duct_out(number_of_blade):
	for n_blade in number_of_blade:
		duct_out_dir = f'{parent_dir}\\ductOut\\macroduct_Out{n_blade}.rpl'
		subprocess.Popen(f'"C:\\Program Files\\ANSYS Inc\\v201\\icemcfd\\win64_amd\\bin\\med_batch.exe" -batch -script "{duct_out_dir}"')
		check_license("med_batch.exe")

def turbogrid(seed):
	for index in range(seed):
		tg_dir = f'{parent_dir}\\tg\\turbogrid_mesh{index}.tse'
		subprocess.Popen(f'"C:\\Program Files\\ANSYS Inc\\v201\\TurboGrid\\bin\\cfxtg.exe" -batch "{tg_dir}"')
		check_license("cfxtg.exe")

def cfxpre(seed):
	for index in range(seed):
		cfxpre_dir = f'{parent_dir}\\cfxpre\\cfxpre_macro{index}.pre'
		subprocess.Popen(f'"C:\\Program Files\\ANSYS Inc\\v201\\CFX\\bin\\cfx5pre.exe" -batch "{cfxpre_dir}"')
		check_license("cfx5pre.exe")

def cfxsolve(cfxsolveinput,np):
	cfxinputsolve_dir = f'{parent_dir}\\cfxpre\\{cfxsolveinput}'
	cfxsolve_env_dir = f'{parent_dir}\\cfxsolve\\'
	subprocess.Popen(f'#"C:\\Program Files\\ANSYS Inc\\v201\\CFX\\bin\\cfx5solve.exe" -batch -double -par-local -part {np} -chdir "{cfxsolve_env_dir}" -def "{cfxinputsolve_dir}"')
	check_license("cfx5pre.exe")

global parent_dir 
parent_dir = "E:\\Pun\\GV\\OptV2"
number_of_blade = [3, 5, 7, 11, 13]
seed = 15
np = 30
icem_duct_in(number_of_blade)
icem_duct_out(number_of_blade)
turbogrid(seed)
cfxpre(seed)

for i in range(seed):
	## Solve
	cfxsolveinput = f'cfxsolveinput{i}.def'
	cfxsolve(cfxsolveinput,np)
	## Post

	## Write output data



#CFX-Pre Batch
#"C:\Program Files\ANSYS Inc\v201\CFX\bin\cfx5pre.exe" -batch "E:\Pun\GV\OptV2\script\cfxpre_macro.pre"

#CFX-Solve Batch
#"C:\Program Files\ANSYS Inc\v201\CFX\bin\cfx5solve.exe" -batch -double -par-local -part 30 -chdir "E:\Pun\GV\OptV2\cfxsolve" -def "E:\Pun\GV\OptV2\cfxpre\cfxsolveinput01.def"