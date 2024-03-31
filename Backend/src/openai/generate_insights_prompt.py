def generate_insights_prompt(filename: str) -> str:
    """
    Generate a concise prompt for the OpenAI API to derive insights from a given CSV file.

    Parameters:
    - filename: str - The name of the uploaded CSV file.

    Returns:
    - str: The generated prompt for OpenAI API.
    """
    # Constructing the prompt with a focus on actionable insights from CSV data
    prompt = (
        f"Given a dataset named '{filename}', extracted from a CSV file uploaded by a user, "
        "analyze the dataset and generate a comprehensive summary of its contents. "
        "Identify key patterns, anomalies, or insights that could assist a non-technical user in making informed "
        "decisions."
        "Provide suggestions on potential actions or considerations based on the data analysis."
    )
    return prompt
