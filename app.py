import streamlit as st
import pandas as pd
import time
from huggingface_hub import InferenceClient

# 網頁基本設定
st.set_page_config(page_title="HK Finance AI Coach", page_icon="", layout="wide")

# 極致清晰 Apple 黑白風 CSS (已修正卡片標題換行 Bug)
st.markdown("""
<style>
    .stApp {
        background-color: #FFFFFF !important;
        color: #111111 !important;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", Arial, sans-serif;
    }
    h1, h2, h3, h4, h5, h6, p, label, span, div {
        color: #111111;
    }
    ::selection {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }
    [data-testid="stSidebar"] {
        background-color: #FBFBFD !important;
        border-right: 1px solid #D2D2D7 !important;
    }
    [data-testid="stSidebar"] * {
        color: #111111 !important;
    }
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
        color: #000000 !important;
    }
    
    /* Apple 框線卡片：強制等高 + 標題強制不換行防 Bug */
    .apple-card {
        border: 1px solid #111111;
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 24px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100%;
    }
    .apple-card h4 {
        font-size: 1.1rem !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        margin-bottom: 4px !important;
    }
    .apple-card * {
        color: #111111 !important;
    }
    
    code, pre {
        background-color: #F1F1F3 !important;
        color: #111111 !important;
        border-radius: 6px;
        padding: 2px 6px;
    }
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
    hr {
        border: none;
        height: 1px;
        background-color: #D2D2D7;
        margin: 2.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

st.title("HK Finance AI 理財教練")
st.write("結合精準數學模型與自動化分帳系統的極簡理財平台。")

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
    age = st.text_input("年齡", "28")
    occupation = st.text_input("職業", "Professional / Sales")
    
with st.sidebar.expander("2. 薪金與現金流 (MPF自動計算)", expanded=True):
    salary_before_mpf = st.number_input("每月薪金（MPF前 HKD）", value=30000, step=1000)
    
    mpf_deduction = min(salary_before_mpf * 0.05, 1500) if salary_before_mpf >= 7100 else 0
    salary_after_mpf = salary_before_mpf - mpf_deduction
    
    st.caption(f"自動計算 MPF 扣除: ${mpf_deduction:,.0f}")
    st.markdown(f"**實收薪金 (MPF後): ${salary_after_mpf:,.0f}**")
    
    monthly_expense = st.number_input("每月總開支 (HKD)", value=12000, step=500)
    monthly_saving = salary_after_mpf - monthly_expense
    st.info(f"自動計算每月淨儲蓄: ${monthly_saving:,.0f}")

with st.sidebar.expander("3. 資產與負債", expanded=True):
    bank_balance = st.number_input("銀行戶口及餘額 (HKD)", value=100000)
    cash = st.number_input("現金 (HKD)", value=5000)
    stocks = st.number_input("股票／ETF (HKD)", value=150000)
    mpf = st.number_input("現有強積金總額 (HKD)", value=80000)
    liabilities = st.number_input("負債（卡數／貸款 HKD）", value=0)

with st.sidebar.expander("4. 目標與背景", expanded=False):
    short_term_goal = st.text_input("短期目標（1年內）", "存夠 20 萬備用金")
    mid_term_goal = st.text_input("中期目標（2-5年）", "儲首期買樓／結婚")
    family_burden = st.text_input("家庭狀況（家用等）", "每月給家用 5000")
    risk_tolerance = st.selectbox("風險承受能力", ["保守", "中等", "進取"], index=1)

total_liquid_assets = bank_balance + cash + stocks
net_worth = total_liquid_assets + mpf - liabilities
savings_rate = (monthly_saving / salary_after_mpf) * 100 if salary_after_mpf > 0 else 0

# --- 儀表板頂部核心數據 ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("每月儲蓄率", f"{savings_rate:.1f}%")
col2.metric("總流動資產", f"${total_liquid_assets:,.0f}")
col3.metric("淨資產總值", f"${net_worth:,.0f}")
col4.metric("預測1年資產增長", f"${(monthly_saving * 12):,.0f}")

st.markdown("<hr>", unsafe_allow_html=True)

# --- 💡 通用化多戶口自動化分帳儀表板 ---
st.subheader("💳 自動化多戶口分帳儀表板（動態比例模型）")
st.write("根據你目前實收糧 **$" + f"{salary_after_mpf:,.0f}" + "** 同埋開支結構，系統自動計算出以下各戶口的最佳分配金額：")

recommended_cc = min(monthly_expense * 0.65, monthly_expense)
weekly_transfer = recommended_cc / 4
recommended_saving_ac = monthly_saving * 0.75
recommended_invest_ac = monthly_saving * 0.25

col_a, col_b, col_c, col_d = st.columns(4)

with col_a:
    st.markdown("""
    <div class="apple-card">
        <div>
            <h4>銀行 A</h4>
            <p style="font-size: 13px; color: #555;">出糧戶口 ＋ 每日開支</p>
            <hr style="margin: 10px 0;">
            <p style="font-size: 18px; font-weight: bold;">維持水位 $5,000</p>
        </div>
        <p style="font-size: 12px; margin-top: 15px; color: #333;">(月尾多出餘額手動轉走)</p>
    </div>
    """, unsafe_allow_html=True)

with col_b:
    st.markdown(f"""
    <div class="apple-card">
        <div>
            <h4>銀行 B</h4>
            <p style="font-size: 13px; color: #555;">信用卡自動找數專用</p>
            <hr style="margin: 10px 0;">
            <p style="font-size: 18px; font-weight: bold;">約 ${recommended_cc:,.0f} /月</p>
        </div>
        <p style="font-size: 12px; margin-top: 15px; color: #333;">每週自動: ${weekly_transfer:,.0f} × 4</p>
    </div>
    """, unsafe_allow_html=True)

with col_c:
    st.markdown(f"""
    <div class="apple-card">
        <div>
            <h4>銀行 C</h4>
            <p style="font-size: 13px; color: #555;">高息儲蓄／備用金</p>
            <hr style="margin: 10px 0;">
            <p style="font-size: 18px; font-weight: bold;">每月轉 ${recommended_saving_ac:,.0f}</p>
        </div>
        <p style="font-size: 12px; margin-top: 15px; color: #333;">(強制鎖定現金資產)</p>
    </div>
    """, unsafe_allow_html=True)

with col_d:
    st.markdown(f"""
    <div class="apple-card">
        <div>
            <h4>證券／銀行 D</h4>
            <p style="font-size: 13px; color: #555;">投資戶口 (VOO月供)</p>
            <hr style="margin: 10px 0;">
            <p style="font-size: 18px; font-weight: bold;">每月轉 ${recommended_invest_ac:,.0f}</p>
        </div>
        <p style="font-size: 12px; margin-top: 15px; color: #333;">(長期資產增長引擎)</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# --- 📈 視覺化：1年與3年資產增長預測 (用程式碼精密計算 + 圖表) ---
st.subheader("📈 36 個月資產累積趨勢預測（程式碼實時運算）")

# 建立 36 個月嘅增長數據
months = list(range(37))
projected_assets = [total_liquid_assets + (monthly_saving * m) for m in months]
df_chart = pd.DataFrame({"月份": [f"第 {m} 個月" for m in months], "預測總資產 (HKD)": projected_assets})
df_chart.set_index("月份", inplace=True)

# 顯示互動圖表 (唔使靠 AI 吹水，100% 準確)
st.line_chart(df_chart)

col_p1, col_p2 = st.columns(2)
with col_p1:
    st.metric("1 年後預測總資產", f"${total_liquid_assets + (monthly_saving * 12):,.0f}", f"+${(monthly_saving * 12):,.0f}")
with col_p2:
    st.metric("3 年後預測總資產", f"${total_liquid_assets + (monthly_saving * 36):,.0f}", f"+${(monthly_saving * 36):,.0f}")

st.markdown("<hr>", unsafe_allow_html=True)

# 淨化後的 System Prompt
system_persona = f"""
You are a professional, precise Hong Kong financial coach. 
You must respond in natural, professional Hong Kong Traditional Chinese, using bullet points exclusively for analysis.

[User Financial Data]
- Net Salary (after MPF): ${salary_after_mpf:,.0f}
- Monthly Expense: ${monthly_expense:,.0f}
- Monthly Savings: ${monthly_saving:,.0f} (Savings Rate: {savings_rate:.1f}% - Exceptionally high)
- Total Liquid Assets: ${total_liquid_assets:,.0f}
- Net Worth: ${net_worth:,.0f}

[Rules]
1. Output concise, meaningful financial analysis structured purely in bullet points (- or *).
2. Directly praise the elite savings rate.
3. Keep it punchy, professional, and entirely free of hallucinated calculations.
"""

if st.button("執行 AI 理財架構分析"):
    if api_key:
        progress_bar = st.progress(0, text="正在初始化理財引擎...")
        time.sleep(0.2)
        progress_bar.progress(50, text="AI 教練正在分析您的理財格局...")
        
        try:
            task_prompt = """
            請根據用戶的財務數據與自動化分帳架構，以精簡的 Bullet Points 提供商業級分析：
            - 現金流與極高儲蓄率（超過 50%）的強勢點評
            - 多戶口自動化分帳（銀行 A、B、C、D）對紀律理財的實戰價值
            - 長期財富累積的核心建議
            """
            messages = [
                {"role": "system", "content": system_persona},
                {"role": "user", "content": task_prompt}
            ]
            
            response = client.chat.completions.create(
                model="meta-llama/Llama-3.1-8B-Instruct",
                messages=messages,
                max_tokens=500,
                temperature=0.3,
                extra_body={"repetition_penalty": 1.25}
            )
            
            progress_bar.progress(100, text="完成！")
            time.sleep(0.2)
            progress_bar.empty()
            
            st.success("分析完成")
            st.markdown(f'<div class="apple-card">{response.choices[0].message.content}</div>', unsafe_allow_html=True)
        except Exception as e:
            progress_bar.empty()
            st.error(f"發生錯誤：{e}")
    else:
        st.error("請先輸入 API Key。")
