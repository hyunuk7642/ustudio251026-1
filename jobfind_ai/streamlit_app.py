import streamlit as st
import openai
import os
from dotenv import load_dotenv
import json

# 환경 변수 로드
load_dotenv()

# 페이지 설정
st.set_page_config(
    page_title="🎯 나의 미래 직업 찾기",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 직업 탐색을 위한 20개 질문
QUESTIONS = [
    "수학이나 과학 과목을 좋아하나요?",
    "사람들과 대화하는 것을 즐기나요?",
    "컴퓨터나 기술에 관심이 많나요?",
    "창작 활동(그림, 글쓰기, 음악 등)을 좋아하나요?",
    "규칙적이고 체계적인 일을 선호하나요?",
    "새로운 것을 배우는 것을 즐기나요?",
    "돈을 관리하거나 계산하는 것을 잘하나요?",
    "다른 사람을 도와주는 것을 좋아하나요?",
    "야외 활동이나 운동을 좋아하나요?",
    "세밀한 작업이나 정확성이 중요한 일을 선호하나요?",
    "리더십을 발휘하는 것을 좋아하나요?",
    "외국어나 다른 문화에 관심이 많나요?",
    "문제를 해결하는 과정을 즐기나요?",
    "계획을 세우고 실행하는 것을 좋아하나요?",
    "예술이나 디자인에 대한 감각이 있다고 생각하나요?",
    "실험하거나 새로운 방법을 시도하는 것을 좋아하나요?",
    "다른 사람의 감정을 이해하고 공감하는 능력이 있나요?",
    "논리적으로 생각하고 분석하는 것을 즐기나요?",
    "팀워크를 중시하고 협력하는 것을 좋아하나요?",
    "미래를 계획하고 목표를 설정하는 것을 좋아하나요?"
]

def get_job_recommendation(answers, user_name, api_key, model):
    """선택한 AI 모델로 답변을 바탕으로 직업을 추천합니다."""
    if model == 'gemini':
        return f"[Gemini(Google) 지원 안내]\n\n아직 Gemini(Google) API 연동은 준비 중입니다. 곧 지원될 예정입니다!\n\n지금은 GPT(OpenAI) 모델을 선택해 사용해 주세요."
    
    # OpenAI GPT-4o 사용
    openai.api_key = api_key
    answers_text = "\n".join([f"질문 {i+1}: {answer}" for i, answer in enumerate(answers)])
    answer_levels = [int(answer) for answer in answers]
    levels_text = "\n".join([f"질문 {i+1}: {level}점" for i, level in enumerate(answer_levels)])
    
    prompt = f"""
당신은 고등학생들의 진로 상담을 도와주는 전문적인 상담사입니다.
{user_name} 학생이 직업 탐색을 위해 답변한 20개 질문을 분석하여 맞춤형 직업을 추천해드리겠습니다.

## 분석 방법
각 질문은 50점 척도(1: 매우 그렇지 않다 ~ 50: 매우 그렇다)로 평가되었으며, 다음과 같은 요소들을 종합적으로 분석했습니다:

1. **수학/과학 성향** (질문 1): 수리적 사고와 논리적 분석 능력
2. **소통 능력** (질문 2): 대인관계와 커뮤니케이션 스킬
3. **기술 관심도** (질문 3): IT/기술 분야에 대한 흥미
4. **창의성** (질문 4): 예술적 감각과 창작 활동
5. **체계성** (질문 5): 규칙적이고 정리된 업무 선호도
6. **학습 의지** (질문 6): 새로운 지식 습득에 대한 열정
7. **계산 능력** (질문 7): 금융/경제적 사고
8. **봉사 정신** (질문 8): 타인을 돕는 성향
9. **활동성** (질문 9): 야외 활동과 운동 선호도
10. **정확성** (질문 10): 세밀한 작업과 정확성 중시
11. **리더십** (질문 11): 팀을 이끌고 의사결정을 하는 능력
12. **국제적 관심** (질문 12): 글로벌 마인드와 문화적 이해
13. **문제해결 능력** (질문 13): 복잡한 문제를 해결하는 능력
14. **계획 및 실행력** (질문 14): 목표 설정과 실행 능력
15. **예술적 감각** (질문 15): 미적 감각과 디자인 능력
16. **혁신성** (질문 16): 새로운 아이디어와 실험 정신
17. **공감 능력** (질문 17): 타인의 감정을 이해하는 능력
18. **논리적 사고** (질문 18): 체계적이고 분석적인 사고
19. **협력성** (질문 19): 팀워크와 협력 능력
20. **전략적 사고** (질문 20): 장기적 관점과 전략적 계획

질문:
1. 수학이나 과학 과목을 좋아하나요?
2. 사람들과 대화하는 것을 즐기나요?
3. 컴퓨터나 기술에 관심이 많나요?
4. 창작 활동(그림, 글쓰기, 음악 등)을 좋아하나요?
5. 규칙적이고 체계적인 일을 선호하나요?
6. 새로운 것을 배우는 것을 즐기나요?
7. 돈을 관리하거나 계산하는 것을 잘하나요?
8. 다른 사람을 도와주는 것을 좋아하나요?
9. 야외 활동이나 운동을 좋아하나요?
10. 세밀한 작업이나 정확성이 중요한 일을 선호하나요?
11. 리더십을 발휘하는 것을 좋아하나요?
12. 외국어나 다른 문화에 관심이 많나요?
13. 문제를 해결하는 과정을 즐기나요?
14. 계획을 세우고 실행하는 것을 좋아하나요?
15. 예술이나 디자인에 대한 감각이 있다고 생각하나요?
16. 실험하거나 새로운 방법을 시도하는 것을 좋아하나요?
17. 다른 사람의 감정을 이해하고 공감하는 능력이 있나요?
18. 논리적으로 생각하고 분석하는 것을 즐기나요?
19. 팀워크를 중시하고 협력하는 것을 좋아하나요?
20. 미래를 계획하고 목표를 설정하는 것을 좋아하나요?

{user_name} 학생의 답변 (50점 척도):
{answers_text}

답변 수준 분석:
{levels_text}

위의 분석을 바탕으로 {user_name} 학생에게 맞는 직업을 추천해주세요:

## 추천 직업

### 1. [직업명]
- **적합한 이유**: [이 직업이 왜 {user_name} 학생에게 적합한지 구체적으로 설명]
- **필요한 능력**: [이 직업에 필요한 주요 능력들]
- **관련 학과**: [대학에서 관련된 학과들]
- **적합도**: [답변 수준을 바탕으로 한 적합도 - 매우 높음/높음/보통/낮음/매우 낮음]

### 2. [직업명]
- **적합한 이유**: [이 직업이 왜 {user_name} 학생에게 적합한지 구체적으로 설명]
- **필요한 능력**: [이 직업에 필요한 주요 능력들]
- **관련 학과**: [대학에서 관련된 학과들]
- **적합도**: [답변 수준을 바탕으로 한 적합도 - 매우 높음/높음/보통/낮음/매우 낮음]

### 3. [직업명]
- **적합한 이유**: [이 직업이 왜 {user_name} 학생에게 적합한지 구체적으로 설명]
- **필요한 능력**: [이 직업에 필요한 주요 능력들]
- **관련 학과**: [대학에서 관련된 학과들]
- **적합도**: [답변 수준을 바탕으로 한 적합도 - 매우 높음/높음/보통/낮음/매우 낮음]

### 4. [직업명]
- **적합한 이유**: [이 직업이 왜 {user_name} 학생에게 적합한지 구체적으로 설명]
- **필요한 능력**: [이 직업에 필요한 주요 능력들]
- **관련 학과**: [대학에서 관련된 학과들]
- **적합도**: [답변 수준을 바탕으로 한 적합도 - 매우 높음/높음/보통/낮음/매우 낮음]

### 5. [직업명]
- **적합한 이유**: [이 직업이 왜 {user_name} 학생에게 적합한지 구체적으로 설명]
- **필요한 능력**: [이 직업에 필요한 주요 능력들]
- **관련 학과**: [대학에서 관련된 학과들]
- **적합도**: [답변 수준을 바탕으로 한 적합도 - 매우 높음/높음/보통/낮음/매우 낮음]

## 성향 분석
[{user_name} 학생의 답변 패턴을 바탕으로 한 전반적인 성향 분석 - 구체적이고 개인화된 내용]

## 추가 조언
[{user_name} 학생에게 도움이 될 만한 구체적인 조언이나 준비 방법]

주의사항:
- 적합도는 반드시 "매우 높음", "높음", "보통", "낮음", "매우 낮음" 중 하나로 표시
- 직업은 적합도가 높은 순서대로 정렬
- 한국의 실제 직업 시장과 관련된 현실적인 직업을 추천
- {user_name} 학생을 직접 호명하며 친근하고 격려하는 톤으로 답변
"""
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"당신은 고등학생들의 진로 상담을 도와주는 친근하고 전문적인 상담사입니다. {user_name} 학생의 개인적인 성향과 답변을 바탕으로 맞춤형 조언을 제공합니다. 한국의 직업 시장에 대한 깊은 이해를 바탕으로 현실적이고 구체적인 조언을 제공합니다."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"죄송합니다. 분석 중 오류가 발생했습니다: {str(e)}"

def main():
    # 커스텀 CSS 스타일링
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    
    .question-container {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #667eea;
        margin-bottom: 1.5rem;
    }
    
    .progress-container {
        background: #e0e0e0;
        border-radius: 10px;
        height: 20px;
        margin-bottom: 2rem;
        overflow: hidden;
    }
    
    .progress-bar {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        height: 100%;
        transition: width 0.3s ease;
        border-radius: 10px;
    }
    
    .result-container {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 15px;
        border-left: 5px solid #28a745;
        margin-top: 2rem;
    }
    
    .job-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 메인 헤더
    st.markdown("""
    <div class="main-header">
        <h1>🎯 나의 미래 직업 찾기</h1>
        <p>20개의 간단한 질문으로 당신에게 딱 맞는 직업을 찾아보세요!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 사이드바 설정
    with st.sidebar:
        st.header("🔧 설정")
        
        # API 키 입력
        api_key = st.text_input(
            "🔑 OpenAI API 키",
            type="password",
            help="OpenAI API 키를 입력하세요"
        )
        
        # 모델 선택
        model = st.radio(
            "🤖 AI 모델 선택",
            ["gpt", "gemini"],
            format_func=lambda x: "GPT (OpenAI)" if x == "gpt" else "Gemini (Google)"
        )
        
        # 사용자 이름 입력
        user_name = st.text_input(
            "👋 이름을 입력하세요",
            placeholder="이름을 입력하세요"
        )
        
        st.markdown("---")
        st.markdown("### 📊 진행률")
        
        # 진행률 계산
        if 'answers' in st.session_state:
            answered_count = sum(1 for answer in st.session_state.answers if answer != 25)
            progress = (answered_count / 20) * 100
            st.progress(progress / 100)
            st.caption(f"{answered_count}/20 질문 완료 ({progress:.1f}%)")
        else:
            st.progress(0)
            st.caption("0/20 질문 완료 (0%)")
    
    # 세션 상태 초기화
    if 'answers' not in st.session_state:
        st.session_state.answers = [25] * 20  # 기본값 25점
    if 'show_results' not in st.session_state:
        st.session_state.show_results = False
    
    # 결과가 있으면 결과 페이지 표시
    if st.session_state.show_results and 'recommendation' in st.session_state:
        show_results_page()
        return
    
    # 메인 폼
    st.markdown("### 📝 질문에 답변해주세요")
    st.markdown("각 질문에 대해 1점(매우 그렇지 않다)부터 50점(매우 그렇다)까지 슬라이더로 답변해주세요.")
    
    # 질문 폼
    with st.form("career_form"):
        answers = []
        
        for i, question in enumerate(QUESTIONS):
            with st.container():
                st.markdown(f"""
                <div class="question-container">
                    <h4>❓ 질문 {i+1}: {question}</h4>
                </div>
                """, unsafe_allow_html=True)
                
                # 슬라이더로 답변
                answer = st.slider(
                    f"답변 {i+1}",
                    min_value=1,
                    max_value=50,
                    value=st.session_state.answers[i],
                    step=1,
                    format="%d점",
                    key=f"question_{i}",
                    label_visibility="collapsed"
                )
                answers.append(answer)
                
                # 세션 상태 업데이트
                st.session_state.answers[i] = answer
        
        # 제출 버튼
        submitted = st.form_submit_button(
            "🚀 직업 추천 받기",
            use_container_width=True
        )
        
        if submitted:
            # 유효성 검사
            if not user_name.strip():
                st.error("이름을 입력해주세요!")
                return
            
            if not api_key.strip():
                st.error("OpenAI API 키를 입력해주세요!")
                return
            
            # 분석 실행
            with st.spinner("🤖 AI가 당신의 답변을 분석하고 있습니다..."):
                try:
                    recommendation = get_job_recommendation(answers, user_name, api_key, model)
                    st.session_state.recommendation = recommendation
                    st.session_state.user_name = user_name
                    st.session_state.show_results = True
                    st.rerun()
                except Exception as e:
                    st.error(f"분석 중 오류가 발생했습니다: {str(e)}")

def show_results_page():
    """결과 페이지를 표시합니다."""
    st.markdown(f"""
    <div class="main-header">
        <h1>🎉 {st.session_state.user_name} 학생의 직업 추천 결과</h1>
        <p>AI가 분석한 당신에게 딱 맞는 직업을 확인해보세요!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 결과 표시
    st.markdown("""
    <div class="result-container">
    """, unsafe_allow_html=True)
    
    # 마크다운 결과를 파싱하여 표시
    recommendation = st.session_state.recommendation
    
    # 추천 직업 섹션
    if "## 추천 직업" in recommendation:
        st.markdown("## 💼 추천 직업")
        
        # 각 직업을 카드 형태로 표시
        lines = recommendation.split('\n')
        current_job = None
        job_content = []
        
        for line in lines:
            if line.startswith('### ') and '.' in line:
                # 이전 직업이 있으면 표시
                if current_job and job_content:
                    show_job_card(current_job, job_content)
                
                # 새 직업 시작
                current_job = line.replace('### ', '').replace('**', '')
                job_content = []
            elif current_job and line.strip():
                job_content.append(line)
        
        # 마지막 직업 표시
        if current_job and job_content:
            show_job_card(current_job, job_content)
    
    # 성향 분석 섹션
    if "## 성향 분석" in recommendation:
        st.markdown("## 🧠 성향 분석")
        start_idx = recommendation.find("## 성향 분석")
        end_idx = recommendation.find("## 추가 조언", start_idx)
        if end_idx == -1:
            end_idx = len(recommendation)
        
        personality_text = recommendation[start_idx:end_idx].replace("## 성향 분석", "").strip()
        st.markdown(personality_text)
    
    # 추가 조언 섹션
    if "## 추가 조언" in recommendation:
        st.markdown("## 💡 추가 조언")
        start_idx = recommendation.find("## 추가 조언")
        advice_text = recommendation[start_idx:].replace("## 추가 조언", "").strip()
        st.markdown(advice_text)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 액션 버튼들
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🏠 처음으로 돌아가기", use_container_width=True):
            st.session_state.show_results = False
            st.session_state.answers = [25] * 20
            st.rerun()
    
    with col2:
        if st.button("🔄 다시 분석하기", use_container_width=True):
            st.session_state.show_results = False
            st.rerun()
    
    with col3:
        if st.button("📄 결과 복사하기", use_container_width=True):
            st.code(recommendation, language="markdown")

def show_job_card(job_title, job_content):
    """직업 카드를 표시합니다."""
    st.markdown(f"""
    <div class="job-card">
        <h3>💼 {job_title}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    for line in job_content:
        if line.strip():
            if line.startswith('- **'):
                # 강조된 항목
                st.markdown(line)
            else:
                st.markdown(line)

if __name__ == "__main__":
    main()
