import re
import spacy
from textblob import TextBlob
import textstat
import language_tool_python

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Initialize LanguageTool
tool = language_tool_python.LanguageTool('en-US')

def analyze_document(text):
    doc = nlp(text)
    suggestions = []

    # Analyze sentences
    for sent in doc.sents:
        suggestions.extend(analyze_sentence(sent))
    
    # Named Entity Recognition
    ner_suggestions = analyze_entities(doc)
    suggestions.extend(ner_suggestions)

    return suggestions

def analyze_sentence(sentence):
    suggestions = []

    # Check for passive voice
    if is_passive(sentence):
        suggestions.append(f"Consider using active voice in: '{sentence.text}'")

    # Check for long sentences
    if len(sentence) > 20:
        suggestions.append(f"Consider breaking down the long sentence: '{sentence.text}'")

    # Check for syntax and grammar issues
    syntax_suggestions = check_syntax(sentence)
    suggestions.extend(syntax_suggestions)
    
    return suggestions

def is_passive(sentence):
    for token in sentence:
        if token.dep_ == "auxpass":
            return True
    return False

def check_syntax(sentence):
    suggestions = []
    # Check for common grammar mistakes
    for token in sentence:
        if token.text.lower() == 'alot':
            suggestions.append("Consider replacing 'alot' with 'a lot'")
    
    return suggestions

def analyze_entities(doc):
    suggestions = []
    # Suggest improvements or standardizations for named entities
    for ent in doc.ents:
        if ent.label_ == "PERSON" and ent.text.lower() == "john doe":
            suggestions.append(f"Consider using the full name or correct spelling for '{ent.text}'.")
    
    return suggestions

def analyze_style_and_tone(text):
    doc = nlp(text)
    suggestions = []
    
    # Check for overly casual language
    casual_words = ["cool", "awesome", "stuff"]
    for token in doc:
        if token.text.lower() in casual_words:
            suggestions.append(f"Consider replacing '{token.text}' with a more formal term.")
    
    # Analyze sentiment using TextBlob for tone detection
    blob = TextBlob(text)
    if blob.sentiment.polarity < 0:
        suggestions.append("The text has a negative tone. Consider making it more positive.")
    
    return suggestions

def readability_analysis(text):
    suggestions = []
    
    flesch_score = textstat.flesch_reading_ease(text)
    if flesch_score < 60:
        suggestions.append("The text is difficult to read. Consider simplifying your sentences and using more common words.")
    
    return suggestions

def improve_clarity_and_conciseness(text):
    doc = nlp(text)
    suggestions = []
    
    # Check for redundant phrases
    redundant_phrases = {
        "in order to": "to",
        "at this point in time": "now",
        "due to the fact that": "because"
    }
    for phrase, replacement in redundant_phrases.items():
        if phrase in text:
            suggestions.append(f"Consider replacing '{phrase}' with '{replacement}'.")

    # Check for complex words
    complex_words = ["utilize", "commence", "terminate"]
    replacements = ["use", "start", "end"]
    for token in doc:
        if token.text.lower() in complex_words:
            index = complex_words.index(token.text.lower())
            suggestions.append(f"Consider replacing '{token.text}' with '{replacements[index]}'.")
    
    return suggestions

def fix_grammar_and_spelling(text):
    # Correct grammar using LanguageTool
    matches = tool.check(text)
    corrected_text = tool.correct(text)

    # Correct spelling using TextBlob
    blob = TextBlob(corrected_text)
    corrected_text = str(blob.correct())

    suggestions = []
    for match in matches:
        suggestions.append(match.message)

    return corrected_text, suggestions

def improve_document_content(original_content):
    # First, fix grammar and spelling
    corrected_content, grammar_suggestions = fix_grammar_and_spelling(original_content)

    # Perform further analysis on the corrected content
    suggestions = []

    # Analyze document using various functions
    suggestions.extend(analyze_document(corrected_content))
    suggestions.extend(analyze_style_and_tone(corrected_content))
    suggestions.extend(readability_analysis(corrected_content))
    suggestions.extend(improve_clarity_and_conciseness(corrected_content))
    suggestions.extend(grammar_suggestions)

    improved_content = apply_suggestions(corrected_content, suggestions)
    return improved_content, suggestions

def apply_suggestions(text, suggestions):
    for suggestion in suggestions:
        print(f"Processing suggestion: {suggestion}")
        try:
            if "Consider replacing" in suggestion:
                parts = suggestion.split("Consider replacing '")
                if len(parts) > 1:
                    old_phrase, new_phrase = parts[1].split("' with '")
                    new_phrase = new_phrase.replace("'.", "")
                    text = re.sub(r'\b' + re.escape(old_phrase) + r'\b', new_phrase, text)
            elif "Grammar issue:" in suggestion:
                match = re.search(r'Consider using (.*?) instead of (.*)', suggestion)
                if match:
                    new_text = match.group(1)
                    old_text = match.group(2)
                    text = re.sub(r'\b' + re.escape(old_text) + r'\b', new_text, text)
            elif "Spelling issue:" in suggestion:
                match = re.search(r"Spelling issue: '(.*?)' is misspelled.", suggestion)
                if match:
                    misspelled_word = match.group(1)
                    corrected_word = spell.candidates(misspelled_word).pop()
                    text = re.sub(r'\b' + re.escape(misspelled_word) + r'\b', corrected_word, text)
        except ValueError as e:
            print(f"Error processing suggestion: {e}")
    return text

