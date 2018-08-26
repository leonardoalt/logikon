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
    SyncUInt = "syncUInt"
    SyncArray = "syncArray"
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

    _arithmetic = [
        Plus,
        Minus,
        Multiplication,
        Division
    ]

    _boolean = [
        Equals,
        NotEquals,
        Not,
        And,
        Or,
        LessThan,
        LessOrEqual,
        GreaterThan,
        GreaterOrEqual
    ]

    _array = [
        Store,
        Select
    ]

    _types = {
        Declare : "state_var_declaration",
        Define: "predicate_declaration",
        Public : "visibility_specifier",
        UInt : "type",
        Array : "type",
        List : "type",
        Sum : "unary_operator",
        Prove : "unary_operator",
        Not : "unary_operator",
        SyncUInt : "binary_operator",
        Select : "binary_operator",
        Store : "ternary_operator",
        SyncArray : "ternary_operator",
        Ite : "ternary_operator",
        Equals : "binary_operator",
        NotEquals : "binary_operator",
        LessThan : "binary_operator",
        LessOrEqual : "binary_operator",
        GreaterThan : "binary_operator",
        GreaterOrEqual : "binary_operator",
        And : "binary_operator",
        Or : "binary_operator",
        Plus : "binary_operator",
        Minus : "binary_operator",
        Multiplication : "binary_operator",
        Division : "binary_operator",
        LeftParent : "left_parent",
        RightParent : "right_parent",
        LeftBrack : "left_brack",
        RightBrack : "right_brack",
        Entails : "entails",
        Period : "period",
        Comma : "comma",
        Pipe : "pipe"
    }
