# Basic Math Operations

from discord.ext import commands

import ast
import math
import operator

OPERATIONS = {
    # operations represented by symbols
    ast.Add: operator.add, # addition
    ast.BitXor: operator.pow, # exponentiation
    ast.Div: operator.truediv, # division
    ast.Mult: operator.mul, # multiplication
    ast.Mod: operator.mod, # modulo
    ast.Sub: operator.sub, # subtraction

    # operations represented by names
    "cos": lambda args: math.cos(args[0]),
    "sin": lambda args: math.sin(args[0]),
    "tan": lambda args: math.tan(args[0])
}

def evaluate_node(node):
    # numbers
    if isinstance(node, ast.Num):
        return node.n

    # unary operators
    elif isinstance(node, ast.UnaryOp):
        op = OPERATIONS[type(node.op)]

        # evaluate the argument first
        arg = evaluate_node(node.operand)

        return op(arg)

    # binary operators
    elif isinstance(node, ast.BinOp):
        op = OPERATIONS[type(node.op)]

        # evaluate both arguments first
        left = evaluate_node(node.left)
        right = evaluate_node(node.right)

        return op(left, right)

    # named functions
    elif isinstance(node, ast.Call):
        op = OPERATIONS[node.func.id]

        # evaluate the arguments first
        args = [evaluate_node(arg) for arg in node.args]

        return op(args)

    # unknown or unsupported
    else:
        raise TypeError("unknown or unsupported operator/function")

def evaluate(expression):
    return evaluate_node(ast.parse(expression, mode="eval").body)

class BasicMath(commands.Cog, name="Basic Math"):
    """Calculates basic math"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def calc(self, context, *, expression):
        """Evaluate the given mathematical expression."""

        try:
            await context.reply(evaluate(expression))
        except Exception as e:
            await context.reply(f"Error: {e}")

async def setup(bot):
    await bot.add_cog(BasicMath(bot))
