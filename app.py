import requests
import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# CONFIG
# -----------------------------
BASE_URL_CURRENT = "https://api.open-meteo.com/v1/forecast"

# -----------------------------
# WEATHER FUNCTION
# -----------------------------
def get_weather_data(city: str):
    """Fetch current weather + forecast using Open-Meteo API"""
    try:
        # Step 1: Get city coordinates
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo_response = requests.get(geo_url, timeout=10).json()
        if "results" not in geo_response:
            return {"error": "City not found. Please try another."}

        lat = geo_response["results"][0]["latitude"]
        lon = geo_response["results"][0]["longitude"]

        # Step 2: Get weather data
        params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": True,
            "hourly": "temperature_2m,relative_humidity_2m,precipitation,cloudcover,windspeed_10m",
            "daily": "temperature_2m_max,temperature_2m_min,sunrise,sunset,precipitation_sum,uv_index_max",
            "timezone": "auto"
        }
        response = requests.get(BASE_URL_CURRENT, params=params, timeout=10)
        data = response.json()

        return {"geo": geo_response["results"][0], "weather": data}
    except Exception as e:
        return {"error": str(e)}

# -----------------------------
# STREAMLIT APP
# -----------------------------
st.set_page_config(page_title="SkyCast – Your Smart Weather Companion", page_icon="🌤️", layout="wide")

st.title("🌤️ SkyCast – Your Smart Weather Companion")
st.markdown("Get **real-time weather**, 🌡️ **temperature trends**, ☔ **rain forecasts**, 🌬️ **wind data**, and more – powered by **Open-Meteo API (Free)** 🌍")

city = st.text_input("🏙️ Enter City Name:")

# Buttons
col1, col2 = st.columns(2)
with col1:
    get_weather_btn = st.button("🌡️ Get Current Weather", use_container_width=True)
with col2:
    forecast_btn = st.button("📅 Show Forecast & Charts", use_container_width=True)

# -----------------------------
# CURRENT WEATHER
# -----------------------------
if get_weather_btn and city:
    result = get_weather_data(city)
    if "error" in result:
        st.error(result["error"])
    else:
        geo = result["geo"]
        weather = result["weather"]
        current = weather["current_weather"]

        st.subheader(f"📍 Current Weather in {geo['name']}, {geo.get('country','')}")

        # Show in columns
        c1, c2, c3 = st.columns(3)
        c1.metric("🌡️ Temperature", f"{current['temperature']} °C")
        c2.metric("💨 Wind Speed", f"{current['windspeed']} km/h")
        c3.metric("🧭 Wind Direction", f"{current['winddirection']}°")

        # Extra hourly data
        st.markdown("### 🌥️ Additional Insights")
        hourly = weather["hourly"]
        st.write(f"☁️ Cloud Cover (Now): {hourly['cloudcover'][0]} %")
        st.write(f"💧 Humidity (Now): {hourly['relative_humidity_2m'][0]} %")
        st.write(f"🌧️ Precipitation (Next Hour): {hourly['precipitation'][0]} mm")

# -----------------------------
# FORECAST + CHARTS
# -----------------------------
if forecast_btn and city:
    result = get_weather_data(city)
    if "error" in result:
        st.error(result["error"])
    else:
        weather = result["weather"]
        daily = weather["daily"]
        hourly = weather["hourly"]

        st.subheader("📅 3-Day Forecast")

        for i in range(3):
            with st.container():
                st.markdown(
                    f"""
                    ### 📌 {daily['time'][i]}
                    - 🌡️ **Max Temp:** {daily['temperature_2m_max'][i]} °C  
                    - ❄️ **Min Temp:** {daily['temperature_2m_min'][i]} °C  
                    - 🌅 **Sunrise:** {daily['sunrise'][i].split('T')[1]}  
                    - 🌇 **Sunset:** {daily['sunset'][i].split('T')[1]}  
                    - 🌧️ **Precipitation:** {daily['precipitation_sum'][i]} mm  
                    - ☀️ **UV Index (Max):** {daily['uv_index_max'][i]}  
                    """
                )
                st.markdown("---")

        # -----------------------------
        # CHARTS (Interactive with Plotly)
        # -----------------------------
        st.subheader("📊 Weather Trends (Next 24 Hours)")

        df = pd.DataFrame({
            "Time": pd.to_datetime(hourly["time"][:24]),
            "Temperature (°C)": hourly["temperature_2m"][:24],
            "Precipitation (mm)": hourly["precipitation"][:24],
            "Humidity (%)": hourly["relative_humidity_2m"][:24]
        })

        # Temperature Trend
        st.markdown("🌡️ **Temperature Trend**")
        fig_temp = px.line(df, x="Time", y="Temperature (°C)", markers=True,
                           title="Next 24h Temperature", template="plotly_white")
        st.plotly_chart(fig_temp, use_container_width=True)

        # Rain Trend
        st.markdown("🌧️ **Rain Forecast**")
        fig_rain = px.bar(df, x="Time", y="Precipitation (mm)",
                          title="Next 24h Rain Forecast", template="plotly_white")
        st.plotly_chart(fig_rain, use_container_width=True)

        # Humidity Trend
        st.markdown("💧 **Humidity Trend**")
        fig_humidity = px.line(df, x="Time", y="Humidity (%)", markers=True,
                               title="Next 24h Humidity", template="plotly_white", color_discrete_sequence=["green"])
        st.plotly_chart(fig_humidity, use_container_width=True)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.markdown("✨ Developed with ❤️ by [Rajed Mehmood](https://www.linkedin.com/in/rajedmehmood)")
