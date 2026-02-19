import streamlit as st

# --- 페이지 설정 ---
st.set_page_config(page_title="고학년 이야기 개요 생성기", layout="wide")

# --- 스타일링 (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stButton>button { width: 100%; border-radius: 12px; }
    .reportview-container .main .block-container { padding-top: 2rem; }
    div[data-testid="stExpander"] { border-radius: 15px; border: 1px solid #e2e8f0; }
    </style>
    """, unsafe_allow_html=True)

# --- 세션 상태 초기화 (동적 입력 필드 관리) ---
if 'characters' not in st.session_state:
    st.session_state.characters = [""]
if 'keywords' not in st.session_state:
    st.session_state.keywords = [""]
if 'outline' not in st.session_state:
    st.session_state.outline = None

# --- 데이터 정의 ---
GRADE_GENRES = {
    "5학년": ['판타지 모험 이야기', '추리/미스터리', '학교 생활 성장 이야기', '우정과 갈등 이야기', '역할 바꾸기 이야기'],
    "6학년": ['성장 드라마 형식 이야기', '사회 문제를 담은 생활 글', 'SF/공상 과학 이야기', '풍자 우화', '리얼 학교 이야기']
}

ENDING_PRESETS = {
    "해피엔딩": "갈등은 깔끔하게 해결되고, 인물들이 서로의 마음을 이해하며 앞으로 나아가는 마무리",
    "씁쓸하지만 성장": "완벽한 결과는 아니지만, 인물들이 책임을 받아들이며 한 단계 성장하는 마무리",
    "열린 결말": "당장의 답은 다 나오지 않았지만, 앞으로 어떤 선택을 할지 여지를 남겨 두는 마무리",
    "반전 결말": "마지막에 예상 밖의 진실이 드러나며 사건을 전혀 새로운 시선으로 보게 되는 마무리"
}

# --- 사이드바 및 헤더 ---
st.title("📝 고학년 이야기 개요 & 삽화 생성기")
st.caption("5·6학년을 위한 발단–전개–절정–결말 구조와 삽화 프롬프트 도구")

# --- 입력 영역 ---
with st.container():
    col1, col2, col3 = st.columns(3)
    
    with col1:
        grade = st.selectbox("학년 *", ["선택하세요", "5학년", "6학년"])
        genre_list = GRADE_GENRES.get(grade, ["학년을 먼저 선택하세요"])
        genre_sel = st.selectbox("추천 장르", genre_list)
        genre_custom = st.text_input("직접 입력(장르)", placeholder="예: 학교 성장 드라마")
        final_genre = genre_custom if genre_custom else genre_sel

    with col2:
        length_level = st.select_slider("개요 분량 단계", options=[1, 2, 3, 4, 5], value=3)
        st.info(f"{length_level}단계: {'간단함' if length_level < 3 else '보통' if length_level == 3 else '매우 상세'}")
        mood = st.selectbox("이야기 분위기", ["현실적이고 차분한", "긴장감 있는 모험", "신비롭고 미스터리한", "감동적이고 따뜻한"])

    with col3:
        style = st.radio("표현 방식", ["기본 표현", "풍부한 표현 (묘사 중심)"])
        ending_type = st.selectbox("결말 방향", list(ENDING_PRESETS.keys()))
        ending_desc = st.text_area("내가 생각한 결말 상세", value=ENDING_PRESETS[ending_type])

    st.divider()

    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("인물 및 키워드")
        # 인물 추가 로직
        for i, char in enumerate(st.session_state.characters):
            st.session_state.characters[i] = st.text_input(f"주요 인물 {i+1} *", value=char, key=f"char_{i}")
        if st.button("+ 인물 추가"):
            st.session_state.characters.append("")
            st.rerun()

    with col_right:
        st.subheader("배경 및 사건")
        time_bg = st.text_input("시간 배경", placeholder="예: 졸업을 앞둔 겨울 오후")
        place_bg = st.text_input("장소 배경", placeholder="예: 6학년 교실, 운동장")
        problem = st.text_area("중심 갈등/사건 *", placeholder="예: 친구와 반장 선거에서 경쟁하게 된 상황")

# --- 개요 생성 로직 (단순화된 예시 버전) ---
def generate_outline():
    chars = ", ".join([c for c in st.session_state.characters if c])
    
    # 실제 로직은 첨부된 HTML의 JS 알고리즘을 파이썬 문법으로 옮긴 것
    outline = {
        "발단": f"{time_bg or '어느 날'}, {place_bg or '어떤 곳'}에서 {chars}에게 {problem}의 전조가 나타난다.",
        "전개": f"{chars}은(는) 문제를 해결하려 노력하지만 상황은 복잡해진다.",
        "절정": f"결정적인 순간, {chars}은(는) 자신의 가치관을 건 선택의 기로에 선다.",
        "결말": f"결국 {ending_desc} 방향으로 이야기가 마무리되며 {chars}은(는) 성장한다."
    }
    return outline

# --- 생성 버튼 ---
if st.button("🔥 발단–전개–절정–결말 개요 만들기", type="primary"):
    if grade == "선택하세요" or not problem or not st.session_state.characters[0]:
        st.error("필수 항목(*)을 입력해주세요.")
    else:
        st.session_state.outline = generate_outline()

# --- 결과 출력 ---
if st.session_state.outline:
    st.divider()
    res_col1, res_col2 = st.columns([2, 1])
    
    with res_col1:
        st.subheader("📍 이야기 개요")
        title = st.text_input("이야기 제목", value=f"{place_bg}에서 생긴 {problem[:10]}...")
        
        for step, content in st.session_state.outline.items():
            with st.expander(f"**{step}**", expanded=True):
                st.write(content)
                
        reflection = st.text_area("깨달은 점 / 메시지")

    with res_col2:
        st.subheader("🎨 삽화 프롬프트")
        illust_style = st.selectbox("그림체", ["어린이 손그림", "만화/웹툰", "수채화", "연필 스케치"])
        target_step = st.multiselect("삽화로 만들 장면", ["발단", "전개", "절정", "결말"], default=["절정"])
        
        if st.button("🪄 프롬프트 생성"):
            for step in target_step:
                prompt = f"({illust_style} 스타일) {st.session_state.outline[step]}"
                st.code(prompt, language="text")
            st.success("위 코드를 복사해 AI 이미지 생성기(Canva 등)에 붙여넣으세요!")

# --- 푸터 ---
st.markdown("---")
st.caption("copyright 말맛 살리기 연구회(석포초등학교 프롬프트 엔지니어링 팀)")
