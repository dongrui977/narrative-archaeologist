import streamlit as st
from openai import OpenAI

# 1. 视觉配置：高级可爱、3D 拟物化、极简甜点
st.set_page_config(page_title="MindMemo | Sweet Archive", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=ZCOOL+XiaoWei&family=Noto+Serif+SC:wght@300;500&display=swap');

    /* 全局背景：奶油色调，极简高级 */
    .stApp {
        background-color: #FFFDF9;
        color: #5D4037;
        font-family: 'Noto Serif SC', serif;
    }

    header, footer, #MainMenu {visibility: hidden;}

    /* 甜点档案馆主容器 */
    .dessert-card {
        background: #FFFFFF;
        border-radius: 40px;
        padding: 60px 50px;
        box-shadow: 20px 20px 60px rgba(93, 64, 55, 0.05), -20px -20px 60px #ffffff;
        text-align: center;
        margin-top: 40px;
        position: relative;
        border: 1px solid rgba(212, 167, 108, 0.1);
    }

    /* 精灵指引：闪烁的小光点 */
    .sprite {
        width: 15px;
        height: 15px;
        background: radial-gradient(circle, #D4A76C 0%, transparent 70%);
        border-radius: 50%;
        margin: 0 auto 20px auto;
        animation: spriteFloat 2s ease-in-out infinite;
        box-shadow: 0 0 15px #D4A76C;
    }
    @keyframes spriteFloat {
        0%, 100% { transform: translateY(0) scale(1); opacity: 0.6; }
        50% { transform: translateY(-10px) scale(1.2); opacity: 1; }
    }

    .title-text {
        font-family: 'ZCOOL XiaoWei', serif;
        font-size: 2.2rem;
        letter-spacing: 4px;
        color: #D4A76C;
        margin-bottom: 30px;
    }

    /* 输入区域：圆润、软绵绵的质感 */
    .stTextArea textarea {
        background-color: #FFFDF9 !important;
        border: 2px solid #F3E5DC !important;
        color: #5D4037 !important;
        font-size: 1.15rem !important;
        text-align: center !important;
        border-radius: 25px !important;
        padding: 25px !important;
        transition: all 0.3s ease;
    }
    .stTextArea textarea:focus {
        border-color: #D4A76C !important;
        background-color: #FFFFFF !important;
        box-shadow: 0 10px 20px rgba(212, 167, 108, 0.1) !important;
    }

    /* 按钮：马卡龙色块 */
    .stButton > button {
        background: linear-gradient(135deg, #F3E5DC 0%, #E8D1C5 100%) !important;
        color: #5D4037 !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 12px 60px !important;
        font-weight: 500 !important;
        letter-spacing: 2px;
        transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        margin-top: 30px;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 15px 30px rgba(212, 167, 108, 0.15) !important;
    }

    /* 圣光闪烁卡片：全息珍珠质感 */
    .holographic-card {
        background: #FFFFFF;
        padding: 50px;
        border-radius: 35px;
        border: 2px solid #FFF;
        box-shadow: 0 20px 50px rgba(0,0,0,0.05);
        position: relative;
        animation: holoShimmer 5s linear infinite;
        text-align: left;
    }
    @keyframes holoShimmer {
        0% { border-color: #F3E5DC; }
        33% { border-color: #D4A76C; }
        66% { border-color: #A9C9D3; }
        100% { border-color: #F3E5DC; }
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 会话管理
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []

scenes = [
    {"icon": "🍮", "title": "原生底色", "q": "童年记忆里，那个最让你安心的味道或画面是什么？"},
    {"icon": "🍰", "title": "闪光时刻", "q": "哪一刻，你觉得自己像缀满珍珠的蛋糕般耀眼？"},
    {"icon": "🌑", "title": "至暗瞬间", "q": "有没有什么时候，生活让你尝到了烧焦般的苦涩？"},
    {"icon": "🌡️", "title": "身体警报", "q": "当你感到压力时，身体哪个部位会先向你发出信号？"},
    {"icon": "🤝", "title": "重要他人", "q": "那个人对你性格的影响，更像哪种甜味的层次？"},
    {"icon": "🌀", "title": "循环怪圈", "q": "有什么不爽的套路，是你一直在‘复读’运行的？"}
]

# 3. 逻辑渲染
if st.session_state.step < len(scenes):
    s = scenes[st.session_state.step]
    
    st.markdown(f'''
        <div class="dessert-card">
            <div class="sprite"></div>
            <div style="font-size: 4rem; margin-bottom: 10px;">{s['icon']}</div>
            <div class="title-text">{s['title']}</div>
            <p style="color: #A9C9D3; letter-spacing: 3px; font-weight: bold;">STAGE 0{st.session_state.step + 1}</p>
            <h3 style="margin-top: 20px; font-weight: 300;">{s['q']}</h3>
        </div>
    ''', unsafe_allow_html=True)
    
    ans = st.text_area("", key=f"f_{st.session_state.step}", height=150, label_visibility="collapsed", placeholder="记录您的真实叙事...")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("品尝下一幕"):
            if ans:
                st.session_state.answers.append(ans)
                st.session_state.step += 1
                st.rerun()

else:
    st.markdown('<div class="title-text" style="text-align:center; margin-top:100px;">打包完成</div>', unsafe_allow_html=True)
    
    if st.button("开启您的心理卡片"):
        with st.spinner("MindMemo 正在提取认知脚本..."):
            try:
                client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
                full_context = "\n".join(st.session_state.answers)
                
                prompt = f"""
                你是一个名为 "MindMemo" 的心理分析引擎。
                任务：生成极其简短、深刻的“心理卡片”。分析：{full_context}
                格式要求（严禁废话）：
                ### 🏷️ 智能标签
                ### 🧠 思维侦探 (CBT)
                ### 🍃 接纳与行动 (ACT)
                """
                
                response = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
                
                st.markdown(f'''
                    <div class="holographic-card">
                        <div style="text-align:center; font-family:ZCOOL XiaoWei; color:#D4A76C; border-bottom:1px dashed #F3E5DC; padding-bottom:15px; margin-bottom:20px;">MINDMEMO REPORT</div>
                        {response.choices[0].message.content}
                    </div>
                ''', unsafe_allow_html=True)
                
                # 循环重置
                if st.button("重新入座 🔄"):
                    st.session_state.step = 0
                    st.session_state.answers = []
                    st.rerun()
                    
            except Exception as e:
                st.error("余额不足或连接失败。")
