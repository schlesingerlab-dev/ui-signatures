#!/bin/bash

####################################
### Structural Signatures Pipeline #
### Written by: Rayees Rahman    ###
### For Mount Sinai DToXs        ###
### Version: 2.0: 1.2.18         ###
### Usage: See Below             ###
####################################

####################################
### Environment Variables:       ###
####################################

##for folds clean input (',',":","'', '""'")

if [ -z "$homed" ]; 
then 
	printf "\nThe variable: homed needs to be defined, please define the variable as such:\n\n\033[34mexport homed='/path/to/structural-signatures' >> ~/.bashrc \n\n"; 
	exit  
else 
	printf "\nInstallation directory:\n\t\033[34m$homed\n\n\033[0m"
fi

u="Usage:\n\t -i input gene list \n\t -t domain enrichment (domain) scop enrichment (fold) or both (both)
 \n\t -n name type: gene name (gn) or uniprot id (uid)\n\t -o output file name \n\n)";  
while getopts ":i:o:t:n:d:b:f:g:T:p:lh:e:P:y:c:zh:" opt; do
    case $opt in
		i) 	input=$OPTARG ;;  #input
		t) 	type=$OPTARG ;; #domain or fold 
        n)  name=$OPTARG ;; #gene name (gn) or uid (uid) 
		o)  output=$OPTARG ;; #output file name 
        \?)
        printf "$" 
        exit 1 ;;
    esac
done

if [ -z $input ] || [ -z $type ] || [ -z $name ] || [ -z $output ]
then
	printf "$u" ;
	exit  1
fi

$homed/bin/scripts/get_struct_from_db.pl $homed/database/structure_database.db $type $name $homed/bin/files/ParentChildTreeFile.txt $input $output $homed/bin/files/available_uniprot_ids.csv yes #2> /dev/null
numgenes=$( cat ./$output.found.genes ) 
if [ $type == "domain" ] 
then
    Rscript $homed/bin/scripts/compute_representation.R $output.domain.cnt $homed/bin/files/backgrounds/default.background.ipr.domain.cnt $numgenes $output domain  #2> /dev/null
	rm $output.domain.cnt
	rm $output.found.genes
elif [ $type == "fold" ]
then

	cat ./$output.scop.fold.cnt | cut -f1,2 -d"," > $output.tmp.fold 
	Rscript $homed/bin/scripts/compute_representation.R $output.tmp.fold $homed/bin/files/backgrounds/default.background.scop.fold.cnt.2 $numgenes $output fold #2> /dev/null
	rm ./$output.tmp.fold
	rm ./$output.scop.fold.cnt 
	cat ./$output.scop.superfam.cnt | cut -f1,2 -d"," > $output.tmp.superfam
	Rscript $homed/bin/scripts/compute_representation.R $output.tmp.superfam $homed/bin/files/backgrounds/default.background.scop.superfam.cnt.2 $numgenes $output superfam  #2> /dev/null
	rm ./$output.tmp.superfam 
	rm ./$output.scop.superfam.cnt
	cat ./$output.scop.family.cnt | cut -f1,2 -d"," > $output.tmp.fam
	Rscript $homed/bin/scripts/compute_representation.R $output.tmp.fam $homed/bin/files/backgrounds/default.background.scop.family.cnt.2 $numgenes $output family  #2> /dev/null
	rm ./$output.tmp.fam
	rm ./$output.scop.family.cnt
	rm $output.found.genes
	rm ./$output.scop.class.cnt
else 
	Rscript $homed/bin/scripts/compute_representation.R $output.domain.cnt $homed/bin/files/backgrounds/default.background.ipr.domain.cnt $numgenes $output domain  #2> /dev/null
	rm $output.domain.cnt
	cat ./$output.scop.fold.cnt | cut -f1,2 -d"," > $output.tmp.fold 
	Rscript $homed/bin/scripts/compute_representation.R $output.tmp.fold $homed/bin/files/backgrounds/default.background.scop.fold.cnt.2 $numgenes $output fold  #2> /dev/null
	rm ./$output.tmp.fold
	rm ./$output.scop.fold.cnt
	cat ./$output.scop.superfam.cnt | cut -f1,2 -d"," > $output.tmp.superfam
	Rscript $homed/bin/scripts/compute_representation.R $output.tmp.superfam $homed/bin/files/backgrounds/default.background.scop.superfam.cnt.2 $numgenes $output superfam  #2> /dev/null
	rm ./$output.tmp.superfam 
	rm ./$output.scop.superfam.cnt 
	cat ./$output.scop.family.cnt | cut -f1,2 -d"," > $output.tmp.fam
	Rscript $homed/bin/scripts/compute_representation.R $output.tmp.fam $homed/bin/files/backgrounds/default.background.scop.family.cnt.2 $numgenes $output family #2> /dev/null
	rm ./$output.tmp.fam
	rm ./$output.scop.family.cnt
	rm $output.found.genes
	rm ./$output.scop.class.cnt
fi
exit ; 

