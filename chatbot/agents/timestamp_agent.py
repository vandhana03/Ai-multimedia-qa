from langchain_openai import ChatOpenAI
import json

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


def extract_timestamps_structured(transcript, topic):
    prompt = f"""
    You extract timestamps from transcript text.
    Return ONLY valid JSON in this exact shape:
    {{
      "timestamps": [
        {{"topic": "short label", "time": "MM:SS", "seconds": 0}}
      ]
    }}

    Rules:
    - Up to 5 most relevant matches.
    - If no match, return {{"timestamps": []}}.
    - "seconds" must be an integer.

    Topic:
    {topic}

    Transcript:
    {transcript}
    """
    raw = llm.invoke(prompt).content.strip()
    try:
        parsed = json.loads(raw)
        data = parsed.get("timestamps", [])
        cleaned = []
        for item in data:
            if not isinstance(item, dict):
                continue
            label = str(item.get("topic", topic)).strip() or topic
            time_value = str(item.get("time", "")).strip()
            seconds = item.get("seconds", 0)
            try:
                seconds = int(seconds)
            except (TypeError, ValueError):
                seconds = 0
            if time_value:
                cleaned.append(
                    {"topic": label, "time": time_value, "seconds": seconds}
                )
        return cleaned
    except json.JSONDecodeError:
        return []