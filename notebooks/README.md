
# 📊 Ethiopian Bank App Reviews Analysis

This repository provides tools to scrape, process, and analyze user reviews from Ethiopian bank mobile applications available on the Google Play Store. The project is designed to extract public feedback on major banking apps to assess user satisfaction, performance, and common issues.

---

## ✅ Task 1 – Scrape and Process Bank Reviews

### 🔧 Methodology

We implemented a modular and automated pipeline to perform the following steps:

1. **Scrape** reviews from Google Play Store using `google-play-scraper`.
2. **Save** raw reviews in timestamped CSV files per bank.
3. **Load** and **process** all review datasets for structured analysis.
4. **Log** progress and status for transparency.

---

### 🏦 Targeted Bank Apps

| Bank Name | Package Name                   | App Name                    | ⭐ Rating |
| --------- | ------------------------------ | --------------------------- | -------- |
| CBE       | `com.combanketh.mobilebanking` | Commercial Bank of Ethiopia | 4.34     |
| BOA       | `com.boa.boaMobileBanking`     | BoA Mobile                  | 2.73     |
| Dashen    | `com.dashen.dashensuperapp`    | Dashen Bank                 | 4.03     |

---

### 🧪 How to Run

#### 1. Scraping Reviews

```python
import sys
sys.path.append('../src')

from src import scrape_bank_reviews

scraped_data = scrape_bank_reviews()
```

📋 Output:

```
🔍 Scraping CBE (com.combanketh.mobilebanking)...
📱 App found: Commercial Bank of Ethiopia (4.34 stars)
Fetched 7501 reviews
📌 Sample: More than garrantty bank EBC....

🔍 Scraping BOA (com.boa.boaMobileBanking)...
📱 App found: BoA Mobile (2.73 stars)
Fetched 1044 reviews
📌 Sample: it's not working...

🔍 Scraping DASHEN (com.dashen.dashensuperapp)...
📱 App found: Dashen Bank (4.03 stars)
Fetched 449 reviews
📌 Sample: I like this mobile banking app very much...

✅ Files saved to:  
- `../data/raw/cbe_reviews_YYYYMMDD_HHMMSS.csv`  
- `../data/raw/boa_reviews_YYYYMMDD_HHMMSS.csv`  
- `../data/raw/dashen_reviews_YYYYMMDD_HHMMSS.csv`
```

---

#### 2. Loading Raw Review Data

```python
import pandas as pd
import sys

sys.path.append('../scripts')
from scripts import load_bank_data

data_path = '../data/raw/boa_reviews_20250608_195402.csv'
df = pd.read_csv(data_path)
print(df.head())
```


#### 3. Processing All Banks

```python
import sys
sys.path.append('../scripts')

from scripts import process_all_banks

final_df = process_all_banks()
print(final_df.head())
```

📋 Output:

```
INFO:scripts.Load_data:✅ Loaded 29982 reviews for cbe
INFO:scripts.process_data:
Initial NaN check for cbe: ...
...
```

✅ Final dataframe includes:

* `reviewid`, `username`, `content`, `score`, `thumbsupcount`
* `appversion`, `reviewcreatedversion`, `at`, `replycontent`
* `bank`, `source_file`, etc.

---
