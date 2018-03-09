#!/usr/bin/python

import argparse
import copy
import sys

import id3_real

parser = argparse.ArgumentParser(
           description='Train (and optionally test) a decision tree')
parser.add_argument('dtree_module',
                    metavar='dtree-module',
                    help='Decision tree module name')
parser.add_argument('classifier',
                    help='Name of the attribute to use for classification')
parser.add_argument('--attributes',
                    type=argparse.FileType('r'),
                    help='Name of the attribute specification file',
                    dest='attributes_file',
                    required=True)
parser.add_argument('--train',
                    type=argparse.FileType('r'),
                    help='Name of the file to use for training',
                    dest='training_file',
                    required=True)
parser.add_argument('--test',
                    type=argparse.FileType('r'),
                    dest='testing_file',
                    help='Name of the file to use for testing')
# debug 1st
#args = parser.parse_args(['id3', 'dangerous', '--attributes', 'tests/dangerous-animals-attributes.txt', '--train', 'tests/dangerous-animals-train.csv'])

# debug 2nd
#args = parser .parse_args(['id3', 'white-can-win', '--attributes', 'tests/kr-vs-kp-attributes.txt', '--train','tests/kr-vs-kp-train.csv','--test','tests/kr-vs-kp-test.csv'])

#args = parser.parse_args(['id3_real', 'income', '--attributes', 'dataset/processed/adult_attrib.txt', '--train', 'dataset/processed/adult.csv'])

#args = parser.parse_args(['id3_real', 'class', '--attributes', 'dataset/realnum/processed/iris_attrib.txt', '--train', 'dataset/realnum/processed/iris.dat', '--test', 'dataset/realnum/processed/iris_test.dat'])


args = parser.parse_args()
# Read in a complete list of attributes.
# global all_attributes
all_attributes = id3_real.Attributes(args.attributes_file)
if args.classifier not in all_attributes.all_names():
  sys.stderr.write("Classifier '%s' not a recognized attribute name\n" %
                   args.classifier)
  sys.exit(1)
classifier = all_attributes[args.classifier]

# Import the d-tree module, removing the .py extension if found
if args.dtree_module.endswith('.py') and len(args.dtree_module) > 3:
  dtree_pkg = __import__(args.dtree_module[:-3])
else:
  dtree_pkg = __import__(args.dtree_module)

# Train
training_data = id3_real.DataSet(args.training_file, all_attributes)
starting_attrs = copy.copy(all_attributes)
starting_attrs.remove(classifier)
dtree = dtree_pkg.DTree(classifier, training_data, starting_attrs)
print dtree.dump()

if args.testing_file:
  testing_data = id3_real.DataSet(args.testing_file, all_attributes)
  correct_results = dtree.test(classifier, testing_data)
  print("%d of %d (%.2f%%) of testing examples correctly identified" %
        (correct_results, len(testing_data),
         (float(correct_results) * 100.0)/ float(len(testing_data))))

