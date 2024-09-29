#Content_Categorization.py

import csv
import nltk
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob

# Download necessary NLTK data for tokenization, stopwords, and lemmatization
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Load spaCy model for named entity recognition (NER)
nlp = spacy.load('en_core_web_sm')

# Initialize lemmatizer for reducing words to their base form
# and load stop words for removing common words like 'the', 'is', etc.
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Define categories and associated keywords for text classification
categories = {
    'politics': ['government', 'election', 'politics', 'president', 'congress', 'senate', 'party', 'vote', 'policy', 'law'],
    'technology': ['technology', 'software', 'hardware', 'internet', 'computer', 'AI', 'gadget', 'innovation', 'device'],
    'sports': [
        'sports', 'football', 'basketball', 'soccer', 'tennis', 'Olympics', 'athlete', 'competition', 'match',
        'WWE', 'NFL', 'Shohei Ohtani', 'cycling', 'championships'
    ],
    'entertainment': [
        'movie', 'music', 'celebrity', 'film', 'TV', 'Hollywood', 'show', 'theater', 'concert',
        'Ananya Panday', 'Arshad Warsi', 'Aishwarya Rai', 'Bhumi Pednekar', 'Bollywood', 'movie reviews'
    ],
    'business': ['business', 'economy', 'finance', 'stock', 'market', 'trade', 'investment', 'profit', 'corporation'],
    'health': [
        'health', 'medicine', 'doctor', 'patient', 'treatment', 'disease', 'wellness', 'nutrition', 'exercise',
        'ADHD', 'relationships', 'stress relief', 'enterovirus'
    ],
    'science': ['science', 'research', 'experiment', 'study', 'biology', 'chemistry', 'physics', 'discovery', 'theory'],
    'travel': ['travel', 'tourism', 'vacation', 'trip', 'destination', 'flight', 'hotel', 'adventure'],
    'lifestyle': [
        'lifestyle', 'fashion', 'food', 'fitness', 'home', 'beauty', 'wellbeing', 'hobby', 'meditation'
    ],
    'reviews': ['review', 'critics', 'hate', 'good'],
    'education': ['education', 'school', 'college', 'university', 'learning', 'student', 'teacher', 'curriculum', 'class'],
    'news / current events': ['Hezbollah', 'Israel', 'Biden', 'Middle East conflict', 'politics'],
    'opinion / features': ['opinions', 'features', 'commentary']
}


def preprocess_text(text):
    """
    Preprocess the given text by:
    1. Lowercasing the text.
    2. Tokenizing the text into words.
    3. Lemmatizing words (reducing them to base form).
    4. Removing stopwords and non-alphanumeric tokens.
    
    Args:
        text (str): The text to be processed.
    Returns:
        list: A list of processed word tokens.
    """
    tokens = word_tokenize(text.lower())  # Tokenize the text
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token.isalnum()]  # Lemmatize and remove non-alphanumeric tokens
    tokens = [token for token in tokens if token not in stop_words]  # Remove stop words
    return tokens


def extract_entities(text):
    """
    Extract named entities (such as people, organizations, locations) using spaCy's NER.
    
    Args:
        text (str): The text to extract entities from.
    Returns:
        list: A list of named entities found in the text.
    """
    doc = nlp(text)
    entities = [ent.text for ent in doc.ents]  # Extract named entities
    return entities


def get_sentiment(text):
    """
    Analyze the sentiment of the given text using TextBlob.
    Sentiment polarity ranges from -1 (negative) to 1 (positive).
    
    Args:
        text (str): The text to analyze for sentiment.
    Returns:
        float: The polarity score of the text.
    """
    blob = TextBlob(text)
    return blob.sentiment.polarity


def categorize_article(title, summary):
    """
    Categorize an article based on its title and summary by:
    1. Preprocessing the text (tokenization, lemmatization, stopword removal).
    2. Extracting named entities (people, places, etc.).
    3. Analyzing sentiment using TextBlob.
    4. Matching tokens and entities with predefined categories and keywords.
    
    Args:
        title (str): The article title.
        summary (str): The article summary.
    Returns:
        str: The most relevant category for the article.
    """
    tokens = preprocess_text(title + " " + summary)  # Preprocess title and summary together
    entities = extract_entities(title + " " + summary)  # Extract named entities
    sentiment = get_sentiment(title + " " + summary)  # Analyze sentiment
    scores = {category: 0 for category in categories}  # Initialize scores for each category

    # Score the tokens by comparing them with category keywords
    for token in tokens:
        for category, keywords in categories.items():
            if token in keywords:
                scores[category] += 1

    # Also score based on named entities
    for entity in entities:
        for category, keywords in categories.items():
            if entity.lower() in keywords:
                scores[category] += 1

    # Determine the best category based on the highest score
    if max(scores.values()) > 0:
        best_category = max(scores, key=scores.get)
        if 'reviews' in best_category or sentiment < 0:
            return 'reviews or opinion-based'
        return best_category
    else:
        return 'general-' + title + ' news'  # If no match, return as general news


def categorize_articles(input_file, output_file):
    """
    Categorize all articles from the input CSV file and save the categorized results to an output CSV file.
    
    Args:
        input_file (str): The name of the input CSV file containing articles.
        output_file (str): The name of the output CSV file to save categorized articles.
    """
    with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        
        # Read articles from the input CSV
        reader = csv.DictReader(infile)
        # Prepare to write categorized articles with an added 'category' column
        fieldnames = reader.fieldnames + ['category']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        
        writer.writeheader()  # Write the header of the output CSV

        # Process each article, categorize it, and write the result
        for row in reader:
            category = categorize_article(row['title'], row['summary'])  # Categorize each article
            row['category'] = category  # Add the category to the article row
            writer.writerow(row)  # Write the categorized article to the output CSV


if __name__ == "__main__":
    # Categorize articles from the 'news_articles.csv' file and save them to 'categorized_news_articles.csv'
    categorize_articles('news_articles.csv', 'categorized_news_articles.csv')
    print("Articles categorized and saved to categorized_news_articles.csv")
