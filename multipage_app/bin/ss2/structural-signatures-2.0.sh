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

#homed=/home/rrahman/structural-signatures-2.0/
homed=/Users/nicolezatorski/Desktop/schless/ss-ui/bin/ss2

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
    Rscript $homed/bin/scripts/compute_representation.R $output.domain.cnt $homed/bin/files/backgrounds/default.background.ipr.domain.cnt $numgenes $output domain  2> /dev/null
elif [ $type == "fold" ]
then

	cat ./$output.scop.fold.cnt | cut -f1,2 -d"," > $output.tmp.fold 
	Rscript $homed/bin/scripts/compute_representation.R $output.tmp.fold $homed/bin/files/backgrounds/default.background.scop.fold.cnt.2 $numgenes $output fold 2> /dev/null
#	rm ./tmp.fold
	cat ./$output.scop.superfam.cnt | cut -f1,2 -d"," > $output.tmp.superfam
	Rscript $homed/bin/scripts/compute_representation.R $output.tmp.superfam $homed/bin/files/backgrounds/default.background.scop.superfam.cnt.2 $numgenes $output superfam  2> /dev/null
#	rm ./tmp.superfam 
	cat ./$output.scop.family.cnt | cut -f1,2 -d"," > $output.tmp.fam
	Rscript $homed/bin/scripts/compute_representation.R $output.tmp.fam $homed/bin/files/backgrounds/default.background.scop.family.cnt.2 $numgenes $output family  2> /dev/null
#	rm ./tmp.fam
else 
	Rscript $homed/bin/scripts/compute_representation.R $output.domain.cnt $homed/bin/files/backgrounds/default.background.ipr.domain.cnt $numgenes $output domain  2> /dev/null
	cat ./$output.scop.fold.cnt | cut -f1,2 -d"," > $output.tmp.fold 
	Rscript $homed/bin/scripts/compute_representation.R $output.tmp.fold $homed/bin/files/backgrounds/default.background.scop.fold.cnt.2 $numgenes $output fold  2> /dev/null
#	rm ./tmp.fold
	cat ./$output.scop.superfam.cnt | cut -f1,2 -d"," > $output.tmp.superfam
	Rscript $homed/bin/scripts/compute_representation.R $output.tmp.superfam $homed/bin/files/backgrounds/default.background.scop.superfam.cnt.2 $numgenes $output superfam  2> /dev/null
#	rm ./tmp.superfam 
	cat ./$output.scop.family.cnt | cut -f1,2 -d"," > $output.tmp.fam
	Rscript $homed/bin/scripts/compute_representation.R $output.tmp.fam $homed/bin/files/backgrounds/default.background.scop.family.cnt.2 $numgenes $output family 2> /dev/null
#	rm ./tmp.fam
fi
#mv ./*.csv ./output/enrichments/
#mv ./*.cnt ./output/counts
exit ; 


exit ;



		T) 	thres=$OPTARG ;;
        b)  numbootstraps=$OPTARG  ;;
        n)  name=$OPTARG   ;;
        g)  numgenes=$OPTARG  ;;
        p)  parallels=$OPTARG ;;
		r) 	disoreg=$OPTARG ;;
		l) 	genelist=1 ;;
		z) 	lonethousand=1 ;; 
		h) 	help=1 ;;
		e) 	ethres=$OPTARG ;; 
		P) 	pthres=$OPTARG ;;
		y) 	prob=$OPTARG ;;
		c) 	cover=$OPTARG ;;
IUPRED=./iupred_predictions
PROF=./human_predict_protein
HHR=./human_proteome_hhpred
SECSTUCT=.
DIR=.

if [ -e ./install.directory ]
then
	DIR=$( cat ./install.directory ) ;
	IUPRED=$( printf "$DIR/Database/iupred/iupred_predictions" )  ;
	PROF=/$( printf "$DIR/Database/human_predict_protein/human_predict_protein" ) ;
	HHR=$( printf "$DIR/Database/human_proteome_hhpred" );
	SECSTRUCT=$( printf $DIR );
fi
if [ ! -d $DIR ] || [ ! -d $IUPRED ] || [ ! -d $PROF ] || [ ! -d $HHR ] || [ ! -d $SECSTUCT ]
then
	printf "In order run structural_signatures.sh you must specify these directories in this script:\n\t\$IUPRED directory to IUPRED predictions\n\t\$PROF directory to predict protein predictions\n\t\$HHR directory to hhpred output\n\t\$SECSTUCT directory to secstruct.sh\nPlease edit secstruct.sh to include these directories\n"
	printf "Or run the install_structural-signatures.sh script\n" ;
	exit
fi

if  hash Rscript 2> /dev/null
then
	printf ""
else
	printf "R/Rscript is required to run this pipeline.\nPlease install the latest version of R and make sure Rscript is accesible from the command line. \n" ;
	exit 1 ;
fi

printf "Working Directory: $DIR \n"
####################################
### Variables:                   ###
####################################
helpout="Help:
	-d: data can be either DToXs data (expected default) or gene list
	    	*if data is a gene list then -l must be called*
	-n: name (prefix) for all output files
	-b: number of total bootstraps, the default value is 0 meaning no bootstraps will run
		*0 bootstraps implies no statistics for 2D structural features*
		*at least 30 bootstraps are required for meaningful statistics*
	-p: number of bootstraps to run in parallel
		default is 1
		for example if -b is 100 and -p is 10 then 10 bootstraps will be run in parallel til a total of 100 bootstraps are run
		if -b is 0 (default) then -p does nothing
	-l: switch to tell script that a gene list is being used instead of a DToXs data
		A gene list is a text file that has each gene on a newline
			**UNIPROT identifiers only!**
		DToXs data is the default data for this script
	-t) type of genes to extract from DToXs data:
		<OVER>expressed genes
		<UNDER>expressed genes
		<BOTH>
		Please input either OVER, UNDER or BOTH, case sensitive, to -t
	-T) scop minimum threshold default 80 *OPTIONAL PARAMETER*
	-r) minumum disordered Region length default 30 *OPTIONAL PARAMETER*
	-h) prints this helpful page! ;)
	-e) = evalue for assigning structure from hhpred output   
	-P) = pvalue for assigning structure from hhpred output 
	-y) = prob for assigning structure from hhpred output 
	-i) = percent identity for assigning structure from hhpred output 
	-c) = coverage for assigning structure from hhpred output
	-q)  use l1000 structure frequencies ; 

An example run of this pipeline using DToXs data looks like this:

	./complete_sec_stuct_pipeline.sh -d Human.A-Hour.48-Plate.4-Calc-CTRL.AXI.tsv -n A,AXI -b 100 -p 10 -t OVER -g 100

This translates to:
	From the "Human.A-Hour.48-Plate.4-Calc-CTRL.AXI.tsv" file (-d Human.A-Hour.48-Plate.4-Calc-CTRL.AXI.tsv )
	all output should have the prefix: "A,AXI" (-n A,AXI)
	bootstrap the data 100 times (-b 100)
	10 boostraps at a time (-p 10 )
	only look at overexpressed signifigant genes (-t OVER)
	and only obtain the top 100 overrepresented genes sorted by p-value ( -g 100 )

An example run of this pipeline using a Gene List data looks like this:

	./complete_sec_stuct_pipeline.sh -d DEGs.list -l -n DEGs -b 100 -p 10

This translates to:
	From the "DEGs.list"  file (-d DEGs.list)
	which is a list of genes (-l)
	all output should have the prefix: "DEGs" (-n DEGs)
	bootstrap the data 100 times (-b 100)
	10 boostraps at a time (-p 10 )

Notice that we call the "-l" option for the gene list example and not for the DToXs example.
Also notice that we call the "-t" & "-g" options for the DToXs example and not for the gene list example.
	The -g option can be left blank to obtain all of the signifigantly expressed genes in the DToXs dataset.
"
help=0
numgenes=0
genelist=0
disoreg=30
numbootstraps=0
ethres='1e-05'
pthres='5e-02'
prob='0'
ident='0'
cover='0'
parallels=1
lonethousand=0 
####################################
### Get Options and Error Check: ###
####################################
##e = evalue for hhpred  P = pvalue for hhpred y = prob for hhpred  i = pident for hhpred c= coverage for hhpred ; 
##q = use l1000 fold frequencies 
while getopts ":d:t:b:f:n:g:T:p:lh:e:P:y:i:c:zh:" opt; do
    case $opt in
        d)  data=$OPTARG ;;
		t) 	type=$OPTARG ;;
		T) 	thres=$OPTARG ;;
        b)  numbootstraps=$OPTARG  ;;
        n)  name=$OPTARG   ;;
        g)  numgenes=$OPTARG  ;;
        p)  parallels=$OPTARG ;;
		r) 	disoreg=$OPTARG ;;
		l) 	genelist=1 ;;
		z) 	lonethousand=1 ;; 
		h) 	help=1 ;;
		e) 	ethres=$OPTARG ;; 
		P) 	pthres=$OPTARG ;;
		y) 	prob=$OPTARG ;;
		i) 	ident=$OPTARG ;;
		c) 	cover=$OPTARG ;;
        #r)  recomb=($OPTARG);;
        \?)
        printf "$usage"
        exit 1 ;;
    esac
done

if [ $help == 1 ]
then
	printf "$usage";
	echo "$helpout"
	exit  1
fi
if [ -z $data ] || [ -z $name ]
then
	printf "$usage" ;
	exit  1
fi

if [ !  -d $DIR/output ]
then
	mkdir $DIR/output
fi

if [ !  -d $DIR/err ]
then
	mkdir $DIR/err
fi

if [ $genelist == 0 ] && [ -z $type ]
then
	printf "You need to specify what types of genes to extract from DToXs data using -t \n\t<OVER>expressed genes\n\t<UNDER>expressed genes\n\t<BOTH>\n "
	exit 1
fi


if [ $numbootstraps -gt 0 ]
then
	if [[ $parallels -gt $numbootstraps ]]
	then
		printf "Number of parallels (-p) cannot be greater than the total number of bootstraps (-b) \nSee -h for help\n"
		exit 1 ;
	fi

fi


####################################
### Functions:					 ###
####################################

bootstrapset ()
{

	if [ !  -d $DIR/bootstrap ]
	then
		mkdir $DIR/bootstrap
	fi
	ls $IUPRED | sort -R | tail -$found > $DIR/bootstrap/$1.$2.protein_set.txt

	while read line
    do
		nam=$( basename $line ".iupred.diso" )

		#disorder
		grep -v "#"  $IUPRED/$line  | sed -E 's/^\s+//'  | sed -E 's/\s+/\t/gi' > $DIR/bootstrap/$1.$2.diso.tmp
		cat $DIR/bootstrap/$1.$2.diso.tmp | awk '{if($3>.5)print;}' | wc -l >> $DIR/bootstrap/$1.$2.bootstrap.disordered.residues.txt
		$SECSTUCT/bin/scripts/get_number_disordered_regions.pl $DIR/bootstrap/$1.$2.diso.tmp  $disoreg | sed -E 's/^\s+//gi' >> $DIR/bootstrap/$1.$2.num.disordered.regions
		#coils
		bs_coils=$(grep "$nam" $SECSTUCT/bin/data/coils_default_output.txt.2 | head -1 )
		if [[ -z $bs_coils ]]
		then
			printf "0\n" >> $DIR/bootstrap/$1.$2.num.coils.bootstrap.txt
		else
			printf "$bs_coils\n" | cut -f1 -d","  >> $DIR/bootstrap/$1.$2.num.coils.bootstrap.txt
		fi
		#sec struct
		grep -v "#" $PROF/$nam.fasta.prof | sed "1d" | cut -f4   >>  $DIR/bootstrap/$1.$2.bootstrap.sec.struct.txt
	done < $DIR/bootstrap/$1.$2.protein_set.txt

	##Disorder
	sumfi $DIR/bootstrap/$1.$2.bootstrap.disordered.residues.txt | sed -E "s/(.+)/\1\n/gi" > $DIR/bootstrap/$1.$2.total.disores.bootstrap.tmp
	sumfi $DIR/bootstrap/$1.$2.num.disordered.regions  | sed -E "s/(.+)/\1\n/gi"  > $DIR/bootstrap/$1.$2.total.disoregi.bootstrap.tmp
	$SECSTUCT/bin/scripts/fc_calc.for.disordered.residues.pl $disorescnt $DIR/bootstrap/$1.$2.total.disores.bootstrap.tmp > $DIR/bootstrap/$1.$2.fold.change.disordered.residues.bootstraps.txt
	$SECSTUCT/bin/scripts/fc_calc.for.disordered.residues.pl $disoregicnt $DIR/bootstrap/$1.$2.total.disoregi.bootstrap.tmp > $DIR/bootstrap/$1.$2.fold.change.disordered.regions.bootstraps.txt
	bgnumdisoregiongene=$( cat $DIR/bootstrap/$1.$2.num.disordered.regions | awk '{ if ( $1 > 0 ) print }' | wc -l 	)
	$SECSTUCT/bin/scripts/fc_calc.generic.pl $numdisoregiongene $bgnumdisoregiongene >> $DIR/output/$2.num.disoregi.gene.fc.txt
	##Coils
	sumfi $DIR/bootstrap/$1.$2.num.coils.bootstrap.txt | sed -E "s/(.+)/\1\n/gi" > $DIR/bootstrap/$1.$2.total.coils.bootstrap.tmp
	bsbgcoil=$( cat $DIR/bootstrap/$1.$2.total.coils.bootstrap.tmp )
	if [[ $bsbgcoil -eq 0 ]]
	then
	    printf "" ##NULL, ignored\n"
		#printf "NULL\n" >> $DIR/err/$3.fold.change.coils.bootstraps.txt.nulls
	else
		$SECSTUCT/bin/scripts/fc_calc.for.disordered.residues.pl $numcoil $DIR/bootstrap/$1.$2.total.coils.bootstrap.tmp | sed -E 's/\t/,/gi' > $DIR/bootstrap/$1.$2.fold.change.coils.bootstraps.txt
	fi
	##Sec Struct
	cat $DIR/bootstrap/$1.$2.bootstrap.sec.struct.txt  | sort | uniq -c | sed -E 's/^\s+//' |  sed -E 's/\s+/,/' | tr -d '\r'  > $DIR/bootstrap/$1.$2.bootstrap.sec.struct.tmp
	$SECSTUCT/bin/scripts/fc_calc.sec.struct.pl $DIR/output/$name.sec.struct.counts.tab $DIR/bootstrap/$1.$2.bootstrap.sec.struct.tmp > $DIR/bootstrap/$1.$2.fold.change.bootstraps.sec.struct.txt

	#sumfi $DIR/bootstrap/$2.$3.bootstrap.disordered.residues.txt | sed -E "s/(.+)/\1\n/gi" >> $DIR/bootstrap/$3.total.disordered.residues.bootstrap.txt
	#sumfi $DIR/bootstrap/$2.$3.num.disordered.regions | sed -E "s/(.+)/\1\n/gi" >> $DIR/bootstrap/$3.total.disordered.regions.bootstrap.txt
	#sumfi $DIR/bootstrap/$2.$3.num.coils.bootstrap.txt | sed -E "s/(.+)/\1\n/gi" > $DIR/bootstrap/$3.total.coils.bootstrap.txt
	#cat $DIR/bootstrap/$2.$3.bootstrap.sec.struct.txt | sort | uniq -c | sed -E 's/^\s+//' |  sed -E 's/\s+/,/' | tr -d '\r'  >> $DIR/bootstrap/$3.bootstrap.sec.struct.txt
	##clean up
#	rm $DIR/bootstrap/$2.$3.bootstrap.folds.txt
#	rm $DIR/bootstrap/$2.$3.bootstrap.sec.struct.txt
#	rm $DIR/bootstrap/$2.$3.num.coils.bootstrap.txt
#	rm $DIR/bootstrap/$2.$3.num.disordered.regions
#	rm $DIR/bootstrap/$2.$3.diso.tmp
#	rm $DIR/bootstrap/$2.$3.bootstrap.disordered.residues.txt
#	rm $DIR/bootstrap/$2.$3.protein_set.txt
}

sumfi ()
{
	i=0
	while read line
	do
		i=$( expr $i + $line)
	done < $1
	printf "$i"
}

####################################
### Main:  						 ###
####################################


if [ $genelist  == 0 ]
then
	if [[ $data =~ \* ]]
	then
		printf ""
	else
		datacheck=$(head -1 $data )
		if [[ ! $datacheck =~ ^CTRL ]]
		then
			printf "It looks like you are not using a DToXs DEG file as input.\nIf you are inputing a gene list you must use the -l option!\n**All genes must be UNIPROT identifiers otherwise they may not be discovered by the script!**\n "
			exit 1 ;
		fi
	fi
	for file in $data  ;
	do
		printf "Working on $file\n";
    	header=$( head -1 $file | sed -E 's/\s+/\n/gi' | wc -l) ### final column in file (FDR)
    	pvalue=$( expr $header - 1 )
		fc=$( expr $pvalue - 2 )
 		if [ $numgenes == 0 ]
		then
			if [[ $type =~ OVER ]]
			then
				cat $file  |  sed -E 's/\t/,/gi' | cut -f1,$fc,$pvalue  -d "," |  sed "1d" | sort -g -k 3 -t$"," |  awk -F"," '{ if ( $2 > 0 && $3 < .05 ) print }' |  cut -f1 -d"," |  sort | uniq  >> $DIR/output/$name.DEGs.txt
			elif [[ $type =~ UNDER ]]
			then
				cat $file  |  sed -E 's/\t/,/gi' | cut -f1,$fc,$pvalue  -d "," |  sed "1d" | sort -g -k 3 -t$"," |  awk -F"," '{ if ( $2 < 0  && $3 < .05 ) print }' |  cut -f1 -d"," |  sort | uniq >> $DIR/output/$name.DEGs.txt
			elif [[ $type =~ BOTH ]]
			then
				cat $file  |  sed -E 's/\t/,/gi' | cut -f1,$fc,$pvalue -d  "," |  sed "1d" | sort -g -k 3 -t$"," |  awk -F"," '{ if ( $3 < .05 ) print }'  | cut -f1 -d"," |  sort | uniq >> $DIR/output/$name.DEGs.txt
			else
				printf "$type not recognized please use either OVER, UNDER or BOTH for -t (case sensitive) \n" ;
				exit 1 ;
			fi
		else
			if [[ $type =~ OVER ]]
			then
				cat $file  |  sed -E 's/\t/,/gi' | cut -f1,$fc,$pvalue -d  "," |  sed "1d" | awk -F"," '{ if ($2 > 0) print }' | sort -g -k 3 -t$"," | head -$numgenes | cut -f1 -d"," | sort | uniq >> $DIR/output/$name.DEGs.txt
			elif [[ $type =~ UNDER ]]
			then
				cat $file  |  sed -E 's/\t/,/gi' | cut -f1,$fc,$pvalue  -d "," |  sed "1d" | awk -F"," '{ if ($2 < 0) print }' | sort -g -k 3 -t$"," | head -$numgenes | cut -f1 -d"," | sort | uniq >> $DIR/output/$name.DEGs.txt
			elif [[ $type =~ BOTH ]]
			then
				cat $file  |  sed -E 's/\t/,/gi' | cut -f1,$fc,$pvalue -d  "," |  sed "1d" | sort -g -k 3 -t$"," | head -$numgenes | cut -f1 -d"," |  sort | uniq >> $DIR/output/$name.DEGs.txt
			else
				printf "$type not recognized please use either OVER, UNDER or BOTH for -t  (case sensitive) \n" ;
				exit 1;
			fi
		fi
	done
else
	cat $data | sort | uniq > $DIR/output/$name.DEGs.txt
fi

cat $DIR/output/$name.DEGs.txt | sort | uniq > $DIR/output/$name.DEGs.uniq.txt
total=$( wc -l $DIR/output/$name.DEGs.uniq.txt | sed -E 's/^([0-9]+).+/\1/gi' )
printf "Extracting structural information for $total genes\n" ;
if [ $lonethousand == 1 ]
then 
	printf "Using L1000 structure frequencies\n"
fi


printf "Gene|Number-of-Disordered-Residues|Number-of-Disordered-Regions|Number-of-Coils|Number-of-transmembrene-helix|Number-of-Strands|Number-of-Helicies|Number-of-Loops|Class|Folds|SuperFamilies|Families\n" > $DIR/output/$name.info
i=1
while read line
do

    gene=$(grep "\-$line-\|^$line-\|\-$line$\|$line$" $SECSTUCT/bin/data/gene.list | head -1 )
	if [[ -z $gene ]]
    then
		printf "$line\n" >> $DIR/output/$name.notfound.txt ;
	else
		###disorder predictions
		printf "$gene|" >> $DIR/output/$name.info
		grep -v "#"  $IUPRED/$gene.iupred.diso | sed -E 's/^\s+//'  | sed -E 's/\s+/\t/gi' > $DIR/output/$name.diso.tmp
		cat $DIR/output/$name.diso.tmp | awk '{if($3>.5)print;}' | wc -l | tr "\n" "|" >> $DIR/output/$name.info
		cat $DIR/output/$name.diso.tmp | awk '{if($3>.5)print;}' | wc -l   >> $DIR/output/$name.DEG.disordered.residue.count.txt
		$SECSTUCT/bin/scripts/get_number_disordered_regions.pl $DIR/output/$name.diso.tmp $disoreg | sed -E 's/^\s+//gi' >> $DIR/output/$name.DEG.disordered.regions.count.txt
		$SECSTUCT/bin/scripts/get_number_disordered_regions.pl $DIR/output/$name.diso.tmp $disoreg | sed -E 's/^\s+//gi' | tr "\n" "|" >> $DIR/output/$name.info

		###Coil Predictions
		coil=$( grep "$gene" $SECSTUCT/bin/data/coils_default_output.txt.2 | head -1 )
		if [[ -z $coil ]]
		then
			printf "0\n" >> $DIR/output/$name.DEG.number.of.coils.per.gene.txt
			printf "0|" >> $DIR/output/$name.info
		else
			printf "$coil\n" | cut -f1 -d"," >> $DIR/output/$name.DEG.number.of.coils.per.gene.txt
			printf "$coil\t" | cut -f1 -d"," | tr "\n" "|" >>  $DIR/output/$name.info
		fi

		###Secondary Structures
		tmh=$( grep -i -A17 "# PROFhtm summary:" $PROF/$gene.fasta.prof  |  grep "HTM_NHTM_BEST"  | sed -E 's/\s+/,/gi' | cut -f5 -d","    )
		if [ -z $tmh ]
		then
			tmh=0 ;
		fi
		printf "$tmh|" >> $DIR/output/$name.info
		printf "$tmh\n" >> $DIR/output/$name.tmh.cnts
		grep -v "#"  $PROF/$gene.fasta.prof | sed "1d" | cut -f4 >> $DIR/output/$name.DEG.sec.struct.txt
		e=$(grep -v "#"  $PROF/$gene.fasta.prof | sed "1d" | cut -f4 | sort | uniq -c | sed -E 's/^\s+//gi' | head -1 | cut -f1 -d" ")
		h=$(grep -v "#"  $PROF/$gene.fasta.prof | sed "1d" | cut -f4 | sort | uniq -c | sed -E 's/^\s+//gi' | head -2 | sed "1d" | cut -f1 -d" ")
		l=$(grep -v "#"  $PROF/$gene.fasta.prof | sed "1d" | cut -f4 | sort | uniq -c | sed -E 's/^\s+//gi' | tail -1 | cut -f1 -d" ")
		printf "$e|$h|$l|" >> $DIR/output/$name.info
		###Folds
		
		$SECSTUCT/bin/scripts/parse_hhr_complete.pl $HHR/$gene/$gene.hhr $SECSTUCT/bin/data/scope_total.txt class $ethres $pthres $prob $ident $cover | cut -f1,4 -d"," >> $DIR/output/$name.DEG.class.txt
		$SECSTUCT/bin/scripts/parse_hhr_complete.pl $HHR/$gene/$gene.hhr $SECSTUCT/bin/data/scope_total.txt class $ethres $pthres $prob $ident $cover  | cut -f4 -d"," | tr "\r" "\n" | tr "\n" "," |  sed -E 's/,,//gi' | sed -E 's/,$//gi' >> $DIR/output/$name.info
		$SECSTUCT/bin/scripts/parse_hhr_complete.pl $HHR/$gene/$gene.hhr $SECSTUCT/bin/data/scope_total.txt fold $ethres $pthres  $prob $ident $cover  | cut -f1,4 -d"," >> $DIR/output/$name.DEG.fold.txt
		$SECSTUCT/bin/scripts/parse_hhr_complete.pl $HHR/$gene/$gene.hhr $SECSTUCT/bin/data/scope_total.txt fold $ethres $pthres $prob $ident $cover  | cut -f4 -d"," | tr "\r" "\n" | tr "\n" "," |  sed -E 's/,,//gi' | sed -E 's/,$//gi' |  sed -E 's/(.+)/\|\1/gi' >> $DIR/output/$name.info
		$SECSTUCT/bin/scripts/parse_hhr_complete.pl $HHR/$gene/$gene.hhr $SECSTUCT/bin/data/scope_total.txt superfamily $ethres $pthres $prob $ident $cover   | cut -f1,4 -d"," >> $DIR/output/$name.DEG.superfam.txt
		$SECSTUCT/bin/scripts/parse_hhr_complete.pl $HHR/$gene/$gene.hhr $SECSTUCT/bin/data/scope_total.txt superfamily $ethres $pthres  $prob $ident $cover  | cut -f4 -d"," | tr "\r" "\n" | tr "\n" "," |  sed -E 's/,,//gi' | sed -E 's/,$//gi' | sed -E 's/(.+)/\|\1/gi'  >> $DIR/output/$name.info
		$SECSTUCT/bin/scripts/parse_hhr_complete.pl $HHR/$gene/$gene.hhr $SECSTUCT/bin/data/scope_total.txt family $ethres $pthres $prob $ident $cover  | cut -f1,4 -d"," >> $DIR/output/$name.DEG.fam.txt
		$SECSTUCT/bin/scripts/parse_hhr_complete.pl $HHR/$gene/$gene.hhr $SECSTUCT/bin/data/scope_total.txt family $ethres $pthres $prob $ident $cover  | cut -f4 -d"," | tr "\r" "\n" | tr "\n" "," |  sed -E 's/,,//gi' | sed -E 's/,$//gi' | sed -E 's/(.+)/\|\1/gi' >> $DIR/output/$name.info
		printf "\n" >> $DIR/output/$name.info
	fi
	pd=$(( 100 * $i))
	pc=$( printf "$pd\t$total" | awk '{printf "%.2f \n", $1/$2}')
	echo -ne "Current percentage completed: $pc% \r"
	i=$( expr $i + 1)
done < $DIR/output/$name.DEGs.uniq.txt
printf "\n" ;

if [ -d $DIR/output/$name.notfound.txt ] ; then
	notfound=$(cat $DIR/output/$name.notfound.txt |  wc -l )
fi
found=""
if [ -z $notfound ]
then
	found=$total
	printf "All $total genes found\n"
else
	found=$( expr $total - $notfound )
	printf "$found out of $total found \n"
fi
printf "$found\n" >> $DIR/output/$name.found.txt

sumfi $DIR/output/$name.tmh.cnts > $DIR/output/$name.tmh.total
cat $DIR/output/$name.DEG.class.txt | cut -f2 -d"," | sort | uniq -c | sed -E 's/^\s+//gi' | sed -E 's/\s+/,/' > $DIR/output/$name.DEG.class.counts
cat $DIR/output/$name.DEG.fold.txt | cut -f2 -d"," | sort | uniq -c | sed -E 's/^\s+//gi' | sed -E 's/\s+/,/' > $DIR/output/$name.DEG.fold.counts
cat $DIR/output/$name.DEG.superfam.txt | cut -f2 -d"," | sort | uniq -c | sed -E 's/^\s+//gi' | sed -E 's/\s+/,/' | sed -E "s/'//gi" > $DIR/output/$name.DEG.superfam.counts
cat $DIR/output/$name.DEG.fam.txt | cut -f2 -d"," | sort | uniq -c | sed -E 's/^\s+//gi' | sed -E 's/\s+/,/' > $DIR/output/$name.DEG.fam.counts
cut -f3 -d"|" $DIR/output/$name.info  | awk '{ if ( $1 > 0 ) print }' | wc -l >  $DIR/output/$name.tot.genes.with.disordered.regions
numdisoregiongene=$( cat $DIR/output/$name.tot.genes.with.disordered.regions | awk '{ if ( $1 > 0 ) print }' | wc -l 	 )
if [ $lonethousand == 0 ]
then 
	Rscript $SECSTUCT/bin/scripts/fold_fisher.R $SECSTUCT/bin/data/proteome.family.80.counts.csv $DIR/output/$name.DEG.fam.counts $found  | sort -g -t$"," -k4 | sed -E "s/(.+)/$name,\1/gi" >> $DIR/output/$name.family.csv
	Rscript $SECSTUCT/bin/scripts/fold_fisher.R $SECSTUCT/bin/data/proteome.superfamily.80.counts.csv $DIR/output/$name.DEG.superfam.counts $found  | sort -g -t$"," -k4 | sed -E "s/(.+)/$name,\1/gi" >> $DIR/output/$name.superfamily.csv
	Rscript $SECSTUCT/bin/scripts/fold_fisher.R $SECSTUCT/bin/data/proteome.fold.80.counts.csv $DIR/output/$name.DEG.fold.counts $found  | sort -g -t$"," -k4 | sed -E "s/(.+)/$name,\1/gi" >> $DIR/output/$name.fold.csv
	Rscript $SECSTUCT/bin/scripts/fold_fisher.R $SECSTUCT/bin/data/proteome.class.80.counts.csv $DIR/output/$name.DEG.class.counts $found  | sort -g -t$"," -k4 | sed -E "s/(.+)/$name,\1/gi" >> $DIR/output/$name.class.csv
else 
	Rscript $SECSTUCT/bin/scripts/fold_fisher.R $SECSTUCT/bin/data/l1000.family.80.csv $DIR/output/$name.DEG.fam.counts $found  | sort -g -t$"," -k4 | sed -E "s/(.+)/$name,\1/gi" >> $DIR/output/$name.family.csv
	Rscript $SECSTUCT/bin/scripts/fold_fisher.R $SECSTUCT/bin/data/l1000.superfamily.80.csv $DIR/output/$name.DEG.superfam.counts $found  | sort -g -t$"," -k4 | sed -E "s/(.+)/$name,\1/gi" >> $DIR/output/$name.superfamily.csv
	Rscript $SECSTUCT/bin/scripts/fold_fisher.R $SECSTUCT/bin/data/l1000.folds.80.csv $DIR/output/$name.DEG.fold.counts $found  | sort -g -t$"," -k4 | sed -E "s/(.+)/$name,\1/gi" >> $DIR/output/$name.fold.csv
	Rscript $SECSTUCT/bin/scripts/fold_fisher.R $SECSTUCT/bin/data/proteome.class.80.counts.csv $DIR/output/$name.DEG.class.counts $found  | sort -g -t$"," -k4 | sed -E "s/(.+)/$name,\1/gi" >> $DIR/output/$name.class.csv
fi 

if [[ $numbootstraps -gt 0 ]]
then
	printf "Performing initial calculations\n"
	###Disorder
	sumfi $DIR/output/$name.DEG.disordered.residue.count.txt | sed -E 's/(.+)/\1\n/gi'  > $DIR/output/$name.total.disordered.residues.txt
	disorescnt=$( sumfi $DIR/output/$name.DEG.disordered.residue.count.txt )
	sumfi $DIR/output/$name.DEG.disordered.regions.count.txt  | sed -E 's/(.+)/\1\n/gi'  > $DIR/output/$name.total.disordered.regions.txt
	disoregicnt=$( sumfi $DIR/output/$name.DEG.disordered.regions.count.txt  )


	###Secondary Structures
	sort $DIR/output/$name.DEG.sec.struct.txt | uniq -c | sed -E 's/^\s+//gi'  | sed -E 's/\s+/,/ gi' > $DIR/output/$name.sec.struct.counts.tab

	###Coils
	numcoil=$( sumfi $DIR/output/$name.DEG.number.of.coils.per.gene.txt  )
	sumfi $DIR/output/$name.DEG.number.of.coils.per.gene.txt   | sed -E "s/(.+)/\1\n/gi" > $DIR/output/$name.total.number.coils.txt

	numsets=$( expr $numbootstraps / $parallels )
	r=$( printf "$numsets\t$parallels" | awk '{ print $1 * $2 }' )
	remain=$(expr $numbootstraps - $r)

	for i in $( seq 1 $numsets)
	do
		echo -ne "Bootstrap set $i of $numsets \r"
		for ii in $( seq 1 $parallels )
		do
			ran=$(perl -MPOSIX -e "print int(rand(1000000000));")
			bootstrapset $ran $name &
		done
		wait
	done
	if [[ $remain -gt 0 ]]
	then
		printf "\n"
		for i in $( seq 1 $remain )
		do
			tot=$(expr $i + $r )
			printf  "Working on remaining bootstraps number: $tot\n"
			ran=$(perl -MPOSIX -e "print int(rand(1000000000));")
			bootstrapset $ran $name &
		done
		wait ;
	fi
	cat $DIR/bootstrap/*.$name.total.disores.bootstrap.tmp >> $DIR/bootstrap/$name.total.disordered.residues.bootstrap.txt
	rm  $DIR/bootstrap/*.$name.total.disores.bootstrap.tmp
	cat $DIR/bootstrap/*.$name.total.disoregi.bootstrap.tmp >> $DIR/bootstrap/$name.total.disordered.regions.bootstrap.txt
	rm 	$DIR/bootstrap/*.$name.total.disoregi.bootstrap.tmp
	cat $DIR/bootstrap/*.$name.fold.change.disordered.residues.bootstraps.txt  >> $DIR/bootstrap/$name.fold.change.disordered.residues.bootstraps.txt
	rm  $DIR/bootstrap/*.$name.fold.change.disordered.residues.bootstraps.txt
	cat $DIR/bootstrap/*.$name.fold.change.disordered.regions.bootstraps.txt >> $DIR/bootstrap/$name.fold.change.disordered.regions.bootstraps.txt
	rm  $DIR/bootstrap/*.$name.fold.change.disordered.regions.bootstraps.txt
	cat $DIR/bootstrap/*.$name.total.coils.bootstrap.tmp >> $DIR/bootstrap/$name.total.coils.bootstrap.txt
	rm  $DIR/bootstrap/*.$name.total.coils.bootstrap.tmp
	cat $DIR/bootstrap/*.$name.fold.change.coils.bootstraps.txt >> $DIR/bootstrap/$name.fold.change.coils.bootstraps.txt
	rm  $DIR/bootstrap/*.$name.fold.change.coils.bootstraps.txt
	cat $DIR/bootstrap/*.$name.bootstrap.sec.struct.tmp >> $DIR/bootstrap/$name.bootstrap.sec.struct.txt
	rm  $DIR/bootstrap/*.$name.bootstrap.sec.struct.tmp
	cat $DIR/bootstrap/*.$name.fold.change.bootstraps.sec.struct.txt >> $DIR/bootstrap/$name.fold.change.bootstraps.sec.struct.txt
	rm  $DIR/bootstrap/*.$name.fold.change.bootstraps.sec.struct.txt
	printf "Performing final calculations\n"
	Rscript $SECSTUCT/bin/scripts/coils.R $DIR/bootstrap/$name.total.coils.bootstrap.txt $DIR/output/$name.total.number.coils.txt bootstrap/$name.fold.change.coils.bootstraps.txt | sed -E 's/\s+//gi' | sed -E "s/(.+)/$name,\1/gi"  > $DIR/output/$name.coils.csv 2> $DIR/err/r.err
	Rscript $SECSTUCT/bin/scripts/coils.R $DIR/bootstrap/$name.total.disordered.residues.bootstrap.txt $DIR/output/$name.total.disordered.residues.txt $DIR/bootstrap/$name.fold.change.disordered.residues.bootstraps.txt | sed -E 's/\s+//gi' | sed -E "s/(.+)/$name,\1/gi" > $DIR/output/$name.disordered.residues.csv
	Rscript $SECSTUCT/bin/scripts/coils.R $DIR/bootstrap/$name.total.disordered.regions.bootstrap.txt $DIR/output/$name.total.disordered.regions.txt $DIR/bootstrap/$name.fold.change.disordered.regions.bootstraps.txt | sed -E 's/\s+//gi' | sed -E "s/(.+)/$name,\1/gi" > $DIR/output/$name.disordered.regions.csv
	Rscript $SECSTUCT/bin/scripts/sec_struct.R $DIR/bootstrap/$name.bootstrap.sec.struct.txt $DIR/output/$name.sec.struct.counts.tab $DIR/bootstrap/$name.fold.change.bootstraps.sec.struct.txt | sed -E 's/\s+//gi' | sed -E "s/(.+)/$name,\1/gi" > $DIR/output/$name.secondary.structure.csv
	sed -i '1s/^/name,number_of_coils,z_score,mean_fold_change\n/' $DIR/output/$name.coils.csv
	sed -i '1s/^/name,Number-of-Disordered-Residues,z_score,mean_fold_change\n/' $DIR/output/$name.disordered.residues.csv
	sed -i '1s/^/name,Number-of-Disordered-Residues,z_score,mean_fold_change\n/' $DIR/output/$name.disordered.regions.csv
	sed -i '1s/^/name,structure,counts,z_score,mean_fold_change,pvalue\n/' $DIR/output/$name.secondary.structure.csv
	rm $DIR/output/$name.num.disoregi.gene.fc.txt
	rm $DIR/output/$name.sec.struct.counts.tab
	rm $DIR/output/$name.total.disordered.regions.txt
	rm $DIR/output/$name.total.disordered.residues.txt
	rm $DIR/output/$name.total.number.coils.txt
	rm -r $DIR/bootstrap
fi

####################################
### Fix Output Headers 			 ###
####################################

sed -i '1s/^/name,family,count,expected_count,fold_change,pvalue\n/' $DIR/output/$name.family.csv
sed -i '1s/^/name,superfamily,count,expected_count,fold_change,pvalue\n/' $DIR/output/$name.superfamily.csv
sed -i '1s/^/name,fold,count,expected_count,fold_change,pvalue\n/' $DIR/output/$name.fold.csv
sed -i '1s/^/name,class,count,expected_count,fold_change,pvalue\n/' $DIR/output/$name.class.csv



####################################
### Clean up:                    ###
####################################
rm $DIR/output/$name.DEGs.txt
rm $DIR/output/$name.DEGs.uniq.txt
rm $DIR/output/$name.diso.tmp
rm $DIR/output/$name.DEG.class.txt
rm $DIR/output/$name.DEG.fold.txt
rm $DIR/output/$name.DEG.superfam.txt
rm $DIR/output/$name.DEG.fam.txt
rm $DIR/output/$name.DEG.sec.struct.txt
rm $DIR/output/$name.found.txt
rm $DIR/output/$name.DEG.fam.counts
rm $DIR/output/$name.DEG.superfam.counts
rm $DIR/output/$name.DEG.fold.counts
rm $DIR/output/$name.DEG.class.counts
rm $DIR/output/$name.tmh.cnts
rm $DIR/output/$name.DEG.disordered.regions.count.txt
rm $DIR/output/$name.DEG.disordered.residue.count.txt
rm $DIR/output/$name.DEG.number.of.coils.per.gene.txt
