import myLogics as logic
import copy

# Resolver resolves two clauses into one
class Resolver:
    def __init__(self):
        pass

    def resolve_lists(self, in_ls1, in_ls2):
        # transform into cnf
        cnf1 = logic.Statement(in_ls1).to_CNF()
        cnf2 = logic.Statement(in_ls2).to_CNF()

        # handles true clause: a or not a
        if len(cnf1.clauses) < 1 or len(cnf2.clauses) < 1:
            return False

        # assume inputs are clauses
        in_clause1 = cnf1[0]
        in_clause2 = cnf2[0]
        return self.resolve_clauses(in_clause1, in_clause2)

    def resolve_clauses(self, in_clause1, in_clause2):
        clause1 = copy.deepcopy(in_clause1)
        clause2 = copy.deepcopy(in_clause2)

        unresolvable = True
        # resolve two clauses st1 and st2
        for lit in clause1.literals:
            complement = lit.complement()
            if complement in clause2.literals:
                # remove from clause 1
                clause1.remove_literal(lit)
                # remove from clause 2
                clause2.remove_literal(complement)
                unresolvable = False
                break
        clause1.literals.extend(clause2.literals)
        clause1.remove_dup()
        if unresolvable or clause1.always_true():
            return False
        return clause1


class InferenceEngine:
    def __init__(self):
        self.knowledge_base = logic.CNF([])
        self.resolver = Resolver()

    def tell(self, in_str):
        s = logic.Statement(in_str)
        cnf = s.to_CNF()
        self.knowledge_base.merge(cnf)

    def ask(self, in_str):
        s = logic.Statement(in_str)
        cnf = s.to_CNF()

        # handles bad input
        if len(cnf.clauses) <1:
            return True

        negated = logic.Operators.notopt.operation([cnf])
        return self.contradiction(negated)

    def clear(self):
        self.knowledge_base.clear()

    # resolve simple clause with kb
    def resolve_cl_with_kb(self, cl):
        negated = cl.negate()
        return self.contradiction(negated)

    # Find contradiction after extend cnf to kb
    def contradiction(self, cnf):
        flag_modified = True
        clauses = copy.copy(cnf.clauses)
        clauses.extend(self.knowledge_base.clauses)

        while flag_modified:
            flag_modified = False
            curr_idx = 0
            while curr_idx < len(clauses):
                target_idx = curr_idx + 1
                while target_idx < len(clauses):
                    cl1 = clauses[curr_idx]
                    cl2 = clauses[target_idx]

                    temp = self.resolver.resolve_clauses(cl1, cl2)
                    if isinstance(temp, logic.SimpleClause):
                        if temp.is_empty():
                            return True
                        if temp not in clauses:
                            # clauses.append(temp)
                            clauses = [temp]+clauses
                            flag_modified = True
                            curr_idx = 0
                            break
                    target_idx += 1

                if flag_modified:
                    break
                curr_idx += 1

        return False
