class ASTNode:
    def __init__(self, _name, _type):
        self.children = []
        self.name = _name
        self.type = _type

    def add_child(self, _child):
        if (_child == None):
            raise Exception('Null child added')
        self.children.append(_child)

    def toString(self, _tabs = 0):
        node = '\t' * _tabs + "Value: " + self.name + ", Type: " + self.type + '\n'
        for child in self.children:
            node += child.toString(_tabs + 1)
        return node

    def accept(self, _visitor):
        print("accept AST")
        pass

    def acceptChildren(self, _visitor):
        for child in self.children:
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

class UserPredicateCallNode(ASTNode):
    def accept(self, _visitor):
        _visitor.visitUserPredicateCall(self)
        self.acceptChildren(_visitor)
        _visitor.endVisitUserPredicateCall(self)

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

class LocalVarsListNode(ASTNode):
    def accept(self, _visitor):
        _visitor.visitLocalVarsList(self)
        self.acceptChildren(_visitor)
        _visitor.endVisitLocalVarsList(self)

class LocalVarDeclNode(VarDecl):
    def accept(self, _visitor):
        _visitor.visitLocalVarDecl(self)
        self.acceptChildren(_visitor)
        _visitor.endVisitLocalVarDecl(self)
