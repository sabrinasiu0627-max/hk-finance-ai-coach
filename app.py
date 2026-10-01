import streamlit as st
import pandas as pd
import time
from huggingface_hub import InferenceClient

# 網頁基本設定
st.set_page_config(page_title="HK Finance AI Coach", page_icon="", layout="wide")

# 極致清晰 Apple 黑白風 CSS (已隱藏 number_input 的加減按鈕)
st.markdown("""
<style>
    /* 全局純白背景與深黑清晰字體 */
    .stApp {
        background-color: #FFFFFF !important;
        color: #111111 !important;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", Arial, sans-serif;
    }
    
    /* 文字、標題與標籤顏色鎖死清晰 */
    h1, h2, h3, h4, h5, h6, p, label, span, div {
        color: #111111;
    }

    /* 徹底修正反白選取顏色 */
    ::selection {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }

    /* 側邊欄風格 */
    [data-testid="stSidebar"] {
        background-color: #FBFBFD !important;
        border-right: 1px solid #D2D2D7 !important;
    }
    [data-testid="stSidebar"] * {
        color: #111111 !important;
    }

    /* 數據儀表板數字與標籤 */
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
        color: #111111 !important;
        border-right: 1px solid #D2D2D7
    }

    /* Apple 框線卡片：白底填色 + 黑色幼線外框 */
    .apple-card {
        border: 1px solid #111111;
        background-color: #FFFFFF;
        padding: 24px;
        border-radius: 12px;
        margin-bottom: 24px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
    }
    .apple-card * {
        color: #111111 !important;
    }

    /* 修正 Code 區塊與 Highlight 顏色 */
    code, pre {
        background-color: #F1F1F3 !important;
        color: #111111 !important;
        border-radius: 6px;
        padding: 2px 6px;
    }

    /* === 按鈕設定：未 hover 前純白底 + 黑色幼邊框；Hover 時極淺灰 === */
    div.stButton > button, 
    div.stFormSubmitButton > button {
        background-color: #FFFFFF !important;
        color: #111111 !important;
        border: 1px solid #111111 !important;
        border-radius: 8px !important;
        padding: 0.5rem 1.2rem !important;
        font-weight: 500 !important;
        box-shadow: none !important;
        outline: none !important;
        transition: all 0.2s ease !important;
    }
    
    div.stButton > button:hover, 
    div.stFormSubmitButton > button:hover {
        background-color: #F5F5F7 !important;
        color: #111111 !important;
        border: 1px solid #111111 !important;
        box-shadow: none !important;
    }
    
    div.stButton > button:focus, 
    div.stButton > button:active,
    div.stFormSubmitButton > button:focus, 
    div.stFormSubmitButton > button:active {
        background-color: #FFFFFF !important;
        color: #111111 !important;
        border: 1px solid #111111 !important;
        box-shadow: none !important;
        outline: none !important;
    }

    /* 側邊欄與主畫面 Expander 樣式 */
    [data-testid="stExpander"] {
        border: 1px solid #D2D2D7 !important;
        border-radius: 8px !important;
        background-color: #FFFFFF !important;
        margin-bottom: 10px;
    }
    [data-testid="stExpander"] summary {
        background-color: #FFFFFF !important;
        color: #111111 !important;
        border-radius: 8px !important;
    }
    [data-testid="stExpander"] summary:hover {
        background-color: #F5F5F7 !important;
        color: #111111 !important;
    }
    [data-testid="stExpander"] summary * {
        color: #111111 !important;
    }

    /* 輸入框幼線設計與隱藏數字輸入框的上下加減按鈕 (Spinners) */
    input, textarea, select {
        border: 1px solid #D2D2D7 !important;
        border-radius: 8px !important;
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    input:focus {
        border-color: #000000 !important;
        box-shadow: none !important;
    }
    input[type="number"]::-webkit-inner-spin-button,
    input[type="number"]::-webkit-outer-spin-button {
        -webkit-appearance: none !important;
        margin: 0 !important;
    }
    input[type="number"] {
        -moz-appearance: textfield !important;
    }

    /* 極細分隔線 */
    hr {
        border: none;
        height: 1px;
        background-color: #D2D2D7;
        margin: 2.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

st.title("HK Finance AI 理財教練")
st.write("結合個人資產數據與智能分析的極簡理財系統。")

default_hf_token = "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"

with st.sidebar:
    st.header("系統設定")
    api_key = st.text_input("Hugging Face Token", value=default_hf_token, type="password")

if api_key:
    client = InferenceClient(api_key=api_key)
else:
    st.warning("請輸入你的 Hugging Face Token。")

st.sidebar.header("客戶理財檔案")

with st.sidebar.expander("1. 基本資料", expanded=False):
    age = st.text_input("年齡", "")
    occupation = st.text_input("職業", "")
    
with st.sidebar.expander("2. 薪金與現金流 (MPF自動計算)", expanded=True):
    salary_before_mpf = st.number_input("每月薪金（MPF前 HKD）", value=0, step=1000)
    
    # 香港 MPF 自動計算邏輯：5% 供款，最高入息水平 $30,000 對應上限 $1,500
    mpf_deduction = min(salary_before_mpf * 0.05) if salary_before_mpf >= 7100 else 0
    salary_after_mpf = salary_before_mpf - mpf_deduction
    
    st.caption(f"自動計算 MPF 扣除: ${mpf_deduction:,.0f}")
    st.markdown(f"**實收薪金 (MPF後): ${salary_after_mpf:,.0f}**")
    
    monthly_expense = st.number_input("每月總開支 (HKD)", value=0, step=500)
    monthly_saving = salary_after_mpf - monthly_expense
    st.info(f"自動計算每月淨儲蓄: ${monthly_saving:,.0f}")

with st.sidebar.expander("3. 資產與負債", expanded=True):
    bank_balance = st.number_input("銀行戶口及餘額 (HKD)", value=0)
    cash = st.number_input("現金 (HKD)", value=0)
    stocks = st.number_input("股票／ETF (HKD)", value=0)
    mpf = st.number_input("現有強積金總額 (HKD)", value=0)
    liabilities = st.number_input("負債（卡數／貸款 HKD）", value=0)

with st.sidebar.expander("4. 目標與背景", expanded=False):
    short_term_goal = st.text_input("短期目標（1年內）", "存夠 20 萬備用金")
    mid_term_goal = st.text_input("中期目標（2-5年）", "儲首期買樓／結婚")
    family_burden = st.text_input("家庭狀況（家用等）", "每月給家用 5000")
    risk_tolerance = st.selectbox("風險承受能力", ["保守", "中等", "進取"], index=1)

total_liquid_assets = bank_balance + cash + stocks
net_worth = total_liquid_assets + mpf - liabilities
savings_rate = (monthly_saving / salary_after_mpf) * 100 if salary_after_mpf > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("每月儲蓄率", f"{savings_rate:.1f}%")
col2.metric("總流動資產", f"${total_liquid_assets:,.0f}")
col3.metric("淨資產總值", f"${net_worth:,.0f}")
col4.metric("預測1年資產增長", f"${(monthly_saving * 12):,.0f}")

st.markdown("<hr>", unsafe_allow_html=True)

# 淨化後的 System Prompt（配備防重複機制）
system_persona = f"""
You are a professional, precise Hong Kong financial coach. 
You must respond in natural, professional Hong Kong Traditional Chinese.

[User Financial Data]
- Age: {age}
- Occupation: {occupation}
- Net Salary (after MPF): ${salary_after_mpf:,.0f}
- Monthly Expense: ${monthly_expense:,.0f}
- Monthly Savings: ${monthly_saving:,.0f} (Savings Rate: {savings_rate:.1f}% - This is an exceptionally high and elite savings rate)
- Total Liquid Assets: ${total_liquid_assets:,.0f}
- MPF Balance: ${mpf:,.0f}
- Liabilities: ${liabilities:,.0f}
- Net Worth: ${net_worth:,.0f}
- Short-term Goal: {short_term_goal}
- Mid-term Goal: {mid_term_goal}

[Rules]
1. Acknowledge and praise the user's high savings rate ({savings_rate:.1f}%) directly and professionally.
2. Provide concrete, accurate numerical analysis based strictly on the provided data.
3. Keep responses structured, concise, and logical. Do not repeat phrases or words.
"""

if st.button("執行 AI 理財架構分析"):
    if api_key:
        progress_bar = st.progress(0, text="正在初始化理財引擎...")
        time.sleep(0.2)
        progress_bar.progress(30, text="正在讀取用戶資產與自動計算現金流...")
        time.sleep(0.3)
        progress_bar.progress(60, text="AI 教練正在進行精準財務模型運算...")
        
        try:
            task_prompt = """
            請根據用戶的財務數據，提供以下 3 個部分的分析報告：
            1. 財務健康狀況與儲蓄率評估
            2. 1年及3年後資產增長推算
            3. 具體自動化儲蓄分配建議
            """
            messages = [
                {"role": "system", "content": system_persona},
                {"role": "user", "content": task_prompt}
            ]
            
            progress_bar.progress(85, text="正在生成分析報告...")
            response = client.chat.completions.create(
                model="meta-llama/Llama-3.1-8B-Instruct",
                messages=messages,
                max_tokens=600,
                temperature=0.3,
                extra_body={"repetition_penalty": 1.25}
            )
            
            progress_bar.progress(100, text="分析完成！")
            time.sleep(0.3)
            progress_bar.empty()
            
            st.success("分析完成")
            st.markdown(f'<div class="apple-card">{response.choices[0].message.content}</div>', unsafe_allow_html=True)
        except Exception as e:
            progress_bar.empty()
            st.error(f"發生錯誤：{e}")
    else:
        st.error("請先輸入 API Key。")

st.markdown("<hr>", unsafe_allow_html=True)

st.subheader("AI 財務諮詢對話")
st.write("向你的專屬教練提問，例如：「我呢個洗費水平夠唔夠買樓？」")

user_question = st.text_input("輸入你的問題：")
if user_question and api_key:
    if st.button("發送查詢"):
        chat_progress = st.progress(0, text="教練思考中...")
        chat_progress.progress(50, text="正在分析您的提問與理財檔案...")
        try:
            chat_messages = [
                {"role": "system", "content": system_persona},
                {"role": "user", "content": user_question}
            ]
            chat_response = client.chat.completions.create(
                model="meta-llama/Llama-3.1-8B-Instruct",
                messages=chat_messages,
                max_tokens=600,
                temperature=0.3,
                extra_body={"repetition_penalty": 1.25}
            )
            chat_progress.progress(100, text="完成！")
            time.sleep(0.2)
            chat_progress.empty()
            
            st.markdown(f'<div class="apple-card">{chat_response.choices[0].message.content}</div>', unsafe_allow_html=True)
        except Exception as e:
            chat_progress.empty()
            st.error(f"發生錯誤：{e}")
            
