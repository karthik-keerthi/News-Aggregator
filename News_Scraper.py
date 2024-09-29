#News_Scraper.py

import csv
from datetime import datetime
import logging
from bs4 import BeautifulSoup
import requests

# Configure logging to capture events for tracking (INFO level)
logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(levelname)s-%(message)s')

def get_article_summary(url):
    """
    Fetches the article content from the provided URL and extracts the first 2-3 paragraphs as a summary.
    Args:
        url (str): The URL of the article to fetch.
    Returns:
        str: A short summary of the article or a default message if the summary cannot be fetched.
    """
    try:
        # Define headers to mimic a real browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        # Make an HTTP request to fetch the article
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the first 3 paragraphs to create a summary
        paragraphs = soup.find_all('p')
        summary = ' '.join([p.get_text().strip() for p in paragraphs[:3]])  # Concatenate the first 3 paragraphs

        # Return the summary if available; otherwise, provide a default message
        if len(summary) > 0:
            return summary
        else:
            return "Summary not available."
    except Exception as e:
        logging.error(f"Error fetching article summary: {str(e)}")
        return "Summary not available."

def scrape_toi():
    """
    Scrapes the homepage of Times of India for article titles, links, and summaries.
    Returns:
        list: A list of dictionaries containing the article title, summary, URL, source, and publication date.
    """
    url = "https://timesofindia.indiatimes.com"
    articles = []

    try:
        logging.info("Scraping Times of India...")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Loop through each article element (using <h2> tags for TOI)
        for article in soup.find_all('h2'):
            title_element = article.find('a')  # Find the <a> tag inside <h2> for the article link
            if title_element:
                title = title_element.text.strip()  # Extract the article title
                article_url = title_element.get('href')
                if article_url and not article_url.startswith('http'):
                    # If the link is relative, create the full URL
                    article_url = f"https://timesofindia.indiatimes.com{article_url}"

                # Get a summary of the article content
                summary = get_article_summary(article_url)

                # Add the article info to the articles list
                articles.append({
                    'title': title,
                    'summary': summary,  # Summary fetched from the article page
                    'url': article_url,
                    'source': 'Times of India',
                    'publication_date': datetime.now().strftime("%Y-%m-%d")  # Current date as the publication date
                })
                logging.info(f"Scraped TOI article: {title}")

        # If no articles are found, log a warning and save the page's HTML for debugging
        if not articles:
            logging.warning("No TOI articles found. Dumping page source for debugging.")
            with open("toi_page_source.html", "w", encoding="utf-8") as f:
                f.write(response.text)

    except Exception as e:
        logging.error(f"Error scraping Times of India: {str(e)}")

    return articles

def scrape_cnn():
    """
    Scrapes the homepage of CNN for article titles, links, and summaries.
    Returns:
        list: A list of dictionaries containing the article title, summary, URL, source, and publication date.
    """
    url = "https://edition.cnn.com/"
    articles = []

    try:
        logging.info("Scraping CNN...")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # CNN article titles are stored in <div> tags with class 'container__headline'
        for article in soup.find_all('div', class_='container__headline'):
            title_element = article.find('span', class_='container__headline-text')  # Extract the title text
            link_element = article.find_parent('a')  # Find the parent <a> tag for the article URL

            if title_element and link_element:
                title = title_element.text.strip()
                article_url = link_element.get('href')
                if article_url and not article_url.startswith('http'):
                    # Handle relative URLs
                    article_url = f"https://edition.cnn.com{article_url}"

                # Get a summary of the article content
                summary = get_article_summary(article_url)

                # Append the article details to the list
                articles.append({
                    'title': title,
                    'summary': summary,  # Summary fetched from the article page
                    'url': article_url,
                    'source': 'CNN',
                    'publication_date': datetime.now().strftime("%Y-%m-%d")  # Current date as the publication date
                })
                logging.info(f"Scraped CNN article: {title}")

    except Exception as e:
        logging.error(f"Error scraping CNN: {str(e)}")

    return articles

def save_to_csv(articles, filename):
    """
    Saves the list of articles to a CSV file.
    Args:
        articles (list): A list of dictionaries containing article details.
        filename (str): The name of the CSV file to save the articles.
    """
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'summary', 'url', 'source', 'publication_date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()  # Write the column headers
        for article in articles:
            writer.writerow(article)  # Write each article's data as a row

if __name__ == "__main__":
    # Scrape articles from Times of India and CNN
    toi_articles = scrape_toi()
    cnn_articles = scrape_cnn()

    # Combine the articles from both sources
    all_articles = toi_articles + cnn_articles

    # Save the articles to a CSV file
    save_to_csv(all_articles, 'news_articles.csv')
    logging.info(f"Scraped {len(all_articles)} articles and saved to news_articles.csv")
