# Basic Math Operations

from discord.ext import commands


class BasicMath(commands.Cog, name="Basic Math"):
    """Calculates basic math"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add(self, context, left: int, right: int):
        """Adds two numbers"""  # this is the description that will show up in !help
        await context.send(left + right)

    @commands.command()
    async def subtract(self, context, left: int, right: int):
        """Subtracts first number from the second"""  # this is the description that will show up in !help
        await context.send(left - right)

    @commands.group()
    async def calc(self, context):
        """ Evaluate the given mathematical expression. Reverse Polish (calc rpn) notation supported."""
        if context.invoked_subcommand is None:
            await context.send("Invalid subcommand")

    @calc.command(name="rpn")
    async def calc_rpn(self, context, *, expression):
        tokens = expression.split()
        stack = []

        try:
            for token in tokens:
                if token == "+":
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(a + b)
                elif token == "-":
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(a - b)
                elif token == "*":
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(a * b)
                elif token == "/":
                    divisor = stack.pop()
                    dividend = stack.pop()

                    if divisor == 0:
                        await context.reply("Division by zero")
                        return

                    stack.append(dividend / dividend)
                elif token == "^":
                    exponent = stack.pop()
                    base = stack.pop()
                    stack.append(base ** exponent)
                else: # assume token is a number by default for now
                    stack.append(float(token))

            await context.reply(stack[0])
        except Exception as e:
            await context.reply("Error:", e)

async def setup(bot):
    await bot.add_cog(BasicMath(bot))
