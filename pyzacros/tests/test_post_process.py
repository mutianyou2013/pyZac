import os

import scm.plams

import pyzacros as pz
from pyzacros.utils.compareReports import compare


def test_post_process():
    """Test of the post_process methods."""
    RUNDIR = os.getcwd()

    print( "---------------------------------------------------" )
    print( ">>> Testing Zacros post_process methods" )
    print( "---------------------------------------------------" )

    #---------------------------------------------
    # Species:
    #---------------------------------------------
    # - Gas-species:
    CO_gas = pz.Species("CO")
    O2_gas = pz.Species("O2")
    CO2_gas = pz.Species("CO2", gas_energy=-2.337)

    # -) Surface species:
    s0 = pz.Species("*", 1)      # Empty adsorption site
    CO_ads = pz.Species("CO*", 1)
    O_ads = pz.Species("O*", 1)

    #---------------------------------------------
    # Lattice setup:
    #---------------------------------------------
    myLattice = pz.Lattice(lattice_type=pz.Lattice.RECTANGULAR, lattice_constant=1.0, repeat_cell=[20,20])

    #---------------------------------------------
    # Clusters:
    #---------------------------------------------
    CO_point = pz.Cluster(species=[CO_ads], cluster_energy=-1.3)
    O_point = pz.Cluster(species=[O_ads], cluster_energy=-2.3)

    #---------------------------------------------
    # Elementary Reactions
    #---------------------------------------------
    # CO_adsorption:
    CO_adsorption = pz.ElementaryReaction( initial=[s0,CO_gas],
                                           final=[CO_ads],
                                           reversible=False,
                                           pre_expon=10.0,
                                           label="CO_adsorption")

    # O2_adsorption:
    O2_adsorption = pz.ElementaryReaction( initial=[s0,s0,O2_gas],
                                           final=[O_ads,O_ads],
                                           neighboring=[(0, 1)],
                                           reversible=False,
                                           pre_expon=2.5,
                                           label="O2_adsorption")

    # CO_oxidation:
    CO_oxidation = pz.ElementaryReaction( initial=[CO_ads, O_ads],
                                          final=[s0, s0, CO2_gas],
                                          neighboring=[(0, 1)],
                                          reversible=False,
                                          pre_expon=1.0e+20,
                                          label="CO_oxidation")

    scm.plams.init( folder='old_results' )

    # Settings:
    sett = pz.Settings()
    sett.molar_fraction.CO = 0.45
    sett.molar_fraction.O2 = 0.55
    sett.random_seed = 953129
    sett.temperature = 500.0
    sett.pressure = 1.0
    sett.snapshots = ('time', 0.1)
    sett.process_statistics = ('time', 0.1)
    sett.species_numbers = ('time', 0.1)
    sett.event_report = 'off'
    sett.max_steps = 'infinity'
    sett.max_time = 1.0
    sett.wall_time = 3600

    job = pz.ZacrosJob( settings=sett,
                        lattice=myLattice,
                        mechanism=[CO_adsorption, O2_adsorption, CO_oxidation],
                        cluster_expansion=[CO_point, O_point] )

    #-----------------------
    # Running the job
    #-----------------------
    load_precalculated = False

    try:
        results = job.run()

        if( not job.ok() ):
            raise "Error: The Zacros calculation FAILED!"

    except pz.ZacrosExecutableNotFoundError:
        print( "Warning: The calculation FAILED because the zacros executable is not available!" )
        print( "         For testing purposes, now we load precalculated results.")
        load_precalculated = True

    scm.plams.finish()

    if( load_precalculated ):
        job = pz.ZacrosJob.load_external( path=RUNDIR+"/tests/test_ZacrosResults.data" )
    else:
        job = pz.ZacrosJob.load_external( path='old_results/plamsjob' )

    data = job.results.provided_quantities()
    output = str(data)
    print(output)

    expectedOutput = """\
{'Entry': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], 'Nevents': [0, 346, 614, 888, 1117, 1314, 1535, 1726, 1920, 2056, 2222], 'Time': [0.0, 0.1, 0.2, 0.30000000000000004, 0.4, 0.5, 0.6, 0.7, 0.7999999999999999, 0.8999999999999999, 0.9999999999999999], 'Temperature': [500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0], 'Energy': [0.0, -362.40000000000106, -435.4000000000014, -481.8000000000016, -531.5000000000013, -514.4000000000016, -528.9000000000013, -530.2000000000013, -614.3999999999997, -653.499999999999, -612.0999999999998], 'CO*': [0, 24, 20, 15, 9, 10, 7, 8, 2, 2, 2], 'O*': [0, 144, 178, 201, 226, 218, 226, 226, 266, 283, 265], 'CO': [0, -124, -222, -324, -407, -488, -573, -650, -716, -767, -837], 'O2': [0, -122, -190, -255, -312, -348, -396, -434, -490, -524, -550], 'CO2': [0, 100, 202, 309, 398, 478, 566, 642, 714, 765, 835]}\
"""

    assert( compare( output, expectedOutput, 1e-3 ) )
