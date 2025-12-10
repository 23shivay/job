# 🚀 AI-Powered  Job Collector
### Automated Job & Internship Extraction for Training & Placement Cells  
**Built using Crawl4AI, Groq Llama-4 Scout, Async Crawling, and Structured LLM Extraction**

---

## 📌 Overview

This project automates the discovery of **fresh job and internship opportunities** from LinkedIn public activity feeds. It is specially optimized for **Training & Placement (TNP) cells**, enabling them to collect the latest opportunities for students (2025/2026/2027 batches) without manual effort.

The system crawls selected LinkedIn profiles, extracts job-related posts using an LLM-powered structured extraction engine, cleans & filters the data, and finally stores the results in a database.

The goal is to create a **fully automated pipeline** that fetches the top relevant opportunities posted in the last **24 hours**—focusing on internships & fresher job openings.

---

## 🧠 Why This Project?

TNP teams waste hours manually opening LinkedIn profiles and scrolling to find:
- Latest job openings  
- Internships  
- Opportunities for college batches  
- Posts with real apply links  

This project reduces the process to **one automated command**:


The system handles crawling + extraction + cleaning + storing — automatically.

---

## ⚙️ Key Features

### ✅ 1. Automated LinkedIn Profile Crawling  
Using **Crawl4AI’s AsyncWebCrawler** and a valid `li_at` cookie, the system:
- Opens public LinkedIn activity pages  
- Scrolls automatically to load posts  
- Captures the newest 2–3 posts per profile  

### ✅ 2. LLM-Based Structured Extraction (Groq Llama-4 Scout)  
Instead of regex or brittle text scraping, the system uses:
- **Groq’s high-speed Llama-4 Scout model**
- **LLMExtractionStrategy**  
- A **JSON schema** to extract:




This ensures reliable, clean, structured output.

### ✅ 3. Filters Only Recent & Relevant Posts  
The system keeps posts that:
- Are truly **job or internship related**
- Contain **apply links**
- Are **from the last 24 hours**
- Target eligible batches 2025/2026/2027

### ✅ 4. Data Cleaning Layer  
A custom cleaner:
- Removes empty or invalid posts  
- Normalizes summary tags  
- Ensures stipend/salary extraction  
- Removes noise fields  

### ✅ 5. Storage to Database  
Final cleaned posts are stored using:
You can plug in:
- MongoDB  
- PostgreSQL  
- Firebase  
- Supabase  
- Or any other DB of your choice

- 

## 🏗️ High-Level Architecture

LinkedIn Profiles
↓
Async Web Crawler (Headless Browser)
↓
LLM Structured Extraction (Groq Llama-4 Scout)
↓
JSON Output (Top 3 posts per profile)
↓
Filtering (Last 24 hours only)
↓
Data Cleaning Module
↓
Database Storage (save_jobs_to_db)
↓
Ready-to-use Job Feed

## 📂 Project Structure

project/
│
├── app.py # Main crawling & extraction pipeline
├── db/
│ └── curd.py # Save-to-database logic
├── .env # GROQ_API_KEY, li_at cookie
└── README.md



