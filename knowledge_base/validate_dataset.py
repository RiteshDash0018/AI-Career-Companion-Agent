import json
import os
from collections import Counter

# ============================================================
# CONFIGURATION
# ============================================================

DATASET_FILE = "data/jobs.json"

# Standard schema for Milestone 2.1
REQUIRED_FIELDS = [
    "job_id",
    "job_title",
    "company",
    "location",
    "job_type",
    "job_description",
    "responsibilities",
    "required_skills",
    "preferred_skills",
    "qualification",
    "experience_requirements",
    "education_requirements"
]

# Fields that must contain text
STRING_FIELDS = [
    "job_id",
    "job_title",
    "company",
    "location",
    "job_type",
    "job_description",
    "qualification",
    "experience_requirements",
    "education_requirements"
]

# Fields that must contain lists
LIST_FIELDS = [
    "responsibilities",
    "required_skills",
    "preferred_skills"
]


# ============================================================
# LOAD DATASET
# ============================================================

def load_dataset(filename):
    print("=" * 60)
    print("LOADING DATASET")
    print("=" * 60)

    if not os.path.exists(filename):
        print(f"ERROR: Dataset file not found: {filename}")
        return None

    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        print(f"Dataset loaded successfully.")
        print(f"Number of records: {len(data)}")

        return data

    except json.JSONDecodeError as e:
        print("ERROR: Invalid JSON format.")
        print(f"Details: {e}")
        return None

    except Exception as e:
        print(f"ERROR while reading dataset: {e}")
        return None


# ============================================================
# VALIDATE RECORD COUNT
# ============================================================

def validate_record_count(data):
    print("\n" + "=" * 60)
    print("1. RECORD COUNT VALIDATION")
    print("=" * 60)

    count = len(data)

    print(f"Total records: {count}")

    if 150 <= count <= 200:
        print("PASS: Dataset contains between 150 and 200 records.")
        return True
    else:
        print("FAIL: Dataset should contain between 150 and 200 records.")
        return False


# ============================================================
# VALIDATE REQUIRED FIELDS
# ============================================================

def validate_required_fields(data):
    print("\n" + "=" * 60)
    print("2. REQUIRED FIELD VALIDATION")
    print("=" * 60)

    errors = []

    for index, job in enumerate(data, start=1):

        if not isinstance(job, dict):
            errors.append(
                f"Record {index}: Record is not a JSON object."
            )
            continue

        # Check missing fields
        missing_fields = [
            field for field in REQUIRED_FIELDS
            if field not in job
        ]

        if missing_fields:
            errors.append(
                f"Record {index}: Missing fields: {missing_fields}"
            )

    if not errors:
        print("PASS: All records contain all required fields.")
        return True

    print("FAIL: Missing fields found.")

    for error in errors[:20]:
        print(" -", error)

    if len(errors) > 20:
        print(f"... and {len(errors) - 20} more errors.")

    return False


# ============================================================
# VALIDATE EMPTY VALUES
# ============================================================

def validate_empty_values(data):
    print("\n" + "=" * 60)
    print("3. EMPTY VALUE VALIDATION")
    print("=" * 60)

    errors = []

    for index, job in enumerate(data, start=1):

        for field in REQUIRED_FIELDS:

            if field not in job:
                continue

            value = job[field]

            # Check empty strings
            if isinstance(value, str):
                if not value.strip():
                    errors.append(
                        f"Record {index} ({job.get('job_id', 'UNKNOWN')}): "
                        f"'{field}' is empty."
                    )

            # Check empty lists
            elif isinstance(value, list):
                if len(value) == 0:
                    errors.append(
                        f"Record {index} ({job.get('job_id', 'UNKNOWN')}): "
                        f"'{field}' is an empty list."
                    )

            # Check None
            elif value is None:
                errors.append(
                    f"Record {index} ({job.get('job_id', 'UNKNOWN')}): "
                    f"'{field}' is None."
                )

    if not errors:
        print("PASS: No empty required fields found.")
        return True

    print(f"FAIL: Found {len(errors)} empty values.")

    for error in errors[:20]:
        print(" -", error)

    if len(errors) > 20:
        print(f"... and {len(errors) - 20} more errors.")

    return False


# ============================================================
# VALIDATE DATA TYPES
# ============================================================

def validate_data_types(data):
    print("\n" + "=" * 60)
    print("4. DATA TYPE VALIDATION")
    print("=" * 60)

    errors = []

    for index, job in enumerate(data, start=1):

        job_id = job.get("job_id", "UNKNOWN")

        # String fields
        for field in STRING_FIELDS:

            if field in job and not isinstance(job[field], str):
                errors.append(
                    f"Record {index} ({job_id}): "
                    f"'{field}' should be a string."
                )

        # List fields
        for field in LIST_FIELDS:

            if field in job and not isinstance(job[field], list):
                errors.append(
                    f"Record {index} ({job_id}): "
                    f"'{field}' should be a list."
                )

            # Check list elements
            elif field in job:

                for item in job[field]:

                    if not isinstance(item, str):
                        errors.append(
                            f"Record {index} ({job_id}): "
                            f"'{field}' contains a non-string value."
                        )

    if not errors:
        print("PASS: All fields have correct data types.")
        return True

    print(f"FAIL: Found {len(errors)} data type errors.")

    for error in errors[:20]:
        print(" -", error)

    if len(errors) > 20:
        print(f"... and {len(errors) - 20} more errors.")

    return False


# ============================================================
# VALIDATE DUPLICATE JOB IDS
# ============================================================

def validate_duplicate_ids(data):
    print("\n" + "=" * 60)
    print("5. DUPLICATE JOB ID VALIDATION")
    print("=" * 60)

    job_ids = []

    for job in data:
        if isinstance(job, dict):
            job_ids.append(job.get("job_id"))

    counter = Counter(job_ids)

    duplicates = {
        job_id: count
        for job_id, count in counter.items()
        if count > 1
    }

    if not duplicates:
        print("PASS: No duplicate job IDs found.")
        return True

    print("FAIL: Duplicate job IDs found.")

    for job_id, count in duplicates.items():
        print(f" - {job_id}: appears {count} times")

    return False


# ============================================================
# VALIDATE JOB ID FORMAT
# ============================================================

def validate_job_id_format(data):
    print("\n" + "=" * 60)
    print("6. JOB ID FORMAT VALIDATION")
    print("=" * 60)

    errors = []

    for index, job in enumerate(data, start=1):

        job_id = job.get("job_id")

        if not isinstance(job_id, str):
            errors.append(
                f"Record {index}: job_id is not a string."
            )
            continue

        if not job_id.startswith("JOB"):
            errors.append(
                f"Record {index}: Invalid job_id format: {job_id}"
            )

    if not errors:
        print("PASS: All job IDs use the expected JOB format.")
        return True

    print("FAIL: Invalid job ID format found.")

    for error in errors[:20]:
        print(" -", error)

    return False


# ============================================================
# CHECK SKILL QUALITY
# ============================================================

def validate_skills(data):
    print("\n" + "=" * 60)
    print("7. SKILLS VALIDATION")
    print("=" * 60)

    errors = []

    for index, job in enumerate(data, start=1):

        job_id = job.get("job_id", "UNKNOWN")

        required = job.get("required_skills", [])
        preferred = job.get("preferred_skills", [])

        if len(required) == 0:
            errors.append(
                f"{job_id}: No required skills."
            )

        if len(preferred) == 0:
            errors.append(
                f"{job_id}: No preferred skills."
            )

    if not errors:
        print("PASS: All jobs contain required and preferred skills.")
        return True

    print(f"FAIL: Found {len(errors)} skill issues.")

    for error in errors[:20]:
        print(" -", error)

    return False


# ============================================================
# CHECK REQUIRED JOB INFORMATION
# ============================================================

def validate_job_information(data):
    print("\n" + "=" * 60)
    print("8. JOB INFORMATION VALIDATION")
    print("=" * 60)

    errors = []

    for index, job in enumerate(data, start=1):

        job_id = job.get("job_id", "UNKNOWN")

        if not job.get("job_title"):
            errors.append(f"{job_id}: Missing job title.")

        if not job.get("company"):
            errors.append(f"{job_id}: Missing company.")

        if not job.get("location"):
            errors.append(f"{job_id}: Missing location.")

        if not job.get("job_description"):
            errors.append(f"{job_id}: Missing job description.")

        if not job.get("qualification"):
            errors.append(f"{job_id}: Missing qualification.")

        if not job.get("experience_requirements"):
            errors.append(
                f"{job_id}: Missing experience requirements."
            )

        if not job.get("education_requirements"):
            errors.append(
                f"{job_id}: Missing education requirements."
            )

    if not errors:
        print("PASS: All jobs contain the important job information.")
        return True

    print(f"FAIL: Found {len(errors)} job information issues.")

    for error in errors[:20]:
        print(" -", error)

    return False


# ============================================================
# DISPLAY DATASET SUMMARY
# ============================================================

def display_summary(data):
    print("\n" + "=" * 60)
    print("9. DATASET SUMMARY")
    print("=" * 60)

    titles = Counter(
        job.get("job_title")
        for job in data
        if isinstance(job, dict)
    )

    locations = Counter(
        job.get("location")
        for job in data
        if isinstance(job, dict)
    )

    job_types = Counter(
        job.get("job_type")
        for job in data
        if isinstance(job, dict)
    )

    print(f"Total job postings : {len(data)}")
    print(f"Unique job IDs     : {len(set(job.get('job_id') for job in data))}")
    print(f"Unique job titles  : {len(titles)}")
    print(f"Unique locations   : {len(locations)}")
    print(f"Job types          : {len(job_types)}")

    print("\nJob titles:")
    for title, count in titles.items():
        print(f"  {title}: {count}")

    print("\nJob types:")
    for job_type, count in job_types.items():
        print(f"  {job_type}: {count}")


# ============================================================
# MAIN VALIDATION FUNCTION
# ============================================================

def main():

    print("\n")
    print("=" * 60)
    print("INTERNSHIP DATASET VALIDATOR")
    print("Milestone 2.1 - Internship Knowledge Base")
    print("=" * 60)

    data = load_dataset(DATASET_FILE)

    if data is None:
        print("\nValidation stopped because the dataset could not be loaded.")
        return

    if not isinstance(data, list):
        print("\nFAIL: Dataset root must be a JSON list.")
        return

    # Run all validations
    results = []

    results.append(validate_record_count(data))
    results.append(validate_required_fields(data))
    results.append(validate_empty_values(data))
    results.append(validate_data_types(data))
    results.append(validate_duplicate_ids(data))
    results.append(validate_job_id_format(data))
    results.append(validate_skills(data))
    results.append(validate_job_information(data))

    display_summary(data)

    # ========================================================
    # FINAL RESULT
    # ========================================================

    print("\n" + "=" * 60)
    print("FINAL VALIDATION RESULT")
    print("=" * 60)

    passed = sum(results)
    total = len(results)

    print(f"Checks passed: {passed}/{total}")

    if all(results):
        print("\nSUCCESS!")
        print("The internship dataset passed all validation checks.")
        print("The dataset is ready for Milestone 2.1.")
    else:
        print("\nWARNING!")
        print("Some validation checks failed.")
        print("Please review the errors above before continuing.")

    print("=" * 60)


# ============================================================
# RUN PROGRAM
# ============================================================

if __name__ == "__main__":
    main()