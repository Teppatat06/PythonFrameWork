from cfdopt import gendata, genscript


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parent_dir = "D:\\PUN\\OPT_GV\\"
    #read Input geometry file
    ogv_hub,ogv_shroud,ogv_radius,ogv_profile = gendata.read_inputdata(parent_dir)
    # constant
    n_profile_point = 84
    diameter = 1.250
    passage_domain_ratio = 0.7
    passage_domain_length = passage_domain_ratio * diameter
    offset_distance = 0.025 * diameter  # from starting point of hub
    hub_to_shroud = ogv_shroud[0][0] - ogv_hub[0][0]
    # variable
    # sweep_angle = 150  # degree
    number_of_blade = [3, 5, 7, 11, 13]  # (2 3 5 7 11 13 17 19 ...)prime number to avoid natural frequencies
    # seed = seed_scale*seed_sweep_angle*seed_number_of_blade
    seed = 50#150
    tol = 1e-12
    # constraint
    #  sweep angle Note that: for sweep angle,both lower and upper constaint are depended on scale(chord size).
    l_scale = 0.15
    u_scale = passage_domain_length - (2 * offset_distance) - tol
    # initial condition
    init_scale = 0.29
    init_sweep_angle = 30
    init_number_of_blade = 5

    # Latin Hyper Cube Sampling Algolithm
    #sampling_scale, sampling_sweep_angle, sampling_number_of_blade =\
    #    gendata.gen_sampling_data(seed, l_scale, u_scale, number_of_blade, \
    #        hub_to_shroud,passage_domain_length,offset_distance,parent_dir)

    sampling_scale, sampling_sweep_angle, sampling_number_of_blade,seed =\
        gendata.gen_ccd_data(l_scale, u_scale, number_of_blade, hub_to_shroud, \
                            passage_domain_length, offset_distance, parent_dir)


    # visualization
    gendata.plot_profile(l_scale, u_scale, seed, sampling_number_of_blade, \
                number_of_blade, sampling_scale,sampling_sweep_angle, \
                    hub_to_shroud, passage_domain_length, offset_distance)

    # transformation

    gendata.gen_curve_file(ogv_profile,ogv_radius,ogv_hub,offset_distance,sampling_scale, \
                      sampling_sweep_angle, n_profile_point,parent_dir,seed)
    genscript.gen_duct_in_script(number_of_blade,parent_dir,seed )
    genscript.gen_duct_out_script(number_of_blade,parent_dir,seed )
    genscript.gen_turbogrid_script(sampling_number_of_blade,parent_dir,seed)
    genscript.gen_cfxpre_script(parent_dir, seed)



