
---

# **train.py – Text Classification with Text Cleaning (Beginner-Friendly Guide)**

This script extends the basic text classifier by adding **text cleaning** before training. It teaches a computer to tell whether a short piece of text sounds **positive** or **negative**, but now with normalized, cleaned input that improves consistency and accuracy.

---

# **1. What This Script Does (in plain English)**

The script:

1. Takes a small list of short sentences (some positive, some negative).
2. **Cleans the text** (lowercase, removes punctuation, normalizes spacing).
3. Converts the cleaned sentences from text into numbers (TF-IDF).
4. Trains a simple model to recognise patterns.
5. Tests the model to see if it learned correctly.
6. Saves the trained model to a file so it can be used later.

**Key difference from task 04:** Text is cleaned before vectorization, which helps the model learn better patterns and makes predictions more consistent.

---

# **2. Important Concepts Explained**

### **A. Text Cleaning**

Text cleaning normalizes input so the model doesn't waste effort learning formatting differences.

**What gets cleaned:**
- **Lowercasing:** "Great" and "great" become the same word
- **Punctuation removal:** "Bad!!" → "Bad"
- **Space normalization:** "This   is   good" → "This is good"
- **Special characters:** Removed (keeps only letters, numbers, spaces)

**Why it matters:**
> Without cleaning, "Great!" and "great" are treated as different words, wasting model capacity on noise instead of meaning.

### **B. Preprocessor Function**

The `clean_text()` function is passed to `TfidfVectorizer` as a `preprocessor`. This means:
- Every text goes through cleaning **before** TF-IDF vectorization
- The model only sees cleaned, normalized text
- Predictions are more consistent because input is standardized

### **C. Pipeline with Preprocessing**

The pipeline now includes:
1. **TF-IDF Vectorizer** (with `preprocessor=clean_text`)
2. **Logistic Regression** classifier

The cleaning happens automatically inside the pipeline, so you don't need to clean text manually before training or prediction.

### **D. Other Concepts**

All other concepts from task 04 still apply:
- **Model:** Mathematical program that classifies text
- **Training:** Learning patterns from examples
- **Features:** TF-IDF converts text to numbers
- **Logistic Regression:** Simple, fast classifier
- **Train/Test Split:** 70% training, 30% testing
- **Accuracy:** How many predictions were correct
- **Saving the Model:** Persists to `models/text_classifier.joblib`

---

# **3. The Data Used**

Same tiny dataset as task 04:
- 10 sentences (5 positive, 5 negative)
- Hard-coded inside the script

**Example:**
- "this is great" → positive
- "I hate this" → negative

Real projects would load data from files, logs, or databases.

---

# **4. What Happens During Training**

Step-by-step:

1. **Load the texts and labels** (positive/negative)
2. **Split them into training and testing sets** (70/30)
3. **Build a pipeline**:
   - **Text cleaning** (via `preprocessor=clean_text`)
   - **TF-IDF vectoriser** → converts cleaned text to numbers
   - **Logistic Regression** → learns patterns
4. **Train the model**:
   ```python
   model.fit(X_train, y_train)
   ```
   This learns:
   - Vocabulary from cleaned texts
   - Patterns to classify positive/negative
5. **Evaluate performance**:
   ```python
   y_pred = model.predict(X_test)
   acc = accuracy_score(y_test, y_pred)
   print(classification_report(y_test, y_pred))
   ```
6. **Save the model**:
   ```python
   joblib.dump(model, "models/text_classifier.joblib")
   ```

**Key difference:** All text is cleaned before vectorization, so the model learns from normalized input.

---

# **5. Code Structure Explained**

### **`clean_text(text: str) -> str`**

This function normalizes text:

```python
def clean_text(text: str) -> str:
    # 1. Convert to lowercase
    text = text.lower()
    # 2. Remove punctuation (keep only letters, numbers, spaces)
    text = re.sub(r"[^a-z0-9\s]", "", text)
    # 3. Collapse multiple spaces into one
    text = re.sub(r"\s+", " ", text).strip()
    return text
```

**Example transformations:**
- "This is GREAT!!" → "this is great"
- "I   love   this" → "i love this"
- "Bad!!! Service." → "bad service"

### **`build_model()`**

Creates a pipeline with cleaning built-in:

```python
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(preprocessor=clean_text)),
    ("clf", LogisticRegression(max_iter=1000, random_state=42)),
])
```

**Key point:** `preprocessor=clean_text` means every text is cleaned automatically before TF-IDF.

### **`main()`**

The main workflow:
1. Load data
2. Split train/test
3. Build model (with cleaning)
4. Train
5. Evaluate
6. Save

---

# **6. How to Run It**

1. Open a terminal in this folder.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Train the model:
   ```
   python train.py
   ```
4. You should see:
   - Classification report
   - Accuracy score
   - TF-IDF vocabulary sample (showing cleaned words)
   - Confirmation that a file was saved in `models/`

---

# **7. What Changed from Task 04**

| Task 04 | Task 05 |
|---------|--------|
| No text cleaning | Text cleaning via `clean_text()` |
| Raw text → TF-IDF | Cleaned text → TF-IDF |
| `TfidfVectorizer()` | `TfidfVectorizer(preprocessor=clean_text)` |
| Text cleaning in separate file | Text cleaning in `text_utils.py` |

**Benefits of cleaning:**
- More consistent predictions
- Better use of model capacity (focuses on meaning, not formatting)
- Handles variations like "Great!" and "great" as the same word

---

# **8. What You Can Improve Later**

Future micro-tasks will add:
- Cross-validation for more reliable evaluation
- Hyperparameter tuning to optimize model settings
- Model versioning to track different versions
- More advanced text processing (stemming, lemmatization)
- Larger datasets
- Deployment behind an API

---

