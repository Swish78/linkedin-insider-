from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from ..models.linkedin_models import LinkedInPage
from ..services.db_service import save_page_data, get_page_by_id, get_filtered_pages, get_page_posts
from ..scrapping.company_info_scraper import scrape_company_info
from ..scrapping.company_post_scrapper import scrape_company_posts

router = APIRouter()


@router.get("/pages/{page_id}")
async def get_page(page_id: str):
    page = get_page_by_id(page_id)
    if not page:
        try:
            page = await scrape_company_info(page_id)
            posts = await scrape_company_posts(page_id)
            page.posts = posts
            save_page_data(page)
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Page not found: {str(e)}")
    return page


@router.get("/pages")
def get_pages(
        min_followers: Optional[int] = Query(None),
        max_followers: Optional[int] = Query(None),
        industry: Optional[str] = Query(None),
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100)
):
    return get_filtered_pages(
        min_followers=min_followers,
        max_followers=max_followers,
        industry=industry,
        skip=skip,
        limit=limit
    )


@router.get("/pages/{page_id}/posts")
def get_posts(
        page_id: str,
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100)
):
    return get_page_posts(page_id, skip=skip, limit=limit)
