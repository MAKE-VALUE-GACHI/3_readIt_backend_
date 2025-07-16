from celery import Celery
from app.api.scrap.schema import StatusEnum
from app.db.session import AsyncSessionLocal
import asyncio
from app.config import settings

from sqlalchemy import select
from app.models.models import Scrap

import httpx
from bs4 import BeautifulSoup
from openai import AsyncOpenAI
from app.models.enums import ScrapType

celery_app = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

CHUNK_SIZE = 8000
CHUNK_OVERLAP = 200

# --- 2. 맵리듀스 헬퍼 함수 정의 ---

def split_text_into_chunks(text: str, chunk_size: int, overlap: int) -> list[str]:
    if len(text) <= chunk_size:
        return [text]
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

async def summarize_chunk(chunk: str, chunk_index: int, summary_type: str) -> str:
    try:
        response = await openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert at summarizing parts of a long document. Extract the key points from the following text chunk in Korean."},
                {"role": "user", "content": f"다음은 긴 글의 일부입니다. 이 부분의 핵심 내용을 '{summary_type}' 형식으로 요약해 주세요:\n\n{chunk}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return ""

async def summarize_final(combined_summary: str, summary_type: str) -> str:
    response = await openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a skilled editor. You will be given a collection of summaries from different parts of a long article. Your task is to synthesize them into a final, coherent summary and a suitable title. Respond in Korean in the format '제목: [Title]\n내용: [Content]'."
            },
            {
                "role": "user",
                "content": f"다음은 긴 글의 각 부분을 요약한 내용입니다. 이 내용들을 바탕으로 전체 글을 아우르는 최종 '제목'과 '{summary_type}' 형식의 '내용'을 생성해줘. 응답 형식은 '제목: [여기에 제목]\n내용: [여기에 내용]' 이 두 가지로만 작성해줘.\n\n---개별 요약본들---\n{combined_summary}"
            }
        ]
    )
    return response.choices[0].message.content



@celery_app.task
def create_scrap_task(task_id: str, type: str, url: str | None = None, text: str | None = None):

    async def _async_update_db():
        async with AsyncSessionLocal() as session:
                
            ai_response = ""
            summary_type = ""

            try:
                if type == "oneline":
                    summary_type = "핵심을 짧고 임팩트 있게 한 문장으로 요약"
                elif type == "fiveline":
                    summary_type = "뉴스레터처럼 전체 내용을 간결하게 10문장 이내로 요약, 분량이 최소 100자 이상이 되도록 작성"
                elif type == "insight":
                    summary_type = "5문장 이상으로 상세히 요약하고, AI의 독창적인 인사이트를 덧붙여 총 분량이 최소 500자 이상이 되도록 작성"
                elif type == "basic":
                    summary_type = "글의 핵심 내용과 주제를 충실하게, 5문장 이상으로 상세히 요약, 분량이 최소 500자 이상이 되도록 작성"
                
                if text is not None:
                    text_content = text.strip()
                else:
                    async with httpx.AsyncClient() as client:
                        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
                        response = await client.get(url, timeout=30.0, follow_redirects=True, headers=headers)
                        response.raise_for_status()
                    soup = BeautifulSoup(response.text, 'lxml')
                    paragraphs = [p.get_text() for p in soup.find_all('p')]
                    text_content = " ".join(paragraphs).strip()

                if not text_content:
                    raise ValueError("페이지에서 텍스트 콘텐츠를 추출할 수 없습니다.")
                

                # --- AI 요약 (맵리듀스 분기 로직) ---
                if len(text_content) <= CHUNK_SIZE:
                    chat_completion = await openai_client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {
                            "role": "system",
                            "content": "You are a helpful assistant that summarizes web content. Please provide a title and a summary based on the text. Respond in Korean."
                            },
                            {
                            "role": "user",
                            "content": f"다음 텍스트를 기반으로, 적절한 '제목'과 '{summary_type}' 형식의 '내용'을 생성해줘. 응답 형식은 '제목: [여기에 제목]\n내용: [여기에 내용]' 이 두 가지로만 작성해줘.\n\n---텍스트 시작---\n{text_content[:3000]}\n---텍스트 끝---"
                            }
                            ]
                    )
                    ai_response = chat_completion.choices[0].message.content
                else:
                    chunks = split_text_into_chunks(text_content, CHUNK_SIZE, CHUNK_OVERLAP)
                    map_tasks = [summarize_chunk(chunk, i, summary_type) for i, chunk in enumerate(chunks)]
                    chunk_summaries = await asyncio.gather(*map_tasks)
                    combined_summary = "\n\n---\n\n".join(s for s in chunk_summaries if s)
                    ai_response = await summarize_final(combined_summary, summary_type)
                
                title = "제목을 찾을 수 없습니다."
                content = "내용을 찾을 수 없습니다."

                if "제목:" in ai_response and "내용:" in ai_response:
                    title = ai_response.split("제목:")[1].split("내용:")[0].strip()
                    content = ai_response.split("내용:")[1].strip()
                elif "제목:" in ai_response:
                    title = ai_response.split("제목:")[1].strip()
                    content = "내용 부분 없음"
                elif "내용:" in ai_response:
                    content = ai_response.split("내용:")[1].strip()
                    title = "제목 부분 없음"
                else:
                    content = ai_response.strip()

                summary_data = {"subject": title, "content": content}
                status = StatusEnum.completed.value

            except Exception as e:
                summary_data = {"content": f"작업 실패: {e}\n\nAI 마지막 응답:\n{ai_response}"}
                status = StatusEnum.failed.value

            # --- DB 업데이트 로직 ---
            result = await session.execute(
                select(Scrap).where(Scrap.task_id == task_id)
            )
            scrap = result.scalar_one_or_none()
            if scrap:
                scrap.status = status
                scrap.subject = summary_data.get("subject", "")
                scrap.content = summary_data.get("content", "")
                await session.commit()
            else:
                pass

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    loop.run_until_complete(_async_update_db())
