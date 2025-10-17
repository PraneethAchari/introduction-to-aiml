# 🌳 Decision Tree - Part 2 (Manual Gini + Optional sklearn check)
# Let's predict if a student passes or fails based on how many hours they study.

import pandas as pd

# -----------------------------
# 🧩 Step 1: Create our small dataset
# -----------------------------
data = pd.DataFrame({
    'Student': [1, 2, 3, 4, 5],
    'Study_Hours': [2, 4, 6, 8, 10],
    'Pass': [0, 0, 1, 1, 1]
})

print("📘 Our Dataset:")
print(data, "\n")

# -----------------------------
# 🪓 Step 2: Find possible split points
# (Between every two consecutive study hour values)
# -----------------------------
unique_hours = sorted(data['Study_Hours'].unique())
split_points = [(unique_hours[i] + unique_hours[i+1]) / 2 for i in range(len(unique_hours)-1)]

print("📍 Possible places to split the data:", split_points, "\n")

# -----------------------------
# ⚖️ Step 3: Define a function to calculate Gini impurity
# (This measures how 'mixed' or 'impure' a group is)
# -----------------------------
def gini_for_groups(groups):
    total = sum(len(g) for g in groups)
    gini = 0.0
    for group in groups:
        size = len(group)
        if size == 0:
            continue

        # Calculate how many pass/fail in this group
        score = 0.0
        for outcome in [0, 1]:  # 0 = Fail, 1 = Pass
            p = (group['Pass'] == outcome).sum() / size
            score += p ** 2

        # Weighted gini impurity for this group
        gini += (1.0 - score) * (size / total)
    
    return gini

# -----------------------------
# 🔢 Step 4: Try each split and calculate its Gini impurity
# -----------------------------
results = []

for split in split_points:
    left = data[data['Study_Hours'] <= split]   # Students who study less than or equal to split
    right = data[data['Study_Hours'] > split]   # Students who study more than split
    
    gini = gini_for_groups([left, right])
    results.append({
        'Split_At': split,
        'Left_Group_Size': len(left),
        'Right_Group_Size': len(right),
        'Gini_Impurity': round(gini, 3)
    })

results_df = pd.DataFrame(results)
print("📊 Gini impurity for each possible split:")
print(results_df, "\n")

# -----------------------------
# 🏆 Step 5: Pick the best split (lowest Gini impurity)
# -----------------------------
best_split = results_df.loc[results_df['Gini_Impurity'].idxmin()]
print("✅ Best Split Found:")
print(best_split, "\n")

# -----------------------------
# 🌲 Step 6: Simple Text Visualization of the Final Decision Tree
# -----------------------------
threshold = best_split['Split_At']
print("🌳 Our Simple Decision Tree:")
print(f"IF Study_Hours <= {threshold} → ❌ FAIL (0)")
print(f"ELSE → ✅ PASS (1)\n")

# -----------------------------
# 🤖 Step 7 (Optional): Check with sklearn’s DecisionTreeClassifier
# -----------------------------
from sklearn.tree import DecisionTreeClassifier, export_text

X = data[['Study_Hours']]
y = data['Pass']

model = DecisionTreeClassifier(criterion='gini', random_state=0)
model.fit(X, y)

print("🤖 sklearn’s Decision Tree result:")
print(export_text(model, feature_names=['Study_Hours']))
