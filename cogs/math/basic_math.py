# Basic Math Operations

from discord.ext import commands

import ast
import math
import operator

class PostfixOperator:
    """Helper class for stack-based postfix operators"""

    def __init__(self, func, arg_count):
        self.func = func # a function that accepts and modifies a stack in place
        self.arg_count = arg_count # exact number of required arguments

    def __call__(self, stack):
        if len(stack) < self.arg_count:
            raise Exception("insufficient number of arguments on stack")

        result = self.func(stack)
        del stack[-self.arg_count:] # pop arg_count values off
        stack.append(result)

POSTFIX_OPS = {
    "neg": PostfixOperator(lambda stack: -stack[-1], 1),
    "+": PostfixOperator(lambda stack: stack[-2] + stack[-1], 2),
    "-": PostfixOperator(lambda stack: stack[-2] - stack[-1], 2),
    "*": PostfixOperator(lambda stack: stack[-2] * stack[-1], 2),
    "/": PostfixOperator(lambda stack: stack[-2] / stack[-1], 2),
    "^": PostfixOperator(lambda stack: math.pow(stack[-2], stack[-1]), 2),
    "sqrt": PostfixOperator(lambda stack: math.sqrt(stack[-1]), 1)
}

def eval_postfix(expression):
    tokens = expression.split()
    stack = []

    for token in tokens:
        if token in POSTFIX_OPS:
            POSTFIX_OPS[token](stack)
        else: # assume anything other than an operator is a value
            stack.append(float(token))

    if len(stack) == 1:
        return stack[0]
    else:
        raise Exception("extraneous values remaining on the stack")

INFIX_OPS = { # basic operators
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.BitXor: operator.pow, # redefine ^ to mean exponentiation
}

def eval_infix_node(node):
    # numbers
    if isinstance(node, ast.Num):
        return node.n

    # unary operators
    elif isinstance(node, ast.UnaryOp):
        op = INFIX_OPS[type(node.op)]

        # evaluate the argument first
        arg = eval_infix_node(node.operand)

        return op(arg)

    # binary operators
    elif isinstance(node, ast.BinOp):
        op = INFIX_OPS[type(node.op)]

        # evaluate both arguments first
        left = eval_infix_node(node.left)
        right = eval_infix_node(node.right)

        return op(left, right)

    # unknown or unsupported
    else:
        raise TypeError("unknown or unsupported operator/function")

def eval_infix(expression):
    return eval_infix_node(ast.parse(expression, mode="eval").body)

class BasicMath(commands.Cog, name="Basic Math"):
    """Calculates basic math"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def calc(self, context):
        """Evaluate the given mathematical expression."""

        if context.invoked_subcommand is None:
            await context.send("Invalid subcommand")

    @calc.command(name="infix")
    async def calc_infix(self, context, *, expression):
        """Evaluate an infix expression (e.g. 1 + 2 => 3)"""
        try:
            await context.reply(eval_infix(expression))
        except Exception as e:
            await context.reply(f"Error: {e}")

    @calc.command(name="postfix")
    async def calc_postfix(self, context, *, expression):
        """Evaluate a postfix expression (e.g. 1 2 + => 3)"""

        try:
            await context.reply(eval_postfix(expression))
        except Exception as e:
            await context.reply(f"Error: {e}")

async def setup(bot):
    await bot.add_cog(BasicMath(bot))
