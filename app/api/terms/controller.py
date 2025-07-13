from fastapi import HTTPException, status
from app.api.terms.schema import TERMS_DB, TermArticle, AllTermsDetailResponse
from fastapi import status, APIRouter

router = APIRouter(prefix="/terms", tags=["terms"])

@router.get("/", response_model=AllTermsDetailResponse) # ✨ response_model 변경
async def get_all_terms_with_content():
    all_terms = list(TERMS_DB.values())
    return {"terms": all_terms}

@router.get("/{article_number}", response_model=TermArticle)
async def get_term_article(article_number: int):
    term = TERMS_DB.get("terms-of-service-20250627")
    if not term:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 ID의 약관 문서를 찾을 수 없습니다."
        )
    
    try:
        article = term["articles"][article_number - 1]
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"해당 약관에 {article_number}조는 존재하지 않습니다."
        )
        
    return article