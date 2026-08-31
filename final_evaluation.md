
# Final Model Evaluation & Comparison

## Regression (Predicting Rating)
Best model: Random Forest, constrained (max_depth=8, min_samples_leaf=20) - R² = 0.0955
- Outperformed both Linear Regression and an unconstrained Random Forest (which overfit
  badly and produced negative R² on test data).
- Overall predictive power is modest across all approaches tried, indicating that
  demographic/attraction-type features alone explain only a small portion of what
  drives individual satisfaction ratings.

## Classification (Predicting Visit Mode)
Best model: Random Forest with class_weight='balanced' - 31% accuracy
- A second, unbalanced version reached 47% accuracy but completely failed to identify
  rare classes (Business, Solo) - 0% recall on both.
- Chose the balanced model as final, prioritizing the project's core goal (segmenting
  ALL traveler types for targeted marketing) over raw accuracy.
- This reflects a deliberate accuracy-vs-fairness trade-off, not a modeling failure.

## Recommendation System
Two complementary systems were built:
- Collaborative Filtering (item-based): works only for the 30 attractions with rating
  history, but leverages real user behavior patterns.
- Content-Based Filtering: covers the full 1,698-attraction catalog using attraction
  type, filling the gap collaborative filtering can't reach.
- Together, they provide full-catalog coverage while still using behavioral data
  where it's available - a practical hybrid approach for a growing platform.

## Overall Conclusion
All three tasks (regression, classification, recommendation) are inherently limited by
the available features - individual taste, group composition, and detailed booking
context aren't captured in this dataset. Given these constraints, the final models
represent well-reasoned, defensible choices with explicitly documented trade-offs
rather than "best possible" performance in absolute terms.
