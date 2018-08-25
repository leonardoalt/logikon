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
            contract_node.add_child(self.checkStateVarOrPredicate())
            token = self.predict_token()
        token = self.next_token(["EOF"])
        return contract_node

    def checkStateVarOrPredicate(self):
        declaration = self.next_token(["state_var_declaration", "predicate_declaration"])
        if declaration.type == "state_var_declaration":
            return self.checkStateVar()
        if declaration.type == "predicate_declaration":
            return self.checkPredicate()

    def checkStateVar(self):
        identifier = self.next_token(["identifier"])
        state_var_node = StateVarDeclNode(identifier.value, "StateVarDeclaration")
        if identifier in self.stateVariables:
            self.report_error("state variable " + identifier + " already declared.")
        self.stateVariables[identifier.value] = state_var_node
        state_var_node.add_child(self.checkVisibility())
        var_type = self.next_token(["type"])
        var_type_node = TypeNode(var_type.value, "Type")
        state_var_node.add_child(var_type_node)
        period = self.next_token(["period"])
        return state_var_node

    def checkPredicate(self):
        self.resetPredicate()
        identifier = self.next_token(["identifier"])
        pred_node = PredicateNode(identifier.value, "PredicateDefinition")
        pred_node.add_child(self.checkVisibility())
        left_parent = self.next_token(["left_parent"])
        pred_node.add_child(self.checkPredicateParameters())
        left_brack = self.next_token(["left_brack"])
        pred_node.add_child(self.checkLocalVarsList())
        right_brack = self.next_token(["right_brack"])
        entails = self.next_token(["entails"])
        token = self.predict_token()
        while token.type == "left_parent":
            pred_node.add_child(self.checkStatement())
            token = self.predict_token()
        token = self.next_token(["period"])
        return pred_node

    def checkStatement(self):
        token = self.next_token(["left_parent"])
        token = self.predict_token()
        statement_node = None
        if token.type == "identifier":
            statement_node = UserPredicateCallNode("", "UserPredicate")
            id_node = self.checkIdentifier()
            id_node.setRef(statement_node)
            statement_node.add_child(id_node)
            token = self.predict_token()
            while token.type != "right_parent":
                statement_node.add_child(self.checkAtom())
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
                statement_node.add_child(self.checkAtom())
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
        else:
            self.report_error("variable " + token.value + " not declared.")
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
        token = self.next_token(["identifier", "right_parent"])
        while token.type == "identifier":
            type_node = TypeNode("UInt", "Type")
            local_var_decl_node = LocalVarDeclNode(token.value, "LocalVarDecl")
            local_var_decl_node.add_child(type_node)
            if token.value in self.localVariables:
                self.report_error("local variable " + token.value + " already declared.")
            self.localVariables[token.value] = local_var_decl_node
            param_list.add_child(local_var_decl_node)
            token = self.next_token(["identifier", "right_parent"])
        return param_list

    def checkLocalVarsList(self):
        local_vars_list_node = LocalVarsListNode("", "LocalVariableList")
        token = self.predict_token()
        while token.type == "identifier":
            local_vars_list_node.add_child(self.checkLocalVariableDeclaration())
            token = self.predict_token()
            if token.type == "comma":
                token = self.next_token(["comma"])
                token = self.predict_token()
        return local_vars_list_node

    def checkLocalVariableDeclaration(self):
        token = self.next_token(["identifier"])
        local_var_node = LocalVarDeclNode(token.value, "LocalVariableDeclaration")
        if token.value in self.localVariables:
            self.report_error("local variable " + token.value + " already declared.")
        self.localVariables[token.value] = local_var_node
        local_var_node.add_child(self.checkType())
        return local_var_node

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
