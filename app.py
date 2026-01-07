import streamlit as st
from openai import OpenAI

# 1. 顶级视觉工程：电影胶卷与大荧幕质感
st.set_page_config(page_title="MindMemo", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;500&display=swap');

    /* 银幕背景：动态光影与胶片颗粒 */
    .stApp {
        background: radial-gradient(circle at center, #1a1a1a 0%, #050505 100%);
        color: #d4a76c;
        font-family: 'Noto Sans SC', sans-serif;
    }
    .stApp::after {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: url('https://www.transparenttextures.com/patterns/stardust.png');
        opacity: 0.05;
        pointer-events: none;
    }

    /* 隐藏杂项 */
    header, footer, #MainMenu {visibility: hidden;}

    /* 胶卷容器 */
    .film-reel {
        border-top: 15px dashed #333;
        border-bottom: 15px dashed #333;
        padding: 40px 0;
        margin: 20px 0;
        background: rgba(255, 255, 255, 0.02);
    }

    /* 输入框：彻底透明，发光字体 */
    .stTextArea textarea {
        background-color: transparent !important;
        border: none !important;
        color: #e0d0bc !important;
        font-size: 1.4rem !important;
        text-align: center !important;
        line-height: 1.8 !important;
        text-shadow: 0 0 10px rgba(212, 167, 108, 0.4);
    }

    /* 按钮：电影开场感 */
    .stButton > button {
        background-color: #8c2a2a !important;
        color: white !important;
        border: none !important;
        width: 100%;
        letter-spacing: 10px;
        font-weight: bold;
        padding: 15px 0 !important;
        box-shadow: 0 0 20px rgba(140, 42, 42, 0.4);
    }

    /* 心理卡片样式 */
    .memo-card {
        background: #fdfdfd;
        color: #1a1a1a;
        padding: 25px;
        border-radius: 2px;
        box-shadow: 10px 10px 0px #8c2a2a;
        font-family: 'serif';
        margin-top: 20px;
    }
    .memo-card h3 { color: #8c2a2a !important; border: none !important; margin-bottom: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. 会话管理
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []

questions = [
    "第一帧：🌱 原生底色（童年、父母、最初的记忆碎片）",
    "第二帧：📈 高光与至暗（最骄傲与最无助的时刻）",
    "第三帧：💊 身体记号（压力下的疼痛、成瘾或慢性病）",
    "第四帧：🤝 关键关系（爱恨交织的那个“重要他人”）",
    "第五帧：🔀 转折与执念（反复坠入的某种行为模式）"
]

# 3. 渲染交互
if st.session_state.step < len(questions):
    st.markdown(f"<div style='text-align:center; opacity:0.5; letter-spacing:3px;'>SCENE {st.session_state.step + 1} / 5</div>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align:center;'>{questions[st.session_state.step]}</h2>", unsafe_allow_html=True)
    
    st.markdown('<div class="film-reel">', unsafe_allow_html=True)
    ans = st.text_area("", key=f"f_{st.session_state.step}", height=200, label_visibility="collapsed", placeholder="在此刻录您的记忆...")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("NEXT FRAME"):
        if ans:
            st.session_state.answers.append(ans)
            st.session_state.step += 1
            st.rerun()
else:
    st.markdown("<h2 style='text-align:center;'>所有胶卷已冲洗完成</h2>", unsafe_allow_html=True)
    if st.button("生成分析卡片"):
        with st.spinner("MindMemo 引擎正在进行静默分析..."):
            try:
                client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
                
                # 严格执行你的 Prompt 逻辑
                full_context = "\n".join(st.session_state.answers)
                prompt = f"""
                你是一个名为 "MindMemo" 的后台心理分析引擎。
                任务：对输入进行“静默分析”，生成结构化的“心理卡片”。
                核心原则：去聊天化、极简主义、结合 ACT 与 CBT。

                用户全量数据：{full_context}

                请按以下格式精准输出，严禁废话：
                ---
                ### 🏷️ 智能标签
                (2-3个标签)

                ### 🧠 思维侦探 (CBT视角)
                (识别认知扭曲，指出具体逻辑谬误，若无则留空)

                ### 🍃 接纳与行动 (ACT视角)
                (一句微小的、立刻能做的行动建议)
                ---
                """
                
                response = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
                st.markdown(f'<div class="memo-card">{response.choices[0].message.content}</div>', unsafe_allow_html=True)
                
                if st.button("重启放映机"):
                    st.session_state.step = 0
                    st.session_state.answers = []
                    st.rerun()
            except Exception as e:
                st.error("引擎暂时离线，请稍后再试。")
