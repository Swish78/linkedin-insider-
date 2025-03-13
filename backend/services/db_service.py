from pymongo import MongoClient
import os
import dotenv
from datetime import datetime
from ..models.linkedin_models import LinkedInPage, Post, Person

dotenv.load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "linkedin_data")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
pages_collection = db.pages
posts_collection = db.posts
people_collection = db.people


def save_page_data(data: LinkedInPage):
    page_dict = data.dict()
    page_dict["updated_at"] = datetime.now()

    posts = page_dict.pop("posts", [])
    employees = page_dict.pop("employees", [])

    pages_collection.update_one(
        {"id": data.id},
        {"$set": page_dict},
        upsert=True
    )

    for post in posts:
        post["page_id"] = data.id
        posts_collection.update_one(
            {"id": post["id"]},
            {"$set": post},
            upsert=True
        )

    for employee in employees:
        employee["company_id"] = data.id
        people_collection.update_one(
            {"id": employee["id"]},
            {"$set": employee},
            upsert=True
        )


def get_page_by_id(page_id: str):
    page = pages_collection.find_one({"id": page_id})
    if not page:
        return None

    posts = list(posts_collection.find({"page_id": page_id}).limit(15))
    page["posts"] = posts

    employees = list(people_collection.find({"company_id": page_id}))
    page["employees"] = employees

    return page


def get_filtered_pages(min_followers=None, max_followers=None, industry=None, skip=0, limit=10):
    query = {}
    if min_followers is not None and max_followers is not None:
        query["followers_count"] = {"$gte": min_followers, "$lte": max_followers}
    if industry:
        query["industry"] = {"$regex": industry, "$options": "i"}

    total = pages_collection.count_documents(query)
    pages = list(pages_collection.find(query).skip(skip).limit(limit))

    return {
        "total": total,
        "pages": pages,
        "skip": skip,
        "limit": limit
    }


def get_page_posts(page_id: str, skip=0, limit=10):
    total = posts_collection.count_documents({"page_id": page_id})
    posts = list(posts_collection.find({"page_id": page_id}).skip(skip).limit(limit))

    return {
        "total": total,
        "posts": posts,
        "skip": skip,
        "limit": limit
    }
