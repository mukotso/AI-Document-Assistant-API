import re
import json
import spacy
import textstat
import language_tool_python
from transformers import pipeline
from textblob import TextBlob

# spaCy model
nlp = spacy.load("en_core_web_sm")

# LanguageTool
tool = language_tool_python.LanguageTool('en-US')

# Transformer models
grammar_corrector = pipeline('text2text-generation', model='pszemraj/flan-t5-large-grammar-synthesis')

# Load configuration from JSON file
def load_config(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

config = load_config('config.json')
redundant_phrases = config.get('redundant_phrases', {})
complex_words = config.get('complex_words', {})
grammar_mistakes = config.get('grammar_mistakes', {})
ner_suggestions = config.get('ner_suggestions', {})
casual_words = config.get('casual_words', [])
ambiguous_words = config.get('ambiguous_words', {})

# NLP Analysis
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
    if len(sentence) > 20:  # Improved to check token count
        suggestions.append(f"Consider breaking down the long sentence: '{sentence.text}'")

    # Check for syntax and grammar issues
    syntax_suggestions = check_syntax(sentence)
    suggestions.extend(syntax_suggestions)

    return suggestions

def is_passive(sentence):
    # Enhanced detection using spaCy
    for token in sentence:
        if token.dep_ in ["auxpass", "nsubjpass"]:
            return True
    return False

def check_syntax(sentence):
    suggestions = []

    # Check for common grammar mistakes using LanguageTool
    matches = tool.check(sentence.text)
    for match in matches:
        for mistake, replacement in grammar_mistakes.items():
            if mistake in match.message.lower():
                suggestions.append(f"Consider replacing '{mistake}' with '{replacement}'")

    return suggestions

def analyze_entities(doc):
    suggestions = []

    # Enhanced NER suggestions
    for ent in doc.ents:
        if ent.label_ in ner_suggestions:
            for term, suggestion in ner_suggestions[ent.label_].items():
                if ent.text.lower() == term:
                    suggestions.append(f"{suggestion} for '{ent.text}'")

    return suggestions

# Grammar and Spelling Correction
def fix_grammar_and_spelling(text):
    # Correct grammar using transformer-based model
    corrected_grammar = grammar_corrector(text, max_length=512)[0]['generated_text']

    # Correct spelling using TextBlob
    blob = TextBlob(corrected_grammar)
    corrected_text = str(blob.correct())

    # Gather suggestions from LanguageTool
    matches = tool.check(corrected_text)
    suggestions = [match.message for match in matches]

    return corrected_text, suggestions

# Style and Tone Analysis
def analyze_style_and_tone(text):
    suggestions = []

    # Check for overly casual language
    for token in nlp(text):
        if token.text.lower() in casual_words:
            suggestions.append(f"Consider replacing '{token.text}' with a more formal term.")

    return suggestions

# Readability Analysis
def readability_analysis(text):
    suggestions = []

    # Flesch-Kincaid Grade Level
    flesch_kincaid_grade = textstat.flesch_kincaid_grade(text)
    if flesch_kincaid_grade > 8:
        suggestions.append("The text is written at a high grade level. Consider simplifying your language.")

    # Gunning-Fog Index
    gunning_fog_index = textstat.gunning_fog(text)
    if gunning_fog_index > 10:
        suggestions.append("The text is difficult to read. Consider simplifying your sentences and using more common words.")

    # Flesch Reading Ease
    flesch_score = textstat.flesch_reading_ease(text)
    if flesch_score < 60:
        suggestions.append("The text is difficult to read. Consider simplifying your sentences and using more common words.")

    # SMOG Index
    smog_index = textstat.smog_index(text)
    if smog_index > 12:
        suggestions.append("The text may be too complex. Consider simplifying it for easier comprehension.")

    return suggestions

def improve_clarity_and_conciseness(text):
    doc = nlp(text)
    suggestions = []

    # Check for redundant phrases
    for phrase, replacement in redundant_phrases.items():
        if phrase in text:
            suggestions.append(f"Consider replacing '{phrase}' with '{replacement}'.")

    # Check for complex words
    for token in doc:
        if token.text.lower() in complex_words:
            replacement = complex_words[token.text.lower()]
            suggestions.append(f"Consider replacing '{token.text}' with '{replacement}'.")

    return suggestions

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
                    corrected_word = TextBlob(misspelled_word).correct()
                    text = re.sub(r'\b' + re.escape(misspelled_word) + r'\b', str(corrected_word), text)
        except ValueError as e:
            print(f"Error processing suggestion: {e}")
    return text
