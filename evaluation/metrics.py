def precision_at_k(relevant_results, k):
    """
    Calculate Precision@K.

    Precision@K = Relevant Retrieved Jobs / K
    """

    if k == 0:
        return 0.0

    return relevant_results / k


def recall_at_k(relevant_results, total_relevant_jobs):
    """
    Calculate Recall@K.

    Recall@K = Relevant Retrieved Jobs /
               Total Relevant Jobs
    """

    if total_relevant_jobs == 0:
        return 0.0

    return relevant_results / total_relevant_jobs


def percentage(value):
    """
    Convert a decimal metric into a percentage.
    """

    return round(value * 100, 2)


def print_metrics(
    relevant_results,
    k,
    total_relevant_jobs
):
    """
    Print Precision@K and Recall@K.
    """

    precision = precision_at_k(
        relevant_results,
        k
    )

    recall = recall_at_k(
        relevant_results,
        total_relevant_jobs
    )

    print("\nEvaluation Metrics:")
    print("-------------------")

    print(
        f"Precision@{k}: "
        f"{percentage(precision):.2f}%"
    )

    print(
        f"Recall@{k}: "
        f"{percentage(recall):.2f}%"
    )

    return precision, recall