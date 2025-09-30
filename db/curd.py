from sqlalchemy.dialects.postgresql import insert
from .database import SessionLocal, engine
from .models import Base, JobPost
from sqlalchemy import or_, and_



def save_jobs_to_db(jobs):
    session = SessionLocal()
    
    try:
        inserted_count = 0
        skipped_count = 0
        skipped_jobs = []
        
        for job_data in jobs:
            # Extract required fields
            apply_link = job_data.get('apply_link')
            company_name = job_data.get('company_name')
            job_title = job_data.get('job_title')
            
            # Skip if missing required fields
            if not apply_link or not company_name:
                skipped_count += 1
                skipped_jobs.append({
                    'job': job_data,
                    'reason': 'Missing required fields (apply_link or company_name)'
                })
                continue
            
            # Check for duplicates
            duplicate_conditions = [
                # Case 1: Same apply_link exists
                JobPost.apply_link == apply_link
            ]
            
            # Case 2: Same company_name AND job_title (only if job_title is not None)
            if job_title is not None:
                duplicate_conditions.append(
                    and_(
                        JobPost.company_name == company_name,
                        JobPost.job_title == job_title
                    )
                )
            
            # Query for existing duplicates
            existing_job = session.query(JobPost).filter(
                or_(*duplicate_conditions)
            ).first()
            
            if existing_job:
                skipped_count += 1
                # Determine which condition matched
                if existing_job.apply_link == apply_link:
                    reason = f'Duplicate apply_link: {apply_link}'
                else:
                    reason = f'Duplicate company_name and job_title: {company_name} - {job_title}'
                
                skipped_jobs.append({
                    'job': job_data,
                    'reason': reason
                })
                continue
            
            # Create new JobPost instance
            new_job = JobPost(
                job_title=job_data.get('job_title'),
                company_name=company_name,
                location=job_data.get('location'),
                eligibility=job_data.get('eligibility'),
                stipend_salary=job_data.get('stipend'),  # Maps to stipend_salary field
                post_summary=job_data.get('post_summary'),
                apply_link=apply_link,
                timestamp=job_data.get('timestamp')
            )
            
            # Add to session
            session.add(new_job)
            inserted_count += 1
        
        # Commit all changes
        session.commit()
        
        return {
            'total_processed': len(jobs),
            'inserted': inserted_count,
            'skipped': skipped_count,
            'skipped_details': skipped_jobs
        }
        
    except Exception as e:
        session.rollback()
        raise Exception(f"Error saving jobs to database: {str(e)}")
    
    finally:
        session.close()

# def save_jobs_to_db(jobs):
#     session = SessionLocal()
#     try:
#         inserted_count = 0
#         skipped_count = 0
#         skipped_jobs = []

#         # --- Track duplicates within this batch ---
#         seen_links = set()
#         seen_pairs = set()  # (company_name, job_title)

#         for job_data in jobs:
#             # --- Normalize values ---
#             apply_link = job_data.get('apply_link')
#             company_name = job_data.get('company_name')
#             job_title = job_data.get('job_title')

#             if apply_link:
#                 apply_link = apply_link.strip().lower()
#             if company_name:
#                 company_name = company_name.strip().lower()
#             if job_title:
#                 job_title = job_title.strip().lower()

#             # --- Skip if missing required fields ---
#             if not apply_link or not company_name:
#                 skipped_count += 1
#                 skipped_jobs.append({
#                     'job': job_data,
#                     'reason': 'Missing required fields (apply_link or company_name)'
#                 })
#                 continue

#             # --- Check duplicates within current batch ---
#             if apply_link in seen_links or (company_name, job_title) in seen_pairs:
#                 skipped_count += 1
#                 skipped_jobs.append({
#                     'job': job_data,
#                     'reason': 'Duplicate in current batch'
#                 })
#                 continue

#             # --- Check duplicates already in DB ---
#             existing_job = session.query(JobPost).filter(
#                 or_(
#                     JobPost.apply_link == apply_link,
#                     and_(
#                         JobPost.company_name == company_name,
#                         JobPost.job_title == job_title
#                     )
#                 )
#             ).first()

#             if existing_job:
#                 skipped_count += 1
#                 skipped_jobs.append({
#                     'job': job_data,
#                     'reason': 'Duplicate already in DB'
#                 })
#                 continue

#             # --- Add new job ---
#             new_job = JobPost(
#                 job_title=job_title,
#                 company_name=company_name,
#                 location=job_data.get('location'),
#                 eligibility=job_data.get('eligibility'),
#                 stipend_salary=job_data.get('stipend'),
#                 post_summary=job_data.get('post_summary'),
#                 apply_link=apply_link,
#                 timestamp=job_data.get('timestamp')
#             )

#             session.add(new_job)
#             inserted_count += 1

#             # --- Track in-memory to prevent duplicates in same batch ---
#             seen_links.add(apply_link)
#             if job_title:
#                 seen_pairs.add((company_name, job_title))

#         # --- Commit all valid inserts ---
#         session.commit()

#         return {
#             'total_processed': len(jobs),
#             'inserted': inserted_count,
#             'skipped': skipped_count,
#             'skipped_details': skipped_jobs
#         }

#     except Exception as e:
#         session.rollback()
#         raise Exception(f"Error saving jobs to database: {str(e)}")
#     finally:
#         session.close()


