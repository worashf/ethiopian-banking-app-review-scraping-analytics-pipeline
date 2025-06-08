

```markdown
# 🏦 Bank App Review Analysis

This project analyzes user reviews from various bank applications to extract sentiment and identify major themes that drive customer satisfaction and dissatisfaction. The project is organized into two main phases:

- **Task 1**: Data Collection and Preprocessing
- **Task 2**: Sentiment and Thematic Analysis

---

## 📁 Project Structure



│
├── scripts/
│   ├── save\_bank\_app\_review\.py            # Save scraped reviews to CSV
│   ├── Load\_data.py                       # Load raw review CSVs
│   ├── process\_data.py                    # Clean and preprocess review text
│   ├── save\_processed\_bank\_data.py        # Save cleaned reviews to CSV
│   ├── sentiment\_analysis.py              # Transformer-based sentiment scoring
│   ├── keyword\_extraction.py              # TF-IDF/spaCy-based keyword extraction
│   ├── theme\_clustering.py                # Grouping keywords into themes
│
├── data/
│   ├── raw/                               # Raw scraped review data
│   └── processed/                         # Cleaned and labeled review data
│
├── models/                                # Saved vectorizers/models
|---src
├── notebooks/                               # Final sentiment and theme results
├── README.md                              # Project documentation
└── requirements.txt                       # Dependencies



---

## 🧠 Task 1: Data Collection & Preprocessing

### ✅ Goals
- Scrape or collect bank review data.
- Preprocess review texts for NLP tasks.

### 📌 Steps
1. **Scrape and Save Raw Data**
   ```bash
   python scripts/save_bank_app_review.py
````

2. **Load Raw Data**

   ```bash
   python scripts/Load_data.py
   ```

3. **Preprocess Reviews**

   * Tokenization
   * Stop-word removal
   * Lowercasing

   ```bash
   python scripts/process_data.py
   ```

4. **Save Cleaned Data**

   ```bash
   python scripts/save_processed_bank_data.py
   ```

---

## 🎯 Task 2: Sentiment and Thematic Analysis

### ✅ Goals

* Analyze review sentiment.
* Identify recurring themes or topics.

### 🔍 Sentiment Analysis

* Uses HuggingFace's `distilbert-base-uncased-finetuned-sst-2-english` transformer model.
* Labels: Positive / Negative (optionally Neutral with thresholds)
* Aggregated scores by bank and star rating.

```bash
python scripts/sentiment_analysis.py
```

### 🧵 Thematic Analysis

* Extracts important keywords using TF-IDF or spaCy.
* Groups keywords into 3–5 themes per bank.
* Example themes:

  * `Account Access Issues`
  * `Transaction Speed`
  * `User Interface`
  * `Customer Support`
  * `Feature Requests`

```bash
python scripts/keyword_extraction.py
python scripts/theme_clustering.py
```

---

## 💾 Outputs

Saved to `/outputs` directory:

* `sentiment_results.csv`: `review_id`, `bank_name`, `sentiment_score`, `label`
* `themes_by_bank.json`: Top themes per bank and associated keywords

---

## 📦 Installation

```bash
git clonegit@github.com:worashf/ethiopian-banking-app-review-scraping-analytics-pipeline.git
cd ethiopian-banking-app-review-scraping-analytics-pipeline
pip install -r requirements.txt
```

---

## 🧪 Dependencies

* Python 3.8+
* pandas
* scikit-learn
* spaCy
* transformers
* torch
* nltk
* matplotlib / seaborn (optional for charts)

---

## 🤝 Contributing

1. Fork this repo
2. Push to your fork

---

## 📌 License

MIT License

