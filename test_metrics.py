from evaluation.metrics import (
    precision_at_k,
    recall_at_k
)


# Example:
# We retrieved 5 jobs.
# 4 of them are relevant.

relevant_results = 4
k = 5

precision = precision_at_k(
    relevant_results,
    k
)

print("Precision@5:")
print(f"{precision * 100:.2f}%")


# Suppose there are 8 relevant jobs
# in the dataset in total.

total_relevant_jobs = 8

recall = recall_at_k(
    relevant_results,
    total_relevant_jobs
)

print("\nRecall@5:")
print(f"{recall * 100:.2f}%")