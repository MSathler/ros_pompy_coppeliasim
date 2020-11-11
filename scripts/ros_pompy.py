#!/usr/bin/env python

import numpy as np
import rospy
from pompy import models, processors
from ros_pompy_point_cloud import pompy_point_cloud

if __name__ == '__main__':
    # Seed random number generator
    seed = 20180517
    rng = np.random.RandomState(seed)

    # Define wind model simulation region
    wind_region = models.Rectangle(x_min=0., x_max=100., y_min=-50., y_max=50.)

    # Define wind model parameters
    wind_model_params = { 
        'n_x': 21,
        'n_y': 21,
        'u_av': 1.,
        'v_av': 0.,
        'k_x': 10.,
        'k_y': 10.,
        'noise_gain': 20.,
        'noise_damp': 0.1,
        'noise_bandwidth': 0.2,
        'use_original_noise_updates': True
    }

    # Create wind model object
    wind_model = models.WindModel(wind_region, rng=rng, **wind_model_params)

    # Define plume simulation region
    # This is a subset of the wind simulation region
    sim_region = models.Rectangle(x_min=0., x_max=50., y_min=-12.5, y_max=12.5)

    # Define plume model parameters
    plume_model_params = {
        'source_pos': (0., -12., 0.),
        'centre_rel_diff_scale': 2.,
        'puff_release_rate': 10,
        'puff_init_rad': 0.001**0.5,
        'puff_spread_rate': 0.001,
        'init_num_puffs': 10,
        'max_num_puffs': 10000,
        'model_z_disp': False,
    }

    # Create plume model object
    plume_model = models.PlumeModel(
        rng=rng, sim_region=sim_region, wind_model=wind_model, **plume_model_params)

    # Define concentration array (image) generator parameters
    array_gen_params = {
        'array_z': 0.,
        'n_x': 500,
        'n_y': 250,
        'puff_mol_amount': 8.3e8
    }

    # Create concentration array generator object
    array_gen = processors.ConcentrationArrayGenerator(
        array_xy_region=sim_region, **array_gen_params)

    # Display initial concentration field
    conc_array = array_gen.generate_single_array(plume_model.puff_array)

    # Simulation timestep
    dt = 0.01

    # Run wind model forward to equilibrate
    
    for k in range(2000):
    
        wind_model.update(dt)

    try:
        pb = pompy_point_cloud(wind_model=wind_model,plume_model=plume_model, conc_array = conc_array, array_gen = array_gen)
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo('caught exception')