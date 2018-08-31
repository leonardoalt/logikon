from visitor import Visitor
from ast import *
from ast import ASTNodeChildrenTypes as ASTChildren
from keywords import *

class Types:
    Bool = "Bool"
    UInt = "UInt"
    Array = "Array"
    List = "List"
    DefaultParam = UInt
    DefaultFunction = Bool

    _arithmetic = [
        Keywords.Plus,
        Keywords.Minus,
        Keywords.Multiplication,
        Keywords.Division,
        Keywords.Select
    ]

    _boolean = [
        Keywords.Equals,
        Keywords.NotEquals,
        Keywords.Not,
        Keywords.And,
        Keywords.Or,
        Keywords.LessThan,
        Keywords.LessOrEqual,
        Keywords.GreaterThan,
        Keywords.GreaterOrEqual
    ]

    _array = [
        Keywords.Store
    ]

    def inferTypeNode(op):
        if op in _arithmetic:
            typeName = UInt
        elif op in _boolean:
            typeName = Bool
        elif op in _array:
            typeName = Array
        return TypeNode(typeName, ASTNodeTypes.Type)

class TypeChecker(Visitor, ASTNodeChildrenTypes):
    def __init__(self):
        self.error = False

    def resetContract(self):
        self.stateVariables = {}
        self.functions = {}
        self.resetPredicate()

    def resetPredicate(self):
        self.localVariables = {}

    def visitContract(self, node):
        self.resetContract()
        self.visitAllStateVars(node)
        self.visitAllFunctionHeaders(node)
        self.inferFunctionTypes(node)

    def inferFunctionTypes(self, contractNode):
        functions = contractNode.children[ASTNodeChildrenTypes.PredicateDefinition]
        for function in functions:
            self.inferFunctionType(function)

    def inferFunctionType(self, functionNode):
        cases = functionNode.children[ASTNodeChildrenTypes.PredicateCase]
        for case in cases:
            self.resetPredicate()
            paramList = case.children[ASTNodeChildrenTypes.ParameterList][0]
            paramList.accept(self)
            retValue = case.children[ASTNodeChildrenTypes.ReturnValue][0]
            if retValue.name == "":
                typeNode = TypeNode(Types.Bool, ASTNodeTypes.Type)
                retValue.add_child(ASTNodeChildrenTypes.Type, typeNode)
                self.updateFunctionTypeNode(functionNode, typeNode)
            elif retValue.name in self.localVariables:
                # This means the return variable already appeared in the parameter list
                origVar = self.localVariables[retValue.name]
                # the parameter var HAS to have a Type at this point
                if not origVar.has_child(ASTNodeChildrenTypes.Type):
                    raise Exception("Parameter types should already have been inferred.")
                typeNode = origVar.children[ASTNodeChildrenTypes.Type][0]
                retValue.add_child(ASTNodeChildrenTypes.Type, typeNode)
                self.updateFunctionTypeNode(functionNode, typeNode)
            else:
                pass
                # Need to search for assignment to ret value in body

    def updateFunctionTypeNode(self, functionNode, typeNode):
        if functionNode.has_child(ASTNodeChildrenTypes.Type):
            previousType = functionNode.children[ASTNodeChildrenTypes.Type][0]
            if typeNode.name != previousType.name:
                self.reportError("Function " + functionNode.name + " has a type conflict (" + typeNode.name + ", " + previousType.name + ").")
        else:
            print("Function " + functionNode.name + " has type " + typeNode.name)
            functionNode.add_child(ASTNodeChildrenTypes.Type, typeNode)

    def visitAllFunctionHeaders(self, contractNode):
        functions = contractNode.children[ASTNodeChildrenTypes.PredicateDefinition]
        for function in functions:
            self.functions[function.name] = function

    def visitAllStateVars(self, contractNode):
        stateVars = contractNode.get_children(ASTNodeChildrenTypes.StateVarDeclaration)
        for var in stateVars:
            self.internalVisitStateVarDecl(var)

    def visitPredicateCase(self, node):
        self.resetPredicate()

    def reportError(self, msg):
        print("TypeError: " + msg)
        self.error = True

    def internalVisitStateVarDecl(self, node):
        if node.name == None or node.name == "":
            self.reportError("Nameless state variable.")
        else:
            if node.name in self.stateVariables:
                self.reportError("State variable " + node.name + " declared twice.")
            else:
                self.stateVariables[node.name] = node
        if ASTChildren.Type not in node.children:
            self.reportError("Typeless state variable.")

    def visitParamVar(self, node):
        if node.name in self.localVariables:
            self.reportError("Parameter " + node.name + " declared twice.")
        else:
            self.localVariables[node.name] = node
            return self.inferParamType(node)
        return False

    def endVisitIdentifier(self, node):
        if node.name in ["Sender", "Value"]:
            typeNode = TypeNode(Types.UInt, ASTNodeTypes.Type)
            node.add_child(ASTNodeChildrenTypes.Type, typeNode)
        elif node.name in self.localVariables:
            ref = self.localVariables[node.name]
            node.setReference(ref)
            if len(ref.children[ASTNodeChildrenTypes.Type]) > 0:
                node.add_child(ASTNodeChildrenTypes.Type, ref.children[ASTNodeChildrenTypes.Type][0])

    def inferParamType(self, node):
        if node.has_child(ASTNodeChildrenTypes.Type):
            return True
        defaultType = TypeNode(Types.DefaultParam, ASTNodeTypes.Type)
        if node.name == "":
            listType = TypeNode(Types.List, ASTNodeTypes.Type)
            if node.has_child(ASTNodeChildrenTypes.Head):
                headNode = node.children[ASTNodeChildrenTypes.Head][0]
                headNode.add_child(ASTNodeChildrenTypes.Type, defaultType)
                self.localVariables[headNode.name] = headNode
            if node.has_child(ASTNodeChildrenTypes.Tail):
                tailNode = node.children[ASTNodeChildrenTypes.Tail][0]
                tailNode.add_child(ASTNodeChildrenTypes.Type, listType)
                self.localVariables[tailNode.name] = tailNode
            node.add_child(ASTNodeChildrenTypes.Type, listType)
            return True
        node.add_child(ASTNodeChildrenTypes.Type, defaultType)
        return False
