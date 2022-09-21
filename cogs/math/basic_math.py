# Basic Math Operations

from discord.ext import commands

import math

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

OPERATORS = {
    "neg": PostfixOperator(lambda stack: -stack[-1], 1),
    "+": PostfixOperator(lambda stack: stack[-2] + stack[-1], 2),
    "-": PostfixOperator(lambda stack: stack[-2] - stack[-1], 2),
    "*": PostfixOperator(lambda stack: stack[-2] * stack[-1], 2),
    "/": PostfixOperator(lambda stack: stack[-2] / stack[-1], 2),
    "^": PostfixOperator(lambda stack: math.pow(stack[-2], stack[-1]), 2),
    "sqrt": PostfixOperator(lambda stack: math.sqrt(stack[-1]), 1)
}

def reverse_polish(expression):
    tokens = expression.split()
    stack = []

    for token in tokens:
        if token in OPERATORS:
            OPERATORS[token](stack)
        else: # assume anything other than an operator is a value
            stack.append(float(token))

    if len(stack) == 1:
        return stack[0]
    else:
        raise Exception("extraneous values remaining on the stack")

class BasicMath(commands.Cog, name="Basic Math"):
    """Calculates basic math"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def calc(self, context):
        """ Evaluate the given mathematical expression. Reverse Polish (calc rpn) notation supported."""
        if context.invoked_subcommand is None:
            await context.send("Invalid subcommand")

    @calc.command(name="rpn")
    async def calc_rpn(self, context, *, expression):
        try:
            await context.reply(reverse_polish(expression))
        except Exception as e:
            await context.reply(f"Error: {e}")

async def setup(bot):
    await bot.add_cog(BasicMath(bot))
