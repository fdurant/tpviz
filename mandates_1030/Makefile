DATADIR=data
SRCDIR=src
OUTDIR=out

EXCEL2CSV=${SRCDIR}/excel2csv.py
BUILDGRAPHML=${SRCDIR}/buildgraphml.py

#INFILE=${DATADIR}/schaerbeek-mandats-partie_1-3.xls
INFILE=${DATADIR}/schaerbeek-mandats-partie_1-3_Frederik.xls

ORG_CSV=${OUTDIR}/organizations_1030.csv
PEOPLE_CSV=${OUTDIR}/people_1030.csv
MANDATES_CSV=${OUTDIR}/mandates_1030.csv

MANDATES_GRAPHML=${OUTDIR}/mandates_1030.graphml

default: ${MANDATES_GRAPHML}

${MANDATES_CSV}: ${EXCEL2CSV} ${INFILE}
	mkdir -p ${OUTDIR}
	python ${EXCEL2CSV} --infile ${INFILE} --outfile_org ${ORG_CSV} --outfile_people ${PEOPLE_CSV} \
				--outfile_mandates ${MANDATES_CSV}

${MANDATES_GRAPHML}: ${BUILDGRAPHML} ${MANDATES_CSV}
	mkdir -p ${OUTDIR}
	python ${BUILDGRAPHML} --infile_edges ${MANDATES_CSV} \
				--source_id_fieldname source \
				--target_id_fieldname target \
				--source_label_fieldname person \
				--target_label_fieldname org \
				--edge_label_fieldname role \
				--source_node_size log2degree \
				--source_min_node_size 5 \
				--source_node_size_multiplier 2 \
				--target_node_size log2degree \
				--target_min_node_size 4 \
				--target_node_size_multiplier 2 \
 				--outfile_graphml ${MANDATES_GRAPHML}
clean:
	rm -rf ${OUTDIR}
