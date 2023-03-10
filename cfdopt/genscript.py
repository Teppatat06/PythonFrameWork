import os
import numpy as np

def gen_duct_in_script(number_of_blade,parent_dir,seed):
    script_dir = parent_dir+"script\\"
    ductIn_dir=parent_dir+"ductIn\\"
    ductIn_w_dir = ductIn_dir.replace("\\","/")
    try:
        os.mkdir(ductIn_dir)
    except FileExistsError:
        print("Warning!!: A design directory already exists")
    with open(script_dir+"macroduct_in.rpl", "r") as text:
        text_data = text.readlines()
    for n in number_of_blade:
        icem_script = f'macroduct_in{n}.rpl'
        with open(f'{ductIn_dir}{icem_script}', "w") as textdesign:
            i = 0
            input_line = [5,687,688,699,700,701, 712, 713]
            for command_line in text_data:
                i += 1
                if i in input_line:
                    if i == input_line[0]:
                        new_var = str(n)
                        command_line_modify = command_line.replace('PYTHON_VARIABLE', new_var)
                    elif i == input_line[1]:
                        new_path = f'{ductIn_w_dir}hex{n}.uns'
                        command_line_modify = command_line.replace('PYTHON_PATH',new_path)
                    elif i == input_line[2]:
                        new_path = f'{ductIn_w_dir}hex{n}.uns'
                        command_line_modify = command_line.replace('PYTHON_PATH',new_path)
                    elif i == input_line[3]:
                        new_path = f'{ductIn_w_dir}ansys{n}.fbc'
                        command_line_modify = command_line.replace('PYTHON_PATH', new_path)
                    elif i == input_line[4]:
                        new_path = f'{ductIn_w_dir}ansys{n}.atr'
                        command_line_modify = command_line.replace('PYTHON_PATH', new_path)
                    elif i == input_line[5]:
                        new_dir = ductIn_w_dir[:-1]
                        command_line_modify = command_line.replace('PYTHON_PATH', new_dir)
                    elif i == input_line[6]:
                        new_path = f'{ductIn_w_dir}project{n}.prj'
                        command_line_modify = command_line.replace('PYTHON_PATH', new_path)
                        command_line_modify = command_line_modify.replace('PYTHON_NAME', f'project{n}')
                    elif i == input_line[7]:
                        new_path = f'{ductIn_w_dir}projectICEM{n}in.cfx5'
                        command_line_modify = command_line.replace('PYTHON_PATH', new_path)
                        command_line_modify = command_line_modify.replace('PYTHON_NAME', f'project{n}')
                elif i in [702,704,706, 710, 711]: # Replace PYTHON_NAME
                    command_line_modify = command_line.replace('PYTHON_NAME', f'project{n}')
                else:
                    command_line_modify = command_line
                textdesign.write(command_line_modify)

def gen_duct_out_script(number_of_blade,parent_dir,seed):
    script_dir = parent_dir+"script\\"
    ductOut_dir =parent_dir+"ductOut\\"
    ductOut_w_dir = ductOut_dir.replace("\\","/")
    try:
        os.mkdir(ductOut_dir)
    except FileExistsError:
        print("Warning!!: A design directory already exists")
    with open(script_dir+"macroduct_out.rpl", "r") as text:
        text_data = text.readlines()
    for n in number_of_blade:
        icem_script = f'macroduct_out{n}.rpl'
        with open(f'{ductOut_dir}{icem_script}', "w") as textdesign:
            i = 0
            input_line = [5,687,688,699,700,701, 712, 713]
            for command_line in text_data:
                i += 1
                if i in input_line:
                    if i == input_line[0]:
                        new_var = str(n)
                        command_line_modify = command_line.replace('PYTHON_VARIABLE', new_var)
                    elif i == input_line[1]:
                        new_path = f'{ductOut_w_dir}hex{n}.uns'
                        command_line_modify = command_line.replace('PYTHON_PATH',new_path)
                    elif i == input_line[2]:
                        new_path = f'{ductOut_w_dir}hex{n}.uns'
                        command_line_modify = command_line.replace('PYTHON_PATH',new_path)
                    elif i == input_line[3]:
                        new_path = f'{ductOut_w_dir}ansys{n}.fbc'
                        command_line_modify = command_line.replace('PYTHON_PATH', new_path)
                    elif i == input_line[4]:
                        new_path = f'{ductOut_w_dir}ansys{n}.atr'
                        command_line_modify = command_line.replace('PYTHON_PATH', new_path)
                    elif i == input_line[5]:
                        new_dir = ductOut_w_dir[:-1]
                        command_line_modify = command_line.replace('PYTHON_PATH', new_dir)
                    elif i == input_line[6]:
                        new_path = f'{ductOut_w_dir}project{n}.prj'
                        command_line_modify = command_line.replace('PYTHON_PATH', new_path)
                        command_line_modify = command_line_modify.replace('PYTHON_NAME', f'project{n}')
                    elif i == input_line[7]:
                        new_path = f'{ductOut_w_dir}projectICEM{n}out.cfx5'
                        command_line_modify = command_line.replace('PYTHON_PATH', new_path)
                        command_line_modify = command_line_modify.replace('PYTHON_NAME', f'project{n}')
                elif i in [702,704,706, 710, 711]: # Replace PYTHON_NAME
                    command_line_modify = command_line.replace('PYTHON_NAME', f'project{n}')
                else:
                    command_line_modify = command_line
                textdesign.write(command_line_modify)

def gen_turbogrid_script(sampling_number_of_blade,parent_dir,seed):
    script_dir = parent_dir + "script\\"
    tg_dir = parent_dir + "tg\\"
    tg_w_dir = tg_dir.replace("\\", "/")
    curve_dir = parent_dir + "curve\\"
    curve_w_dir = curve_dir.replace("\\", "/")
    geo_dir = parent_dir + "geometry\\"
    geo_w_dir = geo_dir.replace("\\", "/")
    try:
        os.mkdir(tg_dir)
    except FileExistsError:
        print("Warning!!: A design directory already exists")
    with open(script_dir + "turbogrid_mesh.tse", "r") as text:
        text_data = text.readlines()
    index_design = 0
    for n in sampling_number_of_blade:
        turbo_script = f'turbogrid_mesh{index_design}.tse'
        with open(f'{tg_dir}{turbo_script}', "w") as textdesign:
            i = 0
            input_line = [22,26,33,42,43,396,397]
            for command_line in text_data:
                i += 1
                if i in input_line:
                    if i == input_line[0]:
                        new_var = str(n)
                        command_line_modify = command_line.replace('PYTHON_VARIABLE', new_var)
                    elif i == input_line[1]:
                        new_path = f'{geo_w_dir}'
                        command_line_modify = command_line.replace('PYTHON_PATH', new_path)
                    elif i == input_line[2]:
                        new_path = f'{geo_w_dir}'
                        command_line_modify = command_line.replace('PYTHON_PATH', new_path)
                    elif i == input_line[3]:
                        new_path = f'{curve_w_dir}'
                        command_line_modify = command_line.replace('PYTHON_PATH', new_path)    
                    elif i == input_line[4]:
                        command_line_modify = command_line.replace('INDEX', str(index_design))
                    elif i == input_line[5]:
                        new_path = f'{tg_w_dir}'
                        command_line_modify = command_line.replace('PYTHON_SAVE_PATH', new_path)
                    elif i == input_line[6]:
                        command_line_modify = command_line.replace('INDEX', str(index_design))
                else:
                    command_line_modify = command_line
                textdesign.write(command_line_modify)
        index_design += 1

def gen_cfxpre_script(parent_dir,seed):
    script_dir = parent_dir + "script\\"
    cfxpre_dir = parent_dir + "cfxpre\\"
    cfxpre_w_dir = cfxpre_dir.replace("\\", "/")
    geo_dir = parent_dir + "geometry\\"
    geo_w_dir = geo_dir.replace("\\", "/")
    tg_dir = parent_dir + "tg\\"
    tg_w_dir = tg_dir.replace("\\", "/")
    ductin_dir = parent_dir + "ductIn\\"
    ductin_w_dir = ductin_dir.replace("\\", "/")
    ductout_dir = parent_dir + "ductOut\\"
    ductout_w_dir = ductout_dir.replace("\\", "/")
    all_designs = np.genfromtxt(parent_dir+"allDesigns.csv", delimiter=",", dtype=float,names=True)
    try:
        os.mkdir(cfxpre_dir)
    except FileExistsError:
        print("Warning!!: A design directory already exists")
    with open(script_dir + "cfxpre_macro.pre", "r") as text:
        text_data = text.readlines()
    index_design = 0
    for n in range(seed):
        cfxpre_script = f'cfxpre_macro{index_design}.pre'
        with open(f'{cfxpre_dir}{cfxpre_script}', "w") as textdesign:
            i = 0
            input_line = [11, 50, 132, 167, 186, 209, 210, 211, 212, 509, 602, 689, 776, 1095]
            for command_line in text_data:
                i += 1
                if i in input_line:
                    if i == input_line[0]:
                        new_path = f'{geo_w_dir}FAN_BLADE.gtm'
                        command_line_modify = command_line.replace('PYTHON_PATH_FAN_BLADE', new_path)
                    elif i == input_line[1]:
                        new_path = f'{tg_w_dir}CFXPRE_{all_designs["Design"][n]:.0f}.gtm'
                        command_line_modify = command_line.replace('PYTHON_PATH_GV', new_path)
                    elif i == input_line[2]:
                        new_path = f'{tg_w_dir}CFXPRE_{all_designs["Design"][n]:.0f}.gtm'
                        command_line_modify = command_line.replace('PYTHON_PATH_GV', new_path)
                    elif i == input_line[3]:
                        new_path = f'{ductin_w_dir}projectICEM{all_designs["N_Blade"][n]:.0f}in.cfx5'
                        command_line_modify = command_line.replace('PYTHON_PATH_DUCTIN', new_path)
                    elif i == input_line[4]:
                        new_path = f'{ductout_w_dir}projectICEM{all_designs["N_Blade"][n]:.0f}out.cfx5'
                        command_line_modify = command_line.replace('PYTHON_PATH_DUCTOUT', new_path)
                    elif i == input_line[5]:
                        new_ver = f'{all_designs["N_Blade"][n]:.0f}'
                        command_line_modify = command_line.replace('PYTHON_VARIABLE', new_ver)
                    elif i == input_line[6]:
                        new_ver = f'{all_designs["N_Blade"][n]:.0f}'
                        command_line_modify = command_line.replace('PYTHON_VARIABLE', new_ver)
                    elif i == input_line[7]:
                        new_ver = f'{all_designs["N_Blade"][n]:.0f}'
                        command_line_modify = command_line.replace('PYTHON_VARIABLE', new_ver)
                    elif i == input_line[8]:
                        new_ver = f'{all_designs["N_Blade"][n]:.0f}'
                        command_line_modify = command_line.replace('PYTHON_VARIABLE', new_ver)
                    elif i == input_line[9]:
                        new_ver = f'{all_designs["N_Blade"][n]:.0f}'
                        command_line_modify = command_line.replace('PYTHON_VARIABLE', new_ver)
                    elif i == input_line[10]:
                        new_ver = f'{all_designs["N_Blade"][n]:.0f}'
                        command_line_modify = command_line.replace('PYTHON_VARIABLE', new_ver)
                    elif i == input_line[11]:
                        new_ver = f'{all_designs["N_Blade"][n]:.0f}'
                        command_line_modify = command_line.replace('PYTHON_VARIABLE', new_ver)
                    elif i == input_line[12]:
                        new_ver = f'{all_designs["N_Blade"][n]:.0f}'
                        command_line_modify = command_line.replace('PYTHON_VARIABLE', new_ver)
                    elif i == input_line[13]:
                        new_path = f'{cfxpre_w_dir}cfxsolveinput{all_designs["Design"][n]:.0f}.def'
                        command_line_modify = command_line.replace('PYTHON_PATH', new_path)
                else:
                    command_line_modify = command_line
                textdesign.write(command_line_modify)
        index_design += 1
#def gen_cfxpre_script(parent_dir):
#    with open(parent_dir+'allDesign.csv', 'r') as file:
#    csv_reader = csv.reader(file)
#    next(csv_reader)  # Skip the header line
#    for row in csv_reader:
        # Process the data row by row