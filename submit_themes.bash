#/bin/bash
export file="chimp2-theme.py --theme 'flower'"
qsub -v "file=$file" ./pbs_chimp2_theme.bash

#export file="chimp2-theme.py --theme 'lake'"
#qsub ./pbs_chimp2_theme.bash
#
#export file="chimp2-theme.py --theme 'mountain'"
#qsub ./pbs_chimp2_theme.bash
#
#export file="chimp2-theme.py --theme 'puppy'"
#qsub ./pbs_chimp2_theme.bash
#
#export file="chimp2-theme.py --theme 'rain'"
#qsub ./pbs_chimp2_theme.bash