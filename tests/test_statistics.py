import numpy as np
import pandas as pd

from yuhub_repro.statistics import average_measure_icc, holm_adjust, paired_signflip_test


def test_icc_is_one_for_identical_raters():
    matrix = pd.DataFrame({"r1": [0.1, 0.4, 0.9], "r2": [0.1, 0.4, 0.9]})
    result = average_measure_icc(matrix)
    assert np.isclose(result["icc_absolute_average"], 1.0)
    assert np.isclose(result["icc_consistency_average"], 1.0)


def test_holm_is_monotone_in_sorted_order():
    adjusted = holm_adjust([0.01, 0.04, 0.03])
    assert adjusted == [0.03, 0.06, 0.06]


def test_exact_signflip_all_positive():
    p_value, method = paired_signflip_test(np.ones(4), np.random.default_rng(1))
    assert method == "exact"
    assert np.isclose(p_value, 2 / 16)
