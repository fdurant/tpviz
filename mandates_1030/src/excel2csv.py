import argparse
import csv
import sys
from xlrd import open_workbook
import re
import codecs

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


def process_file():

    currentOrg = ''
    currentAddress = ''

    currentHeaders = []

    organization2address = {}
    person2address = {}

    wb = open_workbook(filename=args['infile'], encoding_override='utf-8')
    sheet = wb.sheet_by_index(0)
    print >> sys.stderr, "Reading %d rows and %s columns" % (sheet.nrows, sheet.ncols)

    firstRowsToIgnore = 5

    mandateFH = open(args['outfile_mandates_denorm'], 'wb')
    mandateWriter = csv.writer(mandateFH, delimiter='\t')

    mandateHeaders = ['org','person','role']
    mandateWriter.writerow(mandateHeaders)

    for rowNr in range(firstRowsToIgnore,sheet.nrows):

        cells = []

        for colNr in range(sheet.ncols):

            val = sheet.cell_value(rowNr,colNr)
            assert(type(val) == type(u''))
            cells.append(val)
        
        lineType = determineLineType(cells)

        if (lineType == 'org_or_category'):
            # Next line is the exception, actually
            m = re.match(ur'^([^\-]+?)\u2014 ([\S\s]+)$', cells[0], flags=re.UNICODE)
            if m:
                currentOrg = m.group(1)
                address = m.group(2)
            else:
                # And this is the normal case
                parts = re.split(' - ', cells[0], maxsplit=1)
                if len(parts) == 2:
                    currentOrg, address = parts
                else:
                    print >> sys.stderr, "parts = ", parts

            mandateWriter.writerow(['','',''])


#            else:
#                currentOrg, address = ['UNK','UNK']

        if (lineType == 'header'):
            currentHeaders = cells[0:3]

        if (lineType == 'person_with_address'):
            organization2address[currentOrg] = address

            if cells[0] != '':
                person, address = parse_person_address(cells[0])
                person2address[person] = address   
                print >> sys.stderr, "currentOrg = %s" % currentOrg
                print >> sys.stderr, "person = %s" % person
                print >> sys.stderr, "currentHeaders[0] = %s" % currentHeaders[0]
                mandateWriter.writerow([currentOrg.encode('utf-8'), person.encode('utf-8'), currentHeaders[0].encode('utf-8')])
            if cells[1] != '':
                person, address = parse_person_address(cells[1])
                person2address[person] = address
                mandateWriter.writerow([currentOrg.encode('utf-8'), person.encode('utf-8'), currentHeaders[1].encode('utf-8')])
            if cells[2] != '':
                person, address = parse_person_address(cells[2])
                person2address[person] = address
                mandateWriter.writerow([currentOrg.encode('utf-8'), person.encode('utf-8'), currentHeaders[2].encode('utf-8')])

    print >> sys.stderr, "organization2address = ", organization2address
    print >> sys.stderr, "person2address = ", person2address

def parse_person_address(string):

    m = re.match(ur'(\s*M[mevr\.]*)[\s;]+([\S\s\-]+[A-Z\u00C0-\u00DE]{3})\s+([\s\S]+)', string)

    if m:
        return m.group(2), m.group(3)
    else:
        return 'UNKNOWN_PERSON', 'UNKNOWN_ADDRESS'

def determineLineType(cells):
    
    lineTypes = ['empty','header','org_or_category','person_with_address']

    assert(len(cells) == 3)

    if cells[0] == 'AG' or cells[1] == 'CA' or 'sentation' in cells[0]:
        return 'header'
    elif (re.match('M[me. ]',cells[0]) and len(cells[0]) > 40) or (re.match('M[m.]',cells[1]) and len(cells[1]) > 40):
        return 'person_with_address'
    elif cells[0] == '' and cells[1] == '' and cells[2] == '':
        return 'empty'
    else:
        return 'org_or_category'

if __name__ == '__main__':
    init()
    process_file()
