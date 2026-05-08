from langchain_openai import ChatOpenAI
import json
import re

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def extract_timestamp(transcript: str, topic: str) -> str:
    """Simple string response — used by graph.py / LangGraph timestamp_node."""
    prompt = f"""Find the timestamp or time references related to this topic.
If none is present, say "No timestamp found".

Topic: {topic}

Transcript: {transcript}
"""
    return llm.invoke(prompt).content


def _mmss_to_seconds(time_str: str) -> int:
    """Convert MM:SS or HH:MM:SS string to integer seconds."""
    try:
        parts = time_str.strip().split(":")
        if len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
        elif len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    except (ValueError, AttributeError):
        pass
    return 0


def extract_timestamps_structured(transcript: str, topic: str):
    """
    Parse the Whisper-style transcript (lines prefixed with [MM:SS]) and
    ask the LLM to return timestamps relevant to the requested topic.
    """

    # Check if transcript has [MM:SS] markers at all
    has_markers = bool(re.search(r"\[\d{2}:\d{2}\]", transcript))

    if has_markers:
        prompt = f"""You are a transcript search assistant.

The transcript below has lines like:
  [00:12] Welcome to the presentation.
  [01:45] Today we will cover pricing strategies.

TASK: Find segments that are semantically related to the topic: "{topic}"
- "Semantically related" means the segment discusses, mentions, or is clearly about the topic — even if the exact word is not used.
- Return up to 5 most relevant segments, ordered by time.
- Use the exact [MM:SS] value from the start of the matching line.
- Convert MM:SS to seconds (MM×60 + SS).
- If truly nothing is related, return an empty timestamps array.

Respond with ONLY this JSON (no markdown, no explanation):
{{
  "timestamps": [
    {{"topic": "brief label for what is said here", "time": "MM:SS", "seconds": <integer>}}
  ]
}}

Topic: {topic}

Transcript:
{transcript}
"""
    else:
        # PDF or plain-text transcript — no timestamps available
        prompt = f"""You are a transcript search assistant.

The transcript below does NOT have timestamps (it is a plain-text document).
Search for sentences or passages semantically related to the topic: "{topic}"

Since there are no timestamps in this document, return an empty timestamps array.

Respond with ONLY this JSON:
{{"timestamps": []}}

Topic: {topic}

Transcript:
{transcript}
"""

    raw = llm.invoke(prompt).content.strip()

    # Strip accidental markdown code fences
    raw = re.sub(r"^```(?:json)?\s*", "", raw, flags=re.MULTILINE)
    raw = re.sub(r"\s*```\s*$", "", raw, flags=re.MULTILINE)
    raw = raw.strip()

    try:
        parsed = json.loads(raw)
        data = parsed.get("timestamps", [])
        cleaned = []
        for item in data:
            if not isinstance(item, dict):
                continue
            label = str(item.get("topic", topic)).strip() or topic
            time_value = str(item.get("time", "")).strip()

            if not time_value:
                continue

            # Recompute seconds from time string (more reliable than LLM arithmetic)
            computed = _mmss_to_seconds(time_value)
            try:
                llm_seconds = int(item.get("seconds", computed))
                # Accept LLM value only if within 2 s of parsed value
                seconds = llm_seconds if abs(llm_seconds - computed) <= 2 else computed
            except (TypeError, ValueError):
                seconds = computed

            cleaned.append({"topic": label, "time": time_value, "seconds": seconds})

        return cleaned

    except json.JSONDecodeError:
        return []