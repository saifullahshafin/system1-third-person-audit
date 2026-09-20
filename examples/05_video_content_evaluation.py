#!/usr/bin/env python3
"""
Example 5: Video & Long-Form Content Signal Evaluation
Evaluates video transcripts or marketing copy in 80ms using TypeSafe Jev.
"""

from system1.evaluator import evaluate_video_transcript

SAMPLE_TRANSCRIPT = """
In this video, I walk through our exact automated client acquisition architecture.
Instead of sending manual cold emails, we use a headless crawler that monitors job boards
for companies hiring remote software engineers, extracts the hiring manager via LinkedIn,
and drafts personalized video audit briefs in under 60 seconds.
This system generated $42,000 in agency retainer contracts in the last 90 days.
"""

def main():
    print("Evaluating video transcript with System One...")
    res = evaluate_video_transcript(SAMPLE_TRANSCRIPT, title="Automated Client Acquisition Architecture")

    print(f"Signal-to-Noise Score:    {res['signal_score']:.2f} / 2.0")
    print(f"High Signal:              {res['is_high_signal']}")
    print(f"Content Pillar:           {res['content_pillar']}")
    print(f"Monetizable Opportunity:  {res['is_monetizable']}")

if __name__ == "__main__":
    main()
