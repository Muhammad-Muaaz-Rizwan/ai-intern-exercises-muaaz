def calculator(expression: str):

    try:
        result = eval(expression)
        return result
    except Exception as e: 
        return f"Error evaluating expression: {e}"