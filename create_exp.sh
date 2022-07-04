#!/bin/bash

base_dir=$(pwd)
echo "base directory $base_dir"
exp_name='exp_test_8'
exp_dir="$base_dir/$exp_name"
echo "exp directory $exp_dir"
mkdir $exp_dir

gen_dir='/home/chdavis/Code/mpd-md/generate/brushesAndNanoparticles'
time_adjust='/home/chdavis/Code/mpd-md/analysis/changeTime'
int_adjust='/home/chdavis/Code/mpd-md/bin/changeIntervals'

for ((Uindex=1;Uindex<=2;Uindex +=1))
do
Umin_base=-0.175
Umin=`echo 0.0 + $Uindex*$Umin_base | bc`

U_dir="$exp_dir/Umin_$Uindex"
echo $U_dir
mkdir $U_dir

for((radius=2;radius<=4;radius +=2))
do

rad_flt=`echo $radius*1.0 | bc`
rad_dir="$U_dir/rad_$radius"
echo $rad_dir
mkdir $rad_dir

for(( aDen=1;aDen<=20;aDen++ ))
do	
	area_den=`echo 0.0 + $aDen*.03 | bc`
        den_dir="$rad_dir/den_$aDen"
	echo $den_dir
	mkdir $den_dir

	for (( nanos=6;nanos<=10;nanos +=1))
	do
		nan_num=$((2**$nanos))
		
		sim_dir="$den_dir/NP_$nanos"
		echo $sim_dir
		mkdir $sim_dir
		cd $sim_dir
                file_name="$exp_name.Umin$Uindex.rad$radius.den$aDen.NP$nanos"
		echo "filename -> $file_name"
		echo "UMin -> $Umin"
		$gen_dir $file_name $RANDOM 800 $area_den $Umin 40 $nan_num $rad_flt 0 100 100 0.7 3.0 
		$time_adjust $file_name 0 100000
                $int_adjust $file_name 1000 100
		cp "$base_dir/basesim.sh" ./
		#add processing to submission file
		echo "$base_dir/MD $file_name" >> ./basesim.sh
		#add analysis to submission file
		echo "module load python3" >> ./basesim.sh
		echo "python3 /home/chdavis/Code/main.py $sim_dir/ $file_name ">> ./basesim.sh
		sbatch ./basesim.sh
		cd "$base_dir"
	done
done

done
done
