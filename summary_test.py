import os
import asyncio
import httpx
from bs4 import BeautifulSoup
from openai import AsyncOpenAI
from dotenv import load_dotenv

# --- 설정 로드 ---
# .env 파일에서 환경 변수를 로드합니다.
load_dotenv()

# 환경 변수에서 OpenAI API 키를 가져옵니다.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("오류: .env 파일에 OPENAI_API_KEY가 설정되지 않았습니다.")
    exit()

# 비동기 OpenAI 클라이언트를 초기화합니다.
openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)


async def test_summary_creation(url: str, summary_type: str = "한 줄 요약"):
    """
    단일 URL에 대해 크롤링 및 AI 요약 생성을 테스트하는 메인 함수입니다.
    """
    print(f"▶ 테스트 시작: {url}")
    
    try:
        # --- 1. 웹 페이지 크롤링 ---
        print("1. 웹 페이지 크롤링 중...")
        async with httpx.AsyncClient() as client:
            # follow_redirects=True: 리디렉션을 자동으로 따라갑니다.
            # headers: 일부 웹사이트는 브라우저인 것처럼 요청해야 접근을 허용합니다.
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
            response = await client.get(url, timeout=20.0, follow_redirects=True, headers=headers)
            response.raise_for_status()  # 200 OK가 아니면 에러 발생
        # --- 2. HTML 파싱 및 텍스트 추출 ---
        print("2. HTML 콘텐츠 파싱 중...")
        soup = BeautifulSoup(response.text, 'lxml')
        
        # <p> 태그의 텍스트만 간단히 추출합니다.
        paragraphs = [p.get_text() for p in soup.find_all('p')]
        text_content = " ".join(paragraphs).strip()
        print(len(text_content)); input()

        if not text_content:
            raise ValueError("페이지에서 텍스트 콘텐츠를 추출할 수 없습니다.")
        
        print(f"✅ 텍스트 추출 성공 (첫 100자): {text_content[:100]}...")

        # --- 3. ChatGPT API로 요약 요청 ---
        print("\n3. ChatGPT API로 요약 생성 요청 중...")
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
        print("✅ ChatGPT 응답 수신 완료.")
        print("   - 원본 응답:", repr(ai_response)) # 응답 형식을 정확히 보기 위해 repr 사용

        # --- 4. AI 응답 파싱 ---
        print("\n4. 응답 파싱 중...")
        try:
            title = ai_response.split("제목:")[1].split("내용:")[0].strip()
            content = ai_response.split("내용:")[1].strip()
        except IndexError:
            raise ValueError("AI 응답이 예상된 '제목:/내용:' 형식이 아닙니다.")

        summary_data = {
            "subject": title,
            "content": content,
        }
        
        print("\n--- 최종 결과 ---")
        print(f"제목: {summary_data['subject']}")
        print(f"내용: {summary_data['content']}")
        print("-----------------")

    except Exception as e:
        print(f"\n❌ 처리 중 에러 발생: {e}")


# --- 스크립트 실행 ---
if __name__ == "__main__":
    # 테스트하고 싶은 URL을 여기에 입력하세요.
    target_url = "https://velog.io/@dodozee/Redis"
    
    # 비동기 함수를 실행합니다.
    asyncio.run(test_summary_creation(url=target_url, ))
