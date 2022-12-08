SCHEMADIR=/shared/Software/SCHEMA-RASPP
if [ "$#" != "1" ]; then
	$SCHEMADIR/helper_scripts/clustalo -i $1 -outfmt=clustal 
	sed '1d' clustal.aln > clustal_1.aln && mv clustal_1.aln clustal.aln
	binder=${2%.*}
#	binder="$(cut -d'_' -f1 <<< $2)"
	echo $binder
	sed '1i HEADER   binder                2022            '$binder'' "$2" > "${binder}_1.pdb"
	#cp "${1%.*}_nt.txt" $2
	mv "${binder}_1.pdb" $2
	python2 $SCHEMADIR/schemacontacts.py -pdb $2 -msa clustal.aln -o contacts.txt
	python2 $SCHEMADIR/rasppcurve.py -msa clustal.aln -con contacts.txt -xo $3 -o opt.txt -min 4
	python /shared/Software/SCHEMA-RASPP/helper_scripts/extract_averagecross.py opt.txt
	python2 $SCHEMADIR/schemaenergy.py -msa clustal.aln -con contacts.txt -xo Average_xo.txt -o energies.txt -E -m
	python $SCHEMADIR/helper_scripts/extractseq_schema_v2.py -x Average_xo.txt -m clustal.aln -e energies.txt -n "${1%.*}_nt.txt" -o Chimera_sequences_aa.fasta -nto Chimera_sequences_nt.fasta
else
	python2 $SCHEMADIR/schemaenergy.py -msa clustal.aln -con contacts.txt -xo $1 -o energies.txt -E -m
	python $SCHEMADIR/helper_scripts/extractseq_schema_v2.py -x $1 -m clustal.aln -e energies.txt -o Chimera_sequences_aa.fasta
fi
