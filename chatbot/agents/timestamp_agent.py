from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")


def extract_timestamp(transcript, topic):
    prompt = f"""
    Find the timestamp or time references related to this topic.
    If none is present, say "No timestamp found".

    Topic:
    {topic}

    Transcript:
    {transcript}
    """
    return llm.invoke(prompt).content