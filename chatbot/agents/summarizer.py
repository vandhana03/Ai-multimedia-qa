from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")


def summarize(text):
    prompt = f"Summarize this clearly and briefly:\n{text}"
    return llm.invoke(prompt).content