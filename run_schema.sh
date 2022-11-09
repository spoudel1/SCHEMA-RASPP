if [ "$#" != "1" ]; then
	/shared/Software/SCHEMA-RASPP/clustalo -i $1 -outfmt=clustal
	sed '1d' clustal.aln > clustal_1.aln && mv clustal_1.aln clustal.aln
	binder=${2%.*}
	sed '1i HEADER   binder                2022            '$binder'' "$2" > "${binder}_1.pdb"
	mv "${binder}_1.pdb" $2
	python2 /shared/Software/SCHEMA-RASPP/schemacontacts.py -pdb $2 -msa clustal.aln -o contacts.txt
	python2 /shared/Software/SCHEMA-RASPP/rasppcurve.py -msa clustal.aln -con contacts.txt -xo $3 -o opt.txt -min 4
else
	python2 /shared/Software/SCHEMA-RASPP/schemaenergy.py -msa clustal.aln -con contacts.txt -xo $1 -o energies.txt -E -m
	python /shared/Software/SCHEMA-RASPP/helper_scripts/extractseq_schema.py $1 clustal.aln energies.txt
fi
