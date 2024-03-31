import os
from openai import OpenAI
from typing import Optional

# Load environment variables
from dotenv import load_dotenv

load_dotenv()

# Initialize the OpenAI client with your API key
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def generate_insight(data: str, model: str = "gpt-3.5-turbo", temperature: float = 0.9, max_tokens: int = 4096) -> \
        Optional[str]:
    """
    Generate insights from data using the OpenAI API.

    Parameters:
    - data: str - The data or prompt to send to OpenAI for insights.
    - model: str - The model to use for generating insights. Default is "gpt-3.5-turbo".
    - temperature: float - Controls randomness. Lower is more deterministic.
    - max_tokens: int - The maximum number of tokens to generate.

    Returns:
    - str or None: The generated insight or None if an error occurs.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": data
                }
            ],
            max_tokens=min(max_tokens, 60000),  # Limit the output tokens to a maximum of 60000
            temperature=temperature,
        )
        insight = response.choices[0].message.content.strip()
        return insight
    except Exception as e:
        print(f"Error generating insight: {e}")
        return None
