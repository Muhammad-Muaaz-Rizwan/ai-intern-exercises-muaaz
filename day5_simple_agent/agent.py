from google import genai
import os
from dotenv import load_dotenv
from tools import calculator
import time

# Step 1: Load API key and set up the Gemini client
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_NAME = "gemini-flash-lite-latest"


def decide_tool(user_question: str) -> str:
    """
    Ask Gemini whether this question needs the calculator tool.
    Returns 'calculator' or 'none'.
    """
    prompt = f"""User question: {user_question}

Available tools:
- calculator -> performs mathematical calculations

If the question requires math, respond with exactly:
TOOL: calculator

Otherwise respond with exactly:
TOOL: none
"""
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )
    text = response.text.strip()

    if "calculator" in text.lower():
        return "calculator"
    return "none"


def extract_math_expression(user_question: str) -> str:
    """
    Ask Gemini to pull out just the math expression from the question,
    so we can safely pass it to eval() in tools.py.
    """
    prompt = f"""Extract ONLY the mathematical expression from this question.
Respond with nothing except the expression itself (numbers and operators like + - * /).
No words, no explanation.

Question: {user_question}
"""
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )
    return response.text.strip()


def generate_final_answer(user_question: str, tool_result=None) -> str:
    """
    Ask Gemini to produce the final natural-language answer.
    If a tool was used, pass its result in as context.
    """
    if tool_result is not None:
        prompt = f"""User question:
{user_question}

Tool result:
{tool_result}

Write a short, helpful response using this result.
"""
    else:
        prompt = f"""User question:
{user_question}

Answer directly and concisely.
"""
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )
    return response.text.strip()


def run_agent(user_question: str):
    """
    Full agent flow for a single question.
    Returns (tool_used, final_answer).
    """
    tool_choice = decide_tool(user_question)

    if tool_choice == "calculator":
        expression = extract_math_expression(user_question)
        tool_result = calculator(expression)
        final_answer = generate_final_answer(user_question, tool_result)
        return "calculator", final_answer
    else:
        final_answer = generate_final_answer(user_question)
        return "none", final_answer


def main():
    input_file = "queries.txt"
    output_file = "results.txt"

    with open(input_file, "r", encoding="utf-8") as f:
        queries = [line.strip() for line in f if line.strip()]

    results = []
    for query in queries:
        print(f"Processing: {query}")
        tool_used, answer = run_agent(query)

        block = (
            f"Query: {query}\n\n"
            f"Tool used: {tool_used}\n\n"
            f"Answer:\n{answer}\n"
        )
        print(block)
        results.append(block)
        time.sleep(15)  #wait 15 sec as the free tire limit is 5 per min

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n---\n\n".join(results))

    print(f"\nDone. Results written to {output_file}")
            


if __name__ == "__main__":
    main()
