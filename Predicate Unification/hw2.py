import InferenceEngine as ie
import myLogics as logic

logAgent = ie.InferenceEngine()

def resolve(ls1, ls2):
    inferer = ie.Resolver()
    return inferer.resolve_lists(ls1, ls2)

def TELL(ls):
    logAgent.tell(ls)

def ASK(ls):
    return logAgent.ask(ls)

def CLEAR():
    logAgent.clear()