import numpy as np  
import pandas as pd   #{for reading the csv files}
import matplotlib.pyplot as plt #{Using for plotting the graphs}
import os 


from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, f1_score #{Machine learning algorithms imported} 

currentdir = os.getcwd()  

#Reading the dataset 
train_df = pd.read_csv(f"{currentdir}/Data/alpha_gym/train.csv")
test_df = pd.read_csv(f"{currentdir}/Data/alpha_gym/test.csv")

x = train_df.drop('label', axis=1)
y = train_df['label']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

knn = KNeighborsClassifier(n_neighbors=5)


# Corrected variable names
knn.fit(x_train, y_train)

y_pred = knn.predict(x_test)

cm = confusion_matrix(y_test, y_pred)
accuracy = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred, average="macro")

print("Confusion Matrix:")
print(cm)
print("Accuracy:", accuracy)
print("F1 Score:", f1)

# Make predictions on the test data
y_test_pred = knn.predict(test_df)
# Save the predictions to a CSV file
np.savetxt("y_test_pred.csv", y_test_pred, delimiter=",")