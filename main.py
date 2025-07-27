import streamlit as st
from post_generator import generate_post
from chromadb_setup import save_post_to_chroma

st.set_page_config(page_title="LinkedIn Post Generator", layout="centered")

st.subheader("LinkedIn Post Generator By Vidhan Rathore")

# Initialize session state
if "post_generated" not in st.session_state:
    st.session_state.post_generated = False
if "generated_post" not in st.session_state:
    st.session_state.generated_post = ""
if "feedback_given" not in st.session_state:
    st.session_state.feedback_given = False

# Options
length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish", "Hindi"]
tags = ['Productivity', 'Sapne', 'Motivation', 'Self Improvement', 'Organic Growth',
        'Online Dating', 'Career Advice', 'Job Search', 'Mental Health',
        'Time Management', 'Scams', 'Leadership', 'Influencer']

col1, col2, col3 = st.columns(3)
with col1:
    selected_tag = st.selectbox("Topic", options=tags)
with col2:
    selected_length = st.selectbox("Length", options=length_options)
with col3:
    selected_language = st.selectbox("Language", options=language_options)

subject = st.text_input("Subject", placeholder="Enter about your post to make it more customize.", help="💡 What is your post about?",  icon="💡")
post_style = st.text_area("Post Style", placeholder="Enter your post as example to copy writing style.", help="✍️ Enter a sample post or style.")

if st.button("Generate"):
    try:
        with st.spinner("Generating post..."):
            post = generate_post(selected_length, selected_language, selected_tag, subject, post_style)
            st.session_state.generated_post = post
            st.session_state.post_generated = True
            st.session_state.feedback_given = False
    except Exception as e:
        st.error(f"⚠️ Error: {e}")

# Show result
if st.session_state.post_generated:
    st.markdown("### 📄 Generated Post")
    st.write(st.session_state.generated_post)

    if not st.session_state.feedback_given:
        st.markdown("### 🙋 Was this post helpful?")
        col_yes, col_no = st.columns(2)

        with col_yes:
            if st.button("👍 Yes"):
                try:
                    save_post_to_chroma(
                        generated_post=st.session_state.generated_post,
                        tag=selected_tag,
                        length=selected_length,
                        language=selected_language,
                        subject=subject,
                        post_style=post_style
                    )
                    st.success("✅  Thanks for your feedback! Post saved to database")
                    st.session_state.feedback_given = True
                except Exception as e:
                    st.error(f"❌ Failed to save post: {e}")

        with col_no:
            if st.button("👎 No"):
                st.info("Thanks! We'll improve.")
                st.session_state.feedback_given = True
