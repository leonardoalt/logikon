from visitor import Visitor
from ast import *
from ast import ASTNodeChildrenTypes as ASTChildren

class TypeChecker(Visitor, ASTNodeChildrenTypes):
    def __init__(self):
        self.error = False

    def resetContract(self):
        self.stateVariables = {}
        self.resetPredicate()

    def resetPredicate(self):
        self.localVariables = {}

    def endVisitStateVarDecl(self, node):
        if node.name == None or node.name == "":
            self.reportError("Nameless state variable.")
        else:
            if node.name in self.stateVariables:
                self.reportError("State variable " + node.name + " declared twice.")
            else:
                self.stateVariables[node.name] = node
        if ASTChildren.Type not in node.children:
            self.reportError("Typeless state variable.")

    def visitContract(self, node):
        self.resetContract()

    def visitPredicateCase(self, node):
        self.resetPredicate()


    def reportError(self, msg):
        print("TypeError: " + msg)
        self.error = True
