from flask import Flask, render_template, request, jsonify, redirect, url_for
import openai
import os
import json
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

app = Flask(__name__)

# OpenAI API 키 설정
openai.api_key = os.getenv('OPENAI_API_KEY')

# 직업 탐색을 위한 20개 질문
QUESTIONS = [
    "1. 수학이나 과학 과목을 좋아하나요?",
    "2. 사람들과 대화하는 것을 즐기나요?",
    "3. 컴퓨터나 기술에 관심이 많나요?",
    "4. 창작 활동(그림, 글쓰기, 음악 등)을 좋아하나요?",
    "5. 규칙적이고 체계적인 일을 선호하나요?",
    "6. 새로운 것을 배우는 것을 즐기나요?",
    "7. 돈을 관리하거나 계산하는 것을 잘하나요?",
    "8. 다른 사람을 도와주는 것을 좋아하나요?",
    "9. 야외 활동이나 운동을 좋아하나요?",
    "10. 세밀한 작업이나 정확성이 중요한 일을 선호하나요?",
    "11. 리더십을 발휘하는 것을 좋아하나요?",
    "12. 외국어나 다른 문화에 관심이 많나요?",
    "13. 문제를 해결하는 과정을 즐기나요?",
    "14. 계획을 세우고 실행하는 것을 좋아하나요?",
    "15. 예술이나 디자인에 대한 감각이 있다고 생각하나요?",
    "16. 실험하거나 새로운 방법을 시도하는 것을 좋아하나요?",
    "17. 다른 사람의 감정을 이해하고 공감하는 능력이 있나요?",
    "18. 논리적으로 생각하고 분석하는 것을 즐기나요?",
    "19. 팀워크를 중시하고 협력하는 것을 좋아하나요?",
    "20. 미래를 계획하고 목표를 설정하는 것을 좋아하나요?"
]

@app.route('/')
def index():
    return render_template('index.html', questions=QUESTIONS)

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        answers = data.get('answers', [])
        user_name = data.get('userName', '학생')
        api_key = data.get('apiKey', None)
        model = data.get('model', 'gpt')
        
        if len(answers) != 20:
            return jsonify({'error': '모든 질문에 답변해주세요.'}), 400
        
        # 선택한 모델에 따라 직업 추천
        recommendation = get_job_recommendation(answers, user_name, api_key, model)
        
        # 결과 페이지로 리다이렉트
        import urllib.parse
        result_data = urllib.parse.quote(json.dumps({
            'recommendation': recommendation,
            'userName': user_name,
            'success': True
        }))
        
        return jsonify({
            'redirect': f'/result?data={result_data}',
            'success': True
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/result')
def result():
    return render_template('result.html')

def get_job_recommendation(answers, user_name, api_key, model):
    """선택한 AI 모델로 답변을 바탕으로 직업을 추천합니다."""
    if model == 'gemini':
        return f"[Gemini(Google) 지원 안내]\n\n아직 Gemini(Google) API 연동은 준비 중입니다. 곧 지원될 예정입니다!\n\n지금은 GPT(OpenAI) 모델을 선택해 사용해 주세요."
    # OpenAI GPT-4o 사용
    import openai
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

if __name__ == '__main__':
    app.run(debug=True, port=5002) 