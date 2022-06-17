#!/usr/bin/env python 

import scm.plams
import scm.pyzacros as pz
from matplotlib.pyplot import show
from utilities import Position, Make_site

# Gas species
H2_g = pz.Species('H2')
CO2_g = pz.Species('CO2', gas_energy=-2.337)
CH3OH_g = pz.Species('CH3OH',gas_energy=-3.0)
H2O_g = pz.Species('H2O',gas_energy=-1.5)
CO_g = pz.Species('CO',gas_energy=-1)
HCOOH_g = pz.Species('HCOOH', gas_energy = -2.5)
H2CO_g = pz.Species('H2CO', gas_energy = -1.5)

# Surface species
s0 = pz.Species('*', 1) # Empty adsorption site
H_s = pz.Species('H*', 1)
O_s = pz.Species('O*', 1)
OH_s = pz.Species('OH*', 1)
Cs_s = pz.Species('Cs*', 1)

CO2_s = pz.Species('CO2*', 1)
OCO2_s = pz.Species('OCO2*', 1)
OHCOO_s = pz.Species('OHCOO*', 1)
CsOHCOOH_s = pz.Species('CsOHCOOH**', 2)
CsOH2COOH_s = pz.Species('CsOH2COOH**', 2)
OH2CO2H2_s = pz.Species('OH2CO2H2*', 1)
CH3OH_s = pz.Species('CH3OH*', 1)
OOH_s = pz.Species('OOH*', 1)
OH2O_s = pz.Species('OH2O*', 1)

OH2CO_s = pz.Species('OH2CO*', 1)
OH3CO_s = pz.Species('OH3CO*', 1)
OH3COH_s = pz.Species('OH3COH**', 2)

OCOOH_s = pz.Species('OCOOH*', 1)
OCO_s = pz.Species('OCO*', 1)
CsOCHO_s = pz.Species('CsOCHO*', 2)

# save all species to a list
spl = pz.SpeciesList([H2_g, CO2_g, CH3OH_g, H2O_g, CO_g, HCOOH_g, H2CO_g,
                      s0, H_s, O_s, OH_s, Cs_s, 
                      CO2_s,OCO2_s, 
                      OHCOO_s,
                      CsOHCOOH_s,
                      CsOH2COOH_s,
                      OH2CO2H2_s,
                      CH3OH_s,
                      OOH_s,OH2O_s,
                      OH2CO_s, OH3CO_s, OH3COH_s,
                      OCOOH_s,OCO_s, CsOCHO_s])

#print (spl)
#print (spl.gas_species())

#Lattice Setup
repeat_cell = [32, 32] # cell size
lat = pz.Lattice( cell_vectors = [[2.950, 0.00000000],[1.475, 2.555]],
                  repeat_cell = repeat_cell,
                  site_types = ["hcp", "fcc", "top"],
                  site_coordinates = [[0.33333, 0.33333],
                                      [0.66667, 0.66667],
                                      [0.99999, 0.00001]],
                  neighboring_structure = [ [(0,1), pz.Lattice.SELF],
                                            [(1,2), pz.Lattice.SELF],
                                            [(0,2), pz.Lattice.SELF],
                                            [(1,0), pz.Lattice.NORTH],
                                            [(1,2), pz.Lattice.NORTH],
                                            [(0,0), pz.Lattice.NORTH],
                                            [(1,1), pz.Lattice.NORTH],
                                            [(2,2), pz.Lattice.NORTH],
                                            [(1,0), pz.Lattice.EAST],
                                            [(2,0), pz.Lattice.EAST],
                                            [(0,0), pz.Lattice.EAST],
                                            [(1,1), pz.Lattice.EAST],
                                            [(2,2), pz.Lattice.EAST],
                                            [(0,0), pz.Lattice.SOUTHEAST],
                                            [(2,1), pz.Lattice.SOUTHEAST],
                                            [(1,1), pz.Lattice.SOUTHEAST],
                                            [(2,2), pz.Lattice.SOUTHEAST],
                                            [(2,0), pz.Lattice.SOUTHEAST]] )

#lat.plot()
#lat.plot(block=False)

# LatticeState setup (initial state)
ist = pz.LatticeState(lat, surface_species=spl.surface_species())

# Find positions for all clusters
repeat_cell = repeat_cell
n_site_types = 3 # number of site types
width = [6,6] # blocked edge width
site_type = 'hcp' 
clusters_ = 10 # number of clusters on surface
NN_ = 3 # Nearest neighbors blocked

# cluster shape using sites representation
sites = [['fcc','POS'],
         ['fcc','WEST'],
         ['hcp','NORTH'],
         ['fcc','SELF'],
         ['top','NORTH'],
         ['fcc','SOUTHEAST'],
         ['hcp','EAST'],
         ['fcc','SOUTH'],
         ['top','SELF'],
         ['fcc','SOUTH'],
         ['hcp','SELF'],
         ['fcc','WEST'],
         ['top','NORTHWEST']]

Position, _ = Position(sites = sites,
                       repeat_cell = repeat_cell,
                       n_site_types = n_site_types,
                       width = width,
                       site_type = site_type,
                       clusters = clusters_,
                       NN = NN_)

print ('Center:',Position) # print center positions for all clusters

# print positions to file: pos
with open('./pos','w') as f:
    for pos in Position:
        f.write('%s\n' % str(pos))

'''
site_number = []
for i in range(len(Exception_)):
    num = Exception_[i] - 1
    site_number.append(num)
ist1 = pz.LatticeState(lat, surface_species=spl.surface_species())
ist1.fill_site(site_number=site_number,species='O*')
ist1.plot(block=True)
'''

# Generate a list of sites mapping to the lattice using Make_site function
for pos in Position:
    sites = [['fcc',pos],
         ['fcc','WEST'],
         ['hcp','NORTH'],
         ['fcc','SELF'],
         ['top','NORTH'],
         ['fcc','SOUTHEAST'],
         ['hcp','EAST'],
         ['fcc','SOUTH'],
         ['top','SELF'],
         ['fcc','SOUTH'],
         ['hcp','SELF'],
         ['fcc','WEST'],
         ['top','NORTHWEST']]

    list_ = Make_site(sites,repeat_cell, n_site_types)

    site_number = []
    for i in range(len(list_)):
        num = list_[i] - 1
        site_number.append(num)        

    # Generate initial state adsorbate
    ist.fill_site(site_number=site_number[0],species='O*')
    ist.fill_site(site_number=site_number[2],species='Cs*')
    ist.fill_site(site_number=site_number[4],species='OH*')
    ist.fill_site(site_number=site_number[6],species='Cs*')
    ist.fill_site(site_number=site_number[8],species='OH*')
    ist.fill_site(site_number=site_number[10],species='Cs*')
    ist.fill_site(site_number=site_number[12],species='OH*')

#print(ist)
#ist.plot(block=False)

# Clusters:
CO2_p = pz.Cluster( species=[CO2_s], 
                    site_types = ['fcc'],
                    cluster_energy=-1.3 )

ce = pz.ClusterExpansion([CO2_p])
#print(ce)

# Elementary Reactions
O_H2_OH = pz.ElementaryReaction(initial=[O_s,s0,s0,s0,s0,H2_g],
                                final=[OH_s,H_s,s0,s0,s0],
                                site_types = ['top','fcc','hcp','hcp','hcp'],
                                neighboring = [(0,1),(1,2),(0,3),(0,4),(1,3),(1,4)],
                                reversible=False, pre_expon=1.0e+13, activation_energy=0.0 )

O_OH = pz.ElementaryReaction(initial=[O_s,H_s],
                             final=[OH_s,s0],
                             site_types = ['top','fcc'],
                             neighboring = [(0,1)],
                             reversible=False, pre_expon=1.0e+13, activation_energy=0.0 )

CO2_ads = pz.ElementaryReaction(initial=[Cs_s,s0,Cs_s,s0,Cs_s,s0,O_s,CO2_g], 
                                final=[Cs_s,CO2_s,Cs_s,s0,Cs_s,s0,O_s],
                                site_types = ['hcp','hcp','hcp','hcp','hcp','hcp','fcc'],
                                neighboring = [(0,1),(1,2),(2,3),(3,4),(4,5),(5,0),(5,6)],
                                reversible=False, pre_expon=1.0e+13, activation_energy=0.0 )
# Reverse
CO2_ads_re = pz.ElementaryReaction(initial=[Cs_s,CO2_s,Cs_s,s0,Cs_s,s0,O_s],
                                   final=[Cs_s,s0,Cs_s,s0,Cs_s,s0,O_s,CO2_g],
                                   site_types = ['hcp','hcp','hcp','hcp','hcp','hcp','fcc'],
                                   neighboring = [(0,1),(1,2),(2,3),(3,4),(4,5),(5,0),(5,6)],
                                   reversible=False, pre_expon=1.0e+13, activation_energy=0.0 )

CO2_HCOO = pz.ElementaryReaction(initial=[O_s,s0,s0,s0,CO2_s,OH_s],
                                 final=[OHCOO_s,s0,s0,s0,s0,O_s],
                                 site_types = ['fcc','top','top','top','hcp','top'],
                                 neighboring = [(0,1),(0,2),(0,3),(0,4),(4,5)],
                                 reversible=False, pre_expon=1.0e+13, activation_energy=1.2 )
# Reverse
CO2_HCOO_re = pz.ElementaryReaction(initial=[OHCOO_s,s0,s0,s0,s0,O_s],
                                    final=[O_s,s0,s0,s0,CO2_s,OH_s],
                                    site_types = ['fcc','top','top','top','hcp','top'],
                                    neighboring = [(0,1),(0,2),(0,3),(0,4),(4,5)],
                                    reversible=False, pre_expon=1.0e+13, activation_energy=1.9 )

HCOO_HCOOH = pz.ElementaryReaction(initial=[OHCOO_s, s0, Cs_s, s0,OH_s],
                                   final=[CsOHCOOH_s, s0, CsOHCOOH_s, s0,O_s],
                                   site_types = ['fcc','top','hcp','fcc','top'],
                                   neighboring = [(0,1),(1,2),(2,3),(3,4)],
                                   reversible=False, pre_expon=1.0e+13, activation_energy=0.42 )
# Reverse
HCOO_HCOOH_re = pz.ElementaryReaction(initial=[CsOHCOOH_s, s0, CsOHCOOH_s, s0, s0,O_s],
                                      final=[OHCOO_s, s0, Cs_s, s0, s0, OH_s],
                                      site_types = ['fcc','top','hcp','top','top','top'],
                                      neighboring = [(0,1),(1,2),(0,3),(0,4),(0,5),(2,5)],
                                      reversible=False, pre_expon=1.0e+13, activation_energy=0.28 )

HCOOH_des = pz.ElementaryReaction(initial = [CsOHCOOH_s, s0, CsOHCOOH_s],
                                  final = [O_s, s0, Cs_s, HCOOH_g],
                                  site_types = ['fcc','top','hcp'],
                                  neighboring = [(0,1),(1,2)],
                                  reversible=False, pre_expon=1.0e+13, activation_energy=0.0 )

HCOOH_H2COOH = pz.ElementaryReaction(initial=[CsOHCOOH_s, s0, CsOHCOOH_s, s0, OH_s],
                                     final=[CsOH2COOH_s, s0, CsOH2COOH_s, s0, O_s],
                                     site_types = ['fcc','top','hcp','fcc','top'],
                                     neighboring = [(0,1),(1,2),(2,3),(3,4)],
                                     reversible=False, pre_expon=0.05e+13, activation_energy=2.01 )
# Reverse
HCOOH_H2COOH_re = pz.ElementaryReaction(initial=[CsOH2COOH_s, s0, CsOH2COOH_s, s0, O_s],
                                        final=[CsOHCOOH_s, s0, CsOHCOOH_s, s0, OH_s],
                                        site_types = ['fcc','top','hcp','fcc','top'],
                                        neighboring = [(0,1),(1,2),(2,3),(3,4)],
                                        reversible=False, pre_expon=1.0e+13, activation_energy=1.91 )

H2COOH_H2CO2H2 = pz.ElementaryReaction(initial=[CsOH2COOH_s, s0, CsOH2COOH_s, s0, s0, s0, OH_s],
                                       final=[OH2CO2H2_s, s0, Cs_s, s0, s0, s0, O_s],
                                       site_types = ['fcc','top','hcp','top', 'top','hcp','top'],
                                       neighboring = [(0,1),(1,2),(0,3),(0,4),(3,5),(4,5),(5,6)],
                                       reversible=False, pre_expon=1.0e+13, activation_energy=0.33 )
# Reverse
H2COOH_H2CO2H2_re = pz.ElementaryReaction(initial=[OH2CO2H2_s, s0, Cs_s, s0, s0, s0, O_s],
                                          final=[CsOH2COOH_s, s0, CsOH2COOH_s, s0, s0, s0, OH_s],
                                          site_types = ['fcc','top','hcp','top','top','hcp','top'],
                                          neighboring = [(0,1),(1,2),(0,3),(0,4),(3,5),(4,5),(5,6)],
                                          reversible=False, pre_expon=1.0e+13, activation_energy=1.05 )

H2CO2H2_CH3OH_OH = pz.ElementaryReaction(initial = [OH2CO2H2_s,s0,OH_s],
                                         final = [OOH_s,CH3OH_s,O_s],
                                         site_types = ['fcc','hcp','top'],
                                         neighboring = [(0,1),(1,2)],
                                         reversible=False, pre_expon=1.0e+13, activation_energy=2.01 )
# Reverse
H2CO2H2_CH3OH_OH_re = pz.ElementaryReaction(initial = [OOH_s,CH3OH_s,O_s],
                                            final = [OH2CO2H2_s,s0,OH_s],
                                            site_types = ['fcc','hcp','top'],
                                            neighboring = [(0,1),(1,2)],
                                            reversible=False, pre_expon=1.0e+13, activation_energy=1.91 )

OOH_OH2O = pz.ElementaryReaction(initial = [OOH_s,s0,OH_s],
                                 final = [OH2O_s,s0,O_s],
                                 site_types = ['fcc','hcp','top'],
                                 neighboring = [(0,1),(1,2)],
                                 reversible=False, pre_expon=1.0e+13, activation_energy=0.66 )
# Reverse
OOH_OH2O_re = pz.ElementaryReaction(initial = [OH2O_s,s0,O_s],
                                    final = [OOH_s,s0,OH_s],
                                    site_types = ['fcc','hcp','top'],
                                    neighboring = [(0,1),(1,2)],
                                    reversible=False, pre_expon=1.0e+13, activation_energy=0.03 )

# Desorption no reverse step
CH3OH_des = pz.ElementaryReaction(initial = [CH3OH_s],
                                  final = [s0,CH3OH_g],
                                  site_types = ['hcp'],
                                  neighboring = None,
                                  reversible=False, pre_expon=1.0e+13, activation_energy=0.0 )

H2O_des = pz.ElementaryReaction(initial = [OH2O_s],
                                final = [O_s,H2O_g],
                                site_types = ['fcc'],
                                neighboring = None,
                                reversible=False, pre_expon=1.0e+13, activation_energy=0.0 )

H2COOH_H2CO_H2O = pz.ElementaryReaction(initial = [CsOH2COOH_s, s0, CsOH2COOH_s, s0, OH_s],
                                        final = [OH2CO_s, s0, Cs_s, s0, O_s, H2O_g],
                                        site_types = ['fcc','top','hcp','fcc','top'],
                                        neighboring = [(0,1),(1,2),(2,3),(3,4)],
                                        reversible=False, pre_expon=1.0e+13, activation_energy=0.33 )
# Reverse
H2COOH_H2CO_H2O_re = pz.ElementaryReaction(initial = [OH2CO_s, s0, Cs_s, s0, O_s, H2O_g],
                                           final = [CsOH2COOH_s, s0, CsOH2COOH_s, s0, OH_s],
                                           site_types = ['fcc','top','hcp','fcc','top'],
                                           neighboring = [(0,1),(1,2),(2,3),(3,4)],
                                           reversible=False, pre_expon=1.0e+13, activation_energy=0.67 )

H2CO_des = pz.ElementaryReaction(initial = [OH2CO_s],
                                 final = [O_s, H2CO_g],
                                 site_types = ['fcc'],
                                 neighboring = None,
                                 reversible=False, pre_expon=1.0e+13, activation_energy=0.0 )

H2CO_H3CO = pz.ElementaryReaction(initial = [OH2CO_s, s0, OH_s],
                                  final = [OH3CO_s, s0, O_s],
                                  site_types = ['fcc','hcp','top'],
                                  neighboring = [(0,1),(1,2)],
                                  reversible=False, pre_expon=1.0e+13, activation_energy=0.4 )
# Reverse 
H2CO_H3CO_re = pz.ElementaryReaction(initial = [OH3CO_s, s0, O_s],
                                     final = [OH2CO_s, s0, OH_s],
                                     site_types = ['fcc','hcp','top'],
                                     neighboring = [(0,1),(1,2)],
                                     reversible=False, pre_expon=1.0e+13, activation_energy=1.1 )

H3CO_H3COH = pz.ElementaryReaction(initial = [OH3CO_s, s0, OH_s],
                                   final = [OH3COH_s, OH3COH_s, O_s],
                                   site_types = ['fcc','hcp','top'],
                                   neighboring = [(0,1),(1,2)],
                                   reversible=False, pre_expon=1.0e+13, activation_energy=0.59 )
# Reverse 
H3CO_H3COH_re = pz.ElementaryReaction(initial = [OH3COH_s, OH3COH_s, O_s],
                                      final = [OH3CO_s, s0, OH_s],
                                      site_types = ['fcc','hcp','top'],
                                      neighboring = [(0,1),(1,2)],
                                      reversible=False, pre_expon=1.0e+13, activation_energy=0.025 )

H3COH_des = pz.ElementaryReaction(initial = [OH3COH_s, OH3COH_s],
                                  final = [O_s,s0,CH3OH_g],
                                  site_types = ['fcc','hcp'],
                                  neighboring = [(0,1)],
                                  reversible=False, pre_expon=1.0e+13, activation_energy=0.0 )

CO2_COOH = pz.ElementaryReaction(initial = [O_s,CO2_s,OH_s],
                                 final = [OCOOH_s,s0,O_s],
                                 site_types = ['fcc','hcp','top'],
                                 neighboring = [(0,1),(1,2)],
                                 reversible=False, pre_expon=1.0e+13, activation_energy=1.0 )
# Reverse
CO2_COOH_re = pz.ElementaryReaction(initial = [OCOOH_s,s0,O_s],
                                    final = [O_s,CO2_s,OH_s],
                                    site_types = ['fcc','hcp','top'],
                                    neighboring = [(0,1),(1,2)],
                                    reversible=False, pre_expon=1.0e+13, activation_energy=0.0 )

COOH_CO = pz.ElementaryReaction(initial = [OCOOH_s,s0,OH_s],
                                final = [OCO_s,s0,O_s,H2O_g],
                                site_types = ['fcc','hcp','top'],
                                neighboring = [(0,1),(1,2)],
                                reversible=False, pre_expon=1.0e+13, activation_energy=0.74 )
# Reverse
COOH_CO_re = pz.ElementaryReaction(initial = [OCO_s,s0,O_s,H2O_g],
                                   final = [OCOOH_s,s0,OH_s],
                                   site_types = ['fcc','hcp','top'],
                                   neighboring = [(0,1),(1,2)],
                                   reversible=False, pre_expon=1.0e+13, activation_energy=0.0 )

CO_des = pz.ElementaryReaction(initial = [OCO_s],
                               final = [O_s,CO_g],
                               site_types = ['fcc'],
                               neighboring = None,
                               reversible=False, pre_expon=1.0e+13, activation_energy=0.0 )

CO_CHO = pz.ElementaryReaction(initial = [OCO_s, s0, Cs_s, s0, OH_s],
                               final = [CsOCHO_s, s0, CsOCHO_s, s0, O_s],
                               site_types = ['fcc','top','hcp','fcc','top'],
                               neighboring = [(0,1),(1,2),(2,3),(3,4)],
                               reversible=False, pre_expon=1.0e+13, activation_energy=1.51 )
# Reverse
CO_CHO_re = pz.ElementaryReaction(initial = [CsOCHO_s, s0, CsOCHO_s, s0, O_s],
                                  final = [OCO_s, s0, Cs_s, s0, OH_s],
                                  site_types = ['fcc','top','hcp','fcc','top'],
                                  neighboring = [(0,1),(1,2),(2,3),(3,4)],
                                  reversible=False, pre_expon=1.0e+13, activation_energy=0.0 )

CHO_H2CO = pz.ElementaryReaction(initial = [CsOCHO_s, s0, CsOCHO_s, s0, OH_s],
                                 final = [OH2CO_s, s0, Cs_s, s0, O_s],
                                 site_types = ['fcc','top','hcp','fcc','top'],
                                 neighboring = [(0,1),(1,2),(2,3),(3,4)],
                                 reversible=False, pre_expon=1.0e+13, activation_energy=1.0 )
# Reverse
CHO_H2CO_re = pz.ElementaryReaction(initial = [OH2CO_s, s0, Cs_s, s0, O_s],
                                    final = [CsOCHO_s, s0, CsOCHO_s, s0, OH_s],
                                    site_types = ['fcc','top','hcp','fcc','top'],
                                    neighboring = [(0,1),(1,2),(2,3),(3,4)],
                                    reversible=False, pre_expon=1.0e+13, activation_energy=1.0 )

mech = pz.Mechanism([O_OH, O_H2_OH, 
                     CO2_ads, CO2_ads_re,
                     # H2CO2H2 path
                     CO2_HCOO, CO2_HCOO_re,                                                                                                
                     HCOO_HCOOH, HCOO_HCOOH_re,                                                                                         
                     HCOOH_des, 
                     HCOOH_H2COOH, HCOOH_H2COOH_re,                                                                                       
                     H2COOH_H2CO2H2, H2COOH_H2CO2H2_re,                                                                                   
                     H2CO2H2_CH3OH_OH, H2CO2H2_CH3OH_OH_re,                                                                              
                     OOH_OH2O, OOH_OH2O_re, CH3OH_des, H2O_des,                                                                              
                     # H2CO path
                     H2COOH_H2CO_H2O, H2COOH_H2CO_H2O_re,                                                                                 
                     H2CO_des, H2CO_H3CO, H2CO_H3CO_re,                                                                                  
                     H3CO_H3COH, H3CO_H3COH_re, H3COH_des,
                     # RWGS path
                     CO2_COOH, CO2_COOH_re, 
                     COOH_CO, COOH_CO_re,
                     CO_des,
                     CO_CHO, CO_CHO_re,
                     CHO_H2CO, CHO_H2CO_re,
                     ])

#print (mech)

scm.plams.init()

# Settings:
sett = pz.Settings()
sett.temperature = 500.0
sett.pressure = 1.0
sett.snapshots = ('time', 5.0e-3)
sett.process_statistics = ('time', 5.0e-3)
sett.species_numbers = ('time', 5.0e-3)
sett.max_time = 10.0

sett.molar_fraction.CO2 = 0.1
sett.molar_fraction.H2 = 0.9
#print (sett)

myJob = pz.ZacrosJob( settings=sett, 
                      lattice=lat,
                      mechanism=mech,
                      cluster_expansion=ce,
                      species_list=spl,
                      initial_state = ist)

results = myJob.run()

#print (results.files)
#print( "nCO2 = ", results.provided_quantities()['HOCO2*'][-10:] )
results.plot_molecule_numbers( results.gas_species_names(), file_name = 'gas' )
results.plot_molecule_numbers( results.surface_species_names(), file_name = 'surface')
results.plot_lattice_states( results.lattice_states(), file_name = 'snapshots')
results.plot_process_statistics( results.get_process_statistics(), key="number_of_events" , file_name = 'events')
#show()
scm.plams.finish()

#show()
