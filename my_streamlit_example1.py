import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

st.title('🦜🔗 中文小故事生成器')

with st.sidebar:
    st.subheader('API 配置')
    api_key = st.text_input(
        'Deepseek API Key',
        value=st.secrets.get("Deepseek_API_KEY", ""),
        type='password',
        help='请输入您的 Deepseek API Key'
    )

prompt = ChatPromptTemplate.from_template("请编写一篇关于{topic}的中文小故事，不超过100字")

try:
    if not api_key:
        st.warning('请在侧边栏输入您的 Deepseek API Key')
        st.stop()
    
    model = ChatOpenAI(
        base_url="https://api.deepseek.com/v1",
        api_key=api_key,
        model="deepseek-chat",
        temperature=0.8
    )
    chain = prompt | model

    with st.form('my_form'):
        text = st.text_area('输入主题关键词:', '小白兔')
        submitted = st.form_submit_button('提交')
        if submitted:
            with st.spinner('正在生成故事...'):
                response = chain.invoke({"topic": text})
                st.info(response.content)
                
except Exception as e:
    st.error(f'发生错误: {str(e)}')