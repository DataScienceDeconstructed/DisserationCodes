
from ComputationalEquilibriums import ReferenceDistribution
from scipy.stats import chi2_contingency
import numpy as np
import sys

if __name__ == "__main__":
    # start out with empty distributions, a negative index so that it goes to 0 at the start, the testing significance level,
    # and a tracking variable for how many times in a row the test has failed.
    print("starting main script")
    dir_base = sys.argv[1] if len(sys.argv)>1 else "/home/chdavis/Code/mpd-md/bin/main_testing2/exp_test_6/Umin_1/rad_2/den_18/NP_10/"
    filename = sys.argv[2] if len(sys.argv)>2 else "exp_test_6.Umin1.rad2.den18.NP10"
    print(dir_base, filename)
    
    dist = ReferenceDistribution(_type="Binary", _reference=0.0, _dist=[0, 0])
    significance_level = 0.05
    sim_track = 0
    info_lag = []
    brushz_lag= []
    
    system_dimensions = [0.0,0.0,0.0]

    radius = float(dir_base.split("/")[-3].split("_")[-1])
    print(radius)
    NP_Volume = 4.0 / 3.0 * np.pi * radius * radius * radius


    print("Reading Simulation Global Values")
    # get information about the simulation
    with open(dir_base  + filename + ".mpd", 'r') as fp:
        for i, line in enumerate(fp):
            if i == 9:# this is the line with the sim dimensions on it
                split_line = line.strip().split(" ") # split the file line into its components
                system_dimensions = [float(split_line[1]),float(split_line[2]), float(split_line[3])]


    # grab the number of particles and the name of the experiment from the save file
    parts = None
    name = None
    print("Opening Simulation Data File")

    with open(dir_base + "frames_" + filename + ".xyz", 'r') as fp:
        for i, line in enumerate(fp):
            if i == 0:
                parts = int(line.strip())
            if i == 1:
                name = line.strip()
            if i > 1:
                break
    print("processing densities")
    
    # process the file
    with open(dir_base + "frames_"+filename+".xyz", 'r') as fp:
        for i, line in enumerate(fp):
            split_line = line.strip().split("\t") # split the file line into its components

            # if we have a distributions save it
            # there is a line for each particle plus a line for the number of particles and name of experiment.
            # that's why we have (parts+2)
            if i % (parts + 2) == 0:
                if i > 0:
                    # process distributions for Chi squared metric
                    # run this for the first and last info sets.
                    # iterative sets just show that the density growth is not exceptional.
                    # probably need to handle it in 2^N steps.
                    # code below needs refactor to handle multiple lag deltas.
                    info_lag.append(dist.Distribution)
                    # already processed one distribution so save it's max height
                    brushz_lag.append(dist.ReferenceValue)

                    # reset the distributions so that processing can continue.
                    dist = ReferenceDistribution(_type="Binary", _reference=0.0, _dist=[0, 0])


            #grab and record the highest z value
            if split_line[0] == '1': # this value will always exist even on break lines with the number of particles and name of exp.
                if float(split_line[3]) > dist.ReferenceValue: # check to see if z value is higher than current max
                    dist.update_reference(float(split_line[3]))

            #identify the NP inside and outside the brush
            if split_line[0] == '2': # looking at NPs now
                dist.update_distribution(float(split_line[3]))

    print("processing equilibriums")
    print(str(len(info_lag)) + " values in file")

    lags = [int(2 ** c) for c in range(int(np.log2(len(info_lag) / 2)))]
    rValue = [-1, 0]
    skip = """
    #record equilibrium lags    
    with open(dir_base + "equilibriums.txt", 'w') as fp:
        for j in lags:
            rValue[0] = -1
            sim_track = 0
            for i in range(rValue[1], len(info_lag)-j):

                try:
                    stat, p, dof, arr = chi2_contingency([info_lag[i], info_lag[i+j]])
                except Exception as e:
                    print(str(e))   
                    print([info_lag[i], info_lag[i+j]]) 
                    p=0.0
   
                if p <= significance_level:
                    #print(j, p, 'Reject NULL HYPOTHESIS. distributions too different')
                    sim_track = 0
                else:
                    #print(j, p, 'ACCEPT NULL HYPOTHESIS. distributions very similar',info_lag[i], info_lag[i+j])
                    sim_track += 1
                    if sim_track > 3:
                    # the 3 is in a way arbitrary, but it means the distributions have been fairly similar for 3 times in a row.
                        rValue = [j,i]
                        break
            #write out equilibrium results for lag
            fp.write(str(rValue)+str(info_lag[rValue[1]]))
            
            # check if this lag holds equilibrium at the end
            end_index = len(info_lag)-1
            try:
                stat, p, dof, arr = chi2_contingency([info_lag[end_index], info_lag[rValue[1]]])
            except Exception as e:
                print(str(e))
                print([info_lag[i], info_lag[i+j]])
                p=0.0

            if p <= significance_level:
                #print(j, p, 'Reject NULL HYPOTHESIS. distributions too different')
                # format for Accept (Bool), lag value (int), p value (float), comparison index (int), final index (int)
                fp.write("0, " + str(j) + ", "+ str(p) + ", "+ str(rValue[1]) +", "+str(end_index) +"\n" )
            else:
                #print(j, p, 'ACCEPT NULL HYPOTHESIS. distributions very similar',info_lag[i], info_lag[i+j])
                fp.write("1, " + str(j) + ", "+ str(p) + ", "+ str(rValue[1]) +", "+str(end_index) +"\n" )
    """
    print("writing datafiles")
    #write out data of note
    with open(dir_base + "brush_embeddings.dat", 'w') as fp:
        for x in info_lag:
            fp.write(str(x[0]/(x[1]+x[0]))+"\n")

    with open(dir_base + "brush_height.dat", 'w') as fp:
        for i, x in enumerate(info_lag):
            fp.write(str(brushz_lag[i])+"\n")

    # making a big change here on July4th 2022 until now the densities have been #NP / r0^3 I am changing these to
    # volume fraction
    with open(dir_base + "solvent_NP_volume_fraction.dat", 'w') as fp:
        for i, x in enumerate(info_lag):
            fp.write(str ( x[1]*NP_Volume / (system_dimensions[0] * system_dimensions[1] * (system_dimensions[2] - brushz_lag[i] )))+"\n")

    with open(dir_base + "brush_NP_volume_fraction.dat", 'w') as fp:
        for i, x in enumerate(info_lag):
            fp.write(str ( x[0]*NP_Volume / (system_dimensions[0] * system_dimensions[1] *  brushz_lag[i] ))+"\n")

    inv_solvent_density = []
    inv_brush_density = []
    with open(dir_base + "inv_solvent_volume_fraction.dat", 'w') as fp:
        for i, x in enumerate(info_lag):
            solv_data = x[1]*NP_Volume /  (system_dimensions[0] * system_dimensions[1] * (system_dimensions[2] - brushz_lag[i] ))
            fp.write( str(1.0/(float(i)+ 1.0)) +"\t"+ str(solv_data) + " \n")
            inv_solvent_density.append([1.0/(float(i)+ 1.0) , solv_data])
    
    with open(dir_base + "inv_brush_volume_fraction.dat", 'w') as fp:
        for i, x in enumerate(info_lag):
            brush_data = x[0]*NP_Volume /  (system_dimensions[0] * system_dimensions[1] *  brushz_lag[i] )
            fp.write( str(1.0/(float(i)+ 1.0)) +"\t"+ str(brush_data) + " \n")
            inv_brush_density.append([1.0/(float(i)+ 1.0) , brush_data])
 
    len_equil = int(len(inv_solvent_density)*.2) # use last 20% of simulation to approx equalibrium

    with open(dir_base + "equil_densities.dat", 'w') as fp:
        fp.write("solvent density, x\n")
        fp.write(str(np.polyfit(np.asarray(inv_solvent_density)[-1*len_equil:,0],np.asarray(inv_solvent_density)[-1*len_equil:,1],1)))
        fp.write("\nsolvent density, x^2\n")
        fp.write(str(np.polyfit(np.asarray(inv_solvent_density)[-1*len_equil:,0],np.asarray(inv_solvent_density)[-1*len_equil:,1],2)))
        fp.write("\nbrush density, x\n")
        fp.write(str(np.polyfit(np.asarray(inv_brush_density)[-1*len_equil:,0],np.asarray(inv_brush_density)[-1*len_equil:,1],1)))
        fp.write("\nbrush density, x^2\n")
        fp.write(str(np.polyfit(np.asarray(inv_brush_density)[-1*len_equil:,0],np.asarray(inv_brush_density)[-1*len_equil:,1],2)))



