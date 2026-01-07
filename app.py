import streamlit as st
from openai import OpenAI

# 1. 强力视觉覆盖：彻底黑场，琥珀发光字
st.set_page_config(page_title="Narrative Archaeologist", layout="centered")

st.markdown("""
    <style>
    /* 彻底黑场 */
    .stApp { background-color: #000000; color: #d4a76c; font-family: sans-serif; }
    header, footer, #MainMenu {visibility: hidden;}

    /* 输入框整容：无框、无白底、琥珀色字 */
    .stTextArea textarea {
        background-color: transparent !important;
        border: none !important;
        border-bottom: 1px solid #333 !important;
        color: #d4a76c !important; /* 修正：输入字也显示琥珀色 */
        font-size: 1.2rem !important;
        text-align: center !important;
        border-radius: 0 !important;
    }
    .stTextArea textarea:focus {
        border-bottom: 1px solid #d4a76c !important;
        box-shadow: none !important;
    }

    /* 进度条：极致简约 */
    .stProgress > div > div > div > div { background-color: #d4a76c; }

    /* 按钮：深红色的“封存”感 */
    .stButton > button {
        background-color: transparent !important;
        color: #d4a76c !important;
        border: 1px solid #d4a76c !important;
        width: 100%;
        letter-spacing: 5px;
        transition: 0.3s;
    }
    .stButton > button:hover { background-color: #d4a76c !important; color: #000 !important; }

    /* 结果区：干净利落 */
    .result-text {
        color: #f0f0f0;
        line-height: 1.6;
        padding: 20px;
        border-left: 2px solid #d4a76c;
        background: #111;
        font-family: monospace;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 流程控制
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []

questions = [
    {"q": "🌱 原生底色", "d": "出生地、童年最深刻画面、父母教育方式。"},
    {"q": "📈 高光与至暗", "d": "什么时候觉得自己最行？什么时候感到最无助羞耻？"},
    {"q": "💊 身体记号", "d": "慢性病、长期疼痛。压力大时身体哪里先难受？"},
    {"q": "🤝 重要他人", "d": "谁对你爱恨交织？谁在深层影响你的性格？"},
    {"q": "🔀 转折与执念", "d": "换过什么赛道？有什么坑是你反复掉进去的？"}
]

# 3. 渲染
if st.session_state.step < len(questions):
    # 顶部极简进度
    st.progress((st.session_state.step + 1) / len(questions))
    
    st.write(f"### {questions[st.session_state.step]['q']}")
    st.write(f"*{questions[st.session_state.step]['d']}*")
    
    ans = st.text_area("", key=f"q_{st.session_state.step}", height=150, label_visibility="collapsed")
    
    if st.button("NEXT"):
        if ans:
            st.session_state.answers.append(ans)
            st.session_state.step += 1
            st.rerun()
else:
    st.write("### 档案构建完成")
    if st.button("读取考古报告"):
        with st.spinner("剥离冗余信息，直达本质..."):
            client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
            
            # 修正：精简、脱水、无废话的 Prompt
            prompt = f"""
            你是一位毒舌、冷静且精准的心理叙事重构师。
            数据碎片：1.原生:{st.session_state.answers[0]} 2.起伏:{st.session_state.answers[1]} 3.身体:{st.session_state.answers[2]} 4.他人:{st.session_state.answers[3]} 5.模式:{st.session_state.answers[4]}
            
            要求：
            1. 拒绝文艺、拒绝废话、拒绝安慰。
            2. 直接给出以下5个维度的硬核分析（每项不超过30字）：
            - 【逻辑链】：串联行为背后的逻辑。
            - 【底层驱动】：命名他的核心脚本（如：渴望被认可的讨好者）。
            - 【身体信号】：指出压力在身体的投射。
            - 【执念本质】：一句话揭穿他的反复失败。
            - 【灵魂拷问】：提出一个让他无法回避的问题。
            """
            
            try:
                response = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
                st.markdown(f'<div class="result-text">{response.choices[0].message.content}</div>', unsafe_allow_html=True)
                if st.button("RESET"):
                    st.session_state.step = 0
                    st.session_state.answers = []
                    st.rerun()
            except Exception as e:
                st.error("连接超时。")
