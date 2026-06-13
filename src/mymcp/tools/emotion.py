from transformers import pipeline

# Initialize the pipeline globally so the model is only loaded into memory once on startup
try:
    # This specific model classifies text into 7 basic emotions
    emotion_classifier = pipeline(
        "text-classification", 
        model="j-hartmann/emotion-english-distilroberta-base", 
        top_k=3
    )
except Exception as e:
    emotion_classifier = None
    print(f"Warning: Failed to load the emotion classification model. Error: {e}")

def analyze_emotion(text: str) -> str:
    """Analyze the emotional tone of a given text and return the top 3 detected emotions."""
    if emotion_classifier is None:
        return "Error: The emotion classification model failed to load during server startup."
        
    try:
        # The pipeline returns a list of dictionaries when top_k is specified
        results = emotion_classifier(text)[0]
        
        # Truncate long text for the output header
        preview_text = text if len(text) <= 50 else text[:47] + "..."
        output = f"Emotion Analysis for: '{preview_text}'\n\n"
        
        for result in results:
            emotion = result['label']
            score = result['score'] * 100
            output += f"- {emotion.capitalize()}: {score:.1f}%\n"
            
        return output
    except Exception as e:
        return f"Error analyzing emotion: {str(e)}"