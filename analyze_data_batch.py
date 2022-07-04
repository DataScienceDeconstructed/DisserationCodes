import os
import json
import matplotlib.pyplot as plt
import itertools
import numpy as np

base_dir = "/home/chdavis/Code/mpd-md/bin/exp_test_6"

if __name__ == "__main__":
    x1_solvent = []
    x2_solvent = []
    x1_brush = []
    x2_brush = []
    c_value = []
    labels = []
    densities = {}
    colors = {}
    color_cycle= itertools.cycle(["orange","pink","blue","brown","red","grey","yellow","green","purple","black"])
    plotline_styles =itertools.cycle( ["--","-.",":"])

    Umin = "1"
    rad = "2"

    #cylce through the results files
    for (root,dirs,files) in os.walk(base_dir, topdown=True):
        #look only in the equilibrium density files with the proper variables Umin, rad, etc.
        if "equil_densities.dat" in files and "/Umin_"+Umin+"/rad_"+rad+"/" in root and "/den_1" in root:
            fname = os.path.join(root,"equil_densities.dat")
            #here we assign density and color dictionaries based upon the presences of variables in the file name
            #-2 is number of NP
            #-3 is the burch density
            # we will use this for separating the data later.
            c_value_anchor = fname.split('/')[-2]
            if c_value_anchor not in colors:
                colors[c_value_anchor]=next(color_cycle)
            if fname.split('/')[-3] not in densities:
                densities[fname.split('/')[-3]] = []
            #here we parse the equilibrium data out of the equil_density files.
            with open(fname) as myfile:
                data = myfile.readlines()
                #linear regression for solvent density equilibrium
                x1_solvent.append([float(x) for x in data[1].strip('][\n').split(' ') if len(x)>0][-1])
                # quadratic regression for solvent density equilibrium
                x2_solvent.append([float(x) for x in data[3].strip('][\n').split(' ') if len(x)>0][-1])
                # linear regression for brush density equilibrium
                x1_brush.append([float(x) for x in data[5].strip('][\n').split(' ') if len(x)>0][-1])
                # quadratic regression for solvent density equilibrium
                x2_brush.append([float(x) for x in data[7].strip('][\n').split(' ') if len(x)>0][-1])
#                labels.append([fname.split('/')[-3],fname.split('/')[-2]])

                # here we build a label for the data that can be used during plotting
                labels.append(fname.split('/')[-3])
                # here we append the color that will be assigned to this datapoint
                c_value.append(colors[c_value_anchor])
                # here we update the density dictionary to add this value where it belongs
                densities[fname.split('/')[-3]].append([x1_solvent[-1], x1_brush[-1]])



    print(colors)
    # here we select the equilibrium estimate that we will use for our plots
    # we use the linear regression as the quadratic has offered unphysical negative numbers
    x = x1_solvent
    y = x1_brush

    #here we label the graphs as appropriate
    plt.xlabel("solvent density #NP/r0^3")
    plt.ylabel("brush density #NP/r0^3")
    plt.title("NP brush density as a function fof NP solvent density\n Umin = "+Umin+" \n rad = "+rad+" ")

    #here we cycle through our datasets and plot. the scatter plot should be solvent on the x axis and brush on the y axis
    for i in range(len(x)):
        plt.scatter(x[i], y[i], color=c_value[i])


    for i in range(len(x)):
        plt.text(x[i] * (1 + 0.01), y[i] * (1 + 0.01) , str(labels[i]), fontsize=12)
    #    densities[labels[i]].append([x[i],y[i]])

    for k,v in densities.items():

        bfl = np.sort(np.asarray(densities[k]), axis=0)

        #add trendline to plot
        plt.plot(bfl[:,0], bfl[:,1], linestyle=next(plotline_styles))

    plt.show()

    """fig, axs = plt.subplots(2, 2)
    axs[0, 0].plot(x, y)
    axs[0, 0].set_title('Axis [0, 0]')
    axs[0, 1].plot(x, y, 'tab:orange')
    axs[0, 1].set_title('Axis [0, 1]')
    axs[1, 0].plot(x, -y, 'tab:green')
    axs[1, 0].set_title('Axis [1, 0]')
    axs[1, 1].plot(x, -y, 'tab:red')
    axs[1, 1].set_title('Axis [1, 1]')

    for ax in axs.flat:
        ax.set(xlabel='x-label', ylabel='y-label')

    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()
    """
    print ('--------------------------------')
	
