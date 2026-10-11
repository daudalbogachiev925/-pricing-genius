import os
import requests
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

API = os.getenv("API_URL", "http://api:8000")
st.set_page_config(page_title="Pricing Genius", layout="wide")
st.title("Pricing Genius")

@st.cache_data(ttl=15)
def fetch(path):
    return requests.get(f"{API}{path}").json()

obs = pd.DataFrame(fetch("/api/ab-data"))
if obs.empty:
    st.warning("Нет данных. Добавьте наблюдения через POST /api/ab-data")
    st.stop()

c1, c2, c3 = st.columns(3)
c1.metric("Наблюдений", len(obs))
c2.metric("Средняя цена", f"{obs.price.mean():.1f}")
c3.metric("Средний спрос", f"{obs.quantity.mean():.0f}")

st.subheader("Спрос и цена")
st.plotly_chart(px.scatter(obs, x="price", y="quantity", trendline="ols"))

if st.button("Обучить модель спроса (linear)"):
    r = requests.post(f"{API}/api/models/fit",
                      json={"model_type": "linear"}).json()
    st.json(r)

if st.button("Обучить модель (log-log)"):
    r = requests.post(f"{API}/api/models/fit",
                      json={"model_type": "log_log"}).json()
    st.json(r)

unit_cost = st.sidebar.number_input("Unit cost", 1.0, 500.0, 30.0)
objective = st.sidebar.selectbox("Objective", ["profit", "revenue"])

if st.sidebar.button("Оптимизировать"):
    r = requests.post(f"{API}/api/optimize", json={
        "model_type": "linear", "unit_cost": unit_cost,
        "objective": objective}).json()
    st.session_state["opt"] = r

if "opt" in st.session_state:
    o = st.session_state["opt"]
    a, b, c = st.columns(3)
    a.metric("Оптимальная цена", f"{o['optimal_price']:.2f}")
    b.metric("Спрос", f"{o['optimal_quantity']:.0f}")
    c.metric("Значение", f"{o['optimal_value']:.0f}")

    curve = pd.DataFrame(o["curve"])
    st.plotly_chart(px.line(curve, x="price", y="value",
                             title="Кривая значения"))

st.subheader("Сегменты")
segs = pd.DataFrame(fetch("/api/simulation/segments"))
st.dataframe(segs)
st.plotly_chart(px.bar(segs, x="segment", y=["revenue","profit"],
                        barmode="group"))

st.subheader("A/B-тест")
col_a, col_b = st.columns(2)
pa = col_a.number_input("Цена A", 1.0, 500.0, 80.0)
pb = col_b.number_input("Цена B", 1.0, 500.0, 120.0)
if st.button("Запустить A/B"):
    r = requests.post(f"{API}/api/simulation/ab",
                      json={"price_a": pa, "price_b": pb}).json()
    st.json(r)
