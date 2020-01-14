.. title:: User guide : contents

.. _user_guide:

==========================================
User guide: start minimizing your ML model
==========================================

The GeneralizeToRepresentative class
------------------------------------

The main class, :class:`minimization.GeneralizeToRepresentative`, is a scikit-learn compatible ``Transformer``, that receives an existing estimator and labeled training data, and learns the generalizations that can be applied to any newly collected data for analysis by the original model.

* at ``fit``, the generalizations are learned from ``X`` and ``y``;

* at ``transform``, ``X`` will be transformed, using the generalizations learned during ``fit``;

* ``fit_transform`` will both learn the generalizations and then apply them to ``X``.

It is also possible to export the generalizations as feature ranges, for example to create forms for data collection.

The current implementation supports only numeric features, so any categorical features must be transformed to a numeric representation before using this class.

How to use GeneralizeToRepresentative
-------------------------------------

Start by training your machine learning model. In this example, we will use a :class:`sklearn.tree.DecisionTreeClassifier`, but any scikit-learn model can be used. We will use the iris dataset in our example.

.. code:: python

  from sklearn import datasets
  from sklearn.model_selection import train_test_split
  from sklearn.tree import DecisionTreeClassifier

  dataset = datasets.load_iris()
  X_train, X_test, y_train, y_test = train_test_split(dataset.data, dataset.target, test_size=0.2)

  base_est = DecisionTreeClassifier()
  base_est.fit(X_train, y_train)

Now create the :class:`minimization.GeneralizeToRepresentative` transformer and train it. Supply it with the original model and the desired target accuracy. The training process may receive the original labeled training data or the model's predictions on the data.

.. code:: python

  predictions = base_est.predict(X_train)
  gen = GeneralizeToRepresentative(base_est, target_accuracy=0.9)
  gen.fit(X_train, predictions)

Now use the transformer to transform new data, for example the test data.

.. code:: python

  transformed = gen.transform(X_test)

The transformed data has the same columns and formats as the original data, so it can be used directly to derive predictions from the original model.

.. code:: python

  new_predictions = base_est.predict(transformed)

To export the resulting generalizations, retrieve the ``Transformer``'s ``_generalize`` parameter.

.. code:: python

  generalizations = base_est._generalize

The returned object has the following structure::

  {
    ranges:
    {
      list of (<feature name>: [<list of values>])
    },
    untouched: [<list of feature names>]
  }

For example::

  {
    ranges:
    {
      age: [21.5, 39.0, 51.0, 70.5],
      education-years: [8.0, 12.0, 14.5]
    },
    untouched: ["occupation", "marital-status"]
  }

Where each value inside the range list represents a cutoff point. For example, for the ``age`` feature, the ranges in this example are: ``<21.5, 21.5-39.0, 39.0-51.0, 51.0-70.5, >70.5``. The ``untouched`` list represents features that were not generalized, i.e., their values should remain unchanged.
