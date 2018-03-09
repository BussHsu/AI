import math
import re
import sys

EMPTY_DATASET = 'EMPTY_DATASET'

class Example:
  'An individual example with values for each attribute'

  def __init__(self, values, attributes, filename, line_num):
    if len(values) != len(attributes):
      sys.stderr.write(
        "%s: %d: Incorrect number of attributes (saw %d, expected %d)\n" %
        (filename, line_num, len(values), len(attributes)))
      sys.exit(1)
    # Add values, Verifying that they are in the known domains for each
    # attribute
    self.values = {}
    for ndx in range(len(attributes)):
      value = values[ndx]
      attr = attributes.attributes[ndx]
      if value not in attr.values:
        sys.stderr.write(
          "%s: %d: Value %s not in known values %s for attribute %s\n" %
          (filename, line_num, value, attr.values, attr.name))
        sys.exit(1)
      self.values[attr.name] = value

  def __repr__(self):
    return str(self.values)

  # Find a value for the specified attribute, which may be specified as
  # an Attribute instance, or an attribute name.
  def get_value(self, attr):
    if isinstance(attr, str):
      return self.values[attr]
    else:
      return self.values[attr.name]
    

class DataSet:
  'A collection of instances, each representing data and values'
  def __init__(self, data_file=False, attributes=False):
    self.all_examples = []
    if data_file:
      line_num = 1
      # num_attrs = len(attributes)
      for next_line in data_file:
        next_line = next_line.rstrip()
        next_line = re.sub(".*:(.*)$", "\\1", next_line)
        attr_values = next_line.split(',')
        new_example = Example(attr_values, attributes, data_file.name, line_num)
        self.all_examples.append(new_example)

  def __len__(self):
    return len(self.all_examples)

  def __getitem__(self, key):
    return self.all_examples[key]

  def __repr__(self):
    return 'len = %d' % len(self.all_examples)

  def append(self, example):
    self.all_examples.append(example)

  # Determine the entropy of a collection with respect to a classifier.
  def entropy(self, classifier):
    # IMPLEMENT ME!!!
    if len(self.all_examples)<1:
      return 0
    stat = self.label_stats(classifier)
    ret = 0
    num_examples = len(self.all_examples)
    for type in classifier.values:
        prob = float(stat[type])/num_examples
        if prob:
            ret -= prob*math.log(prob, 2)
    return ret

  # Return the population of each labels
  def label_stats(self, classifier):
    name = classifier.name
    values = classifier.values

    # initialize a statistic
    num_examples = len(self.all_examples)
    stat = {}
    for type in values:
      stat[type] = 0

    # accumulating stats
    for example in self.all_examples:
          stat[example.get_value(name)] += 1
    return stat

  # Find the majority label of dataset
  # return: tie_flag, true if no tie occur, false when tie
  #         max_label, majoritie's value
  def majority_label(self, classifier):
    stat = self.label_stats(classifier)
    breaktie_flag = True
    max = 0
    max_label = None
    for key, value in iter(sorted(stat.iteritems())):
      if value>max:
        breaktie_flag = True
        max = value
        max_label = key
      elif value is max:
        breaktie_flag = False

    return breaktie_flag, max_label

  # Check if the dataset has all the same label:
  # return  EMPTY_DATASET when dataset is empty
  #         label if dataset is homogenious
  #         False otherwise
  def homogenious(self, classifier):
    # if no example in set
    if len(self.all_examples) <1:
      return EMPTY_DATASET

    stat = self.label_stats (classifier)
    selected = None

    for key, value in stat.iteritems():
      if value>0:
        if not selected:
          selected = key
        else:
          break
    else:
      return selected

    return False

  # Find the optimal attribute to partition the data into min entropy
  # Returns (attrib, list)
  #   attrib: the attribute to partition
  #   list: the partition that gives minimun entropy

  def optimal_partition(self, attribs, classifier):
    ret_partition = None
    ret_attrib = None
    min = 10

    for attrib in attribs:
      cand = self.partition_data(attrib)


      if self.weighted_entropy(cand, classifier) < min:
        min = self.weighted_entropy(cand, classifier)
        ret_partition = cand
        ret_attrib = attrib


    return ret_attrib, ret_partition

  # Returns the partition_list based on single attribute
  def partition_data(self, attibute):
    partitions = []

    # initialize the return
    for type in attibute.values:
      partitions.append(DataSet())

    for example in self.all_examples:
      for type_idx in xrange(len(attibute.values)):
        if example.get_value(attibute) == attibute.values[type_idx]:
          partitions[type_idx].append(example)
          break
    return partitions

  # Calculate the weighted entropy of a list of sub-dataset
  def weighted_entropy(self, li_partition, classifier):
    ret = 0
    num_toatl = 0
    for dataset in li_partition:
      num_toatl+= len(dataset)
      ret += len(dataset)*dataset.entropy(classifier)
    if num_toatl:
      return ret/num_toatl
    return 0


