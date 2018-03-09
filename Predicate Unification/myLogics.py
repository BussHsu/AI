import copy

# Literal, has name_string (string) and positive (indicating having not)
class Literal:
    def __init__(self, in_name, isPositive= True ):
        self.name_str = in_name
        self.positive = isPositive

    def __repr__(self):
        if self.positive:
            return "'"+self.name_str+"'"
        else:
            return "["+"'not',"+" '"+self.name_str+"']"

    def __hash__(self):
        return hash((self.name_str,self.positive))

    def __lt__(self, other):
        if self.name_str is not other.name_str:
            return self.name_str < other.name_str
        else:
            return self.positive is True

    def __eq__(self, other):
        return self.name_str is other.name_str and self.positive is other.positive

    def is_complement(self,other):
        return self.name_str is other.name_str and self.positive is not other.positive

    # returns a new literal
    def complement(self):
        return Literal(self.name_str, not self.positive)

# Interface of operators NOT, AND, OR, IMP, BIC, LIT
class Operator:
    # return CNF with input CNF list
    def operation(self,a):
        return None

class NOT(Operator):

    def operation(self, in_cnfs):
        cnf = in_cnfs[0]
        # list of CNF
        cnfs = []
        for cl in cnf:
            temp =cl.negate()
            temp.remove_dup()
            cnfs.append(temp)

        return Operators.oropt.operation(cnfs)

class AND(Operator):

    def operation(self,cnfs):
        if len(cnfs) is 1:
            return cnfs[0]
        ret = CNF([])
        for cnf in cnfs:
            ret.merge(cnf)
        return ret

class OR(Operator):

    def operation(self,cnfs):
        if len(cnfs) is 1:
            return cnfs[0]

        idx = 1
        temp = copy.copy(cnfs[0])
        next = cnfs[1]

        while idx < len(cnfs):
            next = cnfs[idx]
            temp = temp.combine(next)
            idx += 1
        temp.remove_dup()
        return temp

class IMP(Operator):

    def operation(self,in_cnfs):
        left = in_cnfs[0]
        right = in_cnfs[1]
        cnfs = [Operators.notopt.operation([left]), right]
        return Operators.oropt.operation(cnfs)

class BIC(Operator):

    def operation(self,in_cnfs):
        left = in_cnfs[0]
        right = in_cnfs[1]
        cnfs = [Operators.impopt.operation(in_cnfs), Operators.impopt.operation(in_cnfs[::-1])]
        return Operators.andopt.operation(cnfs)

# wrapper for string to cnf
class LIT(Operator):

    def operation(self, in_cnfs):
        return in_cnfs[0]

# Function objects for all logic operators
class Operators:
    notopt = NOT()
    andopt = AND()
    oropt  = OR()
    impopt = IMP()
    bicopt = BIC()
    litopt = LIT()
    @staticmethod
    def Create_OP(in_string):
        if in_string is 'not':
            return Operators.notopt
        elif in_string is 'and':
            return Operators.andopt
        elif in_string is 'or':
            return Operators.oropt
        elif in_string is 'implies':
            return Operators.impopt
        elif in_string is 'biconditional':
            return Operators.bicopt
        else:
            return Operators.litopt

class SimpleClause:
    def __init__(self,in_list):
        self.literals = in_list

    def __repr__(self):
        if len(self.literals) > 1:
            str_ls = [str(x) for x in self.literals]
            return "['or', "+", ".join(str_ls) + "]"
        elif len(self.literals) > 0:
            ret = self.literals[0]
            if ret.positive:
                return str(ret).translate(None, "'")
            return str(ret)
        else:
            return '[]'

    def __getitem__(self, key):
        return self.literals[key]

    def __contains__(self, key):
        return key in self.literals

    def __hash__(self):
        return hash(tuple(self.literals))

    def __eq__(self, other):
        if len(self.literals) is not len(other.literals):
            return False
        for x in self.literals:
            if x not in other.literals:
                return False
        return True

    def remove_literal(self, x):
        self.literals.remove(x)

    def is_empty(self):
        if len(self.literals) > 0:
            return False
        return True

    #extend with other clause
    def extend(self,other):
        self.literals.extend(other.literals)
        self.literals = sorted(self.literals)
        self.remove_dup()

    # check if contains [A or NOT A]
    def always_true(self):
        for lit in self.literals:
            comp = lit.complement()
            if comp in self.literals:
                return True
        return False

    # remove duplicate literals
    def remove_dup(self):
        seen = set()
        seen_add = seen.add
        self.literals = [x for x in self.literals if not (x in seen or seen_add(x))]

    #return CNF of negated clause
    def negate(self):
        self.literals = sorted(self.literals)
        self.remove_dup()
        cnf = CNF([])
        for lit in self.literals:
            cnf.and_clause(SimpleClause([lit.complement()]))
        return cnf

    # (a or b or c) contains (a or b)
    def containing(self, other):
        for lit in other.literals:
            if lit not in self.literals:
                return False
        return True

    # return merged clause
    def merge(self,other):
        ret = copy.deepcopy(self)
        for lit in other.literals:
            if lit not in self.literals:
                ret.literals.append(lit)
        if ret.always_true():
            return None
        ret.remove_dup()
        return ret

# Conjuctive Normal Form, used for all conversion.
class CNF:
    def __init__(self, in_clause =[]):
        # list of list
        self.clauses = in_clause

    def __getitem__(self, key):
        return self.clauses[key]

    def __repr__(self):
        return str(self.clauses)

    def and_clause(self, in_clause):
        if in_clause not in self.clauses:
            self.clauses.append(in_clause)
    # for or operation
    def merge(self, in_cnf):
        if not self.clauses:
            self.clauses.extend(in_cnf.clauses)
            return True

        list = copy.copy(self.clauses)
        for cl in in_cnf:
            flag , obj = self.check_containing(cl)
            if flag<0:
                continue
            elif flag == 0:
                list.append(cl)
            else:
                list.remove(obj)
                list.append(cl)
        self.clauses = list
        self.remove_dup()
        return True

    def clear(self):
        self.clauses = []

    def check_containing(self,cl):
        mine = None
        for mine in self.clauses:
            if mine.containing(cl):
                return 1, mine
            elif cl.containing(mine):
                return -1, mine
        return 0, mine

    # for AND operation
    def combine(self, in_cnf):
        ret = CNF([])
        for cl in self.clauses:
            for cl2 in in_cnf:
                temp = cl.merge(cl2)
                if(temp is not None):
                    ret.and_clause(temp)

        ret.remove_dup()
        return ret

    def remove_dup(self):
        seen = set()
        seen_add = seen.add
        self.clauses = [x for x in self.clauses if not (x in seen or seen_add(x))]

# used to wrap arbitrary input sentence
class Statement:
    def __init__(self, in_strlist):
        # handle the case "a"
        if isinstance(in_strlist, basestring):
            self.op = Operators.litopt
            self.list = [in_strlist]

        else:
            self.op = Operators.Create_OP(in_strlist.pop(0))
            self.list = in_strlist

    def __repr__(self):
        return str(self.op)+str(self.list)

    def to_CNF(self):
        cnfs=[]
        for x in self.list:
            if isinstance(x, basestring):
                cnfs.append(CNF([SimpleClause([Literal(x)])]))
            else:
                cnf = Statement(x).to_CNF()
                cnfs.append(cnf)
        ret = self.op.operation(cnfs)
        return ret
