from abc import ABC, abstractmethod
from typing import List, Any

class Expr(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass

class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass

# --- Expressions ---

class Literal(Expr):
    def __init__(self, value: Any):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_literal_expr(self)

class Binary(Expr):
    def __init__(self, left: Expr, operator: str, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_binary_expr(self)

class Unary(Expr):
    def __init__(self, operator: str, right: Expr):
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_unary_expr(self)

class Grouping(Expr):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_grouping_expr(self)

class Variable(Expr):
    def __init__(self, name: str):
        self.name = name

    def accept(self, visitor):
        return visitor.visit_variable_expr(self)

class Call(Expr):
    def __init__(self, callee: Expr, arguments: List[Expr]):
        self.callee = callee
        self.arguments = arguments

    def accept(self, visitor):
        return visitor.visit_call_expr(self)

# --- Statements ---

class ExpressionStmt(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_expression_stmt(self)

class PrintStmt(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_print_stmt(self)

class VarDecl(Stmt):
    def __init__(self, name: str, initializer: Expr, is_mut: bool):
        self.name = name
        self.initializer = initializer
        self.is_mut = is_mut

    def accept(self, visitor):
        return visitor.visit_var_decl_stmt(self)

class Block(Stmt):
    def __init__(self, statements: List[Stmt]):
        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_block_stmt(self)

class FunctionDecl(Stmt):
    def __init__(self, name: str, params: List[str], body: Block):
        self.name = name
        self.params = params
        self.body = body

    def accept(self, visitor):
        return visitor.visit_function_decl_stmt(self)

class Assign(Expr):
    def __init__(self, name: str, value: Expr):
        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visit_assign_expr(self)

class If(Stmt):
    def __init__(self, condition: Expr, then_branch: Stmt, else_branch: Stmt = None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def accept(self, visitor):
        return visitor.visit_if_stmt(self)

class While(Stmt):
    def __init__(self, condition: Expr, body: Stmt):
        self.condition = condition
        self.body = body

    def accept(self, visitor):
        return visitor.visit_while_stmt(self)

class Return(Stmt):
    def __init__(self, keyword: Token, value: Expr = None):
        self.keyword = keyword # For error reporting
        self.value = value

    def accept(self, visitor):
        return visitor.visit_return_stmt(self)

class For(Stmt):
    def __init__(self, initializer: Stmt, condition: Expr, increment: Expr, body: Stmt):
        self.initializer = initializer
        self.condition = condition
        self.increment = increment
        self.body = body

    def accept(self, visitor):
        return visitor.visit_for_stmt(self)

class GetIndex(Expr):
    def __init__(self, object: Expr, index: Expr):
        self.object = object
        self.index = index

    def accept(self, visitor):
        return visitor.visit_get_index_expr(self)

class SetIndex(Expr):
    def __init__(self, object: Expr, index: Expr, value: Expr):
        self.object = object
        self.index = index
        self.value = value

    def accept(self, visitor):
        return visitor.visit_set_index_expr(self)

class ArrayLiteral(Expr):
    def __init__(self, elements: List[Expr]):
        self.elements = elements

    def accept(self, visitor):
        return visitor.visit_array_literal_expr(self)

class StructDecl(Stmt):
    def __init__(self, name: str, fields: List[str], methods: List[MethodDecl]):
        self.name = name
        self.fields = fields
        self.methods = methods

    def accept(self, visitor):
        return visitor.visit_struct_decl_stmt(self)

class StructInstance(Expr):
    def __init__(self, struct_name: str, field_values: Dict[str, Expr]):
        self.struct_name = struct_name
        self.field_values = field_values

    def accept(self, visitor):
        return visitor.visit_struct_instance_expr(self)

class GetProperty(Expr):
    def __init__(self, object: Expr, name: str):
        self.object = object
        self.name = name

    def accept(self, visitor):
        return visitor.visit_get_property_expr(self)

class SetProperty(Expr):
    def __init__(self, object: Expr, name: str, value: Expr):
        self.object = object
        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visit_set_property_expr(self)

class MethodDecl(Stmt):
    def __init__(self, name: str, params: List[str], body: Block):
        self.name = name
        self.params = params
        self.body = body

    def accept(self, visitor):
        return visitor.visit_method_decl_stmt(self)

class Lambda(Expr):
    def __init__(self, params: List[str], body: Block):
        self.params = params
        self.body = body

    def accept(self, visitor):
        return visitor.visit_lambda_expr(self)
