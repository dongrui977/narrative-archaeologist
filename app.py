import streamlit as st
from openai import OpenAI

# 1. 视觉工程：甜品台氛围感 CSS
st.set_page_config(page_title="MindMemo | 心灵甜品台", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@200;500&family=ZCOOL+XiaoWei&display=swap');

    /* 背景：柔和的丝绒米色/奶油色调 */
    .stApp {
        background: radial-gradient(circle at center, #fdf8f2 0%, #f4eae0 100%);
        color: #8c7355;
        font-family: 'Noto Serif SC', serif;
    }

    /* 精灵闪烁动画 */
    .pixie-dust {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        pointer-events: none;
        background-image: radial-gradient(#d4a76c 1px, transparent 1px);
        background-size: 50px 50px;
        animation: sparkle 10s linear infinite;
        opacity: 0.3;
        z-index: 0;
    }
    @keyframes sparkle {
        0% { transform: translateY(0px); opacity: 0.2; }
        50% { opacity: 0.5; }
        100% { transform: translateY(-100px); opacity: 0.2; }
    }

    header, footer, #MainMenu {visibility: hidden;}

    /* 甜品台容器 */
    .dessert-stage {
        text-align: center;
        padding-top: 50px;
        z-index: 1;
        position: relative;
    }

    .dessert-icon {
        font-size: 4rem;
        margin-bottom: 20px;
        filter: drop-shadow(0 10px 15px rgba(140, 115, 85, 0.2));
        animation: float 3s ease-in-out infinite;
    }
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }

    .dessert-title {
        font-family: 'ZCOOL XiaoWei', serif;
        font-size: 2.2rem;
        color: #634d34;
        letter-spacing: 3px;
        margin-bottom: 10px;
    }

    /* 输入框：解决重叠，优雅半透明 */
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.4) !important;
        border: 1px solid rgba(140, 115, 85, 0.1) !important;
        color: #634d34 !important;
        font-size: 1.1rem !important;
        border-radius: 15px !important;
        padding: 20px !important;
        line-height: 1.6 !important;
    }
    .stTextArea textarea:focus {
        background-color: rgba(255, 255, 255, 0.7) !important;
        border: 1px solid #d4a76c !important;
        box-shadow: 0 0 20px rgba(212, 167, 108, 0.2) !important;
    }

    /* 按钮：马卡龙色系按钮 */
    .stButton > button {
        background-color: #8c7355 !important;
        color: #fff !important;
        border-radius: 25px !important;
        border: none !important;
        padding: 10px 40px !important;
        transition: 0.3s;
        box-shadow: 0 4px 15px rgba(140, 115, 85, 0.2) !important;
    }
    .stButton > button:hover {
        background-color: #634d34 !important;
        transform: translateY(-2px);
    }

    /* 结果卡片：骨瓷感 */
    .memo-card {
        background: #fff;
        border: none;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.05);
        color: #634d34;
        line-height: 2;
        margin-top: 30px;
    }
    .memo-card h3 { color: #d4a76c !important; }
    </style>
    <div class="pixie-dust"></div>
    """, unsafe_allow_html=True)

# 2. 会话管理
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []

# 甜品定义
desserts = [
    {"icon": "🍮", "title": "原生底色", "label": "香草焦糖布丁 - 挖掘最柔软的最初记忆"},
    {"icon": "🍰", "title": "高光至暗", "label": "红丝绒蛋糕 - 浓郁的骄傲与深邃的无助"},
    {"icon": "☕", "title": "身体记号", "label": "黑咖啡 - 苦涩中透出的身体警讯"},
    {"icon": "🍬", "title": "重要他人", "label": "手工夹心糖 - 谁是那层让你爱恨交织的糖衣？"},
    {"icon": "🥨", "title": "转折执念", "label": "扭结饼 - 那些发誓不重复却绕不开的圈子"}
]

# 3. 核心流程
if st.session_state.step < len(desserts):
    d = desserts[st.session_state.step]
    st.markdown(f'''
        <div class="dessert-stage">
            <div class="dessert-icon">{d['icon']}</div>
            <div class="dessert-title">{d['title']}</div>
            <p style="opacity:0.7;">{d['label']}</p>
        </div>
    ''', unsafe_allow_html=True)
    
    ans = st.text_area("", key=f"ans_{st.session_state.step}", height=180, label_visibility="collapsed", placeholder="请品尝并记录您的感受...")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("品尝下一款" if st.session_state.step < 4 else "封存今日甜品"):
            if ans:
                st.session_state.answers.append(ans)
                st.session_state.step += 1
                st.rerun()
else:
    st.markdown('<div class="dessert-stage"><div class="dessert-icon">🥨</div><div class="dessert-title">甜品台已撤餐</div></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("查看您的心理卡片"):
            with st.spinner("MindMemo 引擎分析中..."):
                try:
                    client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
                    full_context = "\n".join(st.session_state.answers)
                    
                    prompt = f"""
                    你是一个名为 "MindMemo" 的后台心理分析引擎。
                    任务：对输入进行“静默分析”，生成结构化的“心理卡片”。
                    要求：去聊天化、极简主义、结合 ACT 与 CBT。分析以下生命数据：{full_context}
                    
                    输出格式（严禁多余文字）：
                    ### 🏷️ 智能标签
                    ### 🧠 思维侦探
                    ### 🍃 接纳与行动
                    """
                    
                    response = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
                    st.markdown(f'<div class="memo-card">{response.choices[0].message.content}</div>', unsafe_allow_html=True)
                    
                    # 循环逻辑：回到开头
                    if st.button("重新入座 (再次游玩)"):
                        st.session_state.step = 0
                        st.session_state.answers = []
                        st.rerun()
                except Exception as e:
                    st.error("引擎暂时休息，请刷新。")
