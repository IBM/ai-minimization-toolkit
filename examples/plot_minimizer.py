"""
=============================
Plotting Template Transformer
=============================

An example plot of :class:`minimization.template.TemplateTransformer`
"""
import numpy as np
from matplotlib import pyplot as plt
from minimization import GeneralizeToRepresentative
from sklearn.tree import DecisionTreeClassifier

X = np.arange(50, dtype=np.float).reshape(-1, 1)
X /= 50
y = np.zeros(X.shape[0])
for i in range(X.shape[0]):
    if i > 8 and i < 20:
        y[i] = 1
base_est = DecisionTreeClassifier()
base_est.fit(X, y)
predictions = base_est.predict(X)

estimator = GeneralizeToRepresentative(base_est, target_accuracy=0.9)
X_transformed = estimator.fit_transform(X, predictions)


plt.plot(X.flatten(), label='Original Data')
plt.plot(X_transformed.flatten(), label='Transformed Data')
plt.title('Plots of original and transformed data')

plt.legend(loc='best')
plt.grid(True)
plt.xlabel('Index')
plt.ylabel('Value of Data')

plt.show()
