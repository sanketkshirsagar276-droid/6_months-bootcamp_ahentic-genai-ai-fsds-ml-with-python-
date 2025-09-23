import numpy as np
import pandas as pd

#from subprocess import check_output
#print(check_output(["ls", "../input"]).decode("utf8"))

#Import Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
np.set_printoptions(threshold = np.inf)

#Importing DataSet 
df = pd.read_csv(r'C:\Users\Sanket kshirsagar\OneDrive\Desktop\ML\22nd, 23rd- slr\SLR - House price prediction\House_data.csv')
space=df['sqft_living']
price=df['price']

x = np.array(space).reshape(-1,1)
y = np.array(price)

#Splitting the data into Train and Test
from sklearn.model_selection import train_test_split
xtrain, xtest, ytrain, ytest = train_test_split(x,y,test_size=1/3, random_state=0)

#Fitting simple linear regression to the Training Set
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(xtrain,ytrain)

#Predicting the prices
pred = regressor.predict(xtest)

#Visualizing the training Test Results 
plt.scatter(xtrain, ytrain, color= 'red')
plt.plot(xtrain, regressor.predict(xtrain), color ='blue')
plt.title('Visuals for Training Dataset')
plt.xlabel('Spaces')
plt.ylabel('Price')
plt.show()

#Visualizing the Test Results 
plt.scatter(xtest, ytest, color ='red')
plt.plot(xtrain, regressor.predict(xtrain), color = 'blue')
plt.title('Visuals for Test Dataset')
plt.xlabel('Space')
plt.ylabel('Price')
plt.show()