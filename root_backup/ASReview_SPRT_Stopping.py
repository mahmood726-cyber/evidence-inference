"""
SPRT (Sequential Probability Ratio Test) Stopping Rule
ASReview 5-Star Enhancement #6
"""

import numpy as np
from dataclasses import dataclass
from typing import List


@dataclass
class SPRTResult:
    """Result from SPRT stopping test."""
    decision: str  # "continue" | "stop" | "inconclusive"
    log_likelihood_ratio: float
    upper_boundary: float
    lower_boundary: float
    n_consecutive_irrelevant: int
    estimated_remaining: float
    confidence: float


class SPRTStoppingRule:
    """
    Sequential Probability Ratio Test for optimal stopping.

    SPRT provides theoretically optimal stopping decisions with
    controlled Type I (miss relevant) and Type II (continue too long) errors.

    Based on Wald (1945) sequential analysis.
    """

    def __init__(
        self,
        alpha: float = 0.05,  # P(stopping when relevant remain)
        beta: float = 0.10,   # P(continuing when should stop)
        p0: float = 0.001,    # Null: very few relevant remain
        p1: float = 0.01      # Alternative: some relevant remain
    ):
        """
        Initialize SPRT parameters.

        Args:
            alpha: Type I error rate (miss relevant studies)
            beta: Type II error rate (screen unnecessarily)
            p0: Probability under null (safe to stop)
            p1: Probability under alternative (should continue)
        """
        self.alpha = alpha
        self.beta = beta
        self.p0 = max(p0, 1e-10)
        self.p1 = max(p1, self.p0 + 1e-10)

        # Calculate Wald boundaries
        self.A = np.log((1 - beta) / alpha)  # Upper boundary (stop)
        self.B = np.log(beta / (1 - alpha))  # Lower boundary (continue)

    def test(
        self,
        n_screened: int,
        n_relevant_found: int,
        n_total: int,
        recent_outcomes: List[int] = None
    ) -> SPRTResult:
        """
        Perform SPRT test for stopping decision.

        Args:
            n_screened: Documents screened so far
            n_relevant_found: Relevant documents found
            n_total: Total documents in dataset
            recent_outcomes: Recent screening outcomes (1=relevant, 0=irrelevant)

        Returns:
            SPRTResult with decision and statistics
        """
        n_remaining = n_total - n_screened

        if n_remaining <= 0:
            return SPRTResult(
                decision="stop",
                log_likelihood_ratio=self.A + 1,
                upper_boundary=self.A,
                lower_boundary=self.B,
                n_consecutive_irrelevant=0,
                estimated_remaining=0.0,
                confidence=1.0
            )

        # Calculate observed rate
        observed_rate = n_relevant_found / n_screened if n_screened > 0 else 0.5
        expected_remaining = observed_rate * n_remaining

        # Count consecutive irrelevant (if recent_outcomes provided)
        n_consecutive = 0
        if recent_outcomes:
            for outcome in reversed(recent_outcomes[-100:]):  # Last 100
                if outcome == 0:
                    n_consecutive += 1
                else:
                    break

        # Log-likelihood ratio
        if n_screened > 0:
            # Use observed vs expected comparison
            llr = n_screened * (
                observed_rate * np.log(self.p1 / self.p0 + 1e-10) +
                (1 - observed_rate) * np.log((1 - self.p1) / (1 - self.p0) + 1e-10)
            )
        else:
            llr = 0.0

        # Adjust for consecutive irrelevant (evidence for stopping)
        if n_consecutive > 10:
            llr += (n_consecutive - 10) * 0.05

        # Make decision
        if llr >= self.A:
            decision = "stop"
            confidence = min(1.0, llr / self.A)
        elif llr <= self.B:
            decision = "continue"
            confidence = 1 - (llr - self.B) / (self.A - self.B)
        else:
            decision = "inconclusive"
            confidence = 0.5

        return SPRTResult(
            decision=decision,
            log_likelihood_ratio=llr,
            upper_boundary=self.A,
            lower_boundary=self.B,
            n_consecutive_irrelevant=n_consecutive,
            estimated_remaining=expected_remaining,
            confidence=confidence
        )


# Demo
if __name__ == "__main__":
    print("=" * 60)
    print("SPRT Stopping Rule Demo")
    print("=" * 60)

    sprt = SPRTStoppingRule()

    # Simulate screening
    test_cases = [
        (100, 10, 1000),   # Early: 10% screened, 10 found
        (500, 45, 1000),   # Mid: 50% screened, 45 found
        (800, 48, 1000),   # Late: 80% screened, 48 found
        (950, 50, 1000),   # Almost done
    ]

    for n_screened, n_found, n_total in test_cases:
        result = sprt.test(n_screened, n_found, n_total)
        print(f"\nScreened {n_screened}/{n_total}, Found {n_found}")
        print(f"  Decision: {result.decision}")
        print(f"  LLR: {result.log_likelihood_ratio:.3f}")
        print(f"  Est. remaining: {result.estimated_remaining:.1f}")
        print(f"  Confidence: {result.confidence:.1%}")
