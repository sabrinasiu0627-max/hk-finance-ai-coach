import streamlit as st
import pandas as pd
import google.generativeai as genai

# Page configuration
st.set_page_config(page_title="香港理財教練 AI 系統", page_icon="💰", layout="wide")

st.title("🇭🇰 香港理財教練 AI 系統 (半年實測升級版)")
st.write("結合你嘅理財表格與 Gemini AI，打造專屬嘅智能理財教練！")

# API Key setup (Supports Streamlit Secrets or Manual Input)
api_key = st.secrets.get("GEMINI_API_KEY", "")
if not api_key:
    with st.sidebar:
        st.header("⚙️ 系統設定")
        api_key = st.text_input("請輸入 Google Gemini API Key", type="password")
        st.markdown("[點此免費取得 Gemini API Key](https://aistudio.google.com/)")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
else:
    st.warning("⚠️️ 請先在側邊欄輸入 Gemini API Key 以啟動 AI 教練功能。")

# --- Sidebar: Financial Profile Inputs ---
st.sidebar.header("📋 你的理財檔案資料")

with st.sidebar.expander("1. 基本資料", expanded=False):
    age = st.text_input("年齡", "28")
    occupation = st.text_input("職業", "文職")
    
with st.sidebar.expander("2. 薪金與現金流", expanded=True):
    salary_before_mpf = st.number_input("薪金（MPF前 HKD）", value=30000, step=1000)
    salary_after_mpf = st.number_input("薪金（MPF後 HKD）", value=28500, step=1000)
    monthly_expense = st.number_input("每月總開支 (HKD)", value=12000, step=500)
    monthly_saving = st.number_input("每月儲蓄 (HKD)", value=16500, step=500)

with st.sidebar.expander("3. 資產與負債", expanded=True):
    bank_balance = st.number_input("銀行戶口及餘額 (HKD)", value=100000)
    cash = st.number_input("現金 (HKD)", value=5000)
    stocks = st.number_input("股票／ETF (HKD)", value=150000)
    mpf = st.number_input("強積金 (HKD)", value=80000)
    liabilities = st.number_input("負債（卡數／貸款 HKD）", value=0)

with st.sidebar.expander("4. 目標與背景", expanded=False):
    short_term_goal = st.text_input("短期目標（1年內）", "存夠 20 萬備用金")
    mid_term_goal = st.text_input("中期目標（2–5年）", "儲首期買樓／結婚")
    family_burden = st.text_input("家庭狀況（家用等）", "每月給家用 5000")
    risk_tolerance = st.selectbox("風險承受能力", ["保守", "中等", "進取"], index=1)

# --- Real-time Calculations ---
total_liquid_assets = bank_balance + cash + stocks
net_worth = total_liquid_assets + mpf - liabilities
savings_rate = (monthly_saving / salary_after_mpf) * 100 if salary_after_mpf > 0 else 0

# --- Dashboard Display ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("每月儲蓄率", f"{savings_rate:.1f}%")
col2.metric("總流動資產", f"${total_liquid_assets:,.0f}")
col3.metric("淨資產總值", f"${net_worth:,.0f}")
col4.metric("預測1年資產增長", f"${(monthly_saving * 12):,.0f}")

st.divider()

# --- AI Persona Prompt ---
system_persona = f"""
你現在擔任一個香港理財教練 AI，請用香港繁體中文加適量廣東話回應（例如：用「咁」、「囉」、「冇」、「同埋」、「計計條數」等），幫用戶建立同追蹤理財檔案。

以下係用戶嘅基本資料。請記住呢啲數字同時間線，往後對話直接引用，唔好重複問基本資料：
- 年齡：{age}
- 職業：{occupation}
- 薪金（MPF後）：${salary_after_mpf:,.0f}
- 每月總開支：${monthly_expense:,.0f}
- 每月儲蓄：${monthly_saving:,.0f}（儲蓄率：{savings_rate:.1f}%）
- 總流動資產：${total_liquid_assets:,.0f}
- 負債：${liabilities:,.0f}
- 短期目標：{short_term_goal}
- 中期目標：{mid_term_goal}
- 家庭狀況：{family_burden}
- 風險承受能力：{risk_tolerance}

每次回覆要具體、有數字、可執行，避免空泛建議。
"""

# --- Action Button ---
if st.button("🚀 讓 AI 教練建立理財檔案、計算增長與設計自動化儲蓄", type="primary"):
    if api_key:
        with st.spinner("AI 理財教練正在為你分析資產並訂立自動化儲蓄方案..."):
            try:
                task_prompt = system_persona + """
                請根據以上用戶資料，立即幫用戶完成以下 3 個指定任務：
                1. 建立理財檔案總結；
                2. 計算儲蓄率同資產增長推算（1年、3年）；
                3. 設計具體嘅自動化儲蓄系統方案（例如出糧自動轉賬分配、各戶口分配比例）。
                """
                response = model.generate_content(task_prompt)
                st.success("分析完成！")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"發生錯誤：{e}")
    else:
                st.error("請先在側邊欄輸入 API Key！")

st.divider()

# --- Interactive AI Chat ---
st.subheader("💬 與香港理財教練對話")
st.write("你可以隨便問教練理財問題，例如：「我呢個洗費水平夠唔夠買樓？」、「下個月花紅點分配？」")

user_question = st.text_input("輸入你想問理財教練的問題：")
if user_question and api_key:
    if st.button("發送問題"):
        with st.spinner("教練思考中..."):
            try:
                chat_prompt = system_persona + f"\n\n用戶最新提問：{user_question}"
                chat_response = model.generate_content(chat_prompt)
                st.markdown(chat_response.text)
            except Exception as e:
                st.error(f"發生錯誤：{e}")
