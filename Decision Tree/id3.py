import copy
import dataset as ds

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
      root = BranchNode(None, training_data, attributes, classifier,None)

    self.root = root

  def test(self, classifier, testing_data):
    # IMPLEMENT ME!!!
    total = len(testing_data)
    correct = 0
    for example in testing_data:
      current = self.root
      while not isinstance(current, LeafNode):
        current = current.children[example.get_value(current.attrib)]

      a= current.label
      b = example.get_value(classifier)

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
    self.attrib, children_data = dataset.optimal_partition(attribs, classifier)
    # attributes left for children
    attribs_left = copy.copy(attribs)
    attribs_left.remove(self.attrib)

    for idx in xrange(len(self.attrib.values)):
      type = self.attrib[idx]
      subset = children_data[idx]

      # subset is homogenious or no sample left
      homo = subset.homogenious(classifier)
      if homo:
        if homo is not ds.EMPTY_DATASET:
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