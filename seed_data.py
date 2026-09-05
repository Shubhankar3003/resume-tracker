import requests

BASE_URL = "http://127.0.0.1:8000/api/resumes/upload"

# Test candidate profiles with varying skillsets, locations, and experience
candidates = [
    {
        "name": "Amit Sharma",
        "email": "amit.sharma@example.com",
        "designation": "Senior Node.js Developer",
        "experience_years": 6.0,
        "skills": "Node.js, Express, AWS Lambda, MongoDB, Docker, Microservices",
        "location": "Mumbai",
        "education": "B.E. Computer Engineering, University of Mumbai",
        "status": "Applied",
        "resume_text": "Senior Backend Engineer with 6 years experience specializing in Node.js, Express, MongoDB Atlas, and AWS cloud infrastructure. Built high-scale microservices and event-driven architectures."
    },
    {
        "name": "Rohan Deshmukh",
        "email": "rohan.d@example.com",
        "designation": "Backend Software Engineer",
        "experience_years": 4.5,
        "skills": "Node.js, MongoDB, Redis, Google Cloud",
        "location": "Mumbai",
        "education": "B.Tech Information Technology, VJTI",
        "status": "Screening",
        "resume_text": "Software developer focused on Node.js and MongoDB database design. 4+ years creating REST APIs and message queues."
    },
    {
        "name": "Pooja Verma",
        "email": "pooja.v@example.com",
        "designation": "Lead Full Stack Developer",
        "experience_years": 7.0,
        "skills": "React, Node.js, AWS EC2, DynamoDB, PostgreSQL",
        "location": "Bengaluru",
        "education": "M.Tech Software Engineering, BITS",
        "status": "Applied",
        "resume_text": "Lead Engineer architecting full-stack web platforms. Extensive AWS knowledge, Node.js backend services, and distributed database tuning."
    },
    {
        "name": "Karan Malhotra",
        "email": "karan.m@example.com",
        "designation": "Junior Python Developer",
        "experience_years": 1.5,
        "skills": "Python, Django, PostgreSQL",
        "location": "Delhi",
        "education": "B.Sc Computer Science, DU",
        "status": "Applied",
        "resume_text": "Junior developer specializing in Python scripting and Django web development."
    }
]

# Sends multipart form upload requests to the local API
for c in candidates:
    files = {"file": (f"{c['name'].replace(' ', '_')}.txt", c["resume_text"].encode(), "text/plain")}
    data = {k: v for k, v in c.items() if k != "resume_text"}
    res = requests.post(BASE_URL, data=data, files=files)
    print(f"Added {c['name']}: {res.status_code}")