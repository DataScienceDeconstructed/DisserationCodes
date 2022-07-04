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


    for (root,dirs,files) in os.walk(base_dir, topdown=True):
        if "equil_densities.dat" in files and "/Umin_"+Umin+"/rad_"+rad+"/" in root and "/den_1" in root:
            fname = os.path.join(root,"equil_densities.dat")
            c_value_anchor = fname.split('/')[-2]
            if c_value_anchor not in colors:
                colors[c_value_anchor]=next(color_cycle)
            if fname.split('/')[-3] not in densities:
                densities[fname.split('/')[-3]] = []

            with open(fname) as myfile:
                data = myfile.readlines()
                x1_solvent.append([float(x) for x in data[1].strip('][\n').split(' ') if len(x)>0][-1])
                x2_solvent.append([float(x) for x in data[3].strip('][\n').split(' ') if len(x)>0][-1])
                x1_brush.append([float(x) for x in data[5].strip('][\n').split(' ') if len(x)>0][-1])
                x2_brush.append([float(x) for x in data[7].strip('][\n').split(' ') if len(x)>0][-1])
#                labels.append([fname.split('/')[-3],fname.split('/')[-2]])
                labels.append(fname.split('/')[-3])
                c_value.append(colors[c_value_anchor])


    #print(x1_solvent,"\n" ,x2_solvent,"\n", x1_brush,"\n", x2_brush)
    print(colors)
    x = x1_solvent
    y = x1_brush
    for i in range(len(x)):
        plt.scatter(x[i], y[i], color=c_value[i])

    plt.xlabel("solvent density #NP/r0^3")
    plt.ylabel("brush density #NP/r0^3")
    plt.title("NP brush density as a function fof NP solvent density\n Umin = "+Umin+" \n rad = "+rad+" ")
    for i in range(len(x)):
#        plt.text(x[i] * (1 + 0.01), y[i] * (1 + 0.01) , str(labels[i]), fontsize=12)
        densities[labels[i]].append([x[i],y[i]])

    """for k,v in densities.items():

        bfl = np.sort(np.asarray(densities[k]), axis=0)

        z = np.polyfit(bfl[:,0], bfl[:,1], 1)
        p = np.poly1d(z)

        #add trendline to plot
        plt.plot(bfl[:,0], p(bfl[:,0]), linestyle=next(plotline_styles))
    """
    plt.show()
    print ('--------------------------------')
	
