from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load the Iris dataset
iris = load_iris()
X = iris.data
y = iris.target

# Splitting the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Creating a Decision Tree classifier
clf = DecisionTreeClassifier()

# Training the classifier on the training data
clf.fit(X_train, y_train)

# Get input from the user for sepal and petal measurements
sepal_length = float(input("Enter sepal length: "))
sepal_width = float(input("Enter sepal width: "))
petal_length = float(input("Enter petal length: "))
petal_width = float(input("Enter petal width: "))

# Create an example feature vector from user input
user_input = [[sepal_length, sepal_width, petal_length, petal_width]]

# Predict the class label for the user input
predicted_class = clf.predict(user_input)

# Get the class name using the target_names from the dataset
class_name = iris.target_names[predicted_class]

print(f"The predicted class is: {class_name[0]}")

