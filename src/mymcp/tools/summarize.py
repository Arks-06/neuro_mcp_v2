import re
from collections import Counter
from typing import List

def clean_text(text: str) -> str:
    """Removes basic formatting noise, URLs, and excess whitespace."""
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def tokenize_sentences(text: str) -> List[str]:
    """Splits text into clean individual sentences using basic punctuation boundaries."""
    # match periods, exclamation points, or question marks followed by spaces or newlines
    sentence_end = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s')
    sentences = sentence_end.split(text)
    return [s.strip() for s in sentences if len(s.strip()) > 10]

def summarize_text(text: str, ratio: float = 0.3, max_sentences: int = 5) -> str:
    """
    Performs extractive text summarization using normalized word frequency scoring.
    
    Args:
        text (str): The raw text to condense.
        ratio (float): The target compression fraction (e.g., 0.3 = 30% of original sentences).
        max_sentences (int): An upper limit cap to prevent context window explosion.
    """
    cleaned = clean_text(text)
    if not cleaned:
        return "Error: Provided text is empty or contains only noise."
        
    sentences = tokenize_sentences(cleaned)
    if len(sentences) <= max_sentences:
        return cleaned

    # Tokenize words. calculate raw frequencies (ignoring basic stop words)
    words = re.findall(r'\b\w+\b', cleaned.lower())
    stop_words = {
        'the', 'is', 'at', 'which', 'on', 'and', 'a', 'an', 'to', 'in', 'of', 'for', 
        'with', 'as', 'by', 'for', 'it', 'its', 'this', 'that', 'they', 'their', 'was', 'were'
    }
    filtered_words = [word for word in words if word not in stop_words]
    
    word_frequencies = Counter(filtered_words)
    if not word_frequencies:
        return " ".join(sentences[:max_sentences])

    # Normalize word frequencies against the most common word
    max_freq = max(word_frequencies.values())
    for word in word_frequencies:
        word_frequencies[word] = word_frequencies[word] / max_freq

    # Score sentences based on the cumulative normalized weights of their words
    sentence_scores = {}
    for sent in sentences:
        sent_words = re.findall(r'\b\w+\b', sent.lower())
        score = sum(word_frequencies.get(word, 0) for word in sent_words)
        # Normalize by length slightly to avoid bias toward unnaturally long sentences
        sentence_scores[sent] = score / (1 + len(sent_words) * 0.1)

    # how many sentences to keep
    target_count = max(int(len(sentences) * ratio), 1)
    target_count = min(target_count, max_sentences)

    # Extract top sentences while keeping their original structural order
    top_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:target_count]
    ordered_summary = [sent for sent in sentences if sent in top_sentences]

    return " ".join(ordered_summary)