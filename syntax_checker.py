from ast import *
from keywords import *

import sys

class SyntaxChecker:
    def __init__(self):
        pass

    def check(self, tokens, code):
        self.tokens = tokens
        self.code = code
        self.current = 0
        return self.checkContract()

    def checkContract(self):
        contract_node = ContractNode("", ASTNodeTypes.ContractDefinition)
        token = self.predict_token()
        while token.type != TokenTypes.EOF:
            nodeType, node = self.checkStateVarOrPredicate()
            contract_node.add_child(nodeType, node)
            token = self.predict_token()
        token = self.next_token([TokenTypes.EOF])
        return contract_node

    def checkStateVarOrPredicate(self):
        declaration = self.next_token([TokenTypes.StateVarDeclaration, TokenTypes.PredicateDefinition])
        if declaration.type == TokenTypes.StateVarDeclaration:
            return (ASTNodeChildrenTypes.StateVarDeclaration, self.checkStateVar())
        if declaration.type == TokenTypes.PredicateDefinition:
            return (ASTNodeChildrenTypes.PredicateDefinition, self.checkPredicate())

    def checkStateVar(self):
        identifier = self.next_token([TokenTypes.Identifier])
        state_var_node = StateVarDeclNode(identifier.value, ASTNodeTypes.StateVarDeclaration)
        state_var_node.add_child(ASTNodeChildrenTypes.VisibilitySpecifier, self.checkVisibility())
        var_type = self.next_token([TokenTypes.Type])
        var_type_node = TypeNode(var_type.value, ASTNodeTypes.Type)
        state_var_node.add_child(ASTNodeChildrenTypes.Type, var_type_node)
        period = self.next_token([TokenTypes.Period])
        return state_var_node

    def checkPredicate(self):
        identifier = self.next_token([TokenTypes.Identifier])
        pred_node = PredicateNode(identifier.value, ASTNodeTypes.PredicateDefinition)
        pred_node.add_child(ASTNodeChildrenTypes.VisibilitySpecifier, self.checkVisibility())
        left_parent = self.predict_token()
        while left_parent.type == TokenTypes.LeftParent:
            pred_node.add_child(ASTNodeChildrenTypes.PredicateCase, self.checkPredicateCase())
            left_parent = self.predict_token()
        return pred_node

    def checkPredicateCase(self):
        pred_node = PredicateCaseNode("", ASTNodeTypes.PredicateCase)
        pred_node.add_child(ASTNodeChildrenTypes.ParameterList, self.checkPredicateParameters())
        pred_node.add_child(ASTNodeChildrenTypes.ReturnValue, self.checkReturnValue())
        pred_node.add_child(ASTNodeChildrenTypes.PredicateBody, self.checkPredicateBody())
        return pred_node

    def checkPredicateBody(self):
        predBody = PredicateBodyNode("", ASTNodeTypes.PredicateBody)
        token = self.predict_token()
        if token.type == TokenTypes.Entails:
            entails = self.next_token([TokenTypes.Entails])
            token = self.predict_token()
            while token.type == TokenTypes.LeftParent:
                predBody.add_child(ASTNodeChildrenTypes.Statement, self.checkStatement())
                token = self.predict_token()
        token = self.next_token([TokenTypes.Period])
        return predBody

    def checkReturnValue(self):
        retName = ""
        token = self.predict_token()
        if token.type == TokenTypes.Identifier:
            id_node = self.checkIdentifier()
            retName = id_node.name
        retValue = ReturnValueNode(retName, ASTNodeTypes.ReturnValue)
        return retValue

    def checkStatement(self):
        token = self.next_token([TokenTypes.LeftParent])
        token = self.predict_token()
        statement_node = None
        token = self.predict_token()
        if token.type == TokenTypes.Identifier:
            id_node = self.checkIdentifier()
            statement_node = UserPredicateCallNode(id_node.name, ASTNodeTypes.UserPredicate)
        else:
            token = self.next_token([TokenTypes.UpdateOperator, TokenTypes.UnaryOperator, TokenTypes.BinaryOperator, TokenTypes.TernaryOperator])
            if token.type == TokenTypes.UpdateOperator:
                statement_node = UpdateOperatorNode(token.value, ASTNodeTypes.UpdateOperator)
            elif token.type == TokenTypes.UnaryOperator:
                statement_node = UnaryOperatorNode(token.value, ASTNodeTypes.UnaryOperator)
            elif token.type == TokenTypes.BinaryOperator:
                statement_node = BinaryOperatorNode(token.value, ASTNodeTypes.BinaryOperator)
            elif token.type == TokenTypes.TernaryOperator:
                statement_node = TernaryOperatorNode(token.value, ASTNodeTypes.TernaryOperator)

        token = self.predict_token()
        while token.type != TokenTypes.RightParent:
            statement_node.add_child(ASTNodeChildrenTypes.Argument, self.checkAtom())
            token = self.predict_token()

        token = self.next_token([TokenTypes.RightParent])
        token = self.predict_token()
        if token.type == TokenTypes.Comma:
            token = self.next_token([TokenTypes.Comma])
        return statement_node

    def checkAtom(self):
        token = self.predict_token()
        if token.type == TokenTypes.Number:
            return self.checkNumber()
        if token.type == TokenTypes.Identifier:
            return self.checkIdentifier()
        return self.checkStatement()

    def checkNumber(self):
        token = self.next_token([TokenTypes.Number])
        return NumberNode(token.value, ASTNodeTypes.Number)

    def checkIdentifier(self):
        token = self.next_token([TokenTypes.Identifier])
        id_node = IdentifierNode(token.value, ASTNodeTypes.Identifier)
        #if token.value in self.stateVariables:
        #    id_node.setRef(self.stateVariables[token.value])
        #elif token.value in self.localVariables:
        #    id_node.setRef(self.localVariables[token.value])
        #else:
        #    self.report_error("variable " + token.value + " not declared.")
        return id_node

    def checkVisibility(self):
        token = self.predict_token()
        visible = ""
        if token.type == TokenTypes.VisibilitySpecifier:
            token = self.next_token([TokenTypes.VisibilitySpecifier])
            visible = token.value
        return VisibilityNode(visible, ASTNodeTypes.VisibilitySpecifier)

    def checkPredicateParameters(self):
        param_list = ParamListNode("", ASTNodeTypes.ParameterList)
        token = self.next_token([TokenTypes.LeftParent])
        token = self.predict_token()
        while token.type != TokenTypes.RightParent:
            param_list.add_child(ASTNodeChildrenTypes.ParamVar, self.checkParamVar())
            token = self.predict_token()
        token = self.next_token([TokenTypes.RightParent])
        return param_list

    def checkParamVar(self):
        var = ParamVarNode("", ASTNodeTypes.ParamVar)
        token = self.predict_token()
        if token.type == TokenTypes.Identifier:
            self.checkParamVarId(var)
        elif token.type == TokenTypes.LeftBrack:
            token = self.next_token([TokenTypes.LeftBrack])
            token = self.predict_token()
            if token.type != TokenTypes.RightBrack:
                head_node = ParamVarNode("", ASTNodeTypes.ParamVar)
                self.checkParamVarId(head_node)
                var.add_child(ASTNodeChildrenTypes.Head, head_node)
                token = self.predict_token()
                if token.type == TokenTypes.Pipe:
                    token = self.next_token([TokenTypes.Pipe])
                    tail_node = ParamVarNode("", ASTNodeTypes.ParamVar)
                    self.checkParamVarId(tail_node)
                    var.add_child(ASTNodeChildrenTypes.Tail, tail_node)
            token = self.next_token([TokenTypes.RightBrack])
        return var

    def checkParamVarId(self, varNode):
        id_node = self.checkIdentifier()
        varNode.name = id_node.name

    def checkType(self):
        token = self.next_token([TokenTypes.Type])
        return TypeNode(token.value, ASTNodeTypes.Type)

    def report_error(self, message, position, length):
        msg = "SyntaxError: " + message
        location_left = self.code[:position].rfind('\n')
        location_right = self.code[(position + length):].find('\n') + position + length
        msg += "\nhere: " + self.code[location_left : location_right]
        raise Exception(msg)

    def next_token(self, expected = []):
        if self.current >= len(self.tokens):
            self.report_error("Missing token", 0, 0)
            sys.exit(1)
        token = self.tokens[self.current]
        if len(expected) > 0:
            if token.type not in expected:
                self.report_error("One of the following types of tokens was expected: " + ", ".join(expected) + " but found " + token.type + " of value " + token.value + ".", token.position, token.length)
        self.current += 1
        return token

    def predict_token(self):
        if self.current >= len(self.tokens):
            self.report_error("Missing token", 0, 0)
            sys.exit(1)
        return self.tokens[self.current]
