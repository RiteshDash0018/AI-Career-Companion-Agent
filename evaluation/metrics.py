def precision_at_k(relevant_results, k):
    """
    Calculate Precision@K.

    relevant_results:
        Number of relevant jobs retrieved.

    k:
        Number of jobs retrieved.
    """

    if k == 0:
        return 0.0

    return relevant_results / k


def recall_at_k(relevant_results, total_relevant_jobs):
    """
    Calculate Recall@K.

    relevant_results:
        Number of relevant jobs retrieved.

    total_relevant_jobs:
        Total number of relevant jobs available
        in the dataset.
    """

    if total_relevant_jobs == 0:
        return 0.0

    return relevant_results / total_relevant_jobs