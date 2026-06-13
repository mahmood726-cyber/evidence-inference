"""Smoke / import tests for the evidence_inference package.

Kept dependency-light: the top-level package must import with only the
standard scientific stack installed. Heavy optional NLP dependencies
(spacy, torch, ...) are exercised only when present, via importorskip.
"""

import importlib

import pytest


def test_package_imports():
    """The top-level package must import cleanly."""
    mod = importlib.import_module("evidence_inference")
    assert mod is not None


def test_vectorize_empty_prompt_raises_keyerror():
    """Preprocessor.vectorize must fail loudly (not IndexError) when the
    requested prompt_id matches no rows.

    Regression guard for the empty-DataFrame ``.values[0]`` access at the
    top of ``vectorize`` (Sentinel P1-empty-dataframe-access). Skipped when
    the optional NLP stack the preprocessor depends on is unavailable.
    """
    pytest.importorskip("spacy")
    pd = pytest.importorskip("pandas")

    from evidence_inference.preprocess import preprocessor as pp

    pre = pp.Preprocessor.__new__(pp.Preprocessor)  # avoid heavy __init__
    empty_prompts = pd.DataFrame(
        columns=[pp.PROMPT_ID_COL_NAME, pp.STUDY_ID_COL,
                 "Intervention", "Comparator", "Outcome"]
    )

    with pytest.raises(KeyError):
        pp.Preprocessor.vectorize(pre, empty_prompts, prompt_id=999999)
