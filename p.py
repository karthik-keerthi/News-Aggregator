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

def get_published_date_toi(soup):
    """
    Extracts the publication date from the Times of India article soup.
    Args:
        soup (BeautifulSoup): The BeautifulSoup object for the article page.
    Returns:
        str: The formatted publication date or a default message if not found.
    """
    try:
        date_element = soup.find('div', class_='stroF AZ4wj')
        if date_element:
            date_text = date_element.find_all('span')[-1].get_text(strip=True)  # Get the last span for date
            return date_text.replace("Updated: ", "").strip()  # Remove 'Updated: ' and strip whitespace
    except Exception as e:
        logging.error(f"Error fetching publication date for TOI: {str(e)}")
    return datetime.now().strftime("%Y-%m-%d")


def get_published_date_cnn(soup):
    """
    Extracts the publication date from the CNN article page.
    Args:
        soup (BeautifulSoup): Parsed HTML content of the CNN article page.
    Returns:
        str: The extracted publication date in 'YYYY-MM-DD' format.
    """
    try:
        # Locate the date container in the HTML
        date_element = soup.find('div', class_='timestamp vossi-timestamp')
        if date_element:
            # Extract the date string and convert it to a proper format
            date_str = date_element.get_text(strip=True)
            # Example format: "8:52 PM EDT, Sun September 29, 2024"
            date_obj = datetime.strptime(date_str, "%I:%M %p %Z, %a %B %d, %Y")
            # Format the date as 'YYYY-MM-DD'
            formatted_date = date_obj.strftime("%Y-%m-%d")
            return formatted_date
        else:
            return datetime.now().strftime("%Y-%m-%d")
    except Exception as e:
        logging.error(f"Error extracting CNN article date: {str(e)}")
        return datetime.now().strftime("%Y-%m-%d")


def scrape_toi():
    """
    Scrapes the homepage of Times of India for article titles, links, summaries, and publication dates.
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

        # Loop through each article element in the grid for standard articles
        for article in soup.find_all('div', class_='col_l_6'):
            title_element = article.find('a')  # Extract the <a> tag for the article link

            if title_element:
                title = title_element.text.strip()  # Extract the article title
                article_url = title_element.get('href')  # Get the URL from the <a> tag
                if article_url and not article_url.startswith('http'):
                    article_url = f"https://timesofindia.indiatimes.com{article_url}"

                # Get a summary of the article content
                summary = get_article_summary(article_url)

                # Get publication date from the article page
                publication_date = get_published_date_toi(soup)

                # Add the article info to the articles list
                articles.append({
                    'title': title,
                    'summary': summary,  # Summary fetched from the article page
                    'url': article_url,
                    'source': 'Times of India',
                    'publication_date': publication_date  # Publication date fetched from the article page
                })
                logging.info(f"Scraped TOI article: {title}")

        # Loop through each video element in the grid for videos
        for video in soup.find_all('figure', class_="_YVis"):
            title_element = video.find('figcaption')  # Extract the figcaption for the title
            link_element = video.find('a')  # The <a> tag contains the video link

            if title_element and link_element:
                title = title_element.text.strip()  # Extract the video title
                video_url = link_element.get('href')  # Get the URL from the <a> tag
                if video_url and not video_url.startswith('http'):
                    video_url = f"https://timesofindia.indiatimes.com{video_url}"

                # Default summary for video content
                summary = "Video content available."

                # Add the video info to the articles list
                articles.append({
                    'title': title,
                    'summary': summary,  # Default summary for video content
                    'url': video_url,
                    'source': 'Times of India',
                    'publication_date': datetime.now().strftime("%Y-%m-%d")  # Current date as the publication date
                })
                logging.info(f"Scraped TOI video: {title}")

        # Additional articles in the linktype2 class
        for additional_article in soup.find_all('div', class_='linktype2'):
            title_element = additional_article.find('a')  # Extract the <a> tag for the article link

            if title_element:
                title = title_element.text.strip()  # Extract the article title
                article_url = title_element.get('href')  # Get the URL from the <a> tag
                if article_url and not article_url.startswith('http'):
                    article_url = f"https://timesofindia.indiatimes.com{article_url}"

                # Get a summary of the article content
                summary = get_article_summary(article_url)

                # Get publication date from the article page
                publication_date = get_published_date_toi(soup)

                # Add the article info to the articles list
                articles.append({
                    'title': title,
                    'summary': summary,  # Summary fetched from the article page
                    'url': article_url,
                    'source': 'Times of India',
                    'publication_date': publication_date  # Publication date fetched from the article page
                })
                logging.info(f"Scraped TOI additional article: {title}")

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
    Scrapes the homepage and articles section of CNN for article titles, links, and summaries.
    Returns:
        list: A list of dictionaries containing the article title, summary, URL, source, and publication date.
    """
    articles = []
    urls_to_scrape = [
        "https://edition.cnn.com/",
        "https://edition.cnn.com/articles"
    ]

    for url in urls_to_scrape:
        try:
            logging.info(f"Scraping CNN from {url}...")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            # Scrape articles from the main page
            if url == "https://edition.cnn.com/":
                for article in soup.find_all('div', class_='container__headline'):
                    title_element = article.find('span', class_='container__headline-text')  # Extract the title text
                    link_element = article.find_parent('a')  # Find the parent <a> tag for the article URL

                    if title_element and link_element:
                        title = title_element.text.strip()
                        article_url = link_element.get('href')
                        if article_url and not article_url.startswith('http'):
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

            # Scrape articles from the articles section
            elif url == "https://edition.cnn.com/articles":
                for article in soup.find_all('h3', class_='cd__headline'):
                    title_element = article.find('a')  # Extract the <a> tag for the link

                    if title_element:
                        title = title_element.text.strip()  # Extract the article title
                        article_url = title_element.get('href')  # Get the URL from the <a> tag
                        if article_url and not article_url.startswith('http'):
                            article_url = f"https://edition.cnn.com{article_url}"

                        # Get a summary of the article content
                        summary = get_article_summary(article_url)

                        # Get publication date from the article page
                        publication_date = get_published_date_cnn(soup)

                        # Add the article info to the articles list
                        articles.append({
                            'title': title,
                            'summary': summary,  # Summary fetched from the article page
                            'url': article_url,
                            'source': 'CNN',
                            'publication_date': publication_date  # Publication date fetched from the article page
                        })
                        logging.info(f"Scraped CNN article: {title}")

        except Exception as e:
            logging.error(f"Error scraping CNN from {url}: {str(e)}")

    return articles



def save_to_csv(articles, filename='news_articles.csv'):
    """
    Saves the scraped articles to a CSV file.
    Args:
        articles (list): The list of articles to save.
        filename (str): The name of the file to save the articles in.
    """
    keys = articles[0].keys() if articles else []
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(articles)

    logging.info(f"Saved {len(articles)} articles to {filename}.")


if __name__ == "__main__":
    # Scrape articles from Times of India
    toi_articles = scrape_toi()
    # Scrape articles from CNN
    cnn_articles = scrape_cnn()
    # Combine both lists of articles
    all_articles = toi_articles + cnn_articles
    # Save to CSV
    save_to_csv(all_articles)