import streamlit as st
from post_generator import generate_post


# Options for length and language
length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish", "Hindi"]


# Main app layout
def main():
    st.subheader("LinkedIn Post Generator: Vidhan Rathore")

    # Create three columns for the dropdowns
    col1, col2, col3 = st.columns(3)

    tags = ['Productivity', 'Career Advice', 'Self Improvement', 'Job Search', 'Mental Health', 'Scams', 'Influencer', 'Organic Growth', 'Sapne', 'Motivation', 'Leadership', 'Online Dating', 'Time Management']
    subject = st.text_input("Subject", placeholder="Enter about your post to make it more customize.")
    with col1:
        # Dropdown for Topic (Tags)
        selected_tag = st.selectbox("Topic", options=tags)

    with col2:
        # Dropdown for Length
        selected_length = st.selectbox("Length", options=length_options)

    with col3:
        # Dropdown for Language
        selected_language = st.selectbox("Language", options=language_options)



    # Generate Button
    if st.button("Generate"):
        post = generate_post(selected_length, selected_language, selected_tag, subject)
        st.write(post)


# Run the app
if __name__ == "__main__":
    main()
