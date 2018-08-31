class ASTNodeTypes:
    ContractDefinition = "ContractDefinition"
    StateVarDeclaration = "StateVarDeclaration"
    PredicateDefinition = "PredicateDefinition"
    PredicateCase = "PredicateCase"
    PredicateBody = "PredicateBody"
    VisibilitySpecifier = "VisibilitySpecifier"
    Type = "Type"
    ReturnValue = "ReturnValue"
    UserPredicate = "UserPredicate"
    UpdateOperator = "UpdateOperator"
    UnaryOperator = "UnaryOperator"
    BinaryOperator = "BinaryOperator"
    TernaryOperator = "TernaryOperator"
    Number = "Number"
    Identifier = "Identifier"
    ParameterList = "ParameterList"
    ParamVar = "ParamVar"

class ASTNodeChildrenTypes(ASTNodeTypes):
    Name = "Name"
    Statement = "Statement"
    Argument = "Argument"
    LocalVar = "LocalVar"
    Head = "Head"
    Tail = "Tail"

class ASTNode:
    def __init__(self, _name, _type):
        self.children = {}
        self.name = _name
        self.type = _type

    def add_child(self, _key, _child):
        if _child == None:
            raise Exception('Null child added')
        if _key in self.children:
            self.children[_key].append(_child)
        else:
            self.children[_key] = [_child]

    def toString(self, _tabs = 0):
        node = '\t' * _tabs + "Name: " + self.name + ", Type: " + self.type + '\n'
        for key in self.children:
            for child in self.children[key]:
                node += '\t' * (_tabs + 1) + key + ":\n"
                node += child.toString(_tabs + 1)
        return node

    def accept(self, _visitor):
        pass

    def acceptChildren(self, _visitor):
        for key in self.children:
            for child in self.children[key]:
                child.accept(_visitor)

class ContractNode(ASTNode):
    def accept(self, _visitor):
        _visitor.visitContract(self)
        self.acceptChildren(_visitor)
        _visitor.endVisitContract(self)

class VarDecl(ASTNode):
    pass

class StateVarDeclNode(VarDecl):
    def accept(self, _visitor):
        _visitor.visitStateVarDecl(self)
        self.acceptChildren(_visitor)
        _visitor.endVisitStateVarDecl(self)

class ParamVarNode(VarDecl):
    def accept(self, _visitor):
        _visitor.visitParamVar(self)
        self.acceptChildren(_visitor)
        _visitor.endVisitParamVar(self)

class TypeNode(ASTNode):
    def accept(self, _visitor):
        _visitor.visitType(self)
        self.acceptChildren(_visitor)
        _visitor.endVisitType(self)

class PredicateNode(ASTNode):
    def accept(self, _visitor):
        _visitor.visitPredicate(self)
        self.acceptChildren(_visitor)
        _visitor.endVisitPredicate(self)

class PredicateCaseNode(ASTNode):
    def accept(self, _visitor):
        _visitor.visitPredicateCase(self)
        self.acceptChildren(_visitor)
        _visitor.endVisitPredicateCase(self)

class PredicateBodyNode(ASTNode):
    def accept(self, _visitor):
        _visitor.visitPredicateBody(self)
        self.acceptChildren(_visitor)
        _visitor.endVisitPredicateBody(self)

class UserPredicateCallNode(ASTNode):
    def accept(self, _visitor):
        _visitor.visitUserPredicateCall(self)
        self.acceptChildren(_visitor)
        _visitor.endVisitUserPredicateCall(self)

class UpdateOperatorNode(ASTNode):
    def accept(self, _visitor):
        _visitor.visitUpdateOperator(self)
        self.acceptChildren(_visitor)
        _visitor.endVisitUpdateOperator(self)


class UnaryOperatorNode(ASTNode):
    def accept(self, _visitor):
        _visitor.visitUnaryOperator(self)
        self.acceptChildren(_visitor)
        _visitor.endVisitUnaryOperator(self)

class BinaryOperatorNode(ASTNode):
    def accept(self, _visitor):
        _visitor.visitBinaryOperator(self)
        self.acceptChildren(_visitor)
        _visitor.endVisitBinaryOperator(self)

class TernaryOperatorNode(ASTNode):
    def accept(self, _visitor):
        _visitor.visitTernaryOperator(self)
        self.acceptChildren(_visitor)
        _visitor.endVisitTernaryOperator(self)

class NumberNode(ASTNode):
    def accept(self, _visitor):
        _visitor.visitNumber(self)
        self.acceptChildren(_visitor)
        _visitor.endVisitNumber(self)

class IdentifierNode(ASTNode):
    def accept(self, _visitor):
        _visitor.visitIdentifier(self)
        self.acceptChildren(_visitor)
        _visitor.endVisitIdentifier(self)

    def setRef(self, _ref):
        self.refDecl = _ref

class VisibilityNode(ASTNode):
    def accept(self, _visitor):
        _visitor.visitVisibility(self)
        self.acceptChildren(_visitor)
        _visitor.endVisitVisibility(self)

class ParamListNode(ASTNode):
    def accept(self, _visitor):
        _visitor.visitParamList(self)
        self.acceptChildren(_visitor)
        _visitor.endVisitParamList(self)

class ReturnValueNode(ASTNode):
    def accept(self, _visitor):
        _visitor.visitReturnValue(self)
        self.acceptChildren(_visitor)
        _visitor.endVisitReturnValue(self)
