import streamlit as st
import requests

st.set_page_config(page_title="Weather API Demo", page_icon="🌦️")

st.title("Weather API Demo")

city = st.text_input("Enter city", "Chennai")

if st.button("Get Weather"):

    API_KEY = st.secrets.get("API_KEY", "")

    if not API_KEY:
        st.error("Please add your API key in secrets.toml")

    elif not city.strip():
        st.warning("Please enter a city name.")

    else:
        url = "https://api.openweathermap.org/data/2.5/weather"

        params = {
            "q": city.strip(),
            "appid": API_KEY,
            "units": "metric"
        }

        try:
            with st.spinner("Fetching weather data..."):
                response = requests.get(
                    url,
                    params=params,
                    timeout=10
                )

                response.raise_for_status()
                data = response.json()

            temperature = data["main"]["temp"]
            condition = data["weather"][0]["description"].title()
            humidity = data["main"]["humidity"]

            st.subheader("Weather Details")
            st.json(data)

            col1, col2, col3 = st.columns(3)

            col1.metric("Temperature", f"{temperature} °C")
            col2.metric("Condition", condition)
            col3.metric("Humidity", f"{humidity}%")

        except requests.exceptions.Timeout:
            st.error("Request timed out. Please try again.")

        except requests.exceptions.HTTPError:
            if response.status_code == 401:
                st.error("Invalid API key or key not activated.")
            elif response.status_code == 404:
                st.error("City not found. Please enter a valid city.")
            else:
                st.error(f"API error: {response.status_code}")

        except requests.exceptions.RequestException:
            st.error("Network error. Check your internet connection.")

        except (KeyError, IndexError, ValueError):
            st.error("Unable to read weather data.")

st.markdown("---")
st.subheader("HTTP Methods")

st.write("GET - Retrieve data")
st.write("POST - Send data")
st.write("PUT - Update data")
st.write("DELETE - Delete data")