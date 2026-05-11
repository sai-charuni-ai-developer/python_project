"""
Simple Calculator Agent — Using LangChain!

Install:  pip3 install langchain numexpr
Run:      python3 calculator_agent.py
"""

import math
import re
from langchain.tools import tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain.llms.base import LLM
from typing import Optional, List

#   LangChain Tools (the calculator functions)
@tool
def add(input: str) -> str:
    """Add two numbers. Input format: 'a,b'"""
    a, b = map(float, input.split(","))
    return f"{a} + {b} = {a + b}"

@tool
def subtract(input: str) -> str:
    """Subtract two numbers. Input format: 'a,b'"""
    a, b = map(float, input.split(","))
    return f"{a} - {b} = {a - b}"

@tool
def multiply(input: str) -> str:
    """Multiply two numbers. Input format: 'a,b'"""
    a, b = map(float, input.split(","))
    return f"{a} × {b} = {a * b}"

@tool
def divide(input: str) -> str:
    """Divide two numbers. Input format: 'a,b'"""
    a, b = map(float, input.split(","))
    if b == 0:
        return "Error: Cannot divide by zero!"
    return f"{a} ÷ {b} = {a / b}"

@tool
def power(input: str) -> str:
    """Raise a number to a power. Input format: 'base,exponent'"""
    a, b = map(float, input.split(","))
    return f"{a} ^ {b} = {a ** b}"

@tool
def square_root(input: str) -> str:
    """Find square root of a number. Input format: 'a'"""
    a = float(input.strip())
    if a < 0:
        return "Error: Cannot find square root of a negative number!"
    return f"√{a} = {math.sqrt(a)}"

@tool
def percentage(input: str) -> str:
    """Find percentage. Input format: 'value,percent'"""
    a, b = map(float, input.split(","))
    return f"{b}% of {a} = {(a * b) / 100}"

#   Local Brain — figures out which tool to use

tools = [add, subtract, multiply, divide, power, square_root, percentage]
tool_map = {t.name: t for t in tools}

def extract_numbers(text):
    return re.findall(r'\d+\.?\d*', text)

def solve(question):
    q = question.lower().strip()
    numbers = extract_numbers(q)

    try:
        if "percent" in q or "%" in q:
            if len(numbers) >= 2:
                return percentage.invoke(f"{numbers[0]},{numbers[1]}")

        elif "square root" in q or "sqrt" in q:
            if numbers:
                return square_root.invoke(numbers[0])

        elif "power" in q or "exponent" in q or "squared" in q or "cubed" in q:
            if "squared" in q and numbers:
                return power.invoke(f"{numbers[0]},2")
            elif "cubed" in q and numbers:
                return power.invoke(f"{numbers[0]},3")
            elif len(numbers) >= 2:
                return power.invoke(f"{numbers[0]},{numbers[1]}")

        elif "divide" in q or "divided" in q:
            if len(numbers) >= 2:
                return divide.invoke(f"{numbers[0]},{numbers[1]}")

        elif "multiply" in q or "times" in q or "product" in q:
            if len(numbers) >= 2:
                return multiply.invoke(f"{numbers[0]},{numbers[1]}")

        elif "subtract" in q or "minus" in q or "take away" in q:
            if len(numbers) >= 2:
                return subtract.invoke(f"{numbers[0]},{numbers[1]}")

        elif "add" in q or "plus" in q or "sum" in q or "total" in q:
            if len(numbers) >= 2:
                return add.invoke(f"{numbers[0]},{numbers[1]}")

        # Try evaluating direct expressions
        safe = re.sub(r'[^0-9+\-*/().\s]', '', question).strip()
        if safe:
            result = eval(safe)
            return f"{safe} = {result}"

    except Exception as e:
        return f"Error: {e}"

    return (
        "I couldn't understand that. Try:\n"
        "  • add 10 and 25\n"
        "  • subtract 5 from 20\n"
        "  • multiply 4 times 6\n"
        "  • divide 100 by 4\n"
        "  • 15 percent of 200\n"
        "  • square root of 144\n"
        "  • 2 to the power of 8\n"
        "  • 10 + 20"
    )

#   Chat Loop

print("\n LangChain Calculator Agent")
print("────────────────────────────────────────────────────")
print("Ask me any math question! Examples:")
print("  • add 10 and 25")
print("  • 15 percent of 200")
print("  • square root of 144")
print("  • 2 to the power of 8")
print("  • divide 100 by 4")
print("  • multiply 6 times 7")
print("  • 10 + 20")
print("────────────────────────────────────────────────────\n")

while True:
    user_input = input("You: ").strip()

    if not user_input:
        continue

    if user_input.lower() in {"exit", "quit", "q", "bye"}:
        print("👋 Goodbye!")
        break

    answer = solve(user_input)
    print(f"\n🤖 Agent: {answer}\n")

