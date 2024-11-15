# model.py

from llama_index.core import GPTIndex

def get_model(schema):
#     return GPTIndex(schema=schema)

# """
# This file provides a `get_model` function to initialize a model with a specified schema.
# The function uses LlamaIndex's `GPTIndex` to support different data structures.
# """

   """
    Get a model based on the environment variable.
    """

    state_model = state.get("model")
    model = os.getenv("MODEL", state_model)

    # print(f"Using model: {model}")
    # if model == "openai":
    #     from langchain_openai import ChatOpenAI
    #     return ChatOpenAI(temperature=0, model="gpt-4o-mini")
    # raise ValueError("Invalid model specified")

    return ChatOpenAI(
        temperature = 0, 
        model       = "gpt-4o"
    )