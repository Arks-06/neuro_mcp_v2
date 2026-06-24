import os
import sys
import warnings

os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
warnings.filterwarnings("ignore")

emotion_classifier = None  

def load_model():
    """Initializes the model only when requested."""
    global emotion_classifier
    if emotion_classifier is None:
        original_stdout = sys.stdout
        sys.stdout = sys.stderr
        try:
            from transformers import pipeline
            emotion_classifier = pipeline(
                "text-classification", 
                model="j-hartmann/emotion-english-distilroberta-base", 
                top_k=3
            )
        except Exception as e:
            print(f"Failed to load emotion model: {e}", file=sys.stderr)
        finally:
            sys.stdout = original_stdout

def analyze_emotion(text: str) -> str:
    """Analyze the emotional tone of a given text and return the top 3 detected emotions."""
    load_model()
    
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