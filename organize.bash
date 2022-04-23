themes=("flower" "lake" "mountain" "puppy" "rain")
for theme in ${themes[@]}; do
    awk 'NF' logs/chimp1-themes-$theme.txt | sort -k 9 >> results/chimp1.txt
    echo "" >> results/chimp1.txt
    awk 'NF' logs/chimp2-themes-$theme.txt | sort -k 9 >> results/chimp2.txt
    awk 'NF' logs/comp-themes-$theme.txt | sort -k 8 >> results/comp.txt
done