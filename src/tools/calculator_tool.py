import ast
import operator
import re
from collections.abc import Callable

BinaryOperator = Callable[[float, float], float]
UnaryOperator = Callable[[float], float]

ALLOWED_BINARY_OPERATORS: dict[type[ast.operator], BinaryOperator] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

ALLOWED_UNARY_OPERATORS: dict[type[ast.unaryop], UnaryOperator] = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


class CalculatorTool:
    async def execute(self, message: str) -> str:
        expression = self._extract_expression(message)
        result = self._evaluate(expression)

        return f"O resultado e {self._format_number(result)}."

    def _extract_expression(self, message: str) -> str:
        normalized = message.lower()
        normalized = normalized.replace("quanto e", "")
        normalized = normalized.replace("quanto é", "")
        normalized = normalized.replace("calcule", "")
        normalized = normalized.replace("calcular", "")
        normalized = normalized.replace("resultado de", "")

        expression = re.sub(r"[^0-9+\-*/().,% ]", "", normalized)
        expression = expression.replace(",", ".").strip()

        if not expression:
            raise ValueError("Nenhuma expressao matematica encontrada.")

        return expression

    def _evaluate(self, expression: str) -> float:
        parsed = ast.parse(expression, mode="eval")
        return self._evaluate_node(parsed.body)

    def _evaluate_node(self, node: ast.AST) -> float:
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return float(node.value)

        if isinstance(node, ast.BinOp):
            operator_func = ALLOWED_BINARY_OPERATORS.get(type(node.op))

            if operator_func is None:
                raise ValueError("Operador nao permitido.")

            return operator_func(
                self._evaluate_node(node.left),
                self._evaluate_node(node.right),
            )

        if isinstance(node, ast.UnaryOp):
            operator_func = ALLOWED_UNARY_OPERATORS.get(type(node.op))

            if operator_func is None:
                raise ValueError("Operador nao permitido.")

            return operator_func(self._evaluate_node(node.operand))

        raise ValueError("Expressao matematica invalida.")

    def _format_number(self, value: float) -> str:
        if value.is_integer():
            return str(int(value))

        return f"{value:.6f}".rstrip("0").rstrip(".")
