import pytest

from sklearn.utils.estimator_checks import check_estimator

from minimization import GeneralizeToRepresentative


@pytest.mark.parametrize(
    "Estimator", [GeneralizeToRepresentative]
)
def test_all_estimators(Estimator):
    return check_estimator(Estimator)
