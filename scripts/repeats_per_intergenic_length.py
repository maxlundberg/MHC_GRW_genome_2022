#!/usr/bin/python3

"""
Analysis of BED file created from intersections of intergenic regions BED file with repeat element bed file in which bed features were merged.

$ python3 repeats_per_intergenic_length.py intersection_repeats_intergenic_merged.bed
"""

import sys
import os
import matplotlib
matplotlib.use('Agg')


infile=open(sys.argv[1], 'r')
out=os.path.splitext(os.path.basename(sys.argv[1]))[0]
outfile=open(out + ".perc_repeat_per_intergenic.txt", 'w')

def create_list_of_lengths(file):
    """Split each line of the bed file and store lengths of intergenic region, lengths of repeats, repeat names, and percentage of repeats per intergenic region in a list"""
    lengthsList = [] # list of lists of intergenic and repeat lengths
    speciesNamesDict = {"HC": "Ccor", "JD": "Cmon", "ZF": "Tgut", "CH": "Ggal", "GRW": "Aaru"}
    for line in file:
        edited = line.strip().split("\t")
        repeatIntergenicLengthList = [] # list of species, intergenic region name, intergenic region length, total length of repeat elements in that intergenic region, % repeat coverage per intergenic region, names of repeats
        repeatIntergenicLengthList.append(edited[0]) # species 0
        inter_name = edited[1] + "_" + edited[2] + "_" + edited[3] # Contig name + start + end position of intergenic region
        repeatIntergenicLengthList.append(inter_name) # intergenic name 1 
        repeatIntergenicLengthList.append(int(edited[4])) # intergenic length 2 
        repeatLengthList = [ int(x) for x in edited[8].strip().split(",")] # sum up lengths of all repeat elements in that intergenic region
        repeatIntergenicLengthList.append(sum(repeatLengthList)) # total repeat element length 3
        percentage = int(repeatIntergenicLengthList[3]) / int(repeatIntergenicLengthList[2]) * 100
        repeatIntergenicLengthList.append(percentage) # percentage of repeat element per gene (length) 4
        repeatIntergenicLengthList.append(edited[7]) # repeat element types 5 

        lengthsList.append(repeatIntergenicLengthList) # add intergenic region list to list of lists
    fixedNamesList = [[speciesNamesDict.get(item,item) for item in repeatIntergenicLengthList] for repeatIntergenicLengthList in lengthsList]
    return fixedNamesList

finalList = create_list_of_lengths(infile)

# write percentage repeats per gene to output file
outfile.write("species" + "\t" + "intergenic_region" + "\t" + "intergenic_region_length" + "\t" + "total_repeat_length" + "\t" + "percentage_repeat_per_intergenic_region_length" + "\t" + "repeat_types" + "\n")
for region in finalList:
    line ="\t".join([ str(x) for x in region ])
    outfile.write(line + "\n")

infile.close()
outfile.close()
