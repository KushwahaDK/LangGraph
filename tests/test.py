import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(dotenv_path=".env", override=True)


def get_gpt_answer(question: str):
    """
    Get an answer from GPT model for the given question.

    Args:
        question (str): The question to ask GPT

    Returns:
        str: The answer from GPT
    """
    if not question:
        return "Please provide a question."

    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # You can change the model as needed
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant providing concise answers to questions about any topic.",
                },
                {"role": "user", "content": question},
            ],
            temperature=0.7,
            max_tokens=300,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error getting answer from GPT: {str(e)}")
        return f"Error: {str(e)}"


if __name__ == "__main__":
    question = "What is the capital of France?"
    answer = get_gpt_answer(question)
    print(answer)
