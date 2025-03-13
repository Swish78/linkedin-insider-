import asyncio
import re
from crawl4ai import AsyncWebCrawler
from datetime import datetime
from ..models.linkedin_models import Post


async def scrape_company_posts(page_id: str):
    url = f"https://www.linkedin.com/company/{page_id}/posts"
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url)
        markdown_text = result.markdown.raw_markdown

        markdown_text = re.split(r"##\s*Join now to see what you are missing", markdown_text)[0]
        posts = re.split(r"\[ Report this post \].*?\)", markdown_text)
        posts = [post.strip() for post in posts if post.strip()][2:17]

        POSTS = []
        for post in posts:
            post = re.sub(r"https?://\S+", "", post)
            post = re.sub(r"\[.*?\]\(.*?\)", "", post)

            likes = int(re.search(r"\[ (\d+)  \]", post).group(1) if re.search(r"\[ (\d+)  \]", post) else 0)
            has_comments = bool(re.search(r"\[ Comment  \]", post))

            content = re.sub(r"\[\s*\d+\s*\]", "", post)
            content = re.sub(r"\[\s*(Like|Comment|Share)\s*\]", "", content).strip()

            POSTS.append(Post(
                id=f"{page_id}-post-{len(POSTS)}",
                page_id=page_id,
                content=content,
                likes_count=likes,
                has_comments=has_comments,
            ))

        return POSTS


asyncio.run(scrape_company_posts("deepsolv"))
