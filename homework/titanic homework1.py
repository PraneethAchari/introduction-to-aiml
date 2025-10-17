# Our tiny dataset of 5 students
# Each student has:
#   - Study hours
#   - Exam result (1 = Pass, 0 = Fail)
students = [
    {'hours': 2, 'label': 0},
    {'hours': 4, 'label': 0},
    {'hours': 6, 'label': 1},
    {'hours': 8, 'label': 1},
    {'hours': 10, 'label': 1}
]


# Step 1: Define a function to calculate Gini impurity
def gini_impurity(groups, classes):
    """
    Calculates the Gini impurity for a given split of data.
    Lower Gini = better (purer) split.
    """
    total_samples = float(sum(len(group) for group in groups))
    gini = 0.0

    for group in groups:
        size = float(len(group))
        if size == 0:
            continue  # Avoid division by zero

        score = 0.0
        for class_val in classes:
            proportion = [row['label'] for row in group].count(class_val) / size
            score += proportion ** 2

        gini += (1.0 - score) * (size / total_samples)

    return gini


# Step 2: Define how we split the dataset
def split_dataset(threshold, dataset):
    """
    Splits the dataset into two groups based on a threshold value.
    """
    left_group, right_group = [], []
    for row in dataset:
        if row['hours'] <= threshold:
            left_group.append(row)
        else:
            right_group.append(row)
    return left_group, right_group


# Step 3: Try all possible splits and find the best one
classes = [0, 1]
best_gini = 1.0  # start with worst possible impurity
best_threshold = None
best_groups = None

possible_splits = [3, 5, 7, 9]

print("🔍 Checking possible splits and their Gini impurities:\n")

for threshold in possible_splits:
    groups = split_dataset(threshold, students)
    gini = gini_impurity(groups, classes)
    print(f" - Split at {threshold} hours → Gini = {gini:.3f}")

    if gini < best_gini:
        best_gini = gini
        best_threshold = threshold
        best_groups = groups


# Step 4: Show the best split
print("\n✅ Best Split Found:")
print(f"   Study hours threshold = {best_threshold}")
print(f"   Gini impurity = {best_gini:.3f}")


# Step 5: Visualize the simple decision tree
print("\n📘 Final Decision Tree:")
print(f"IF study_hours <= {best_threshold} → FAIL (0)")
print(f"ELSE → PASS (1)")
