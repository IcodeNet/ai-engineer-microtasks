# **README.md — Micro-Task 1.2 (Text Cleaning Preprocessor)**

### *20-minute micro-task | Node + Python track | Beginner-friendly | Practical*

## **🎯 Goal**

Add a **text cleaning preprocessor** to your Python ML pipeline so that:

* all text is cleaned before TF-IDF
* noise is removed (punctuation, stray symbols, uppercase)
* the model trains on normalised input
* predictions become more consistent

You’ll create a new micro-task folder, copy your previous code, add cleaning, and run training again.

---

# **📁 Folder Structure**

Create:

```
05.micro-task-1.2-text-cleaning/
  train.py
  predict.py
  requirements.txt
  models/      (created after running train.py)
  README.md     <-- (this file)
  LEARNING.md   <-- separate full explanation
```

Copy all files from:

```
04.micro-task-1.1-python-sklearn-baseline
```

into this folder before starting.

---

# **🧠 What You Will Learn**

* How to write a **clean_text()** function
* How to integrate cleaning into `TfidfVectorizer`
* How to check the effect of cleaning on the vocabulary
* Why cleaning improves model stability

This is your first “data preprocessing” step — core ML skill.

---

# **🛠️ Step-by-Step Instructions**

## **1. Copy previous micro-task**

Copy everything from:

```
04.micro-task-1.1-python-sklearn-baseline/
```

into:

```
05.micro-task-1.2-text-cleaning/
```

---

## **2. Add the cleaning function**

In `train.py`, at the top:

```python
import re

def clean_text(text: str) -> str:
    # 1. Lowercase
    text = text.lower()
    # 2. Remove punctuation / symbols
    text = re.sub(r"[^a-z0-9\s]", "", text)
    # 3. Collapse multiple spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text
```

---

## **3. Plug cleaning into TF-IDF**

Modify your pipeline:

```python
pipeline = Pipeline(
    [
        (
            "tfidf",
            TfidfVectorizer(
                preprocessor=clean_text
            ),
        ),
        ("clf", LogisticRegression(max_iter=1000)),
    ]
)
```

This line tells TF-IDF to clean your text **before** vectorising it.

---

## **4. (Optional) Print the vocabulary to verify cleaning**

Add this somewhere after training:

```python
print("Vocabulary sample:", list(model.named_steps["tfidf"].vocabulary_.keys())[:15])
```

You should see *clean*, lowercase words only — no punctuation, no uppercase.

---

## **5. Train the cleaned model**

Run:

```bash
python train.py
```

Expected output:

* training runs normally
* classification_report still prints
* model saved to `models/text_classifier.joblib`
* vocabulary printout shows cleaned text

---

## **6. Test predict.py**

Prediction should now behave the same regardless of input format:

```bash
python predict.py "THIS IS GREAT!!!"
python predict.py "this is great"
python predict.py "This    is   GREAT!!"
```

All should return the same sentiment.

---

# **🧪 Acceptance Criteria (What “done” looks like)**

* [ ] `clean_text()` added correctly
* [ ] pipeline updated with `preprocessor=clean_text`
* [ ] training runs without errors
* [ ] model saved successfully
* [ ] predict.py still works
* [ ] cleaned tokens appear in vocabulary (optional)
* [ ] LEARNING.md added to folder

When all checkboxes are true → micro-task is complete.

---

# **⏱️ Expected Duration**

**~20 minutes**
(If you did micro-task 1.1, this will be very fast.)

---

# **➡️ Next Micro-Task**

Once done, proceed to:

```
06.micro-task-1.3-cross-validation
```

---
 