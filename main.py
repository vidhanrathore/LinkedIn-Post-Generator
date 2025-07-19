import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post


# Options for length and language
length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish", "Hindi"]


# Main app layout
def main():
    st.subheader("LinkedIn Post Generator By Vidhan Rathore")

    # Create three columns for the dropdowns
    col1, col2, col3 = st.columns(3)

    tags = ['Sapne', 'Productivity', 'Motivation', 'Self Improvement', 'Organic Growth', 'Online Dating', 'Career Advice', 'Job Search', 'Mental Health', 'Time Management', 'Scams', 'Leadership', 'Influencer']
    subject = st.text_input("Subject", placeholder="Enter about your post to make it more customize.", icon="🚨")
    post_style = st.text_input("Post Style", placeholder="Enter your post as example to copy writing style.")
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
        post = generate_post(selected_length, selected_language, selected_tag, subject, post_style)
        st.write(post)


# Run the app
if __name__ == "__main__":
    main()
