import re
import sys
import math
import copy

# Attributes
class Attribute:
    'A single attribute description: name + permissible values'

    def __init__(self, name):
        self.name = name
        self.is_category = True

    def __lt__(self, other):
        return self.name < other.name

    def __eq__(self, other):
        return self.name == other.name

    # Calculate the weighted entropy of a list of sub-dataset
    def weighted_entropy(self, li_partition, classifier):
        ret = 0
        num_toatl = 0
        for dataset in li_partition:
            num_toatl += len(dataset)
            ret += len(dataset) * dataset.entropy(classifier)
        if num_toatl:
            return ret / num_toatl
        return 0

    def split_data(self, dataset, classifier):
        return 0, None, None

class RealNumAttribute(Attribute):
    partition_symbole = ['<', '>=']

    def __init__(self, name):
        Attribute.__init__(self, name)
        self.is_category = False

    def __repr__(self):
        return self.name + ' --> Real Value'

    # split data according to min entropy
    #

    def split_data(self, dataset, classifier):

        opt_bound = 0
        opt_partition = []
        sorted_list = sorted(dataset.all_examples, key=lambda k: k.get_value(self.name))
        # minimum entropy and binary partition list
        min = 10
        for idx in xrange(len(sorted_list)-1):
            left = float(sorted_list[idx].get_value(self))
            right = float(sorted_list[idx+1].get_value(self))
            deci_bound = (left+right)/2
            li_partition = [DataSet.CreateDataset(sorted_list[:idx+1]), DataSet.CreateDataset(sorted_list[idx+1:])]
            entropy = self.weighted_entropy(li_partition, classifier)
            if entropy < min:
                min = entropy
                opt_bound = deci_bound
                opt_partition = li_partition
                # Debug check
                if opt_bound > 1000:
                    a = sorted_list[idx]
                    b = a.get_value(self)
                    c = sorted_list[idx+1]
                    d = c.get_value(self)

        return min, opt_bound, opt_partition

class CategoryAttribute(Attribute):
    def __init__(self, name, values):
        Attribute.__init__(self, name)
        self.values = values

    def __repr__(self):
        return self.name + ' --> ' + str(self.values)

    def __getitem__(self, idx):
        return self.values[idx]

    # Returns the partition_list based on attribute
    def split_data(self, dataset, classifier):
        partitions = []

        # initialize the return
        for type in self.values:
            partitions.append(DataSet())

        for example in dataset.all_examples:
            for type_idx in xrange(len(self.values)):
                if example.get_value(self.name) == self.values[type_idx]:
                    partitions[type_idx].append(example)
                    break

        return self.weighted_entropy(partitions, classifier), None, partitions

class Attributes:
    'An ordered collection of attributes and values'

    # Create a new instance of an attribute collection. If a file is
    # specified, use it to initialize the collection from that file.
    # The expected file format is:
    # attr-name:value[,value]...
    def __init__(self, attribute_file=False):
        self.attributes = []
        if attribute_file:
            line_num = 1
            for next_line in attribute_file:
                valid_line = re.match("^(.*[^ ]+)\s*:\s*(\S*)\s*$", next_line)
                if not valid_line:
                    sys.stderr.write("%s: %d: Failed to parse\n" %
                                     (attribute_file.name, line_num))
                    sys.exit(1)
                name = valid_line.group(1)
                values = valid_line.group(2).split(',')

                if len(values)==1 and values[0] == 'continuous':
                    new_attr = RealNumAttribute(name)
                else:
                    new_attr = CategoryAttribute(name, values)

                self.attributes.append(new_attr)
                line_num += 1

    # Implement the [] operator. If an index is specified, return the
    # corresponding attribute. This is useful for correlating an attribute
    # to a value from an example, where we don't know the attribute's
    # name, but we have the order from the example. A string can also
    # be used as an index to retrieve the attribute with the specified
    # name.
    def __getitem__(self, key):
        if isinstance(key, int):
            return self.attributes[key]
        elif isinstance(key, str):
            for attr in self.attributes:
                if attr.name == key:
                    return attr
            sys.stderr.write("Erroneous call to __getitem__\n")
            sys.exit(1)

    def __len__(self):
        return len(self.attributes)

    def __str__(self):
        result = '[\n'
        for attr in self.attributes:
            result += ('  ' + str(attr) + '\n')
        result += ']'
        return result

    def __copy__(self):
        new_instance = Attributes()
        new_instance.attributes = self.attributes[:]
        return new_instance

    def all_names(self):
        return [attr.name for attr in self.attributes]

    # If the key is a name, remove the attribute(s) with that name. If the
    # key is an attribute, remove that attribute.
    def remove(self, key):
        if isinstance(key, str):
            for attr in self.attributes:
                if attr.name == key:
                    self.attributes.remove(attr)
        else:
            self.attributes.remove(key)


 # Examples
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
      if attr.is_category and value not in attr.values:
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

# signal of empty dataset
EMPTY_DATASET = 'EMPTY_DATASET'

# DataSet
class DataSet:
  'A collection of instances, each representing data and values'
  def __init__(self, data_file=False, attributes=False):
    self.all_examples = []
    if data_file:
      line_num = 1
      for next_line in data_file:
        next_line = next_line.rstrip()
        next_line = re.sub(".*:(.*)$", "\\1", next_line)
        attr_values = next_line.split(',')
        new_example = Example(attr_values, attributes, data_file.name, line_num)
        self.all_examples.append(new_example)

  @staticmethod
  def CreateDataset(data):
    ret = DataSet()
    ret.all_examples = copy.copy(data)
    return ret

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
    if isinstance(classifier, RealNumAttribute):
      sys.stderr.write("Classifier should have category value!")
      sys.exit(1)

    if len(self.all_examples) < 1:
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
    if isinstance(classifier, RealNumAttribute):
      sys.stderr.write("Classifier should have category value!")
      sys.exit(1)
    name = classifier.name
    values = classifier.values

    # initialize a statistic
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
    if len(self.all_examples) < 1:
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
    ret_boundary = None
    min = 10

    for attrib in attribs:
      entropy, deci_bound, partitions = attrib.split_data(self, classifier)
      if entropy < min:
        min = entropy
        ret_attrib = attrib
        ret_partition = partitions
        ret_boundary = deci_bound

    return ret_attrib, ret_boundary, ret_partition

# TODO Tree

class DTree:
  'Represents a decision tree created with the ID3 algorithm'

  def __init__(self, classifier, training_data, attributes):
    # Assumes training_data size > 0
    #         attribute size > 0
    attributes.attributes.sort()
    self.classifier = classifier
    # IMPLEMENT ME!!!
    root = None
    label = training_data.homogenious(classifier)
    if label and label:
        root = LeafNode(None, label, None)
    else:
      root = BranchNode(None, training_data, attributes, classifier, None)

    self.root = root

  def test(self, classifier, testing_data):
    # IMPLEMENT ME!!!
    if classifier != self.classifier:
        sys.stderr.write("tree is build on %s, cannot resolve based on %s" %
                         (self.classifier, classifier.name))
        sys.exit(1)

    total = len(testing_data)
    correct = 0
    for example in testing_data:
      current = self.root
      while not isinstance(current, LeafNode):
        if current.attrib.is_category:
          current = current.children[example.get_value(current.attrib)]
        else:
          realnum = float(example.get_value(current.attrib))
          if realnum < current.deci_bound:
              current = current.children['<'+str(current.deci_bound)]
          else:
              current = current.children['>='+str(current.deci_bound)]

      if current.label == example.get_value(classifier):
        correct += 1
    return correct

  def dump(self):
    # IMPLEMENT ME
    # DF traversal, pre-order print
    self.root.on_dump()
    return ""

class LeafNode:
  def __init__(self,parent,label,value):
    self.parent = parent
    if parent:
      self.level = parent.level+1
    else:
      self.level = 0
    self.value = value
    self.label = label

  def __repr__(self):
    if self.parent:
      return self.level*' '+self.parent.attrib.name+':'+self.value+'\n'+(self.level+1)*' '+'<'+self.label+'>'
    return '<'+self.label+'>'

  def __lt__(self, o):
    return self.value < o.value

  def on_dump(self):
    print str(self)

class BranchNode:

  def __init__(self, parent, dataset, attribs, classifier, value):
    self.parent = parent
    self.value = value
    self.deci_bound = None
    if not parent:
      self.level = -1 # root
    else:
      self.level = parent.level+1

    # create label by majority
    breaktie , self.label = dataset.majority_label(classifier)
    if not breaktie and parent:
      self.label = parent.label

    # create children
    self.children = {}
    self.attrib, self.deci_bound, children_data = dataset.optimal_partition(attribs, classifier)
    # attributes left for children
    attribs_left = copy.copy(attribs)
    attribs_left.remove(self.attrib)

    # Branching for categorical attribute
    if self.deci_bound == None:
        for idx in xrange(len(self.attrib.values)):
          type = self.attrib[idx]
          subset = children_data[idx]

          # subset is homogenious or no sample left
          homo = subset.homogenious(classifier)
          if homo:
            if homo is not EMPTY_DATASET:
              self.children[type] = LeafNode(self, homo, type)
            else:
              self.children[type] = LeafNode(self, self.label, type)

            continue

          # no attribute left
          if len(attribs_left)<1:
            breaktie, label = subset.majority_label(classifier)
            if breaktie:
              self.children[type] = LeafNode(self, label, type)
            else:
              stat = subset.label_stats(classifier)
              # handle cases when self.label is not one of the majorities
              if stat[label] > stat[self.label]:
                self.children[type] = LeafNode(self, label, type)
              self.children[type] = LeafNode(self, self.label, type)
            continue

          # need furthur branching
          self.children[type] = BranchNode(self, subset, attribs_left, classifier, type)
    # binary braching for RealNum Attribute
    else:
        for idx in xrange(2):
          type = RealNumAttribute.partition_symbole[idx]+str(self.deci_bound)
          subset = children_data[idx]
          homo = subset.homogenious(classifier)
          if homo:
            if homo is not EMPTY_DATASET:
              self.children[type] = LeafNode(self, homo, type)
            else:
              self.children[type] = LeafNode(self, self.label, type)
            continue

          # no attribute left
          if len(attribs_left) < 1:
            breaktie, label = subset.majority_label(classifier)
            if breaktie:
              self.children[type] = LeafNode(self, label, type)
            else:
              stat = subset.label_stats(classifier)
              # handle cases when self.label is not one of the majorities
              if stat[label] > stat[self.label]:
                self.children[type] = LeafNode(self, label, type)
              self.children[type] = LeafNode(self, self.label, type)
            continue

          # need furthur branching
          self.children[type] = BranchNode(self, subset, attribs_left, classifier, type)


  def __repr__(self):
    # root
    if not self.parent:
      return ''

    return self.level*' '+self.parent.attrib.name+':'+self.value

  def __lt__(self, o):
    return self.value < o.value


  def on_dump(self):
    if str(self):
      print str(self)
    vlist = sorted(self.children.values())
    for value in vlist:
      value.on_dump()
