import streamlit as st
import google.generativeai as ai

# Configure the Gemini model with your API key
API_KEY = st.secrets["GOOGLE_API_KEY"]  # Store your API key in .streamlit/secrets.toml
ai.configure(api_key=API_KEY)

# Instruction for the Gemini model
instruction = (
    "You are a friendly and helpful bot specializing in solving issues related to "
    "face recognition-based attendance systems. Provide practical solutions and "
    "explanations for common problems like camera issues, recognition errors, "
    "database integration challenges, and more. Always respond in a kind and helpful tone.\n"
    "1. Provide the answer in bullet form for clarity.\n"
    "2. Do not respond in bold letters, only use normal text.\n"
    "3. Only respond to questions specifically related to face recognition-based attendance systems.\n"
    "4. Summarize lengthy responses into at most 2-3 lines.\n"
)

# Start the chat model with the instruction
model = ai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=instruction
)

# App title
st.title("ChatBot For Attendance Management System")

# Initialize chat history in the session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input field for user messages
user_input = st.chat_input("Enter your message")
if user_input:
    # Display the user's message
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Check for special commands (bye and admin)
    if user_input.lower() in ["bye", "exit", "quit"]:
        st.session_state.messages.append({"role": "assistant", "content": "Goodbye! The application will now close."})
        st.markdown("Thank you for using the ChatBot. Any questions feel free to ask?")
    elif user_input.lower() in ["admin", "administrator"]:
        st.session_state.messages.append({"role": "assistant", "content": "Admin is available."})
        st.markdown("Communicate with admin at Home Page")
    else:
        with st.spinner("Generating response..."):
        # Generate response using the Gemini model
            with st.chat_message("assistant"):
                try:
                    # Start a new chat session and send the user's message
                    chat = model.start_chat()
                    response = chat.send_message(user_input).text
                    st.markdown(response)
                except Exception as e:
                    response = "Sorry, I encountered an error. Please try again later."
                    st.error(f"Error: {str(e)}")  # Log the error

        # Save the assistant's response to the session state
        st.session_state.messages.append({"role": "assistant", "content": response})
