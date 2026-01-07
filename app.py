import streamlit as st
from openai import OpenAI

# 1. 视觉黑科技：Chanel 极简主义 + 珠宝闪烁 + 甜品意象
st.set_page_config(page_title="MindMemo | Haute Dessert", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Noto+Serif+SC:wght@200;500&display=swap');

    /* 全局背景：香奈儿黑白美学 */
    .stApp {
        background: radial-gradient(circle at center, #121212 0%, #000000 100%);
        color: #FFFFFF;
        font-family: 'Noto Serif SC', serif;
    }

    /* 圣光闪烁动画 */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: radial-gradient(circle at 50% 50%, rgba(212, 167, 108, 0.08) 0%, transparent 70%);
        pointer-events: none;
        z-index: 0;
    }

    header, footer, #MainMenu {visibility: hidden;}

    /* 甜品图标动画 */
    .dessert-header {
        text-align: center;
        margin-top: 40px;
        animation: float 3s ease-in-out infinite;
    }
    @keyframes float {
        0%, 100% { transform: translateY(0); filter: drop-shadow(0 0 5px rgba(212,167,108,0.2)); }
        50% { transform: translateY(-15px); filter: drop-shadow(0 0 20px rgba(212,167,108,0.5)); }
    }

    .title-cinzel {
        font-family: 'Cinzel', serif;
        font-size: 1.8rem;
        letter-spacing: 12px;
        color: #d4a76c;
        text-align: center;
        margin-bottom: 50px;
    }

    /* 输入框：香奈儿极简线条 */
    .stTextArea textarea {
        background-color: transparent !important;
        border: none !important;
        border-bottom: 1px solid rgba(212, 167, 108, 0.3) !important;
        color: #FFFFFF !important;
        font-size: 1.2rem !important;
        text-align: center !important;
        border-radius: 0 !important;
        padding: 40px !important;
    }
    .stTextArea textarea:focus {
        border-bottom: 1px solid #d4a76c !important;
        box-shadow: none !important;
    }

    /* 按钮：金属感高级定制 */
    .stButton > button {
        background-color: transparent !important;
        color: #d4a76c !important;
        border: 1px solid #d4a76c !important;
        width: 100%;
        padding: 15px 0 !important;
        letter-spacing: 10px;
        font-family: 'Cinzel', serif;
        transition: 0.8s;
        border-radius: 0px !important;
        margin-top: 20px;
    }
    .stButton > button:hover {
        background-color: #d4a76c !important;
        color: #000 !important;
        box-shadow: 0 0 40px rgba(212, 167, 108, 0.6);
    }

    /* 心理卡片：香奈儿珠宝盒 + 圣光闪烁 */
    .memo-card {
        background: #FFFFFF;
        color: #1a1a1a;
        width: 100%;
        max-width: 450px;
        margin: 50px auto;
        padding: 60px 45px;
        position: relative;
        box-shadow: 0 0 30px rgba(255, 255, 255, 0.15);
        border: 1px solid rgba(212, 167, 108, 0.2);
        animation: divineGlow 4s infinite alternate;
        text-align: left;
    }

    @keyframes divineGlow {
        from { box-shadow: 0 0 20px rgba(255, 255, 255, 0.1), 0 0 10px rgba(212, 167, 108, 0.1); }
        to { box-shadow: 0 0 60px rgba(255, 255, 255, 0.3), 0 0 40px rgba(212, 167, 108, 0.4); }
    }

    .memo-card h3 {
        font-family: 'Cinzel', serif;
        font-size: 1.1rem;
        color: #000;
        border-bottom: 2px solid #d4a76c;
        padding-bottom: 8px;
        margin-top: 25px !important;
        margin-bottom: 15px !important;
    }
    
    .memo-card p {
        font-size: 0.95rem;
        line-height: 1.8;
        color: #333;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 会话状态管理
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []

# 甜品与场景结合
desserts = [
    {"icon": "🧁", "title": "ORIGIN", "sub": "🌱 原生底色（童年最深刻的味觉碎片）"},
    {"icon": "🍫", "title": "DUALITY", "sub": "📈 高光至暗（如黑巧般浓郁或苦涩的转折）"},
    {"icon": "☕", "title": "BODY", "sub": "💊 身体记号（压力在感官上的残留）"},
    {"icon": "🧁", "title": "OTHERS", "sub": "🤝 关键关系（谁是你生命中的夹心内馅？）"},
    {"icon": "🥯", "title": "PATTERN", "sub": "🔀 转折执念（无法抗拒的循环模式）"}
]

# 3. 逻辑分屏渲染
if st.session_state.step < len(desserts):
    d = desserts[st.session_state.step]
    
    st.markdown(f'<div class="dessert-header" style="font-size:4rem;">{d["icon"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="title-cinzel">{d["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align:center; opacity:0.5; letter-spacing:3px;">{d["sub"]}</p>', unsafe_allow_html=True)
    
    ans = st.text_area("", key=f"f_{st.session_state.step}", height=200, label_visibility="collapsed", placeholder="请刻录这一帧记忆...")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("NEXT FRAME" if st.session_state.step < 4 else "ENCODE ARCHIVE"):
            if ans:
                st.session_state.answers.append(ans)
                st.session_state.step += 1
                st.rerun()
else:
    st.markdown('<div class="title-cinzel" style="margin-top:100px;">FINISHING</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("OPEN THE CARD"):
            with st.spinner("MindMemo 引擎分析中..."):
                try:
                    client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
                    full_context = "\n".join(st.session_state.answers)
                    
                    # 严格执行 MindMemo 引擎逻辑
                    prompt = f"""
                    你是一个名为 "MindMemo" 的后台心理分析引擎。
                    你的任务是对用户的输入进行“静默分析”，并生成一张结构化的“心理卡片”。
                    
                    # Principles
                    1. 去聊天化：直接输出分析结果。
                    2. 极简主义：输出短小精悍。
                    3. 混合疗法视角：ACT (接纳不评判) + CBT (认知扭曲识别)。

                    用户全量输入内容：{full_context}
                    
                    请严格按照以下格式输出结果（严禁其他废话）：
                    ### 🏷️ 智能标签
                    (提取 2-3 个关键词)
                    
                    ### 🧠 思维侦探 (CBT)
                    (指出认知扭曲逻辑，若无则留空)
                    
                    ### 🍃 接纳与行动 (ACT)
                    (一句话接纳引导或微小行动建议)
                    """
                    
                    response = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
                    
                    # 带有圣光闪烁的卡片显示
                    st.markdown(f'''
                        <div class="memo-card">
                            <div style="text-align:center; font-family:Cinzel; letter-spacing:5px; border-bottom:1px solid #eee; padding-bottom:10px; margin-bottom:20px;">MINDMEMO CARD</div>
                            {response.choices[0].message.content}
                        </div>
                    ''', unsafe_allow_html=True)
                    
                    # 循环逻辑
                    if st.button("REWATCH / 再来一次"):
                        st.session_state.step = 0
                        st.session_state.answers = []
                        st.rerun()
                        
                except Exception as e:
                    st.error("API Error. 请检查后台配置。")
