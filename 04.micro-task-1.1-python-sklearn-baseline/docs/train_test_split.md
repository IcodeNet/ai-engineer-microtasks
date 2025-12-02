# Understanding `train_test_split`

## Overview

The `train_test_split` function splits your dataset into training and testing sets. This is a fundamental step in machine learning to evaluate how well your model performs on unseen data.

## Code Reference

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)
```

**Location:** `train.py` lines 63-65

## Parameters Explained

### 1. `X` (Features) - Input Texts
- The 10 text examples from `get_data()`
- Example: `["this is great", "I love this product", ...]`

### 2. `y` (Labels) - Target Classes
- The corresponding labels: `["positive", "positive", "negative", ...]`

### 3. `test_size=0.3` - 30% for Testing
- **70% for training** (7 examples)
- **30% for testing** (3 examples)
- This is a common split ratio in ML

### 4. `random_state=42` - Reproducibility
- Sets a random seed for the split
- Ensures you get the **same split every time** you run the code
- Important for reproducible experiments

### 5. `stratify=y` - Maintain Class Balance
- **Critical parameter** for small datasets
- Ensures both training and test sets have the same proportion of classes
- Without it, you might get imbalanced splits

## What It Returns

Four arrays:
- **`X_train`** - Training texts (7 examples)
- **`X_test`** - Testing texts (3 examples)
- **`y_train`** - Training labels (7 labels)
- **`y_test`** - Testing labels (3 labels)

## Why This Matters

### Training Set (`X_train`, `y_train`)
- Used to **teach the model**
- The model learns patterns from these examples

### Test Set (`X_test`, `y_test`)
- Used to **evaluate performance**
- Tests how well the model generalizes to unseen data
- Simulates real-world performance

## Example with Your Data

You have **10 examples**:
- 5 positive, 5 negative

With `test_size=0.3` and `stratify=y`:
- **Training**: ~3-4 positive, ~3-4 negative (7 total)
- **Testing**: ~1-2 positive, ~1-2 negative (3 total)

The `stratify` parameter ensures the class balance is maintained in both sets.

## Why `stratify=y` is Important

### Without `stratify`:
You might get:
- Training: 6 positive, 1 negative (imbalanced)
- Testing: 0 positive, 3 negative (no positives to test!)

### With `stratify=y`:
- Both sets maintain the 50/50 positive/negative ratio
- More reliable evaluation
- Better representation of your data

## Visual Representation

```
Original Dataset (10 examples):
[text1, text2, text3, text4, text5, text6, text7, text8, text9, text10]
[pos,   pos,   pos,   neg,   neg,   neg,   neg,   pos,   pos,   neg]

After train_test_split:

Training Set (7 examples - 70%):
[text1, text3, text5, text6, text7, text8, text10]
[pos,   pos,   neg,   neg,   neg,   pos,   neg]

Testing Set (3 examples - 30%):
[text2, text4, text9]
[pos,   neg,   pos]
```

## Documentation

- **Official Docs**: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
- **User Guide**: https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation

## Key Takeaways

1. **Always split your data** before training
2. **Use `stratify`** for classification tasks to maintain class balance
3. **Set `random_state`** for reproducible results
4. **Never train on test data** - it would give misleading results!

