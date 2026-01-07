import streamlit as st
from openai import OpenAI

# 1. 高级视觉定义：奢华暗黑胶片
st.set_page_config(page_title="MindMemo | 叙事档案馆", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@200;500&display=swap');

    /* 全局背景：丝绒黑与动态暗光 */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #1a1a1a 0%, #050505 100%);
        color: #d4a76c;
        font-family: 'Noto Serif SC', serif;
    }

    /* 隐藏杂项 */
    header, footer, #MainMenu {visibility: hidden;}

    /* 奢华输入容器：悬浮感 */
    .input-stage {
        max-width: 800px;
        margin: 100px auto;
        text-align: center;
        animation: fadeInBlur 2s ease-out;
    }

    @keyframes fadeInBlur {
        0% { opacity: 0; filter: blur(10px); transform: translateY(20px); }
        100% { opacity: 1; filter: blur(0); transform: translateY(0); }
    }

    /* 标题：奢华琥珀金 */
    .scene-label {
        letter-spacing: 0.5rem;
        font-size: 0.9rem;
        color: rgba(212, 167, 108, 0.4);
        margin-bottom: 2rem;
    }

    .scene-title {
        font-size: 2.2rem;
        font-weight: 200;
        margin-bottom: 3rem;
        text-shadow: 0 0 20px rgba(212, 167, 108, 0.2);
    }

    /* 输入区域：彻底无感化 */
    .stTextArea textarea {
        background: transparent !important;
        border: none !important;
        border-bottom: 1px solid rgba(212, 167, 108, 0.2) !important;
        color: #f5f5f5 !important;
        font-size: 1.5rem !important;
        text-align: center !important;
        border-radius: 0 !important;
        padding: 20px !important;
    }
    .stTextArea textarea:focus {
        border-bottom: 1px solid #d4a76c !important;
        box-shadow: none !important;
    }

    /* 按钮：金属光泽 */
    .stButton > button {
        background: transparent !important;
        color: #d4a76c !important;
        border: 1px solid rgba(212, 167, 108, 0.5) !important;
        padding: 12px 60px !important;
        letter-spacing: 5px !important;
        font-size: 0.8rem !important;
        transition: 0.8s;
        margin-top: 50px;
    }
    .stButton > button:hover {
        border-color: #d4a76c !important;
        box-shadow: 0 0 30px rgba(212, 167, 108, 0.3);
        transform: scale(1.05);
    }

    /* flomo 式奢华卡片 */
    .memo-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(212, 167, 108, 0.1);
        backdrop-filter: blur(20px);
        padding: 40px;
        border-radius: 4px;
        margin: 20px auto;
        max-width: 600px;
        line-height: 2;
        color: #eee;
        position: relative;
        overflow: hidden;
    }
    .memo-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 4px; height: 100%;
        background: #d4a76c;
    }
    .memo-card h3 { color: #d4a76c !important; font-size: 1.1rem !important; margin-bottom: 20px !important;}
    </style>
    """, unsafe_allow_html=True)

# 2. 会话管理
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []

scenes = [
    {"label": "STAGE 01", "title": "🌱 原生底色"},
    {"label": "STAGE 02", "title": "📈 高光与至暗"},
    {"label": "STAGE 03", "title": "💊 身体记号"},
    {"label": "STAGE 04", "title": "🤝 关键关系"},
    {"label": "STAGE 05", "title": "🔀 转折与执念"}
]

# 3. 核心流程
if st.session_state.step < len(scenes):
    scene = scenes[st.session_state.step]
    st.markdown(f'''
        <div class="input-stage">
            <div class="scene-label">{scene['label']}</div>
            <div class="scene-title">{scene['title']}</div>
        </div>
    ''', unsafe_allow_html=True)
    
    ans = st.text_area("", key=f"ans_{st.session_state.step}", height=200, label_visibility="collapsed", placeholder=". . . .")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("继续刻录" if st.session_state.step < 4 else "开启档案馆"):
            if ans:
                st.session_state.answers.append(ans)
                st.session_state.step += 1
                st.rerun()

else:
    st.markdown('<div class="input-stage"><div class="scene-title">档案已封存</div></div>', unsafe_allow_html=True)
    
    if st.button("读取卡片"):
        with st.spinner("MindMemo 引擎分析中..."):
            try:
                client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
                full_context = "\n".join(st.session_state.answers)
                
                prompt = f"""
                你是一个名为 "MindMemo" 的后台心理分析引擎。
                任务：对输入进行“静默分析”，生成结构化的“心理卡片”。
                原则：去聊天化、极简、ACT + CBT 视角。
                
                输入：{full_context}
                
                格式：
                ### 🏷️ 智能标签
                ### 🧠 思维侦探 (CBT)
                ### 🍃 接纳与行动 (ACT)
                """
                
                response = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
                st.markdown(f'<div class="memo-card">{response.choices[0].message.content}</div>', unsafe_allow_html=True)
                
                if st.button("重启放映"):
                    st.session_state.step = 0
                    st.session_state.answers = []
                    st.rerun()
            except Exception as e:
                st.error("API 调用失败，请检查余额。")
