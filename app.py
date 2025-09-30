import asyncio
import json
from typing import List
from crawl4ai import AsyncWebCrawler, LLMExtractionStrategy, LLMConfig, CrawlerRunConfig, BrowserConfig, CrawlResult
from dotenv import load_dotenv
import os
from db.curd import save_jobs_to_db

# Load .env variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
li_at_cookie=os.getenv("li_at_cookie")
print("GROQ_API_KEY loaded:", bool(GROQ_API_KEY))
print("GROQ_API_KEY loaded:", bool(li_at_cookie))


# --- Function to crawl and extract LinkedIn job posts ---
async def demo_llm_structured_extraction_recent_posts_improved():
    

    extraction_strategy = LLMExtractionStrategy(
        llm_config=LLMConfig(
            provider="groq/meta-llama/llama-4-scout-17b-16e-instruct",
            api_token="env:GROQ_API_KEY",
        ),
        instruction="""
        You are acting as a Training & Placement (TNP) cell assistant.
        Extract only the top 3 most recent posts about jobs, internships, or fresher openings (0–1 years).
        Target eligibility batches: 2025, 2026, 2027.
        Only include posts within last 24 hours.
        Ensure 'apply_link' is present; otherwise ignore the post.
        Extract stipend if mentioned in description.
        In post_summary, tag only as 'Internship' or 'Fresher Opening'.
        Return JSON in newest → oldest order.
        """,
        extract_type="schema",
        schema="""[{
            "apply_link": "string or leave it empty blank",
            "eligibility": "string or leave it empty blank",
            "company_name": "string or leave it empty blank",
            "stipend/salary": "string or leave it empty blank",
            "job_title": "string or leave it empty blank",
            "location": "string or leave it empty blank",
            "timestamp": "string or leave it empty blank",
            "post_summary": "string or leave it empty blank"
        }]""",
        extra_args={"temperature": 0.1, "max_tokens": 2048},
        verbose=True,
    )

    browser_config = BrowserConfig(
        headless=False,
        cookies=[
            {
                "name": "li_at",
                "value": li_at_cookie,
                "domain": ".linkedin.com",
                "path": "/",
                "httpOnly": True,
                "secure": True,
            }
        ],
        viewport={"width": 1920, "height": 1080},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    )

    config = CrawlerRunConfig(
        extraction_strategy=extraction_strategy,
        wait_for="css:.feed-shared-update-v2, .update-components-text",
        wait_for_timeout=30000,  # 30s timeout
        delay_before_return_html=5.0,
        js_code=[
            "window.scrollTo(0, 500);",
            "await new Promise(resolve => setTimeout(resolve, 1500));",
            "window.scrollTo(0, 1000);",
            "await new Promise(resolve => setTimeout(resolve, 1500));",
            "window.scrollTo(0, 0);",
            "await new Promise(resolve => setTimeout(resolve, 1000));",
        ],
        css_selector=".feed-shared-update-v2:nth-of-type(-n+3), .update-components-text:nth-of-type(-n+3)",
        exclude_external_links=False,
        exclude_external_images=True,
    )

    urls = [
        #"https://www.linkedin.com/in/raunakyadush/recent-activity/all/",
        #  "https://www.linkedin.com/in/rohangoyal16/recent-activity/all/",
        #  "https://www.linkedin.com/in/venkattramana/recent-activity/all/",
        #  "https://www.linkedin.com/in/srishti-76a658277/recent-activity/all/",
         
        #  ##"https://www.linkedin.com/in/riyasha-jaiswal-765071199/recent-activity/all/",
          "https://www.linkedin.com/in/riya-dubey2000/recent-activity/all/",
          "https://www.linkedin.com/in/shubhamaa064/recent-activity/all/",
          "https://www.linkedin.com/in/krishan-kumar08/recent-activity/all/",
          "https://www.linkedin.com/in/rjritikjain/recent-activity/all/"

    ]

    async with AsyncWebCrawler(config=browser_config) as crawler:
        results: List[CrawlResult] = await crawler.arun_many(urls=urls, config=config)

    all_posts = []

    for i, result in enumerate(results, 1):
        profile_name = (
            result.url.split("/in/")[1].split("/")[0]
            if "/in/" in result.url
            else f"Profile_{i}"
        )
        print(f"\n📋 ANALYZING PROFILE: {profile_name}")
        print(f"URL: {result.url}")
        print(f"Status: {'✅ Success' if result.success else '❌ Failed'}")
        print("-" * 60)

        if not result.success or not result.extracted_content:
            continue

        try:
            data = json.loads(result.extracted_content)
            if isinstance(data, list) and len(data) > 0:
                for post in data:
                    all_posts.append(post)
        except json.JSONDecodeError:
            pass  # ignore errors

    # --- Filter only posts within last 24 hours ---
    def is_recent(timestamp: str) -> bool:
        if not timestamp:
            return False
        ts = timestamp.lower().strip()
        if "d ago" in ts or "day" in ts:
            return False
        return any(x in ts for x in ["h ago", "hour", "hours", "min", "minutes"])

    recent_posts = [p for p in all_posts if is_recent(p.get("timestamp", ""))]

    return recent_posts


def clean_posts(posts):
    cleaned = []
    for p in posts:
        # Skip invalid posts
        if not p.get("apply_link") or not p.get("company_name"):
            continue  

        # Tag post_summary
        summary_text = (p.get("post_summary") or "").lower()
        if "intern" in summary_text:
            p["post_summary"] = "Internship"
        else:
            p["post_summary"] = "Fresher Opening"

        # Ensure stipend is captured if mentioned in description
        if not p.get("stipend") and any(word in summary_text for word in ["stipend", "salary", "ctc", "lpa", "lakhs", "package"]):
            p["stipend"] = p.get("post_summary", "")  # crude fallback

        # Remove unwanted keys
        p.pop("error", None)
        p.pop("source_profile", None)

        cleaned.append(p)
    return cleaned


# --- Entry point ---
if __name__ == "__main__":
    all_posts = asyncio.run(demo_llm_structured_extraction_recent_posts_improved())
    cleaned_posts = clean_posts(all_posts)
    
    print(json.dumps(cleaned_posts, indent=2))
    save_jobs_to_db(cleaned_posts)
    print("data saved")

