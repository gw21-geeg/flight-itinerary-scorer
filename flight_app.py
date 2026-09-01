import streamlit as st
import requests
duffel_token = st.secrets["DUFFEL_TOKEN"]

st.title("Flight Itinerary Scorer")
origin = st.text_input("From", placeholder="BNA")
destination = st.text_input("To", placeholder="DEN")
travel_date = st.date_input("Travel date")

def score_flight(price, stops, duration, connection, preference):
    score = 100

    if preference == "Balanced":
        score -= stops * 15
        score -= (price / 100) * 5
        score -= duration * 2

    elif preference == "Cheapest":
        score -= stops * 10
        score -= (price / 100) * 10
        score -= duration * 1

    elif preference == "Shortest Travel Time":
        score -= stops * 10
        score -= (price / 100) * 3
        score -= duration * 5

    elif preference == "Fewest Stops":
        score -= stops * 30
        score -= (price / 100) * 3
        score -= duration * 1.5

    if stops == 0:
        score += 10

    if stops > 0 and connection < 45:
        score -= 15

    if stops > 0 and connection >= 180:
        score -= 10

    score = max(0, min(100, score))

    return score

def get_rating(score):
    if score >= 80:
        return "Excellent"
    elif score >= 65:
        return "Good"
    elif score >= 50:
        return "Fair"
    else:
        return "Poor"


number_of_flights = st.number_input(
    "How many flights do you want to compare?",
    min_value=2,
    max_value=6,
    value=2,
    step=1
)
preference = st.selectbox(
    "What matters most to you?",
    ["Balanced", "Cheapest", "Shortest Travel Time", "Fewest Stops"]
)

flights = []

for i in range(number_of_flights):
    st.subheader(f"Flight {i + 1}")

    airline = st.text_input(
        "Airline",
        key=f"airline_{i}"
    )

    route = st.text_input(
        "Route",
        placeholder="BNA-DEN",
        key=f"route_{i}"
    )

    price = st.number_input(
        "Ticket price",
        min_value=0.0,
        key=f"price_{i}"
    )

    stops = st.number_input(
        "Number of stops",
        min_value=0,
        step=1,
        key=f"stops_{i}"
    )

    duration = st.number_input(
        "Total travel time in hours",
        min_value=0.0,
        key=f"duration_{i}"
    )

    connection = st.number_input(
        "Connection time in minutes",
        min_value=0,
        step=1,
        key=f"connection_{i}"
    )

    score = score_flight(
        price,
        stops,
        duration,
        connection,
        preference
    )

    flights.append({
        "flight_number": i + 1,
        "airline": airline,
        "route": route,
        "price": price,
        "stops": stops,
        "duration": duration,
        "connection": connection,
        "score": score
    })



if st.button("Compare Flights"):

    flights_sorted = sorted(
        flights,
        key=lambda flight: flight["score"],
        reverse=True
    )
    st.write(f"### {origin} → {destination}")
    st.write(f"Travel date: {travel_date}")

    st.header("Flight Rankings")

    for rank, flight in enumerate(
        flights_sorted,
        start=1
    ):
        rating = get_rating(flight["score"])

        st.write(
            f"**{rank}. {flight['airline']} "
            f"{flight['route']}** — "
            f"{flight['score']:.1f}/100 — "
            f"{rating}"
        )

    best_flight = flights_sorted[0]

    st.header("Recommended Flight")

    st.write(
        f"### {best_flight['airline']} "
        f"{best_flight['route']}"
    )

    st.write(f"Price: **${best_flight['price']:.2f}**")
    st.write(f"Stops: **{best_flight['stops']}**")
    st.write(
        f"Travel time: "
        f"**{best_flight['duration']} hours**"
    )
    st.write(
        f"Connection: "
        f"**{best_flight['connection']} minutes**"
    )
    st.write(
        f"Score: "
        f"**{best_flight['score']:.1f}/100**"
    )
    st.write(
        f"Rating: "
        f"**{get_rating(best_flight['score'])}**"
    )

    st.write(f"Preference: **{preference}**")

    if preference == "Cheapest":
        st.write("- This flight scored best mainly because of price.")

    elif preference == "Shortest Travel Time":
        st.write("- This flight scored best mainly because of travel time.")

    elif preference == "Fewest Stops":
        st.write("- This flight scored best mainly because it had fewer stops.")

    else:
        st.write("- This flight had the best overall balance of price, stops, and travel time.")
