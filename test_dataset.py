import json

with open("data/jobs.json", "r", encoding="utf-8") as file:
    jobs = json.load(file)

print("Total job postings:", len(jobs))

print("\nFirst job:")
print(jobs[0])