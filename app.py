import streamlit as st
from openai import OpenAI

# 1. 注入高级电影美学 CSS
st.set_page_config(page_title="Narrative Archaeologist", page_icon="🎞️", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@300;600&display=swap');

    /* 全局胶片底色：并非纯黑，而是带有一点深灰的电影质感 */
    .stApp {
        background-color: #0a0a0a;
        color: #c9ad8d; 
        font-family: 'Noto Serif SC', serif;
    }

    /* 模拟胶片颗粒感的覆盖层 */
    .stApp::before {
        content: " ";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        opacity: 0.03;
        pointer-events: none;
        background-image: url('https://www.transparenttextures.com/patterns/stardust.png');
    }

    /* 隐藏系统组件 */
    header, footer, #MainMenu {visibility: hidden;}

    /* 场景容器 */
    .scene-container {
        padding: 60px 20px;
        text-align: left;
        max-width: 600px;
        margin: 0 auto;
        animation: filmBlurIn 2s ease-out;
    }

    @keyframes filmBlurIn {
        0% { opacity: 0; filter: blur(10px); }
        100% { opacity: 1; filter: blur(0); }
    }

    /* 电影剧本标题样式 */
    .film-header {
        font-size: 0.8rem;
        letter-spacing: 0.5rem;
        text-transform: uppercase;
        color: rgba(201, 173, 141, 0.5);
        margin-bottom: 2rem;
    }

    .question-title {
        font-size: 1.8rem;
        font-weight: 600;
        line-height: 1.4;
        margin-bottom: 1.5rem;
        color: #e0d0bc;
    }

    .question-desc {
        font-size: 1rem;
        color: rgba(201, 173, 141, 0.7);
        line-height: 1.8;
        margin-bottom: 2rem;
    }

    /* 极简输入框：像在剧本上写字 */
    .stTextArea textarea {
        background-color: transparent !important;
        border: none !important;
        border-bottom: 1px solid rgba(201, 173, 141, 0.2) !important;
        color: #f5f5f5 !important;
        font-size: 1.1rem !important;
        border-radius: 0 !important;
        padding: 10px 0 !important;
    }

    /* 进度条：电影拉片感 */
    .progress-bar {
        width: 100%;
        height: 2px;
        background: rgba(201, 173, 141, 0.1);
        margin-bottom: 40px;
    }
    .progress-fill {
        height: 100%;
        background: #c9ad8d;
        box-shadow: 0 0 10px #c9ad8d;
        transition: width 1s ease;
    }

    /* 按钮：电影转场感 */
    .stButton > button {
        background-color: transparent !important;
        color: #c9ad8d !important;
        border: 1px solid #c9ad8d !important;
        padding: 8px 30px !important;
        font-family: 'Noto Serif SC', serif !important;
        letter-spacing: 0.2rem !important;
        font-size: 0.8rem !important;
        margin-top: 30px;
    }

    /* 分析报告样式 */
    .analysis-card {
        background: rgba(255, 255, 255, 0.03);
        border-left: 2px solid #c9ad8d;
        padding: 30px;
        margin: 20px 0;
        line-height: 1.8;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 核心逻辑
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []

# 定义 5 个核心维度
dimensions = [
    {
        "title": "🌱 原生底色",
        "desc": "出生在哪里？童年记忆中最深刻的一个画面是什么？父母的关系以及他们对你的教育方式是怎样的？",
        "label": "SCENE 01: THE ORIGIN"
    },
    {
        "title": "📈 高光与至暗",
        "desc": "从小到大，哪一刻让你觉得自己是世界的中心？又是哪一刻让你感到彻底的羞耻、绝望或无助？",
        "label": "SCENE 02: THE PEAKS & VALLEYS"
    },
    {
        "title": "💊 身体的记号",
        "desc": "你的身体生过什么病？当你压力最大时，身体的哪个部位会先向你报警？",
        "label": "SCENE 03: THE BODY MEMORY"
    },
    {
        "title": "🤝 关键关系人",
        "desc": "谁是你生命中的重要他人？那些让你爱恨交织、甚至深深影响你性格的人是谁？",
        "label": "SCENE 04: THE OTHERS"
    },
    {
        "title": "🔀 转折与执念",
        "desc": "你换过哪些赛道？有没有什么模式是你发誓不想重复，却一直在循环的？",
        "label": "SCENE 05: THE PERSISTENCE"
    }
]

client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")

# --- 场景渲染 ---
if st.session_state.step < len(dimensions):
    dim = dimensions[st.session_state.step]
    
    # 渲染进度条
    progress = (st.session_state.step + 1) / len(dimensions) * 100
    st.markdown(f'<div class="progress-bar"><div class="progress-fill" style="width: {progress}%;"></div></div>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="scene-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="film-header">{dim["label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="question-title">{dim["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="question-desc">{dim["desc"]}</div>', unsafe_allow_html=True)
    
    ans = st.text_area("请如实记录...", height=150, key=f"ans_{st.session_state.step}", label_visibility="collapsed")
    
    if st.button("进入下一幕" if st.session_state.step < 4 else "开始叙事考古"):
        if ans:
            st.session_state.answers.append(ans)
            st.session_state.step += 1
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- 分析报告渲染 ---
else:
    st.markdown('<div class="scene-container">', unsafe_allow_html=True)
    st.markdown('<div class="film-header">FINAL ANALYSIS: RECONSTRUCTION</div>', unsafe_allow_html=True)
    st.markdown('<div class="question-title">系统已完成档案构建</div>', unsafe_allow_html=True)
    
    if st.button("开启您的心理档案"):
        with st.spinner("正在拉片，挖掘潜意识脚本..."):
            all_data = st.session_state.answers
            # 注入你给的硬核 Prompt 逻辑
            analysis_prompt = f"""
            # Role: 心理叙事重构师 (The Narrative Archaeologist)
            ## 核心理念: 你是一面会说话的镜子，通过分析全量数据找出自动化脚本。
            ## 绝对禁令: 禁止行动建议，禁止说教。
            ## 分析目标: 
            用户提供的碎片如下:
            1.原生底色: {all_data[0]}
            2.高光与至暗: {all_data[1]}
            3.身体记号: {all_data[2]}
            4.关键关系: {all_data[3]}
            5.转折执念: {all_data[4]}

            请严格按以下维度输出分析报告，使用深邃、诗意且客观的语言：
            1. **【叙事重构】**：串联关键转折点。
            2. **【核心图式】**：命名底层驱动模式。
            3. **【躯体化标记】**：解读身体与心理关系。
            4. **【未完成的情结】**：挖掘反复出现的执念。
            5. **【觉察时刻】**：提出1-2个直击灵魂的反思问题。
            """
            
            response = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": analysis_prompt}])
            st.markdown(f'<div class="analysis-card">{response.choices[0].message.content}</div>', unsafe_allow_html=True)
            
            if st.button("重启剧本"):
                st.session_state.step = 0
                st.session_state.answers = []
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
