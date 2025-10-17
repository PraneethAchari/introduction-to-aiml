import pandas as pd

# 📘 Step 1: Create the dataset
# Each student has study hours and whether they passed (1) or failed (0)
data = pd.DataFrame({
    'Student': [1, 2, 3, 4, 5],
    'Study_Hours': [2, 4, 6, 8, 10],
    'Pass': [0, 0, 1, 1, 1]
})

# 📍 Step 2: Find possible split points
# We can split between consecutive study hour values
unique_hours = sorted(data['Study_Hours'].unique())
split_points = [(unique_hours[i] + unique_hours[i+1]) / 2 for i in range(len(unique_hours)-1)]

print("👉 Possible split points:", split_points)

# 📊 Step 3: Define a helper function to calculate Gini impurity
def gini_for_groups(groups):
    total = sum(len(group) for group in groups)
    gini = 0.0
    
    for group in groups:
        size = len(group)
        if size == 0:
            continue
        
        # Calculate probability of each class (Pass/Fail)
        score = 0.0
        for outcome in [0, 1]:
            p = (group['Pass'] == outcome).sum() / size
            score += p ** 2
        
        # Weighted Gini for this group
        gini += (1.0 - score) * (size / total)
    
    return gini

# 🧮 Step 4: Try each possible split and calculate Gini impurity
results = []

for split in split_points:
    left_group = data[data['Study_Hours'] <= split]
    right_group = data[data['Study_Hours'] > split]
    
    gini = gini_for_groups([left_group, right_group])
    results.append({'Split_At': split, 'Gini_Impurity': round(gini, 3)})

# 🏁 Step 5: Show all results and pick the best split (lowest Gini)
results_df = pd.DataFrame(results)
best_split = results_df.loc[results_df['Gini_Impurity'].idxmin()]

print("\n📊 Gini Impurity for each split:")
print(results_df)

print("\n✅ Best split found:")
print(best_split)
