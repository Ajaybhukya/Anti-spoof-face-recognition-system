import streamlit as st
import pymysql
import pandas as pd


def fetch_student_attendance(student_id):
    connection = connect_to_mysql("localhost", user="root", password="1234", database="face")
    if not connection:
        return None

    try:
        query = """
        SELECT 
            s.id AS student_id, 
            s.name AS student_name,
            s.email AS student_email,
            YEAR(a.attendance_date) AS year,
            MONTH(a.attendance_date) AS month,
            COUNT(DISTINCT a.attendance_date) AS days_present
        FROM 
            students s
        LEFT JOIN 
            attendance a ON s.id = a.id
        WHERE 
            s.id = %s
        GROUP BY 
            s.id, s.name, s.email, YEAR(a.attendance_date), MONTH(a.attendance_date)
        ORDER BY 
            year, month;
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query, (student_id,))
            data = cursor.fetchall()

            if data:
                filtered_data = [row for row in data if row['days_present'] > 0]

                if not filtered_data:
                    st.warning(f"⚠️ No suitable attendance data found for Student ID {student_id}.")
                    st.session_state.attendance_data = None
                else:
                    st.session_state.attendance_data = pd.DataFrame(filtered_data)
                    st.session_state.student_email = filtered_data[0]['student_email']
                    st.session_state.student_name = filtered_data[0]['student_name']
            else:
                st.error(f"⚠️ Student not found for Student ID {student_id}.")
                st.session_state.attendance_data = None

    except pymysql.MySQLError as e:
        st.error(f"❌ SQL Query Error: {e}")
        st.session_state.attendance_data = None
    finally:
        connection.close()


if st.button("Fetch Attendance Data"):
    with st.spinner("Fetching attendance data..."):
        fetch_student_attendance(student_id)

if st.session_state.attendance_data is not None:
    st.write(f"### Attendance Data for Student ID {student_id}")
    st.dataframe(st.session_state.attendance_data)

    # Initialize badge_awarded in session state
    st.session_state.badge_awarded = False

    # Store badge images and captions
    badges = []

    # Group by year and month for structured display
    grouped_data = st.session_state.attendance_data.groupby(["year", "month"])

    for (year, month), group in grouped_data:
        days_present = group["days_present"].sum()

        if days_present > 0:  # Check eligibility per month
            badge, caption = assign_badge(days_present, month)
            if badge:
                badges.append((badge, f"{month}/{year}: {caption}"))
                st.session_state.badge_awarded = True

                # Display badges in a row
    if st.session_state.badge_awarded:
        st.write("### 🎉 Monthly Achievements: 🎊")
        cols = st.columns(len(badges))  # Create dynamic columns
        for col, (badge, caption) in zip(cols, badges):
            with col:
                st.image(badge, caption=caption, width=120)
    else:
        st.warning("⚠️ No badges available based on attendance.")
