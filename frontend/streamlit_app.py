import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://127.0.0.1:8000"

st.title("💰 Трекер финансов")

tab1, tab2, tab3 = st.tabs([
    "📂 Загрузка операций из файла",
    "➕ Добавить операцию",
    "📊 Аналитика расходов по месяцу"
])

with tab1:
    st.header("Загрузка операций из файла")

    file = st.file_uploader("Загрузи файл", type=["csv"])

    if file:
        if st.button("Загрузи файл"):
            res = requests.post(
                f"{API_URL}/transactions/upload-csv",
                files={"file": file}
            )

            st.json(res.json())

with tab2:
    st.header("Добавить операцию")

    with st.form("Добавить операцию"):
        operation_date = st.date_input("Operation date")
        payment_date = st.date_input("Payment date")
        card_number = st.text_input("Card number")
        status = st.text_input("Status")
        operation_amount = st.number_input("Operation amount")
        operation_curr = st.text_input("Operation currency")
        payment_amount = st.number_input("Payment amount")
        payment_curr = st.text_input("Payment currency")
        cashback = st.number_input("Cashback")
        category = st.text_input("Category")
        mcc = st.number_input("MCC")
        description = st.text_area("Description")
        bonus = st.number_input("Bonus")
        investment_round = st.number_input("Investment round")
        operation_round = st.number_input("Operation round")

        submit = st.form_submit_button("Add")

    if submit:
        payload = {
            "operation_date": str(operation_date),
            "payment_date": str(payment_date),
            "card_number": card_number,
            "status": status,
            "operation_amount": operation_amount,
            "operation_curr": operation_curr,
            "payment_amount": payment_amount,
            "payment_curr": payment_curr,
            "cashback": cashback,
            "category": category,
            "mcc": mcc,
            "description": description,
            "bonus": bonus,
            "investment_round": investment_round,
            "operation_round": operation_round
        }

        res = requests.post(
            f"{API_URL}/transactions/addtransaction",
            json=payload
        )

        st.success("Transaction added!")
        st.json(res.json())

with tab3:
    st.header("📊 Аналитика расходов по месяцу")

    response = requests.get(f"{API_URL}/transactions/load_transaction")
    data = response.json()

    if not isinstance(data, list):
        st.error("Invalid data")
        st.stop()

    df = pd.DataFrame(data)

    df["operation_date"] = pd.to_datetime(df["operation_date"])
    df["month"] = df["operation_date"].dt.to_period("M")

    months = sorted(df["month"].astype(str).unique())
    selected_month = st.selectbox("Select month", months)

    df_month = df[df["month"].astype(str) == selected_month ]

    df_month = df_month[df_month["operation_amount"] < 0]

    df_month["operation_amount"] = -df_month["operation_amount"]

    total_expenses = df_month["operation_amount"].sum()

    st.metric(
        label="💸 Всего трат за месяц",
        value=f"{total_expenses:,.2f}"
    )

    st.subheader(f"Аналитика за {selected_month}")

    daily = df_month.groupby("operation_date")["operation_amount"].sum().reset_index()

    st.markdown("### 📈 Траты по дням")

    st.bar_chart(
        daily.set_index("operation_date")
    )

    st.markdown("### 🥧 Траты по категориям")

    category = df_month.groupby("category")["operation_amount"].sum()

    fig = px.pie(
        names=category.index,
        values=category.values
    )

    st.plotly_chart(fig)