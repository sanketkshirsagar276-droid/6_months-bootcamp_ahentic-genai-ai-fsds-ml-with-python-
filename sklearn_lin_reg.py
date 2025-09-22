import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv(r'C:\Users\Sanket kshirsagar\Downloads\Salary_Data.csv')

X = df.iloc[:, :-1]
y = df.iloc[:, -1]

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X, y, test_size=0.20, random_state=0)

from sklearn.linear_model import LinearRegression 
regressor = LinearRegression()
regressor.fit(X_train, y_train)

y_pred = regressor.predict(X_test)

comparison = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
print(comparison)

plt.scatter(X_test, y_test, color = 'red') # Real salary data (testing)
plt.plot(X_train, regressor.predict(X_train), color = 'blue') # Regression line from training set
plt.title('salary vs Experience (Test set)')
plt.xlabel('Years of Experience')
plt.ylabel('Salary')
plt.show()

m = regressor.coef_
print(m)

c = regressor.intercept_
print(c)

y_12 = m * 12 + c
print(y_12)

y_20 = m * 20 + c
print(y_20)

y_10 = m * 10 + c
print(y_10)
