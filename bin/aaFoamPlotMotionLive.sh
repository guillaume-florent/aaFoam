#!/usr/bin/env bash

# log file extract sample
# -----------------------
#Time = 18.038
#
#PIMPLE: iteration 1
#forces forces:
#    Not including porosity effects
#
#6-DoF rigid body motion
#    Centre of rotation: (0.844878009 0 -0.0203574655)
#    Centre of mass: (0.844878009 0 -0.0203574655)
#    Orientation: (0.999348123 0 0.0361016531 0 1 0 -0.0361016531 0 0.999348123)
#    Linear velocity: (0 0 -7.38444211e-05)
#    Angular velocity: (0 9.57820088e-05 0)
#Execution time for mesh.update() = 0.44 s

#########################################################
#                                                       #
# awk 'NR == 1 || (NR-1) % 5 == 0'                      #
#                                                       #
# 5 is the number of outer correctors -> ADJUST         #
#                                                       #
#########################################################

if [$1 == ""]
then
    logfile='logs/solve/log.interFoam'
else
    logfile=$1
fi

#pick centre of mass
grep 'Centre of mass' $logfile | cut -d '(' -f 2 | tr -d ")" > motionCentreMassExtract
grep -e "^Time = " $logfile | cut -d " " -f 3 > motionTimesExtract

awk 'NR == 1 || (NR-1) % 5 == 0' motionCentreMassExtract > motionCentreMassExtract1

paste motionTimesExtract motionCentreMassExtract1 > motionCmPartial
sed -e 's/ [ ]*/\t/g' motionCmPartial > motionCm


#pick euler angle and convert it to degree
grep 'Orientation' $logfile | cut -d '(' -f 2 | tr -d ")" > motionOrt
awk 'NR == 1 || (NR-1) % 5 == 0' motionOrt > motionOrt1

awk '{ print $2 }' motionOrt1 > motionSinTheta
awk '{ print $3 }' motionOrt1 > motionSinTheta

awk '
function acos(x){return atan2(sqrt(1-x*x),x);}
function asin(x){return atan2(x,sqrt(1-x*x));}
function pi(){return 2*asin(1);}
{
        trim_in_deg=asin($logfile)/pi()*180
        print trim_in_deg
}' motionSinTheta > motionTrimExtract
paste motionTimesExtract motionTrimExtract > motionTrim

rm motionCmPartial
rm motionTimesExtract
rm motionCentreMassExtract
rm motionCentreMassExtract1

rm motionOrt
rm motionOrt1
rm motionSinTheta
rm motionTrimExtract

#plot cm and trim angle
gnuplot -persist > /dev/null 2>&1 << EOF
        set title "Motion vs. Time"
        set xlabel "Time / Iteration"
        set ylabel "CG Rise (cm) or Trim Angle (degree)"
		set grid
#        set xrange [3.06:]
        plot    "motionCm" using 1:(100*\$4) title 'CG Rise' with linespoints lt rgb "#3D4F99" lw 1 ps -1,\
                        "motionTrim" using 1:(-\$2) title 'Trim Angle' with linespoints lt rgb "#FF8840" lw 1 ps -1
EOF