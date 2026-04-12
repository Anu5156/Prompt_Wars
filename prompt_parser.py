import re

def extract_subjects_and_priority(text):
    text = text.lower()

    words = re.findall(r'\b[a-zA-Z&]+\b', text)

    stopwords = [
        "i", "need", "to", "learn", "which", "are",
        "equally", "important", "complete", "finish"
    ]

    subjects = [w.upper() for w in words if w not in stopwords]
    subjects = list(dict.fromkeys(subjects))

    priorities = ["medium"] * len(subjects)

    if "important" in text:
        priorities = ["high"] * len(subjects)

    return subjects, priorities