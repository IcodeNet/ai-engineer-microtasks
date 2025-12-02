```
05.micro-task-1.2-text-cleaning/LEARNING.md
```

---

# **LEARNING.md – Micro-Task 1.2 (Text Cleaning Preprocessor)**

*A Beginner-Friendly, Line-Mapped Explanation of Text Normalisation Before ML*

This micro-task teaches you how to clean text **before** the model sees it.
Clean text helps the model learn better, reduces noise, and makes predictions more stable.

This document explains:

* Why text needs cleaning
* What lowercasing, punctuation removal, and space normalisation do
* How the cleaning function works
* How it plugs into TF-IDF
* Which lines of code implement each concept
* How to verify the cleaning works
* Problems you encountered → solutions

---

# **1. What This Micro-Task Does (Simple Summary)**

In Micro-Task 1.1, you trained a model on raw text like:

```
"This is GREAT!!!"
"this is great"
"This    is      great"
```

To a beginner model, these look **completely different**.

This micro-task adds a **clean_text()** function that:

1. lowercases text
2. removes punctuation
3. collapses extra spaces

so the model sees them all as:

```
this is great
```

This improves stability and makes learning easier.

---

# **2. Why Text Cleaning Matters (Plain English)**

Real-world text is messy:

* Uppercase/lowercase variations
* Punctuation
* Emoji
* Multiple spaces
* Typos
* Random symbols

For simple ML models, these differences create **extra noise**.

Example:

```
"BAD!!"
"bad"
"Bad"
```

Without cleaning: 3 completely different patterns
With cleaning: **1 pattern**

Cleaning helps your model:

* generalise better
* learn faster
* avoid overfitting
* be more accurate

---

# **3. The Cleaning Steps Explained**

Your `clean_text()` function performs **three** beginner-friendly transformations.

---

## **3.1 Lowercasing**

Input:

```
"This is GREAT"
```

Becomes:

```
"this is great"
```

**Why:**
Models treat `"Great"` and `"great"` as different words if not normalised.

**Code mapping:**

```python
text = text.lower()
```

---

## **3.2 Remove punctuation**

Input:

```
"this is great!!!"
```

Becomes:

```
"this is great"
```

**Why:**
Punctuation does not contribute to meaning in simple sentiment tasks.
Removing it reduces noise.

**Code mapping:**

```python
text = re.sub(r"[^a-z0-9\s]", "", text)
```

This keeps only:

* letters
* numbers
* spaces

---

## **3.3 Collapse multiple spaces**

Input:

```
"this   is    great"
```

Becomes:

```
"this is great"
```

**Why:**
Extra spaces confuse TF-IDF (it sees them as separate token boundaries).

**Code mapping:**

```python
text = re.sub(r"\s+", " ", text).strip()
```

---

# **4. Full Cleaning Function (Code-Mapped)**

This is the exact function you added:

```python
def clean_text(text: str) -> str:
    # 1. Lowercase
    text = text.lower()
    # 2. Remove punctuation
    text = re.sub(r"[^a-z0-9\s]", "", text)
    # 3. Collapse multiple spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text
```

Each comment maps to a concept in Section 3.

---

# **5. Plugging Cleaning into TF-IDF (Critical Step)**

In your pipeline, TF-IDF is configured like this:

```python
TfidfVectorizer(preprocessor=clean_text)
```

This tells TF-IDF:

> “Before you turn text into numbers, run clean_text() first.”

This ensures all downstream learning uses clean inputs.

**Line-mapped location:**

```python
("tfidf", TfidfVectorizer(preprocessor=clean_text))
```

This is the single most important line in this micro-task.

---

# **6. How to Verify Cleaning Works**

Run:

```bash
python train.py
```

Look at the **vocabulary** learned by TF-IDF:

Add this before saving the model:

```python
print(model.named_steps["tfidf"].vocabulary_)
```

If cleaning works, you will **not** see:

* uppercase words
* punctuation
* weird tokens

All tokens should look clean, lowercase, simple.

Example expected tokens:

```
"this": 12
"great": 7
"terrible": 20
"hate": 14
```

---

# **7. Understanding the Impact on the Model**

Text cleaning improves:

* feature consistency
* vocabulary stability
* generalisation
* prediction stability

Models become less sensitive to user input variations:

```
"I LOVE THIS!!!"  
"I love this"  
"i love this"
```

All mapped to:

```
i love this
```

which improves accuracy.

---

# **8. Problem → Solution (Your Questions Incorporated)**

These come from real confusion you had earlier and are important for beginners.

---

### **Problem 1: “Does cleaning happen before or after TF-IDF?”**

**Solution:**
Before.
The line:

```python
preprocessor=clean_text
```

makes TF-IDF call `clean_text()` **first**, then vectorise.

---

### **Problem 2: “Will cleaning change model predictions?”**

**Solution:**
Yes.
Cleaning reduces noise → model sees more consistent patterns → predictions become more reliable.

---

### **Problem 3: “Why remove punctuation? Doesn’t it matter?”**

**Solution:**
For basic sentiment tasks, punctuation rarely adds meaning.
And too much noise creates extra TF-IDF tokens like:

* `great!!!`
* `great!!`
* `great`

Cleaning merges them into one.

---

### **Problem 4: “How do I know cleaning didn’t break something?”**

**Solution:**

1. Model still trains
2. TF-IDF vocabulary looks clean
3. Predictions still run via predict.py
4. No errors appear

This micro-task only **normalises** input, it does not change logic.

---

# **9. Commands Cheat Sheet**

### Install dependencies:

```
pip install -r requirements.txt
```

### Run training with cleaning enabled:

```
python train.py
```

### Predict custom text:

```
python predict.py "THIS is GREAT!!!"
```

Should now produce the same result as:

```
python predict.py "this is great"
```

---

# **10. End-to-End Flow with Cleaning**

```
raw text
   ↓
clean_text()
   ↓
TF-IDF (text → numbers)
   ↓
Logistic Regression (learn patterns)
   ↓
Evaluation (precision/recall/F1)
   ↓
model saved
   ↓
predict.py loads saved model
   ↓
input text → clean_text() → prediction
```

You now have a fully normalised training + prediction loop.

---

# **11. Next Steps (What You’ll Learn in Upcoming Micro-Tasks)**

Now that text is clean, the next micro-tasks will teach you:

* **cross-validation** (more reliable testing)
* **hyperparameter tuning** (improving performance)
* **model versioning**
* **deploying the model via API**
* **turning this into a Node → Python bridge**
* **LLM fine-tuning**
* **RAG with vector databases**

Each micro-task builds on this one.

---

# **12. Summary**

In this micro-task you learned:

* Why text cleaning is essential for ML
* How lowercasing, punctuation removal, and space normalisation work
* The exact lines of code that implement each step
* How cleaning plugs into TF-IDF
* How to verify cleaning works
* How to think like an ML engineer working with raw text

 

---
 
