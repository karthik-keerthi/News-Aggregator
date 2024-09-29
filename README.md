

# 📰 **News Aggregator Project**

A complete solution for aggregating, categorizing, and displaying news articles from **Times of India** and **CNN** using Python 🐍 for web scraping, Natural Language Processing (NLP) 🧠, and FastAPI 🚀 for serving the data.

---

## **Project Components** 🔧

- 📰 **News Scraper**: Collects and extracts the latest news articles from Times of India and CNN.
- 🧠 **Content Categorization**: Processes and classifies news articles using NLP techniques.
- 🔗 **API Service**: Provides RESTful API endpoints to access the categorized news.
- 💻 **Web Interface**: Displays the news articles on a user-friendly webpage.

---

## **Setup and Installation** 🛠️

Follow these steps to install and run the project on your local machine:

### 1. 🐍 **Install Python**
Download and install Python 3.12.6 from [here](https://www.python.org/ftp/python/3.12.6/python-3.12.6-amd64.exe). Ensure Python is added to your system's PATH during installation.

### 2. 📂 **Clone the Project**
Clone or download this project repository to your local machine.

### 3. 📦 **Install Required Packages**
Navigate to your project directory and install the necessary Python packages by running:

```bash
pip install -r requirements.txt
```

**Additional Setup**:

- Download the **spaCy English model** 🧠 with this command:

```bash
python -m spacy download en_core_web_sm
```

### 4. 🚀 **Run the Project**

#### 📰 **Scrape News Articles**:
To collect the latest articles, run:

```bash
python News_Scraper.py
```

This will generate `news_articles.csv` 🗂️ with the scraped articles.

#### 🧠 **Categorize Articles**:
After scraping, categorize the articles by running:

```bash
python Content_Categorization.py
```

This will produce `categorized_news_articles.csv` 🗂️ with categorized articles.

#### 🔗 **Start the API Server**:
To serve the articles via a REST API, run:

```bash
python News_Api.py
```

The API will be available at `http://0.0.0.0:8000` 🌐.

#### 💻 **View the Frontend**:
Open the `Web_News_Scraper_Home.html` file in a web browser to view and interact with the news articles. Make sure the API server is running.

---

## **Project Files Overview** 📜

### 1. 📰 **News_Scraper.py**
- **What it does**: Scrapes news articles from Times of India and CNN, extracts summaries, and saves the data into `news_articles.csv` 🗂️.
- **Libraries used**: `requests`, `BeautifulSoup`, `csv`, `logging`
- **Run**: `python News_Scraper.py`

### 2. 🧠 **Content_Categorization.py**
- **What it does**: Reads scraped articles, categorizes them using NLP 🧠, and saves categorized articles in `categorized_news_articles.csv` 🗂️.
- **Libraries used**: `nltk`, `spaCy`, `TextBlob`, `csv`
- **Run**: `python Content_Categorization.py`

### 3. 🔗 **News_Api.py**
- **What it does**: Serves the categorized articles through RESTful API 🚀 endpoints.
- **Libraries used**: `FastAPI`, `uvicorn`, `pydantic`, `csv`
- **Run**: `python News_Api.py`

### 4. 💻 **Web_News_Scraper_Home.html**
- **What it does**: Displays the news articles on a web page 📄. Allows users to search and filter news using an interactive interface 🔍.
- **Libraries used**: `Axios`, `HTML/CSS/JavaScript`
- **Open**: In any web browser after starting the API.

---

## **API Endpoints** 📡

- **`GET /articles`**: Fetch all articles, with optional filters for category and date 📅.
- **`GET /articles/{article_id}`**: Get a specific article by its ID 🔑.
- **`GET /search`**: Search for articles based on keywords 🔍.

---

## **Technologies Used** ⚙️

- **Python** 🐍: Primary language for scraping, processing, and serving data.
- **FastAPI** 🚀: Framework for building API services.
- **BeautifulSoup** 🥣: For web scraping and HTML parsing.
- **NLTK** 📚 & **spaCy** 🧠: For Natural Language Processing.
- **TextBlob** 🌥️: For sentiment analysis.
- **Axios** 🔗: For making HTTP requests in the frontend.

---

## **Step-by-Step Guide** 📝

1. 📰 **Scrape Articles**: Run `News_Scraper.py` to collect news articles.
2. 🧠 **Categorize Articles**: Run `Content_Categorization.py` to classify articles.
3. 🔗 **Start API**: Run `News_Api.py` to serve the articles through the API.
4. 💻 **View in Browser**: Open `Web_News_Scraper_Home.html` to view the news articles.

---

## **Summary** 🏁

This project demonstrates the creation of a news aggregator using web scraping, NLP 🧠, API development 🚀, and frontend technologies 💻. By following the setup steps, you can scrape, categorize, and display news articles with ease.

If you run into any issues or need further assistance, feel free to ask! 🙋‍♂️ :- https://www.linkedin.com/in/karthik132003
