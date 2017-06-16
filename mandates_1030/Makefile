DATADIR=data
SRCDIR=src
OUTDIR=out

EXCEL2CSV=${SRCDIR}/excel2csv.py

#INFILE=${DATADIR}/schaerbeek-mandats-partie_1-3.xls
INFILE=${DATADIR}/schaerbeek-mandats-partie_1-3_Frederik.xls

OUTFILE_ORG=${OUTDIR}/organizations_1030.csv
OUTFILE_PEOPLE=${OUTDIR}/people_1030.csv
OUTFILE_MANDATES=${OUTDIR}/mandates_1030.csv

default: ${OUTFILE_MANDATES}

${OUTFILE_MANDATES}: ${EXCEL2CSV} ${INFILE}
	mkdir -p ${OUTDIR}
	python ${EXCEL2CSV} --infile ${INFILE} --outfile_org ${OUTFILE_ORG} --outfile_people ${OUTFILE_PEOPLE} \
				--outfile_mandates ${OUTFILE_MANDATES}

clean:
	rm -rf ${OUTDIR}
