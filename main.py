import streamlit as st
from post_generator import generate_post
from chromadb_setup import save_post_to_chroma, get_all_posts
import json
import pandas as pd
import io


# Options for length and language
length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish", "Hindi"]

# Initialize session state variables
if "post_generated" not in st.session_state:
    st.session_state.post_generated = False
if "generated_post" not in st.session_state:
    st.session_state.generated_post = ""
if "feedback_given" not in st.session_state:
    st.session_state.feedback_given = False

# Main app layout
def main():
    st.subheader("LinkedIn Post Generator By Vidhan Rathore")

    col1, col2, col3 = st.columns(3)

    tags = ['Productivity', 'Sapne', 'Motivation', 'Self Improvement', 'Organic Growth',
            'Online Dating', 'Career Advice', 'Job Search', 'Mental Health',
            'Time Management', 'Scams', 'Leadership', 'Influencer']

    subject = st.text_input("Subject", placeholder="Enter about your post to make it more customize.", help="💡 What is your post about?",  icon="💡")
    post_style = st.text_area("Post Style", placeholder="Enter your post as example to copy writing style.", help="✍️ Enter a sample post or style.")

    with col1:
        selected_tag = st.selectbox("Topic", options=tags)

    with col2:
        selected_length = st.selectbox("Length", options=length_options)

    with col3:
        selected_language = st.selectbox("Language", options=language_options)

    # Generate Button
    if st.button("Generate"):
        try:
            with st.spinner("Generating post..."):
                post = generate_post(
                    selected_length,
                    selected_language,
                    selected_tag,
                    subject,
                    post_style
                )
                st.session_state.generated_post = post
                st.session_state.post_generated = True
                st.session_state.feedback_given = False  # Reset feedback state
        except Exception as e:
            st.error(f"⚠️ Error while generating post: {e}")

    # Show the generated post
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
                        st.success("✅ Thanks for your feedback! Post saved to database.")
                        st.session_state.feedback_given = True
                    except Exception as e:
                        st.error(f"❌ Failed to save post: {e}")

            with col_no:
                if st.button("👎 No"):
                    st.info("Thanks for your feedback! We'll work on improving it.")
                    st.session_state.feedback_given = True
                    
                    
    if st.button("📂 Show Previously Liked Posts"):
        try:
            with st.spinner("Loading your liked posts..."):
                
                liked_posts = get_all_posts()
                
                if not liked_posts:
                    st.info("No liked posts found.")
                else:
                    st.markdown("## ❤️ Your Liked Posts")
                    for idx, post in enumerate(liked_posts, start=1):
                        with st.expander(f"Post #{idx}"):
                            st.write(post)
                            
                    st.markdown("---")
                    st.subheader("⬇️ Download Your Liked Posts")
                    
                    download1, download2, download3 = st.columns(3)

                    # 🔹 Prepare TXT data
                    txt_data = ""
                    for idx, post in enumerate(liked_posts, start=1):
                        txt_data += f"Post #{idx}\n"
                        txt_data += post["content"] + "\n"
                        txt_data += f"Tags: {post['metadata']}\n"
                        txt_data += "-" * 60 + "\n"

                    with download1:
                        st.download_button(
                            label="📄 Download as TXT",
                            data=txt_data,
                            file_name="liked_posts.txt",
                            mime="text/plain"
                        )

                    with download2:
                        # 🔹 Prepare JSON data
                        json_data = json.dumps(liked_posts, indent=2, ensure_ascii=False)
                        st.download_button(
                            label="🧾 Download as JSON",
                            data=json_data,
                            file_name="liked_posts.json",
                            mime="application/json"
                        )

                    # 🔹 Prepare CSV data
                    flat_data = []
                    for post in liked_posts:
                        flat_row = {
                            "id": post.get("id", ""),
                            "content": post.get("content", ""),
                            "subject": post["metadata"].get("subject", ""),
                            "tag": post["metadata"].get("tag", ""),
                            "length": post["metadata"].get("length", ""),
                            "language": post["metadata"].get("language", ""),
                            "post_style": post["metadata"].get("post_style", "")
                        }
                        flat_data.append(flat_row)

                    df = pd.DataFrame(flat_data)
                    csv_buffer = io.StringIO()
                    df.to_csv(csv_buffer, index=False)

                    with download3:
                        st.download_button(
                            label="📊 Download as CSV",
                            data=csv_buffer.getvalue(),
                            file_name="liked_posts.csv",
                            mime="text/csv"
                        )
        except Exception as e:
            st.error(f"⚠️ Failed to load liked posts: {e}")

# Run the app
if __name__ == "__main__":
    main()
