# Visualization Quick Reference

Static (matplotlib/seaborn) and interactive (plotly) recipes. Pair with `SKILL.md` validation discipline.

## Project Design Contract

If a `DESIGN.md` exists in the project root, read its YAML frontmatter (colors → data-1 through data-N; typography → body-md, label) and the `Cross-Media Application → Data visualization` section. Apply these values before using the defaults below. The contract's chart palette, labeling policy, uncertainty display, and accessibility rules take precedence.

## Static plots

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Distribution
sns.histplot(data, kde=True)

# Categorical
sns.countplot(x="category", data=df)

# Correlation
sns.heatmap(corr, annot=True, fmt=".2f")

# Relationship
sns.scatterplot(x="var1", y="var2", hue="category", data=df)
sns.boxplot(x="category", y="value", data=df)
```

## Interactive plots

```python
import plotly.express as px

fig = px.scatter(df, x="var1", y="var2", color="category")
fig.show()
```

## Styling

- Consistent font (Arial, sans-serif).
- Light backgrounds.
- Color meaningfully — categorical uses a qualitative palette, continuous uses a sequential one.
- Label axes with units.
- Include legends where they help.
- For presentations: simplify, increase font size.

## Saving results

```python
plt.savefig("output/plot.png", dpi=150)
df.to_csv("output/results.csv", index=False)
```
