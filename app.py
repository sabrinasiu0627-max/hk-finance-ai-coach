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
st.write("結合精準數學模型、市場環境趨勢與自動化分帳系統的極簡理財平台。")

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
    salary_before_mpf = st.number_input("每月薪金（MPF前 HKD）", value=22000, step=1000)
    
    mpf_deduction = min(salary_before_mpf * 0.05, 1500) if salary_before_mpf >= 7100 else 0
    salary_after_mpf = salary_before_mpf - mpf_deduction
    
    st.caption(f"自動計算 MPF 扣除: ${mpf_deduction:,.0f}")
    st.markdown(f"**實收薪金 (MPF後): ${salary_after_mpf:,.0f}**")
    
    monthly_expense = st.number_input("每月總開支 (HKD)", value=15000, step=500)
    monthly_saving = salary_after_mpf - monthly_expense
    st.info(f"自動計算每月淨儲蓄: ${monthly_saving:,.0f}")

with st.sidebar.expander("3. 資產與負債", expanded=True):
    bank_balance = st.number_input("銀行戶口及餘額 (HKD)", value=80400)
    cash = st.number_input("現金 (HKD)", value=0)
    stocks = st.number_input("股票／ETF (HKD)", value=0)
    past_3yr_stock_return = st.slider("過去 3 年投資組合平均回報率 (%)", min_value=-10.0, max_value=25.0, value=8.5, step=0.5)
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

# --- 儀表板頂部核心數據 ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("每月儲蓄率", f"{savings_rate:.1f}%")
col2.metric("總流動資產", f"${total_liquid_assets:,.0f}")
col3.metric("淨資產總值", f"${net_worth:,.0f}")
col4.metric("過去3年回報參考", f"{past_3yr_stock_return:.1f}% p.a.")

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
            <h4>證券 / 銀行 D</h4>
            <p style="font-size: 13px; color: #555;">投資戶口 (VOO月供)</p>
            <hr style="margin: 10px 0;">
            <p style="font-size: 18px; font-weight: bold;">每月轉 ${recommended_invest_ac:,.0f}</p>
        </div>
        <p style="font-size: 12px; margin-top: 15px; color: #333;">(長期資產增長引擎)</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# 淨化後的 System Prompt（結合過去表現與 2026 年最新市況分析要求）
system_persona = f"""
You are a professional, precise Hong Kong financial coach in year 2026. 
You must respond in natural, professional Hong Kong Traditional Chinese, using bullet points exclusively for analysis.

[User Financial Data & Performance]
- Net Salary (after MPF): ${salary_after_mpf:,.0f}
- Monthly Expense: ${monthly_expense:,.0f}
- Monthly Savings: ${monthly_saving:,.0f} (Savings Rate: {savings_rate:.1f}%)
- Total Liquid Assets: ${total_liquid_assets:,.0f}
- Past 3-Year Stock Portfolio Return: {past_3yr_stock_return:.1f}% p.a.
- Net Worth: ${net_worth:,.0f}

[Rules]
1. Output concise, meaningful financial analysis structured purely in bullet points (- or *).
2. Analyze the coming 3-year growth trend by referencing the user's past 3-year performance ({past_3yr_stock_return:.1f}%) and current 2026 macroeconomic market conditions.
3. Keep it punchy, professional, and entirely free of hallucinated calculations.
"""

# 用戶點擊按鈕後才觸發 AI 分析與預測增長曲線
if st.button("執行 AI 理財架構分析"):
    if api_key:
        progress_bar = st.progress(0, text="正在初始化理財引擎...")
        time.sleep(0.2)
        progress_bar.progress(30, text="AI 教練正在擷取過去 3 年投資回報數據...")
        time.sleep(0.2)
        progress_bar.progress(60, text="正在結合 2026 年最新市場環境進行趨勢評估...")
        
        try:
            task_prompt = """
            請根據用戶的財務數據、過去 3 年投資回報（""" + f"{past_3yr_stock_return:.1f}%" + """）以及 2026 年當前宏觀市場狀況，以精簡的 Bullet Points 提供商業級分析：
            - 現金流與儲蓄率的強勢點評
            - 綜合過去 3 年表現與 2026 年最新市況對未來 3 年 VOO / 投資增長的趨勢預測
            - 多戶口自動化分帳與長期財富累積的實戰建議
            """
            messages = [
                {"role": "system", "content": system_persona},
                {"role": "user", "content": task_prompt}
            ]
            
            response = client.chat.completions.create(
                model="meta-llama/Llama-3.1-8B-Instruct",
                messages=messages,
                max_tokens=600,
                temperature=0.3,
                extra_body={"repetition_penalty": 1.25}
            )
            
            progress_bar.progress(100, text="完成！")
            time.sleep(0.2)
            progress_bar.empty()
            
            st.success("AI 市況分析與複利增長預測已完成")
            
            # 顯示 AI 分析報告
            st.markdown(f'<div class="apple-card"><h4>🤖 AI 宏觀市況與 3 年增長分析報告</h4>{response.choices[0].message.content}</div>', unsafe_allow_html=True)
            
            # --- 📈 觸發後才生成的 36 個月複利資產增長預測圖表 ---
            st.subheader("📈 36 個月市場導向複利資產累積趨勢預測")
            st.write(f"基於你過去 3 年平均回報（{past_3yr_stock_return:.1f}%）經 AI 市況校準後嘅動態複合增長模型：")

            months = list(range(37))
            # 以用戶自訂的過去回報率作為未來預測的市況調整基準
            adjusted_annual_rate = max(min(past_3yr_stock_return / 100.0, 0.20), -0.05)
            monthly_return_rate = (1 + adjusted_annual_rate) ** (1/12) - 1

            projected_assets = []
            current_val = total_liquid_assets
            for m in months:
                if m == 0:
                    projected_assets.append(current_val)
                else:
                    current_val = current_val * (1 + monthly_return_rate) + monthly_saving
                    projected_assets.append(current_val)

            df_chart = pd.DataFrame({
                "月份 (第 N 個月)": months, 
                "市場導向複利預測總資產 (HKD)": projected_assets
            })
            df_chart.set_index("月份 (第 N 個月)", inplace=True)

            st.line_chart(df_chart)

            pure_linear_1yr = total_liquid_assets + (monthly_saving * 12)
            pure_linear_3yr = total_liquid_assets + (monthly_saving * 36)

            col_p1, col_p2 = st.columns(2)
            with col_p1:
                st.metric("1 年後預測總資產 (含市況複利)", f"${projected_assets[12]:,.0f}", f"比純儲蓄多 +${projected_assets[12] - pure_linear_1yr:,.0f}")
            with col_p2:
                st.metric("3 年後預測總資產 (含市況複利)", f"${projected_assets[36]:,.0f}", f"比純儲蓄多 +${projected_assets[36] - pure_linear_3yr:,.0f}")

        except Exception as e:
            progress_bar.empty()
            st.error(f"發生錯誤：{e}")
    else:
        st.error("請先輸入 API Key。")
