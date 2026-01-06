import streamlit as st
import time
import google.generativeai as genai

# --- 1. 页面配置与王家卫风格 CSS ---
st.set_page_config(page_title="私人叙事档案馆", page_icon="🎞️")

st.markdown("""
    <style>
    .stApp { background-color: #0a0a0a; color: #d4a373; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea { 
        background-color: transparent; color: #d4a373; border-color: #7f5539; border-radius: 0; 
    }
    .stButton>button { background-color: transparent; color: #d4a373; border: 1px solid #7f5539; width: 100%; }
    .stButton>button:hover { background-color: #7f5539; color: white; }
    .scene-label { color: #7f5539; font-size: 0.8rem; letter-spacing: 0.2em; margin-bottom: 20px; }
    h3 { font-weight: 300; line-height: 1.6; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 剧本数据库 ---
SCENES = [
    {"id": 0, "label": "PROLOGUE", "text": "“所有的记忆都是潮湿的。我们以为自己在往前走，其实只是在不同的旧剧本里，换了套衣裳，重新登场。”", "btn": "转动放映机"},
    {"id": 1, "label": "SCENE 01: 底色", "text": "回到最初。在你还像一张白纸的时候，那个最初的画面里，光线是亮的还是暗的？父母是并排坐着，还是隔着距离？", "btn": "存入底片"},
    {"id": 2, "label": "SCENE 02: 光影", "text": "人的一生总有两次剧烈曝光。一次让你觉得万物皆为你而生，一次让你恨不得原地消散。那两个瞬间，分别发生在哪里？", "btn": "存入底片"},
    {"id": 3, "label": "SCENE 03: 记号", "text": "身体是不会撒谎的。当你撑不住的时候，哪个部位会先替你哭泣？你和你的痛苦，相处多久了？", "btn": "存入底片"},
    {"id": 4, "label": "SCENE 04: 幽灵", "text": "谁是你生命里那个‘避不开的幽灵’？如果此时你们再次对视，你会想逃跑，还是想拥抱？", "btn": "存入底片"},
    {"id": 5, "label": "SCENE 05: 轮回", "text": "这是最后一页。你发誓不再重复，可为什么有些模式总在深夜里回头？那个生锈的梦，还在吗？", "btn": "封存档案"}
]

# --- 3. 核心交互逻辑 ---
if 'stage' not in st.session_state:
    st.session_state.stage = 0
if 'archive_data' not in st.session_state:
    st.session_state.archive_data = {}

if st.session_state.stage <= 5:
    current = SCENES[st.session_state.stage]
    st.markdown(f"<div class='scene-label'>{current['label']}</div>", unsafe_allow_html=True)
    st.markdown(f"### {current['text']}")

    if st.session_state.stage > 0:
        user_input = st.text_area("输入你的独白...", key=f"text_{st.session_state.stage}", height=150)
        if st.button(current['btn']):
            if user_input:
                st.session_state.archive_data[current['label']] = user_input
                st.session_state.stage += 1
                st.rerun()
    else:
        if st.button(current['btn']):
            st.session_state.stage = 1
            st.rerun()

# --- 4. 结尾：接入 AI 重构报告 ---
else:
    st.markdown("<div class='scene-label'>EPILOGUE: THE RECONSTRUCTION</div>", unsafe_allow_html=True)
    
    if "report" not in st.session_state:
        with st.spinner('正在分析潜意识脚本...'):
            try:
                # 从 Secrets 读取 API KEY
                api_key = st.secrets["GEMINI_API_KEY"]
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                user_data = "\n".join([f"{k}: {v}" for k, v in st.session_state.archive_data.items()])
                prompt = f"你是一位心理叙事重构师。基于以下碎片进行深度分析，禁止给建议，禁止说教，需深挖根源。格式包含：【叙事重构】【核心图式】【躯体化标记】【未完成的情结】【觉察时刻】。碎片内容：\n{user_data}"
                
                response = model.generate_content(prompt)
                st.session_state.report = response.text
            except Exception as e:
                st.error("档案库连接失败，请检查 API Key 配置。")

    if "report" in st.session_state:
        st.markdown(st.session_state.report)
        if st.button("重新开启一段对话"):
            st.session_state.stage = 0
            st.session_state.archive_data = {}
            del st.session_state.report
            st.rerun()
