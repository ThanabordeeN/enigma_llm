import os
import dotenv
dotenv.load_dotenv()
from groq import Groq
def get_llm_response(context):
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )
    chat_completion = client.chat.completions.create(
    messages=context
    ,
    model="llama3-70b-8192",
)

    return (chat_completion.choices[0].message.content)
