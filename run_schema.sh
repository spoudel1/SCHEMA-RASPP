SCHEMADIR=/shared/Software/SCHEMA-RASPP
if [ "$#" != "1" ]; then
	$SCHEMADIR/helper_scripts/clustalo -i $1 -outfmt=clustal
	sed '1d' clustal.aln > clustal_1.aln && mv clustal_1.aln clustal.aln
	binder=${2%.*}
	sed '1i HEADER   binder                2022            '$binder'' "$2" > "${binder}_1.pdb"
	mv "${binder}_1.pdb" $2
	python2 $SCHEMADIR/schemacontacts.py -pdb $2 -msa clustal.aln -o contacts.txt
	python2 $SCHEMADIR/rasppcurve.py -msa clustal.aln -con contacts.txt -xo $3 -o opt.txt -min 4
	python $SCHEMADIR/helper_scripts/extract_averagecross.py opt.txt
	python2 $SCHEMADIR/schemaenergy.py -msa clustal.aln -con contacts.txt -xo Average_xo.txt -o energies.txt -E -m
	python $SCHEMADIR/helper_scripts/extractseq_schema.py Average_xo.txt clustal.aln energies.txt
else
	python2 $SCHEMADIR/schemaenergy.py -msa clustal.aln -con contacts.txt -xo $1 -o energies.txt -E -m
	python $SCHEMADIR/helper_scripts/extractseq_schema.py $1 clustal.aln energies.txt
fi
