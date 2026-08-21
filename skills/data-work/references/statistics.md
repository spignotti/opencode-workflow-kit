# Statistics Quick Reference

Load this reference when you need a test-selection matrix, model-selection decision tree, or evaluation-metric table. Pair with `SKILL.md` validation discipline.

## Test selection

| Goal | Test |
|------|------|
| Compare means of 2 groups | t-test |
| Compare means of 3+ groups | ANOVA |
| Compare proportions | chi-square |
| Check normality | Shapiro-Wilk |
| Check correlation significance | Pearson / Spearman r |
| Test distribution differences | KS test |

## Common pitfalls

- Don't assume normality — check with histogram or test.
- Don't ignore multicollinearity in regression.
- Don't p-hack: pre-specify your analysis.
- Don't confuse correlation with causation.

## Problem type selection

```
Is the target...
├── Categorical (2 classes) → Binary Classification
├── Categorical (3+ classes) → Multi-class Classification
├── Continuous number → Regression
└── No target variable → Clustering / Dimensionality Reduction
```

## Model selection decision tree

```
Classification:
├── Tabular, medium data → Random Forest or Gradient Boosting (XGBoost, LightGBM)
├── High dimensional → Logistic Regression with regularization
├── Image/Text → Deep Learning (CNN, Transformer)
└── Simple, interpretable needed → Logistic Regression, Decision Tree

Regression:
├── Tabular → Linear Regression, Ridge/Lasso, Random Forest, Gradient Boosting
├── Time series → ARIMA, Prophet, LightGBM with time features
└── High dimensional → Regularized regression (Ridge)

Clustering:
├── Numeric data → K-Means
├── Mixed data → HDBSCAN
└── Hierarchical needed → Agglomerative Clustering
```

## Evaluation metrics

| Problem Type | Metric |
|-------------|--------|
| Classification (imbalanced) | F1, AUC-ROC, Precision-Recall |
| Classification (balanced) | Accuracy |
| Regression | RMSE, MAE, R² |
| Time Series | MAE, MAPE |

## Train / Validation / Test split

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
# Time series: chronological split, not random
```

## Cross-validation

```python
from sklearn.model_selection import cross_val_score

scores = cross_val_score(model, X, y, cv=5, scoring="f1")
```
