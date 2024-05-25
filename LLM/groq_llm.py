import os
import dotenv
dotenv.load_dotenv()
from groq import Groq
def get_llm_response(context):
    """
    Retrieves a response from the LLM (Language Learning Model) using the given context.

    Args:
        context (list): A list of messages representing the conversation context.

    Returns:
        str: The response generated by the LLM.
    """
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )
    chat_completion = client.chat.completions.create(
        messages=context,
        model="llama3-70b-8192",
    )

    return chat_completion.choices[0].message.content
