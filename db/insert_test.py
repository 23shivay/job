import sys
import os

# Add the 'db' directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'db'))

from db.curd import save_jobs_to_db

jobs_to_test = [
   {
    "apply_link": "https://lnkd.in/gFJE_gXW",
    "eligibility": "B.Tech",
    "company_name": "Strategy",
    "stipend/salary": "",
    "job_title": "Associate Software Engineer",
    "location": "Chennai",
    "timestamp": "23 hours ago",
    "post_summary": "Fresher Opening"
  }
]



if __name__ == "__main__":
    print("Starting job data insertion test...")
    save_jobs_to_db(jobs_to_test)
    print("Test finished. Check your database for the new entries.")