import json
import re
from openai import OpenAI

client = OpenAI()

def extract_subjects_and_priority(text: str):
    """
    OpenAI-powered parser with fallback (STRICT + RELIABLE)
    """

    prompt = f"""
You are an intelligent academic planner.

TASK:
Extract ONLY valid academic subjects and assign priority.

STRICT RULES:
- Subjects must be real academic topics (e.g., TOC, DBMS, DAA, OS, COA, FSD)
- DO NOT include normal words like: "important", "and", "have", "days"

PRIORITY MAPPING (STRICT):
- "very important", "urgent" → high
- "important" → high
- "medium", "moderate" → medium
- "less important", "optional", "not important" → low
- If no priority mentioned → medium

OUTPUT FORMAT (STRICT JSON ONLY):
{{
  "subjects": ["TOC", "DBMS"],
  "priorities": {{
    "TOC": "high",
    "DBMS": "medium"
  }}
}}

INPUT:
{text}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        content = response.choices[0].message.content.strip()
        content = content.replace("```json", "").replace("```", "").strip()

        data = json.loads(content)

        subjects = data.get("subjects", [])
        priorities = data.get("priorities", {})

        if subjects and priorities:
            return subjects, priorities

    except Exception as e:
        print("AI ERROR:", e)

    # ==========================
    # 🔁 FALLBACK PARSER (STRICT FIX)
    # ==========================
    text_lower = text.lower()

    # 🔥 Extract only valid subjects (UPPERCASE words like TOC, DBMS)
    subjects = re.findall(r'\b[A-Z]{2,}\b', text)
    subjects = list(dict.fromkeys(subjects))  # remove duplicates

    priorities = {}

    for subject in subjects:
        s = subject.lower()

      # 🔥 STRICT PRIORITY MATCH (ORDER MATTERS)
        if re.search(rf"{s}.*?(less important|not important|optional)", text_lower):
          priorities[subject] = "low"

        elif re.search(rf"{s}.*?(very important|urgent)", text_lower):
          priorities[subject] = "high"

        elif re.search(rf"{s}.*?(important)", text_lower):
          priorities[subject] = "high"

        elif re.search(rf"{s}.*?(medium|moderate|average)", text_lower):
          priorities[subject] = "medium"

        else:
          priorities[subject] = "medium"

    return subjects, priorities