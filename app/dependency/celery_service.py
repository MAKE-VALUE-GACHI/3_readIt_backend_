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

celery_app = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

@celery_app.task
def create_scrap_task(task_id: str, url: str, summary_type: str):


    async def _async_update_db():

        async with AsyncSessionLocal() as session:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(url, timeout=20.0, follow_redirects=True)
                    response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'lxml')

                paragraphs = [p.get_text() for p in soup.find_all('p')]
                text_content = " ".join(paragraphs).strip()

                if not text_content:
                    raise ValueError("페이지에서 텍스트 콘텐츠를 추출할 수 없습니다.")
                
                print(f"[{task_id}] ChatGPT API로 요약 생성 중...")
                chat_completion = await openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful assistant that summarizes web content. Please provide a title and a summary based on the text. Respond in Korean."
                        },
                        {
                            "role": "user",
                            "content": f"다음 텍스트를 기반으로, 적절한 '제목'과 '{summary_type}' 형식의 '내용'을 생성해줘. 응답 형식은 '제목: [여기에 제목]\n내용: [여기에 내용]' 이 두 줄로만 작성해줘.\n\n---텍스트 시작---\n{text_content[:3000]}\n---텍스트 끝---"
                        }
                    ]
                )
                ai_response = chat_completion.choices[0].message.content
                
                title = ai_response.split("제목:")[1].split("내용:")[0].strip()
                content = ai_response.split("내용:")[1].strip()

                summary_data = {
                    "subject": title,
                    "content": content,
                }
                status = StatusEnum.completed.value

            except Exception as e:
                summary_data = {}
                status = StatusEnum.failed.value

            
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
        asyncio.run(_async_update_db())
    except Exception as e:
        pass