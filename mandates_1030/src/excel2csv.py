import argparse
import csv
import sys
from xlrd import open_workbook
import re


def init():
    parser = argparse.ArgumentParser()
    parser.add_argument('--infile', dest='infile', 
                        help='input file with mandate data in MS Excel format',
                        required=True)
    parser.add_argument('--outfile_org', dest='outfile_org', 
                        help='output file with organizations in CSV format',
                        required=True)
    parser.add_argument('--outfile_people', dest='outfile_people', 
                        help='output file with people in CSV format',
                        required=True)
    parser.add_argument('--outfile_mandates', dest='outfile_mandates', 
                        help='normalized output file with mandates (people/organizations) in CSV format',
                        required=True)
    parser.add_argument('--outfile_mandates_denorm', dest='outfile_mandates_denorm', 
                        help='denormalized output file with mandates (people/organizations) in CSV format',
                        required=False)
    global args
    args = vars(parser.parse_args())
    print >> sys.stderr, args


def read_file(fn):

    currentOrg = ''
    currentAddress = ''

    currentHeaders = []

    organization2address = {}
    person2address = {}

    wb = open_workbook(filename=fn)
    sheet = wb.sheet_by_index(0)
    print >> sys.stderr, "Reading %d rows and %s columns" % (sheet.nrows, sheet.ncols)

    firstRowsToIgnore = 5

    for rowNr in range(firstRowsToIgnore,sheet.nrows):

        cells = []

        for colNr in range(sheet.ncols):

            cells.append(sheet.cell_value(rowNr,colNr))
        
        lineType = determineLineType(cells)

        if (lineType == 'org_or_category'):
            parts = re.split(' - ', cells[0], maxsplit=1)
            if len(parts) == 2:
                currentOrg, address = parts
#            else:
#                currentOrg, address = ['UNK','UNK']

        if (lineType == 'header'):
            currentHeaders = cells[0:3]

        if (lineType == 'person_with_address'):
            organization2address[currentOrg] = address

            if cells[0] != '':
                person, address = parse_person_address(cells[0])
                person2address[person] = address
                print "%s\t%s\t%s" % (currentOrg, person, currentHeaders[0])
            if cells[1] != '':
                person, address = parse_person_address(cells[1])
                person2address[person] = address
                print "%s\t%s\t%s" % (currentOrg, person, currentHeaders[1])
            if cells[2] != '':
                person, address = parse_person_address(cells[2])
                person2address[person] = address
                print "%s\t%s\t%s" % (currentOrg, person, 'Commissaire')

    print >> sys.stderr, "organization2address = ", organization2address
    print >> sys.stderr, "person2address = ", person2address

def parse_person_address(string):

    m = re.match(r'(\s*M[me\.]*)\s([\S\s]+[A-Z])\s+([\s\S]+){2}', string)

    if m:
        return m.group(2), m.group(3)
    else:
        return 'UNKNOWN_PERSON', 'UNKNOWN_ADDRESS'

def determineLineType(cells):
    
    lineTypes = ['empty','header','org_or_category','person_with_address']

    assert(len(cells) == 3)

    if cells[0] == 'AG' or cells[1] == 'CA' or 'sentation' in cells[0]:
        return 'header'
    elif re.match('M[m.]',cells[0]) and len(cells[0]) > 40:
        return 'person_with_address'
    elif cells[0] == '' and cells[1] == '' and cells[2] == '':
        return 'empty'
    else:
        return 'org_or_category'

if __name__ == '__main__':
    init()
    read_file(args['infile'])
