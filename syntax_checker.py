from ast import *

import sys

class SyntaxChecker:
    def __init__(self):
        self.resetContract()

    def resetContract(self):
        self.stateVariables = {}
        self.resetPredicate()

    def resetPredicate(self):
        self.localVariables = {}

    def check(self, tokens):
        self.tokens = tokens
        self.current = 0
        return self.checkContract()

    def checkContract(self):
        self.resetContract()
        contract_node = ContractNode("", "ContractDefinition")
        token = self.predict_token()
        while token.type != "EOF":
            nodeType, node = self.checkStateVarOrPredicate()
            contract_node.add_child(nodeType, node)
            token = self.predict_token()
        token = self.next_token(["EOF"])
        return contract_node

    def checkStateVarOrPredicate(self):
        declaration = self.next_token(["state_var_declaration", "predicate_declaration"])
        if declaration.type == "state_var_declaration":
            return ("StateVarDeclaration", self.checkStateVar())
        if declaration.type == "predicate_declaration":
            return ("PredicateDefinition", self.checkPredicate())

    def checkStateVar(self):
        identifier = self.next_token(["identifier"])
        state_var_node = StateVarDeclNode(identifier.value, "StateVarDeclaration")
        if identifier in self.stateVariables:
            self.report_error("state variable " + identifier + " already declared.")
        self.stateVariables[identifier.value] = state_var_node
        state_var_node.add_child("Visibility", self.checkVisibility())
        var_type = self.next_token(["type"])
        var_type_node = TypeNode(var_type.value, "Type")
        state_var_node.add_child("Type", var_type_node)
        period = self.next_token(["period"])
        return state_var_node

    def checkPredicate(self):
        identifier = self.next_token(["identifier"])
        pred_node = PredicateNode(identifier.value, "PredicateDefinition")
        pred_node.add_child("Visibility", self.checkVisibility())
        left_parent = self.predict_token()
        while left_parent.type == "left_parent":
            pred_node.add_child("PredicateCase", self.checkPredicateCase())
            left_parent = self.predict_token()
        return pred_node

    def checkPredicateCase(self):
        self.resetPredicate()
        pred_node = PredicateCaseNode("", "PredicateCase")
        pred_node.add_child("PredicateParameters", self.checkPredicateParameters())
        pred_node.add_child("ReturnValue", self.checkReturnValue())
        pred_node.add_child("PredicateBody", self.checkPredicateBody())
        return pred_node

    def checkPredicateBody(self):
        predBody = PredicateBodyNode("", "PredicateBody")
        token = self.predict_token()
        if token.type == "entails":
            entails = self.next_token(["entails"])
            token = self.predict_token()
            while token.type == "left_parent":
                predBody.add_child("Statement", self.checkStatement())
                token = self.predict_token()
        token = self.next_token(["period"])
        return predBody

    def checkReturnValue(self):
        retValue = ReturnValueNode("", "ReturnValue")
        token = self.predict_token()
        if token.type == "identifier":
            retValue.add_child("Name", self.checkIdentifier())
        return retValue

    def checkStatement(self):
        token = self.next_token(["left_parent"])
        token = self.predict_token()
        statement_node = None
        if token.type == "identifier":
            statement_node = UserPredicateCallNode("", "UserPredicate")
            id_node = self.checkIdentifier()
            id_node.setRef(statement_node)
            statement_node.add_child("Name", id_node)
            token = self.predict_token()
            while token.type != "right_parent":
                statement_node.add_child("Argument", self.checkAtom())
                token = self.predict_token()
        else:
            token = self.next_token(["unary_operator", "binary_operator", "ternary_operator"])
            atoms = 0
            if token.type == "unary_operator":
                statement_node = UnaryOperatorNode(token.value, "UnaryOperator")
                atoms = 1
            elif token.type == "binary_operator":
                statement_node = BinaryOperatorNode(token.value, "BinaryOperator")
                atoms = 2
            elif token.type == "ternary_operator":
                statement_node = TernaryOperatorNode(token.value, "TernaryOperator")
                atoms = 3
            for i in range(atoms):
                statement_node.add_child("Argument", self.checkAtom())
        token = self.next_token(["right_parent"])
        token = self.predict_token()
        if token.type == "comma":
            token = self.next_token(["comma"])
        return statement_node

    def checkAtom(self):
        token = self.predict_token()
        if token.type == "number":
            return self.checkNumber()
        if token.type == "identifier":
            return self.checkIdentifier()
        return self.checkStatement()

    def checkNumber(self):
        token = self.next_token(["number"])
        return NumberNode(token.value, "Number")

    def checkIdentifier(self):
        token = self.next_token(["identifier"])
        id_node = IdentifierNode(token.value, "Identifier")
        if token.value in self.stateVariables:
            id_node.setRef(self.stateVariables[token.value])
        elif token.value in self.localVariables:
            id_node.setRef(self.localVariables[token.value])
        #else:
        #    self.report_error("variable " + token.value + " not declared.")
        return id_node

    def checkVisibility(self):
        token = self.predict_token()
        visible = ""
        if token.type == "visibility_specifier":
            token = self.next_token(["visibility_specifier"])
            visible = token.value
        return VisibilityNode(visible, "Visibility")

    def checkPredicateParameters(self):
        param_list = ParamListNode("", "ParameterList")
        token = self.next_token(["left_parent"])
        token = self.predict_token()
        while token.type != "right_parent":
            param_list.add_child("Variable", self.checkParamVar())
            token = self.predict_token()
        token = self.next_token(["right_parent"])
        return param_list

    def checkParamVar(self):
        var = ParamVarNode("", "ParamVar")
        token = self.predict_token()
        if token.type == "identifier":
            self.checkParamVarWithType(var, "UInt")
        elif token.type == "left_brack":
            token = self.next_token(["left_brack"])
            type_node = TypeNode("List", "Type")
            var.add_child("Type", type_node)
            token = self.predict_token()
            if token.type != "right_brack":
                head_node = ParamVarNode("", "ParamVar")
                self.checkParamVarWithType(head_node, "UInt")
                var.add_child("Head", head_node)
                token = self.predict_token()
                if token.type == "pipe":
                    token = self.next_token(["pipe"])
                    tail_node = ParamVarNode("", "ParamVar")
                    self.checkParamVarWithType(tail_node, "List")
                    var.add_child("Tail", tail_node)
            token = self.next_token(["right_brack"])
        return var

    def checkParamVarWithType(self, varNode, varType):
        type_node = TypeNode(varType, "Type")
        id_node = self.checkIdentifier()
        varNode.add_child("Type", type_node)
        varNode.add_child("Name", id_node)
        self.checkLocalVar(id_node.name, varNode)


    def checkLocalVar(self, name, node):
        if name in self.localVariables:
            self.report_error("local variable " + name + " already declared.")
        self.localVariables[name] = node

    def checkType(self):
        token = self.next_token(["type"])
        return TypeNode(token.value, "Type")

    def report_error(self, message):
        print("SyntaxError: " + message)
        sys.exit(1)

    def next_token(self, expected = []):
        if self.current >= len(self.tokens):
            self.report_error("Missing token")
            sys.exit(1)
        token = self.tokens[self.current]
        if len(expected) > 0:
            if token.type not in expected:
                self.report_error("One of the following types of tokens was expected: " + ", ".join(expected) + " but found " + token.type + " of value " + token.value + ".")
        self.current += 1
        return token

    def predict_token(self):
        if self.current >= len(self.tokens):
            self.report_error("Missing token")
            sys.exit(1)
        return self.tokens[self.current]
