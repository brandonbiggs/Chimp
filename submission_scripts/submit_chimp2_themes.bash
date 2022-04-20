#/bin/bash
threshholds=(0.5 0.55 0.6 0.65 0.7 0.75 0.8 0.85 0.9 0.95)
themes=("flower" "lake" "mountain" "puppy" "rain")
for threshhold in ${threshholds[@]}; do
    for theme in ${themes[@]}; do
        command="chimp2-theme.py --theme '${theme}' --threshhold ${threshhold}"
        qsub -v "command=$command" ./pbs_chimp2_theme.bash
    done
done