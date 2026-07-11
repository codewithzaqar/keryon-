from ..ast import nodes as ast
from .environment import Environment, RuntimeError
from ..lexer.tokens import Token
import time

class KryonRuntimeError(RuntimeError):
    pass

class ReturnSignal(Exception):
    """Used to unwind the stack when a return statement is encountered."""
    def __init__(self, value):
        self.value = value

class Interpreter:
    def __init__(self):
        self.globals = Environment()
        self.environment = self.globals
        self._setup_builtins()

    def _setup_builtins(self):
        self.globals.define("print", lambda *args: print(*args))
        self.globals.define("clock", lambda: time.time())
        self.globals.define("input", lambda prompt="": input(prompt))

    def interpret(self, statements: list[ast.Stmt]):
        try:
            for statement in statements:
                self.execute(statement)
        except KryonRuntimeError as e:
            print(f"Runtime Error: {e.message}")
        except ReturnSignal as e:
            print(f"Unexpected return outside function")

    def execute(self, stmt: ast.Stmt):
        stmt.accept(self)

    def evaluate(self, expr: ast.Expr) -> Any:
        return expr.accept(self)

    # --- Statement Visitors ---

    def visit_struct_decl_stmt(self, stmt: ast.StructDecl):
        # Store struct definition in current environment
        self.environment.define(stmt.name, stmt)

    def visit_expression_stmt(self, stmt: ast.ExpressionStmt):
        self.evaluate(stmt.expression)

    def visit_var_decl_stmt(self, stmt: ast.VarDecl):
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)
        self.environment.define(stmt.name, value)

    def visit_block_stmt(self, stmt: ast.Block):
        # Create a new scope
        previous_env = self.environment
        self.environment = Environment(self.environment)
        
        try:
            for statement in stmt.statements:
                self.execute(statement)
        finally:
            # Restore previous scope
            self.environment = previous_env

    def visit_if_stmt(self, stmt: ast.If):
        if self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self.execute(stmt.else_branch)

    def visit_while_stmt(self, stmt: ast.While):
        while self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)

    def visit_function_decl_stmt(self, stmt: ast.FunctionDecl):
        # Define function in current environment
        self.environment.define(stmt.name, stmt)

    def visit_return_stmt(self, stmt: ast.Return):
        value = None
        if stmt.value is not None:
            value = self.evaluate(stmt.value)
        raise ReturnSignal(value)

    def visit_for_stmt(self, stmt: ast.For):
        # Execute initializer in current scope
        if stmt.initializer is not None:
            self.execute(stmt.initializer)

        while True:
            # Check condition
            if stmt.condition is not None:
                if not self.is_truthy(self.evaluate(stmt.condition)):
                    break

            # Execute body
            # Note: In a real language, for-loop body might have its own scope for the init var
            # But for simplicity, we execute in current scope or block scope if body is block
            self.execute(stmt.body)

            # Execute increment
            if stmt.increment is not None:
                self.evaluate(stmt.increment)

    # --- Expression Visitors ---

    def visit_struct_instance_expr(self, expr: ast.StructInstance):
        # Create instance dictionary
        instance = {"__type__": expr.struct_name}
        
        # Evaluate field values
        for field_name, field_expr in expr.field_values.items():
            instance[field_name] = self.evaluate(field_expr)
            
        return instance

    def visit_get_property_expr(self, expr: ast.GetProperty):
        obj = self.evaluate(expr.object)
        
        if isinstance(obj, dict) and "__type__" in obj:
            if expr.name in obj:
                return obj[expr.name]
            else:
                raise KryonRuntimeError(None, f"Undefined property '{expr.name}' on struct '{obj['__type__']}'")
        
        raise KryonRuntimeError(None, "Can only get properties on structs")

    def visit_set_property_expr(self, expr: ast.SetProperty):
        obj = self.evaluate(expr.object)
        value = self.evaluate(expr.value)
        
        if isinstance(obj, dict) and "__type__" in obj:
            if expr.name in obj:
                obj[expr.name] = value
                return value
            else:
                raise KryonRuntimeError(None, f"Undefined property '{expr.name}' on struct '{obj['__type__']}'")
        
        raise KryonRuntimeError(None, "Can only set properties on structs")

    def visit_array_literal_expr(self, expr: ast.ArrayLiteral):
        elements = [self.evaluate(e) for e in expr.elements]
        return list(elements)

    def visit_get_index_expr(self, expr: ast.GetIndex):
        obj = self.evaluate(expr.object)
        index = self.evaluate(expr.index)

        if isinstance(obj, list):
            if not isinstance(index, int) and not isinstance(index, float):
                raise KryonRuntimeError(None, "Array index must be a number")
            idx = int(index)
            if idx < 0 or idx >= len(obj):
                raise KryonRuntimeError(None, f"Array index out of bounds: {idx}")
            return obj[idx]

        raise KryonRuntimeError(None, "Can only index into arrays")

    def visit_set_index_expr(self, expr: ast.SetIndex):
        obj = self.evaluate(expr.object)
        index = self.evaluate(expr.index)
        value = self.evaluate(expr.value)

        if isinstance(obj, list):
            if not isinstance(index, int) and not isinstance(index, float):
                raise KryonRuntimeError(None, "Array index must be a number")
            idx = int(index)
            if idx < 0 or idx >= len(obj):
                raise KryonRuntimeError(None, f"Array index out of bounds: {idx}")
            obj[idx] = value
            return value

        raise KryonRuntimeError(None, "Can only set index on arrays")

    def visit_literal_expr(self, expr: ast.Literal):
        return expr.value

    def visit_grouping_expr(self, expr: ast.Grouping):
        return self.evaluate(expr.expression)

    def visit_unary_expr(self, expr: ast.Unary):
        right = self.evaluate(expr.right)
        if expr.operator == "-":
            return -right
        if expr.operator == "!":
            return not self.is_truthy(right)
        return None

    def visit_binary_expr(self, expr: ast.Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if expr.operator == "+":
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)
            return left + right
        if expr.operator == "-": return left - right
        if expr.operator == "*": return left * right
        if expr.operator == "/": 
            if right == 0: raise KryonRuntimeError(None, "Division by zero")
            return left / right
        
        if expr.operator == ">": return left > right
        if expr.operator == ">=": return left >= right
        if expr.operator == "<": return left < right
        if expr.operator == "<=": return left <= right
        if expr.operator == "==": return left == right
        if expr.operator == "!=": return left != right
        
        if expr.operator == "and": # Logical AND
            if not self.is_truthy(left): return left
            return right
        if expr.operator == "or": # Logical OR
            if self.is_truthy(left): return left
            return right

        return None

    def visit_variable_expr(self, expr: ast.Variable):
        return self.environment.get(expr.name)

    def visit_assign_expr(self, expr: ast.Assign):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value

    def visit_call_expr(self, expr: ast.Call):
        callee = self.evaluate(expr.callee)
        arguments = [self.evaluate(arg) for arg in expr.arguments]

        if callable(callee):
            if len(arguments) != callee.__code__.co_argcount:
                 # Simple check, doesn't handle *args
                 pass 
            return callee(*arguments)
        
        if isinstance(callee, ast.FunctionDecl):
            return self.execute_function(callee, arguments)
            
        raise KryonRuntimeError(None, "Can only call functions and classes.")

    def execute_function(self, func: ast.FunctionDecl, arguments: list):
        # Create new environment for function scope
        previous_env = self.environment
        self.environment = Environment(self.environment)
        
        # Bind parameters
        for param, arg in zip(func.params, arguments):
            self.environment.define(param, arg)
        
        try:
            for stmt in func.body.statements:
                self.execute(stmt)
        except ReturnSignal as e:
            value = e.value
            self.environment = previous_env
            return value
        
        self.environment = previous_env
        return None

    def is_truthy(self, obj):
        if obj is None: return False
        if isinstance(obj, bool): return obj
        return True
