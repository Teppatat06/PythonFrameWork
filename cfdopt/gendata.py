import numpy as np
import matplotlib.pyplot as plt
import pyDOE2
import os

def sweep_profile(profile, sweep_angle, n_profile_point):
    # convert degree to redian
    angle = np.deg2rad(sweep_angle)

    # init parameter
    out_profile = np.zeros((len(profile), 3))
    center = [0 for i in range(int(len(profile) / n_profile_point))]
    offset_length = [0 for i in range(len(center))]

    # create center
    count = 0
    d_center = 0
    j = 0;
    for i in range(len(profile)):
        d_center += profile[i][0]
        count += 1
        if count == n_profile_point:
            center[j] = d_center / n_profile_point
            j += 1
            count = 0
            d_center = 0
        else:
            pass

    center -= center[0]

    # create offset length
    if sweep_angle != 90:
        for i in range(len(center)):
            if i != 0:
                offset_length[i] = center[i] / np.tan(angle)
            else:
                offset_length[i] = 0

    else:
        pass
    # sweep profile
    count = 0
    j = 0
    for i in range(len(profile)):
        out_profile[i][0] = profile[i][0]
        out_profile[i][1] = profile[i][1]
        out_profile[i][2] = profile[i][2] + offset_length[j]
        # print(f'{offset_length[j]:.3f}'+' + '+f'{profile[i][2]:.3f}'+' = '+f'{out_profile[i][2]:.3f}')
        count += 1
        if count == n_profile_point:
            count = 0
            j += 1
        else:
            pass

    return out_profile

def scale_profile(profile, scale):
    # init
    out_profile = np.zeros((len(profile), 3))
    # create scaling
    min_root = 0
    min_out_root = 0
    for i in range(len(profile)):
        out_profile[i][0] = profile[i][0]
        out_profile[i][1] = scale * profile[i][1]
        out_profile[i][2] = scale * profile[i][2]
        if i == 0 or profile[i][2] < min_root:
            min_root = profile[i][2]
        else:
            pass
        if i == 0 or out_profile[i][2] < min_out_root:
            min_out_root = out_profile[i][2]
        else:
            pass

    # offset to original leading edge
    for i in range(len(profile)):
        out_profile[i][2] -= min_out_root - min_root

    return out_profile

def project_profile(profile, radius, n_profile_point):
    out_profile = profile
    count = 0
    j = 0
    for i in range(len(out_profile)):
        out_profile[i][0] = (out_profile[i][0] / np.linalg.norm([out_profile[i][0], out_profile[i][1]])) * radius[j]
        out_profile[i][1] = (out_profile[i][1] / np.linalg.norm([out_profile[i][0], out_profile[i][1]])) * radius[j]
        count += 1
        if count == n_profile_point:
            count = 0
            j += 1
        else:
            pass
    return out_profile

def offset_profile(profile, hub,offset_distance):
    out_profile = profile
    offset_length = np.amin(out_profile, axis=0)[2] - hub[0][2]
    for i in range(len(profile)):
        out_profile[i][2] -= (offset_length - offset_distance)

    return out_profile

def save_out_profile_curve(profile, n_profile_point, index_seed, curve_dir):
    curve_path = curve_dir+'out_profile_design_'
    with open(curve_path + str(index_seed) + '.curve', 'w') as f:
        f.write('#point')
        f.write('\n')
        count = 0
        count_row = 0
        for line in profile:
            f.write(f'{line[0]:.6f}' + ' ' + f'{line[1]:.6f}' + ' ' + f'{line[2]:.6f}')
            f.write('\n')
            count += 1
            count_row += 1
            if count == n_profile_point and count_row != len(profile):
                f.write('\n')
                f.write('#point')
                f.write('\n')
                count = 0
            else:
                pass

    return 0

def save_out_profile_spaceclaim(profile, n_profile_point, index_seed):
    with open('out_profile_' + 'design_' + str(index_seed) + '.txt', 'w') as f:
        f.write('3d=true')
        f.write('\n')
        f.write('polyline=true')
        f.write('\n')
        f.write('fit=false')
        f.write('\n')
        f.write('fittol=0.01')
        f.write('\n')
        count = 0
        count_row = 0
        for line in profile:
            f.write(f'{line[0]:.6f}' + ' ' + f'{line[1]:.6f}' + ' ' + f'{line[2]:.6f}')
            f.write('\n')
            count += 1
            count_row += 1
            if count == n_profile_point and count_row != len(profile):
                f.write('\n')
                f.write('\n')
                count = 0
            else:
                pass

    return 0

def plot_profile(l_scale, u_scale, seed, sampling_number_of_blade, number_of_blade, \
                 sampling_scale, sampling_sweep_angle, \
                 hub_to_shroud,passage_domain_length,offset_distance):
    #  constraint
    sampling_chord = np.linspace(l_scale, u_scale, 50)
    sampling_l_sweep_angle = np.rad2deg(np.arctan(hub_to_shroud / (passage_domain_length - \
                                                                   (2 * offset_distance) - sampling_chord)))
    sampling_u_sweep_angle = np.rad2deg(np.pi-np.arctan(hub_to_shroud / (passage_domain_length - \
                                                                         (2 * offset_distance) - sampling_chord)))

    plt.plot(sampling_l_sweep_angle, sampling_chord, label="Lower Bound-Sweep Angle")
    plt.plot(sampling_u_sweep_angle, sampling_chord, label="Upper Bound-Sweep Angle")
    color_plot = [True for i in range(len(number_of_blade))]
    for i in range(seed):
        if sampling_number_of_blade[i] == number_of_blade[0]:
            if color_plot[0]:
                plt.plot(sampling_sweep_angle[i], sampling_scale[i], 'ob', label="N(Blade):" + str(number_of_blade[0]))
                color_plot[0] = False
            else:
                plt.plot(sampling_sweep_angle[i], sampling_scale[i], 'ob')
        elif sampling_number_of_blade[i] == number_of_blade[1]:
            if color_plot[1]:
                plt.plot(sampling_sweep_angle[i], sampling_scale[i], 'og', label="N(Blade):" + str(number_of_blade[1]))
                color_plot[1] = False
            else:
                plt.plot(sampling_sweep_angle[i], sampling_scale[i], 'og')
        elif sampling_number_of_blade[i] == number_of_blade[2]:
            if color_plot[2]:
                plt.plot(sampling_sweep_angle[i], sampling_scale[i], 'or', label="N(Blade):" + str(number_of_blade[2]))
                color_plot[2] = False
            else:
                plt.plot(sampling_sweep_angle[i], sampling_scale[i], 'or')
        elif sampling_number_of_blade[i] == number_of_blade[3]:
            if color_plot[3]:
                plt.plot(sampling_sweep_angle[i], sampling_scale[i], 'oc', label="N(Blade):" + str(number_of_blade[3]))
                color_plot[3] = False
            else:
                plt.plot(sampling_sweep_angle[i], sampling_scale[i], 'oc')
        else:
            if color_plot[4]:
                plt.plot(sampling_sweep_angle[i], sampling_scale[i], 'oy', label="N(Blade):" + str(number_of_blade[4]))
                color_plot[4] = False
            else:
                plt.plot(sampling_sweep_angle[i], sampling_scale[i], 'oy')

    plt.legend()
    plt.grid()
    plt.xlabel('Sweep Angle (Degree)')
    plt.ylabel('Chord (m)')
    plt.title('Feasible Design: HUB to SHROUD =' + f'{hub_to_shroud:.2f}' + ' m')
    plt.show()

def gen_sampling_data(seed, l_scale, u_scale, number_of_blade,hub_to_shroud,passage_domain_length,offset_distance,parent_dir):
    # create sampling data
    # k = lhsmdu.sample(3,seed,random.randint(1, 20))
    # k = np.array(k)
    k = pyDOE2.lhs(3, samples=seed, criterion='correlation', iterations=None)
    k = np.array(k)
    # encode LHC
    sampling_scale = [0 for i in range(seed)]
    sampling_sweep_angle = [0 for i in range(seed)]
    sampling_number_of_blade = [0 for i in range(seed)]
    for i in range(seed):
        sampling_scale[i] = l_scale + k[i][0] * (u_scale - l_scale)
        # if greater than 90 ...
        ll_sweep_angle = np.arctan(hub_to_shroud / (passage_domain_length - (2 * offset_distance) - sampling_scale[i]))
        uu_sweep_angle = np.pi - np.arctan(
            hub_to_shroud / (passage_domain_length - (2 * offset_distance) - sampling_scale[i]))
        sampling_sweep_angle[i] = np.rad2deg(ll_sweep_angle + k[i][1] * (uu_sweep_angle - ll_sweep_angle))
        index_number_of_blade = int(np.floor(len(number_of_blade) * k[i][2]))
        sampling_number_of_blade[i] = number_of_blade[index_number_of_blade]

    with open(parent_dir+"allDesigns.csv", "w") as designpoint:
        designpoint.write('Design,Chord_m,SweepAngle_degree,N_Blade\n')
        for each_design in range(seed):
            designpoint.write(f'{each_design},{sampling_scale[each_design]:.2f},{sampling_sweep_angle[each_design]:.2f},{sampling_number_of_blade[each_design]}\n')

    return sampling_scale, sampling_sweep_angle , sampling_number_of_blade

def gen_ccd_data(l_scale, u_scale, number_of_blade,hub_to_shroud \
                 ,passage_domain_length,offset_distance,parent_dir):
    # gen Normalized design
    # ccc ccf cci
    ccd = pyDOE2.ccdesign(3, [0, 0], alpha='orthogonal',face='cci')

    k = np.zeros([len(ccd) + 1, 3])
    sampling_scale = [0 for i in range(len(ccd) + 1)]
    sampling_sweep_angle = [0 for i in range(len(ccd) + 1)]
    sampling_number_of_blade= [0 for i in range(len(ccd) + 1)]
    count = 0

    for norm_mem in ccd:
        k[count+1] = norm_mem
        count += 1

    # encoded data
    for i in range(len(k)):
        sampling_scale[i] = (u_scale + l_scale)/2.0 + k[i][0] * (u_scale - l_scale)/2.0
        # if greater than 90 ...
        ll_sweep_angle = np.arctan(hub_to_shroud / (passage_domain_length - (2 * offset_distance) - sampling_scale[i]))
        uu_sweep_angle = np.pi - np.arctan(
            hub_to_shroud / (passage_domain_length - (2 * offset_distance) - sampling_scale[i]))
        sampling_sweep_angle[i] = np.rad2deg((uu_sweep_angle + ll_sweep_angle)/2+ \
                                             k[i][1] * (uu_sweep_angle - ll_sweep_angle)/2)
        index_number_of_blade = int(np.round((len(number_of_blade)-1)/2 +k[i][2]*(len(number_of_blade)-1)/2))
        sampling_number_of_blade[i] = int(number_of_blade[index_number_of_blade])

    with open(parent_dir + "allDesigns.csv", "w") as designpoint:
        designpoint.write('Design,Chord_m,SweepAngle_degree,N_Blade\n')
        for each_design in range(len(k)):
            designpoint.write(\
                f'{each_design},{sampling_scale[each_design]:.2f},{sampling_sweep_angle[each_design]:.2f},{sampling_number_of_blade[each_design]}\n')

    seed = len(k)
    return sampling_scale, sampling_sweep_angle , sampling_number_of_blade, seed

def read_inputdata(parent_dir):
    parent_geo_dir = parent_dir+"geometry\\"
    hub_path = parent_geo_dir+"OGV_hub.curve"
    shroud_path = parent_geo_dir + "OGV_shroud.curve"
    radius_path = parent_geo_dir + "OGV_radius.txt"
    profile_path = parent_geo_dir + "OGV_profile.curve"

    input_hub = np.loadtxt(hub_path, delimiter=" ", dtype=float)
    input_shroud = np.loadtxt(shroud_path, delimiter=" ", dtype=float)
    input_radius = np.loadtxt(radius_path, delimiter=" ", dtype=float)
    # read variable file
    input_profile = np.loadtxt(profile_path, delimiter=" ", dtype=float)
    return input_hub, input_shroud, input_radius, input_profile

def gen_curve_file(ogv_profile,ogv_radius,ogv_hub,offset_distance,sampling_scale,sampling_sweep_angle,\
                   n_profile_point,parent_dir,seed ):
    curve_dir=parent_dir+"curve\\"
    try:
        os.mkdir(curve_dir)
    except FileExistsError:
        print("A curve directory already exists.")

    for i in range(seed):
        out_profile = scale_profile(ogv_profile, sampling_scale[i])
        out_profile = sweep_profile(out_profile, sampling_sweep_angle[i], n_profile_point)
        out_profile = project_profile(out_profile, ogv_radius, n_profile_point)
        out_profile = offset_profile(out_profile, ogv_hub,offset_distance)
        # save file
        save_out_profile_curve(out_profile, n_profile_point, i, curve_dir)
        #save_out_profile_spaceclaim(out_profile, n_profile_point, i)
        # plot profile
        # plot_profile(offset_out_profile,ogv_hub,ogv_shroud)