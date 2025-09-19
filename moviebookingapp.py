
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine("mysql+mysqlconnector://root:0206@localhost/moviebooking")

st.title('🎬 Movie Ticket Booking System')

movies = pd.read_sql('select * from movies', engine)

if movies.empty:
    st.warning('No movies found in the database')
else:
    movie_choice = st.selectbox('choose a movie',movies['title'].tolist())

    if movie_choice:
        movie_id = movies[movies['title']== movie_choice]['movie_id'].values[0]
        shows = pd.read_sql(f'select * from shows where movie_id={movie_id}',engine)

        if not shows.empty:
            show_choice = st.selectbox('select show time', shows['show_time'].tolist())
            select_show = shows[shows['show_time'] == show_choice].iloc[0]

            seats = st.number_input('number of seats', min_value=1, max_value=10)
            user_name = st.text_input('enter your name')
            user_email = st.text_input('enter your email')

            if st.button('book now'):
                with engine.begin() as conn:
                    
                    user_id = conn.execute(
                        text('select user_id from users where email=:email'),
                        {'email': user_email}

                    ).scalar()
                    if not user_id:
                        conn.execute(
                            text('insert into users (name, email) values (:name, :email)'),
                            {'name': user_name, 'email': user_email}

                        )
                        user_id = conn.execute(text('select last_insert_id()')).scalar()

                    conn.execute(
                        text('insert into bookings (user_id, show_id, seats) values (:user_id,:show_id, :seats)'),
                        {'user_id': user_id, 'show_id': int(select_show['show_id']), 'seats': int(seats)}

                    )

                    booking_id = conn.execute(text('select last_insert_id()')).scalar()

                    amount = seats * select_show['price']
                    conn.execute(
                        text('insert into payments (booking_id, amount, method, status) values (:booking_id, :amount, :method, :status)'),
                        {'booking_id': booking_id, 'amount': float(amount), 'method': 'upi', 'status': 'success'}

                    )

                st.success(f'Booking Confirmed! Total Amount: ₹{amount}')
            else:
                st.warning("No shows available for this movie.")

