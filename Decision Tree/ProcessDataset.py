import argparse
import attributes
import sys
import re
import copy


def mainscript():
    # parse argument
    ap = argparse.ArgumentParser(description='Handle Missing Values in Dataset')
    ap.add_argument('--datafile', '-d',
                        # type = argparse.FileType('r'),
                        help = 'Name of the data file',
                        dest = 'datafile',
                        required = True)
    ap.add_argument('--testfile', '-t',
                    # type=argparse.FileType('r'),
                    help='Name of the test file',
                    dest='testfile')
    ap.add_argument('--attributes', '-a',
                        # type=argparse.FileType('r'),
                        help = 'Name of the attribute specification file',
                        dest = 'attributes_file',
                        required = True)
    # ap.add_argument('--intermediate', '-inter',
    #                 help='Name of attribute intermeiate output file',
    #                 dest='inter'
    #                 )
    ap.add_argument('--output', '-oa',
                    type=argparse.FileType('w'),
                    help='Name of attribute output file',
                    dest='att_outfile',
                    default=sys.stdout)
    ap.add_argument('--output2', '-od',
                    type=argparse.FileType('w'),
                    help='Name of training set output file',
                    dest='train_outfile',
                    default=sys.stdout)
    ap.add_argument('--output3', '-ot',
                    type=argparse.FileType('w'),
                    help='Name of test set output file',
                    dest='test_outfile',
                    default=sys.stdout)
    args = ap.parse_args(['--datafile', './dataset/src/adult.dat',
                          '--attributes','./dataset/src/adult_attrib.txt',
                          '--testfile','./dataset/src/adult_test.dat',
                          '-inter', './dataset/preprocessed/adult_attrib.txt',
                          '-oa', './dataset/processed/adult_attrib.txt',
                          '-od', './dataset/processed/adult.csv',
                          '-ot', './dataset/processed/adult_test.csv'])

    # create training datatable
    preprocess_file(args.datafile, args.datafile + '_preprocessed')
    datatable = create_data_table(args.datafile + '_preprocessed')

    # create testing datatable
    if args.testfile:
        preprocess_file(args.testfile, args.testfile + '_preprocessed')
        testtable = create_data_table(args.datafile + '_preprocessed')

    # create attribute file
    preprocess_file(args.attributes_file, args.attributes_file+'_preprocessed')
    file = open(args.attributes_file+'_preprocessed','r')
    all_attributes = attributes.Attributes(file)
    file.close()

    mod_attributes = modify_attributes(datatable, all_attributes)
    if testtable:
        mod_attributes = modify_attributes(testtable, mod_attributes)
    # output attibutes file
    output_attribute(mod_attributes, args.att_outfile)
    # output datatable
    output_datatable(datatable,args.train_outfile)
    output_datatable(datatable, args.test_outfile)

def modify_attributes(datatable, all_attributes):
    mod_attributes = copy.copy(all_attributes)

    # create '?' in attributes if it exists in data
    for data in datatable:

        for attr_idx in xrange(len(all_attributes)):
            if data[attr_idx] == '?':
                if '?' not in mod_attributes[attr_idx].values:
                    mod_attributes[attr_idx].values.append('?')
    return mod_attributes

def output_datatable(dt, outfile):
    for data in dt:
        line = str(data)
        line = line.replace('[','')
        line = line.replace(']', '')
        line = line.replace('\'', '')
        line = line.replace(' ', '')
        line += '\n'
        outfile.write(line)

def output_attribute(attribs, outfile):
    for attr in attribs:
        typestring =''
        for idx in xrange(len(attr.values)):
            typestring+=attr.values[idx]
            if idx < len(attr.values)-1:
                typestring+=','
        outfile.write(attr.name+':'+typestring+'\n')

# remove space and .
def preprocess_file(infile, outfile = False):
    if not outfile:
        outfile = infile+'_preprocessed'
    o = open(outfile,"w") #open for append
    for line in open(infile):
       line = line.replace(" ","")
       line = line.replace(".", "")
       o.write(line)
    o.close()

def create_data_table(data_file=False):
    ret = []
    if data_file:
        for next_line in open(data_file,'r'):
            # run directly into
            if not next_line or next_line == '\n':
                break
            next_line = next_line.rstrip()
            next_line = re.sub(".*:(.*)$", "\\1", next_line)
            attr_values = next_line.split(',')
            new_example = attr_values
            ret.append(new_example)
    return ret


if __name__ == "__main__":
    mainscript()