#!/usr/bin/env python3
"""
Example 1: Core System One Decision Primitives
Demonstrates Choice, Score, and Noul evaluations in sub-100ms.
"""

from system1.bridge import evaluate_state, ChoiceQuestion, ScoreQuestion, NoulQuestion

def main():
    state = "Our caching layer latency spiked from 2ms to 450ms following the v2.4.1 release."

    questions = {
        "severity": ScoreQuestion(
            instructions="Rate the incident severity.",
            criteria=[
                "Negligible impact",
                "Moderate performance degradation",
                "Critical customer-facing degradation"
            ]
        ),
        "primary_suspect": ChoiceQuestion(
            instructions="What is the most likely root cause?",
            criteria={
                "memory_leak": "Redis node running out of RAM and swapping",
                "unindexed_query": "New database query causing sequential scans",
                "network_congestion": "Bandwidth saturation between app and cache",
                "configuration_drift": "Cache eviction policy misconfigured"
            }
        ),
        "requires_rollback": NoulQuestion(
            instructions="Should we initiate an immediate hotfix rollback?"
        )
    }

    print("Evaluating state with System One...")
    result = evaluate_state(state, questions)
    answers = result.get("answers", {})

    print(f"Severity Score:     {answers['severity']['score']:.2f} / 2.0")
    print(f"Primary Suspect:    {answers['primary_suspect']['choice']} (Conf: {answers['primary_suspect']['confidence']*100:.1f}%)")
    print(f"Requires Rollback:  {answers['requires_rollback']['noul'] >= 0.5} (Prob: {answers['requires_rollback']['noul']:.2f})")

if __name__ == "__main__":
    main()
