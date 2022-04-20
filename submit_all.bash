#/bin/bash
threshholds=(0.5 0.55 0.6 0.62 0.64 0.66 0.68 0.7 0.72 0.74 0.76 0.78 0.8 0.82 0.84 0.86 0.88 0.9 0.92 0.94 0.96)
themes=("flower" "lake" "mountain" "puppy" "rain")
for threshhold in ${threshholds[@]}; do
    for theme in ${themes[@]}; do
        command="comp-theme.py --theme '${theme}' --threshhold ${threshhold}"
        qsub -v "command=$command" ./pbs_submit.bash
        
        command="chimp1-theme.py --theme '${theme}' --threshhold ${threshhold}"
        qsub -v "command=$command" ./pbs_submit.bash

        command="chimp2-theme.py --theme '${theme}' --threshhold ${threshhold}"
        qsub -v "command=$command" ./pbs_submit.bash
    done
done
