from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")


def ask_question(context, question):
    prompt = f"""
    Answer only from the given context.

    Context:
    {context}

    Question:
    {question}
    """
    return llm.invoke(prompt).content