import asyncio
import re
from crawl4ai import AsyncWebCrawler
from ..models.linkedin_models import LinkedInPage, Person
from groq import Groq
import aiohttp
from ..services.s3_service import upload_image_to_s3, get_image_url
import os
import dotenv

dotenv.load_dotenv()
api_key = os.getenv("GROQ_API_KEY")


async def download_image(url: str) -> bytes | None:
    if not url:
        return None
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.read()
        except Exception:
            return None
    return None


async def generate_company_insights(data: dict) -> str:
    client = Groq(api_key=api_key)
    prompt = f"""Analyze this company information and provide concise, valuable insights about their market position, growth potential, and industry impact:
    Company: {data['name']}
    Industry: {data['industry']}
    Description: {data['description']}
    Followers: {data['followers_count']}
    Employee Count: {data['employee_count']}
    Specialties: {', '.join(data['specialities'])}
    """

    completion = client.chat.completions.create(
        model="llama-3.2-3b-preview",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_completion_tokens=1024,
        top_p=1,
        stream=False,
        stop=None
    )
    return completion.choices[0].message.content


async def scrape_company_info(pid: str):
    url = f"https://www.linkedin.com/company/{pid}"
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url)
        md_text = result.markdown.raw_markdown

        def extract(pattern, text, default="N/A", flags=0):
            match = re.search(pattern, text, flags)
            return match.group(1).strip() if match else default

        name = extract(r"#\s+(.*?)\s*\n", md_text)
        pic = extract(r"!\[(?!.*cover).*?\]\((https://media\.licdn\.com/dms/image/[^)]+)\)", md_text)
        desc = extract(r"##\s+About us\s+(.*?)\s*Website", md_text, flags=re.DOTALL)
        web = extract(r"\[\s*(https://[^\]]+)\s*\]\(", md_text)
        ind = extract(r"Industry\s+([^\n]+)", md_text)
        followers = int(extract(r"(\d[\d,]*)\s+followers", md_text, "0").replace(",", ""))
        count = extract(r"Company size\s+([^\n]+)", md_text)
        specs = [s.strip() for s in extract(r"Specialties\s+([^\n]+)", md_text, "").split(",") if s.strip()]

        pic_bytes = await download_image(pic)
        pic_s3 = await upload_image_to_s3(pic_bytes) if pic_bytes else None

        emps = []
        emp_matches = re.findall(r"### \[ ([^\]]+) \]", md_text)
        for emp_name in emp_matches[:4]:
            emps.append(Person(
                id=f"{emp_name.lower().replace(' ', '-')}-{pid}",
                name=emp_name,
                title=extract(f"{re.escape(emp_name)}\s+([^\n]+)", md_text, "Unknown"),
                company_id=pid
            ))

        data = {
            "name": name,
            "industry": ind,
            "description": desc,
            "followers_count": followers,
            "employee_count": int(count.split('-')[0].replace("+", "").replace(",", "")) if count != "N/A" else None,
            "specialities": specs
        }

        insights = await generate_company_insights(data)

        page = LinkedInPage(
            id=pid,
            name=name,
            url=url,
            profile_picture_url=await get_image_url(pic_s3) if pic_s3 else None,
            description=desc,
            website=web,
            industry=ind,
            followers_count=followers,
            employee_count=int(count.split('-')[0].replace("+", "").replace(",", "")) if count != "N/A" else None,
            specialities=specs,
            employees=emps,
            ai_insights=insights
        )

        return page

asyncio.run(scrape_company_info("deepsolv"))
