# Understanding Build → Train → Predict Workflow

## Overview

These three steps form the core machine learning workflow. Understanding this sequence is fundamental to ML.

## Code Reference

```python
model = build_model()           # Line 71
model.fit(X_train, y_train)     # Line 77
y_pred = model.predict(X_test)  # Line 83
```

**Location:** `train.py` lines 71, 77, 83

## Step 1: Build the Model (`model = build_model()`)

### What It Does
- Creates the ML pipeline structure
- **Does NOT train yet** - just sets up the architecture

### What `build_model()` Returns
A scikit-learn `Pipeline` with two steps:

1. **`TfidfVectorizer()`** - Converts text to numbers
   - Transforms: `"this is great"` → `[0.5, 0.2, 0.8, ...]` (TF-IDF features)
   - Converts human-readable text into numerical features

2. **`LogisticRegression()`** - The classifier
   - Learns to predict "positive" or "negative" from the numbers
   - A linear classifier that finds patterns in the numerical features

### Pipeline Flow
```python
# The pipeline does this automatically:
text → [TF-IDF vectorization] → [numbers] → [Logistic Regression] → prediction
```

### Think of It Like
- Building a factory blueprint
- The structure is ready, but nothing has been produced yet
- The model exists but hasn't learned anything

## Step 2: Train the Model (`model.fit(X_train, y_train)`)

### What It Does
- **Trains the model** on the training data
- This is where **learning happens**

### What Happens Internally

#### 1. TfidfVectorizer Learns:
- **Vocabulary** from training texts
- How to convert text to TF-IDF vectors
- Example: learns that "great" is an important word

#### 2. LogisticRegression Learns:
- **Patterns** in the TF-IDF vectors
- Which word patterns → "positive"
- Which word patterns → "negative"
- Example: learns that texts with "great", "love", "fantastic" → positive

### After `fit()`
- The model has **learned from the 7 training examples**
- It can now make predictions on new text
- The model is "trained" and ready to use

### Think of It Like
- Teaching the model by showing it examples
- The model memorizes patterns and relationships
- Like a student studying for an exam

## Step 3: Predict (`y_pred = model.predict(X_test)`)

### What It Does
- Makes predictions on the **test set** (the 3 examples not used for training)
- Evaluates how well the model **generalizes** to unseen data

### What Happens

1. Takes `X_test` (3 test texts)
2. Runs them through the pipeline:
   - Text → TF-IDF vectorization → numbers
   - Numbers → Logistic Regression → prediction
3. Returns `y_pred` (3 predictions)

### Example
```python
X_test = ["I love this", "this is terrible", "pretty nice"]

# After model.predict(X_test):
y_pred = ["positive", "negative", "positive"]
```

### Think of It Like
- Taking a test after studying
- The model applies what it learned to new examples
- This shows how well it really understands the patterns

## Visual Flow

```
Step 1: model = build_model()
         ↓
    Creates empty pipeline structure
    [TfidfVectorizer] → [LogisticRegression]
         ↓
    (Not trained yet - just the blueprint)

Step 2: model.fit(X_train, y_train)
         ↓
    Trains on 7 examples:
    - TfidfVectorizer learns vocabulary
    - LogisticRegression learns patterns
         ↓
    Model is now "trained" and ready

Step 3: y_pred = model.predict(X_test)
         ↓
    Tests on 3 examples:
    - Converts text → numbers → prediction
         ↓
    Returns: ["positive", "negative", "positive"]
```

## Why This Order Matters

1. **Build first** - Create the structure
2. **Fit second** - Learn from training data
3. **Predict third** - Evaluate on test data

**You can't predict before fitting** - the model needs to learn first!

## What Happens Next

The code compares:
- **`y_test`** (true labels): what the actual labels are
- **`y_pred`** (predictions): what the model predicted

This lets you measure:
- **Accuracy**: How many predictions were correct?
- **Performance**: How well does the model generalize?

## Documentation Links

### Pipeline
- **Official Docs**: https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html
- **User Guide**: https://scikit-learn.org/stable/modules/compose.html#pipeline

### Fit Method
- **Pipeline.fit()**: https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html#sklearn.pipeline.Pipeline.fit
- **General fit() concept**: https://scikit-learn.org/stable/developers/develop.html#fitting

### Predict Method
- **Pipeline.predict()**: https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html#sklearn.pipeline.Pipeline.predict
- **General predict() concept**: https://scikit-learn.org/stable/developers/develop.html#prediction

## Key Takeaways

1. **Build** - Create the model structure (empty, untrained)
2. **Fit** - Train the model on data (learning phase)
3. **Predict** - Use the model on new data (evaluation phase)

This is the **standard ML workflow** that applies to almost all machine learning models!

## Common Mistakes

❌ **Trying to predict before fitting**
```python
model = build_model()
y_pred = model.predict(X_test)  # ERROR! Model hasn't learned yet
```

✅ **Correct order**
```python
model = build_model()
model.fit(X_train, y_train)     # Learn first
y_pred = model.predict(X_test)  # Then predict
```

❌ **Training on test data**
```python
model.fit(X_test, y_test)  # WRONG! Test data should be unseen
```

✅ **Correct approach**
```python
model.fit(X_train, y_train)     # Train on training data
y_pred = model.predict(X_test)  # Test on separate test data
```

