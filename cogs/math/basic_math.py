# Basic Math Operations

from discord.ext import commands

import ast
import math
import operator

# basic unary and binary operators
BASIC_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.BitXor: operator.pow, # redefine ^ to mean exponentiation
}

def evaluate_node(node):
    # numbers
    if isinstance(node, ast.Num):
        return node.n

    # unary operators
    elif isinstance(node, ast.UnaryOp):
        op = BASIC_OPS[type(node.op)]

        # evaluate the argument first
        arg = evaluate_node(node.operand)

        return op(arg)

    # binary operators
    elif isinstance(node, ast.BinOp):
        op = BASIC_OPS[type(node.op)]

        # evaluate both arguments first
        left = evaluate_node(node.left)
        right = evaluate_node(node.right)

        return op(left, right)

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
