from visitor import Visitor

from z3 import *

class FormalChecker(Visitor):
    def __init__(self):
        self.expressions = {}
        self.solver = Solver()

    def endVisitPredicate(self, node):
        self.expressions[node] = And([self.expressions[c] for c in node.children[3:]])
        self.solver.add(self.expressions[node])
        self.check()

    def check(self):
        result = self.solver.check()
        print(result)
        if result == sat:
            model = self.solver.model()
            print(model)

    def endVisitNumber(self, node):
        self.expressions[node] = BitVecVal(node.name, 256)

    def endVisitStateVarDecl(self, node):
        self.expressions[node] = self.mkVar(node.name, node.children[1].name)

    def endVisitLocalVarDecl(self, node):
        self.expressions[node] = self.mkVar(node.name, node.children[0].name)

    def endVisitIdentifier(self, node):
        self.expressions[node] = self.expressions[node.refDecl]

    def endVisitUnaryOperator(self, node):
        expr = self.expressions[node.children[0]]
        if node.name == "sum":
            self.expressions[node] = Sum(expr)
        elif node.name == "prove":
            self.expressions[node] = Not(expr)
        elif node.name == "not":
            self.expressions[node] = Not(expr)

    def endVisitTernaryOperator(self, node):
        op = node.name
        first = self.expressions[node.children[0]]
        second = self.expressions[node.children[1]]
        third = self.expressions[node.children[2]]
        if op == "store":
            expr = Store(first, second, third)
        elif op == "ite":
            expr = Ite(first, second, third)
        self.expressions[node] = expr

    def endVisitBinaryOperator(self, node):
        op = node.name
        print(node.toString())
        left = self.expressions[node.children[0]]
        right = self.expressions[node.children[1]]
        if op in ["+", "-", "*", "/"]:
            self.expressions[node] = self.arithmeticOperator(op, left, right)
        elif op in ["=", "!=", "<", "<=", ">", ">="]:
            self.expressions[node] = self.comparisonOperator(op, left, right)
        elif op in ["and", "or"]:
            self.expressions[node] = self.booleanOperator(op, left, right)
        elif op == "select":
            self.expressions[node] = self.arraySelect(left, right)

    def booleanOperator(self, op, left, right):
        if op == "and":
            expr = left and right
        elif op == "or":
            expr = left or right
        return expr

    def comparisonOperator(self, op, left, right):
        if op == "=":
            expr = left == right
        elif op == "!=":
            expr = left != right
        elif op == "<":
            expr = left < right
        elif op == "<=":
            expr = left <= right
        elif op == ">":
            expr = left > right
        elif op == ">=":
            expr = left >= right
        return expr

    def arraySelect(self, left, right):
        return Select(left, right)

    def arithmeticOperator(self, op, left, right):
        if op == "+":
            expr = left + right
        elif op == "-":
            expr = left - right
        elif op == "*":
            expr = left * right
        elif op == "/":
            expr = left / right
        return expr

    def mkVar(self, varName, varType):
        if varType == "UInt":
            var = BitVec(varName, 256)
        elif varType == "Array":
            bvSort = BitVecSort(256)
            var = Array(varName, bvSort, bvSort)
        return var
