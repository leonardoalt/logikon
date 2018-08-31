class Keywords:
    Declare = "declare"
    Define = "define"
    Public = "public"
    UInt = "UInt"
    Array = "Array"
    List = "List"
    Sum = "sum"
    Prove = "prove"
    Not = "not"
    And = "and"
    Or = "or"
    Ite = "ite"
    Equals = "="
    NotEquals = "!="
    LessThan = "<"
    LessOrEqual = "<="
    GreaterThan = ">"
    GreaterOrEqual = ">="
    Plus = "+"
    Minus = "-"
    Multiplication = "*"
    Division = "/"
    Store = "store"
    Select = "select"
    Update = "update"
    LeftParent = "("
    RightParent = ")"
    LeftBrack = "["
    RightBrack = "]"
    Entails = ":-"
    Period = "."
    Comma = ","
    Pipe = "|"
    Space = " "
    Tab = "\t"
    LineBreak = "\n"
    EOF = 0

    _blanks = [
        Space,
        Tab,
        LineBreak
    ]

    _separators = [
        LeftParent,
        RightParent,
        LeftBrack,
        RightBrack,
        Comma,
        Period,
        Pipe
    ]

class TokenTypes:
    StateVarDeclaration = "state_var_declaration"
    PredicateDefinition = "predicate_definition"
    VisibilitySpecifier = "visibility_specifier"
    Type = "type"
    Identifier = "identifier"
    Number = "number"
    Period = "period"
    Comma = "comma"
    Pipe = "pipe"
    LeftParent = "left_parent"
    RightParent = "right_parent"
    LeftBrack = "left_brack"
    RightBrack = "right_brack"
    Entails = "entails"
    UpdateOperator = "update_operator"
    UnaryOperator = "unary_operator"
    BinaryOperator = "binary_operator"
    TernaryOperator = "ternary_operator"
    EOF = "EOF"

    types = {
        Keywords.Declare : StateVarDeclaration,
        Keywords.Define : PredicateDefinition,
        Keywords.Public : VisibilitySpecifier,
        Keywords.UInt : Type,
        Keywords.Array : Type,
        Keywords.List : Type,
        Keywords.Sum : UnaryOperator,
        Keywords.Prove : UnaryOperator,
        Keywords.Not : UnaryOperator,
        Keywords.Update : UnaryOperator,
        Keywords.Select : BinaryOperator,
        Keywords.Store : TernaryOperator,
        Keywords.Ite : TernaryOperator,
        Keywords.Equals : BinaryOperator,
        Keywords.NotEquals : BinaryOperator,
        Keywords.LessThan : BinaryOperator,
        Keywords.LessOrEqual : BinaryOperator,
        Keywords.GreaterThan : BinaryOperator,
        Keywords.GreaterOrEqual : BinaryOperator,
        Keywords.And : BinaryOperator,
        Keywords.Or : BinaryOperator,
        Keywords.Plus : BinaryOperator,
        Keywords.Minus : BinaryOperator,
        Keywords.Multiplication : BinaryOperator,
        Keywords.Division : BinaryOperator,
        Keywords.LeftParent : LeftParent,
        Keywords.RightParent : RightParent,
        Keywords.LeftBrack : LeftBrack,
        Keywords.RightBrack : RightBrack,
        Keywords.Entails : Entails,
        Keywords.Period : Period,
        Keywords.Comma : Comma,
        Keywords.Pipe : Pipe,
        Keywords.EOF : EOF
    }
