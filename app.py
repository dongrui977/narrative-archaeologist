import streamlit as st
from openai import OpenAI

# 1. 视觉黑科技：韦斯·安德森色调 + 3D 拟物化
st.set_page_config(page_title="MindMemo | 灵魂扭蛋机", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=ZCOOL+XiaoWei&display=swap');

    /* 全局背景：复古薄荷绿与奶油粉 */
    .stApp {
        background: #F4EAE0;
        background-image: radial-gradient(#D4A373 1px, transparent 1px);
        background-size: 30px 30px;
        color: #6B705C;
    }

    header, footer, #MainMenu {visibility: hidden;}

    /* 3D 扭蛋球样式 */
    .gacha-ball {
        width: 120px;
        height: 120px;
        background: linear-gradient(135deg, #FFB5A7 0%, #FF8FAB 100%);
        border-radius: 50%;
        margin: 40px auto;
        box-shadow: inset -10px -10px 20px rgba(0,0,0,0.1), 10px 20px 30px rgba(255, 143, 171, 0.3);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3rem;
        animation: bob 3s ease-in-out infinite;
    }

    @keyframes bob {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-20px); }
    }

    /* 复古电影感容器 */
    .machine-case {
        background: #FFFFFF;
        border: 8px solid #FFB5A7;
        border-radius: 40px;
        padding: 50px 30px;
        box-shadow: 0 30px 0px #F6BD60;
        text-align: center;
    }

    .step-title {
        font-family: 'ZCOOL XiaoWei', serif;
        font-size: 2rem;
        color: #E76F51;
        letter-spacing: 2px;
        margin-bottom: 20px;
    }

    /* 输入框：干净的高级感 */
    .stTextArea textarea {
        background-color: #FDFCF0 !important;
        border: 2px solid #FFB5A7 !important;
        border-radius: 20px !important;
        color: #6B705C !important;
        font-size: 1.1rem !important;
        padding: 20px !important;
    }

    /* 按钮：像投币口的按钮 */
    .stButton > button {
        background-color: #E76F51 !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 15px 50px !important;
        font-weight: bold !important;
        box-shadow: 0 8px 0px #A24936;
        transition: 0.1s;
    }
    .stButton > button:active {
        transform: translateY(4px);
        box-shadow: 0 4px 0px #A24936;
    }

    /* 圣光闪烁卡片：像刚抽出来的手办卡 */
    .soul-card {
        background: #FFFFFF;
        border: 2px solid #E76F51;
        padding: 40px;
        border-radius: 20px;
        position: relative;
        animation: sparkleGlow 2s infinite alternate;
    }

    @keyframes sparkleGlow {
        from { box-shadow: 0 0 10px rgba(231, 111, 81, 0.2); }
        to { box-shadow: 0 0 40px rgba(231, 111, 81, 0.6), 0 0 20px rgba(246, 189, 96, 0.4); }
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 会话状态
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []

scenes = [
    {"icon": "🥚", "title": "原生底色", "q": "你的童年记忆里，哪一个瞬间像还没打开的彩蛋？"},
    {"icon": "✨", "title": "闪光碎片", "q": "哪一次成就感，让你觉得自己全身涂满了亮粉？"},
    {"icon": "🏚️", "title": "至暗角落", "q": "哪一段经历，像掉漆的零件一样让你想藏起来？"},
    {"icon": "⚡", "title": "身体电流", "q": "压力大时，身体哪个部位在闪烁预警？"},
    {"icon": "🎎", "title": "重要镜像", "q": "谁是那个深刻影响你，让你又爱又怕的‘限定款’？"},
    {"icon": "♾️", "title": "循环脚本", "q": "有什么不爽的套路，是你一直在‘复读’运行的？"}
]

# 3. 游戏化流程
if st.session_state.step < len(scenes):
    s = scenes[st.session_state.step]
    
    st.markdown(f'''
        <div class="machine-case">
            <div class="gacha-ball">{s['icon']}</div>
            <div class="step-title">{s['title']}</div>
            <p style="opacity:0.6;">INSERT COIN FOR SCENE 0{st.session_state.step + 1}</p>
            <h3 style="margin: 20px 0;">{s['q']}</h3>
        </div>
    ''', unsafe_allow_html=True)
    
    ans = st.text_area("", key=f"gacha_{st.session_state.step}", height=120, label_visibility="collapsed", placeholder="请投入您的记忆硬币...")
    
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        if st.button("扭转旋钮，进入下一关"):
            if ans:
                st.session_state.answers.append(ans)
                st.session_state.step += 1
                st.rerun()

else:
    st.markdown('<div class="step-title" style="text-align:center; margin-top:50px;">扭蛋机已停止运行</div>', unsafe_allow_html=True)
    
    if st.button("查看我的灵魂手办卡 🎫"):
        with st.spinner("正在注塑、喷漆、重构叙事中..."):
            try:
                client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
                full_context = "\n".join(st.session_state.answers)
                
                # 执行硬核 MindMemo 引擎
                prompt = f"""
                你是一个名为 "MindMemo" 的后台分析引擎。
                任务：根据输入生成一张极其深刻、极简的“灵魂手办卡”。
                输入：{full_context}
                格式：
                ### 🏷️ 灵魂标签
                ### 🧠 脚本监测 (CBT)
                ### 🍃 进化指南 (ACT)
                """
                
                response = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
                
                st.markdown(f'''
                    <div class="soul-card">
                        <div style="text-align:center; font-family:ZCOOL XiaoWei; font-size:1.5rem; color:#E76F51; margin-bottom:20px;">📜 灵魂限定档案</div>
                        {response.choices[0].message.content}
                    </div>
                ''', unsafe_allow_html=True)
                
                # 循环
                if st.button("再投一次币 🔄"):
                    st.session_state.step = 0
                    st.session_state.answers = []
                    st.rerun()
                    
            except Exception as e:
                st.error("机器卡币了，请刷新重试。")
