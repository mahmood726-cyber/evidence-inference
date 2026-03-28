"""
ASReview Simulation Runner for 5-Star Benchmarking
Phase 2.2: Run active learning simulations on 501 Cochrane reviews

Simulates ASReview-style active learning without requiring full ASReview installation.
Calculates WSS@95, RRF, and stopping rule accuracy metrics.
"""

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import os

# Import our 5-Star enhancements
import sys
sys.path.insert(0, "C:/Users/user")
from ASReview_5Star_Enhancements import (
    BayesianStoppingRule,
    StoppingEstimate,
    RecallCertifier
)


@dataclass
class SimulationResult:
    """Results from a single active learning simulation."""
    review_id: str
    n_total: int
    n_included: int
    n_excluded: int
    wss_95: float  # Work Saved over Sampling at 95% recall
    rrf: float  # Relevant Records Found
    recall_at_stop: float
    n_screened_at_stop: int
    stopping_method: str
    classifier: str
    correct_stopping: bool  # Did we achieve target recall?


@dataclass
class BenchmarkSummary:
    """Summary of benchmark across multiple reviews."""
    n_reviews: int
    mean_wss95: float
    median_wss95: float
    mean_rrf: float
    correct_stopping_rate: float
    results: List[SimulationResult]


class ActiveLearningSimulator:
    """
    Simulates ASReview-style active learning for benchmarking.

    Implements:
    - TF-IDF feature extraction
    - Multiple classifiers (SVM, NB, LR)
    - Uncertainty sampling query strategy
    - Bayesian stopping rule evaluation
    """

    def __init__(
        self,
        classifier: str = "svm",
        n_initial: int = 10,
        batch_size: int = 5,
        target_recall: float = 0.95
    ):
        """
        Initialize simulator.

        Args:
            classifier: "svm", "nb", or "lr"
            n_initial: Number of initial labeled documents
            batch_size: Documents queried per iteration
            target_recall: Target recall for stopping
        """
        self.classifier_name = classifier
        self.n_initial = n_initial
        self.batch_size = batch_size
        self.target_recall = target_recall

        # Initialize components
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            stop_words="english"
        )

        if classifier == "svm":
            self.classifier = SVC(kernel="linear", probability=True, C=1.0)
        elif classifier == "nb":
            self.classifier = MultinomialNB(alpha=0.1)
        else:
            self.classifier = LogisticRegression(max_iter=1000, C=1.0)

        self.stopping_rule = BayesianStoppingRule()

    def _create_text_features(self, titles: List[str]) -> np.ndarray:
        """Create TF-IDF features from titles."""
        # Handle empty/missing titles
        titles = [str(t) if t and str(t) != "nan" else "no title" for t in titles]
        return self.vectorizer.fit_transform(titles)

    def simulate_review(
        self,
        review_id: str,
        titles: List[str],
        labels: List[int]
    ) -> SimulationResult:
        """
        Simulate active learning on a single review.

        Args:
            review_id: Identifier for the review
            titles: List of document titles
            labels: List of binary labels (1=included, 0=excluded)

        Returns:
            SimulationResult with metrics
        """
        n_total = len(titles)
        n_included = sum(labels)
        n_excluded = n_total - n_included

        # Edge case: too few documents
        if n_total < 20 or n_included < 3:
            return SimulationResult(
                review_id=review_id,
                n_total=n_total,
                n_included=n_included,
                n_excluded=n_excluded,
                wss_95=0.0,
                rrf=0.0,
                recall_at_stop=0.0,
                n_screened_at_stop=n_total,
                stopping_method="insufficient_data",
                classifier=self.classifier_name,
                correct_stopping=False
            )

        # Create features
        try:
            X = self._create_text_features(titles)
        except Exception:
            # Fallback: random features
            X = np.random.randn(n_total, 100)

        y = np.array(labels)

        # Initialize: random sample with at least 1 positive
        indices = np.arange(n_total)
        np.random.shuffle(indices)

        # Ensure initial sample has at least 1 positive
        labeled_idx = []
        pos_found = False
        for i in indices:
            if len(labeled_idx) < self.n_initial:
                labeled_idx.append(i)
                if y[i] == 1:
                    pos_found = True
            elif not pos_found and y[i] == 1:
                labeled_idx.append(i)
                pos_found = True
                break

        if not pos_found:
            # No positives in initial sample - just use first n
            labeled_idx = list(indices[:self.n_initial])

        labeled_idx = set(labeled_idx)
        unlabeled_idx = set(indices) - labeled_idx

        # Tracking
        n_relevant_found = sum(y[i] for i in labeled_idx)
        screening_history = [(len(labeled_idx), n_relevant_found)]
        stopped = False
        stopping_point = None

        # Active learning loop
        while unlabeled_idx and not stopped:
            # Train classifier
            train_X = X[list(labeled_idx)]
            train_y = y[list(labeled_idx)]

            try:
                self.classifier.fit(train_X.toarray() if hasattr(train_X, 'toarray') else train_X, train_y)
            except Exception:
                # If training fails, continue with random selection
                pass

            # Get uncertainty scores for unlabeled
            unlabeled_list = list(unlabeled_idx)
            test_X = X[unlabeled_list]

            try:
                if hasattr(self.classifier, 'predict_proba'):
                    probs = self.classifier.predict_proba(
                        test_X.toarray() if hasattr(test_X, 'toarray') else test_X
                    )
                    # Uncertainty = entropy or distance from 0.5
                    uncertainty = 1 - np.abs(probs[:, 1] - 0.5) * 2
                else:
                    uncertainty = np.random.rand(len(unlabeled_list))
            except Exception:
                uncertainty = np.random.rand(len(unlabeled_list))

            # Select top uncertain documents
            top_k = min(self.batch_size, len(unlabeled_list))
            selected_local_idx = np.argsort(uncertainty)[-top_k:][::-1]
            selected_idx = [unlabeled_list[i] for i in selected_local_idx]

            # Update labeled/unlabeled
            for idx in selected_idx:
                labeled_idx.add(idx)
                unlabeled_idx.discard(idx)
                if y[idx] == 1:
                    n_relevant_found += 1

            screening_history.append((len(labeled_idx), n_relevant_found))

            # Check stopping rule
            estimate = self.stopping_rule.estimate_remaining(
                n_screened=len(labeled_idx),
                n_relevant_found=n_relevant_found,
                n_total=n_total,
                target_recall=self.target_recall
            )

            if estimate.recommendation == "safe_to_stop":
                stopped = True
                stopping_point = len(labeled_idx)

            # Safety: stop if we've screened 95%
            if len(labeled_idx) >= 0.95 * n_total:
                stopped = True
                stopping_point = len(labeled_idx)

        if stopping_point is None:
            stopping_point = len(labeled_idx)

        # Calculate metrics
        recall_at_stop = n_relevant_found / n_included if n_included > 0 else 1.0

        # WSS@95: Work saved at 95% recall
        # Find when 95% recall was achieved
        for n_screened, n_found in screening_history:
            if n_found >= 0.95 * n_included:
                wss_95 = 1 - (n_screened / n_total) - (1 - 0.95)
                break
        else:
            wss_95 = 0.0  # Never achieved 95% recall

        # RRF: Relevant Records Found normalized
        rrf = recall_at_stop

        # Did we achieve target recall?
        correct_stopping = recall_at_stop >= self.target_recall

        return SimulationResult(
            review_id=review_id,
            n_total=n_total,
            n_included=n_included,
            n_excluded=n_excluded,
            wss_95=max(0, wss_95),
            rrf=rrf,
            recall_at_stop=recall_at_stop,
            n_screened_at_stop=stopping_point,
            stopping_method="bayesian",
            classifier=self.classifier_name,
            correct_stopping=correct_stopping
        )


def run_benchmark(
    ground_truth_file: str,
    n_reviews: int = None,
    classifier: str = "svm"
) -> BenchmarkSummary:
    """
    Run benchmark on ground truth data.

    Args:
        ground_truth_file: Path to mega ground truth CSV
        n_reviews: Number of reviews to test (None = all)
        classifier: Classifier to use

    Returns:
        BenchmarkSummary with results
    """
    print("=" * 60)
    print("ASReview 5-Star Benchmark Runner")
    print("=" * 60)

    # Load data
    print(f"\nLoading: {ground_truth_file}")
    df = pd.read_csv(ground_truth_file)

    print(f"Total records: {len(df):,}")
    print(f"Total reviews: {df['review_id'].nunique()}")

    # Initialize simulator
    simulator = ActiveLearningSimulator(classifier=classifier)

    # Get unique reviews
    reviews = df['review_id'].unique()
    if n_reviews:
        reviews = reviews[:n_reviews]

    print(f"\nRunning simulations on {len(reviews)} reviews...")
    print("-" * 60)

    results = []
    for i, review_id in enumerate(reviews):
        review_data = df[df['review_id'] == review_id]

        titles = review_data['title'].tolist()
        labels = review_data['label_included'].tolist()

        result = simulator.simulate_review(review_id, titles, labels)
        results.append(result)

        if (i + 1) % 50 == 0:
            print(f"  Processed {i + 1}/{len(reviews)} reviews")

    # Calculate summary
    valid_results = [r for r in results if r.n_included >= 3]

    wss_values = [r.wss_95 for r in valid_results]
    rrf_values = [r.rrf for r in valid_results]
    correct = [r.correct_stopping for r in valid_results]

    summary = BenchmarkSummary(
        n_reviews=len(valid_results),
        mean_wss95=np.mean(wss_values) if wss_values else 0,
        median_wss95=np.median(wss_values) if wss_values else 0,
        mean_rrf=np.mean(rrf_values) if rrf_values else 0,
        correct_stopping_rate=np.mean(correct) if correct else 0,
        results=results
    )

    # Print summary
    print("\n" + "=" * 60)
    print("BENCHMARK RESULTS")
    print("=" * 60)
    print(f"Reviews tested: {summary.n_reviews}")
    print(f"Classifier: {classifier}")
    print(f"\nWSS@95:")
    print(f"  Mean: {summary.mean_wss95:.1%}")
    print(f"  Median: {summary.median_wss95:.1%}")
    print(f"\nRecall (RRF):")
    print(f"  Mean: {summary.mean_rrf:.1%}")
    print(f"\nStopping Accuracy:")
    print(f"  Correct (>=95% recall): {summary.correct_stopping_rate:.1%}")

    return summary


def save_results(summary: BenchmarkSummary, output_file: str):
    """Save benchmark results to CSV."""
    results_df = pd.DataFrame([
        {
            'review_id': r.review_id,
            'n_total': r.n_total,
            'n_included': r.n_included,
            'n_excluded': r.n_excluded,
            'wss_95': r.wss_95,
            'rrf': r.rrf,
            'recall_at_stop': r.recall_at_stop,
            'n_screened_at_stop': r.n_screened_at_stop,
            'correct_stopping': r.correct_stopping,
            'classifier': r.classifier
        }
        for r in summary.results
    ])

    results_df.to_csv(output_file, index=False)
    print(f"\nResults saved to: {output_file}")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    # Run benchmark on mega ground truth
    ground_truth = "C:/Users/user/asreview_MEGA_groundtruth.csv"

    if os.path.exists(ground_truth):
        # Quick test on first 50 reviews
        print("\n*** QUICK BENCHMARK (50 reviews) ***\n")
        summary = run_benchmark(ground_truth, n_reviews=50, classifier="svm")

        # Save results
        save_results(summary, "C:/Users/user/asreview_benchmark_results.csv")

        # Compare with SYNERGY reference
        synergy_ref = pd.read_csv("C:/Users/user/synergy_benchmark/synergy_reference.csv")

        print("\n" + "=" * 60)
        print("COMPARISON WITH SYNERGY BENCHMARK")
        print("=" * 60)
        print(f"\nPairwise70 (our benchmark):")
        print(f"  Mean WSS@95: {summary.mean_wss95:.1%}")
        print(f"  Mean RRF: {summary.mean_rrf:.1%}")
        print(f"\nSYNERGY reference:")
        print(f"  Datasets: {len(synergy_ref)}")
        print(f"  Total records: {synergy_ref['records'].sum():,}")
        print(f"  Mean prevalence: {synergy_ref['prevalence'].mean():.1f}%")
        print(f"  (SYNERGY WSS@95 benchmarks vary by dataset)")
    else:
        print(f"Ground truth file not found: {ground_truth}")
        print("Run build_mega_groundtruth.R first!")
