import streamlit as st
from chromadb_setup import semantic_search_posts
import streamlit as st
import pandas as pd
import json
import io

def liked_posts_page():
    st.title("❤️ Your Liked Posts")

    # --- Filters ---
    # with st.expander("🔍 Filter Your Posts"):
    search_text = st.text_input("Search text", placeholder="Search something specific...")
    
    # Assume get_all_tags() fetches tags from DB
    all_tags = ['Productivity', 'Sapne', 'Motivation', 'Self Improvement', 'Organic Growth',
    'Online Dating', 'Career Advice', 'Job Search', 'Mental Health',
    'Time Management', 'Scams', 'Leadership', 'Influencer']
    selected_tags = st.multiselect("Filter by Tag(s)", options=all_tags)

    limit = st.slider("Number of Posts to Display", 1, 20, 5)

    try:
        with st.spinner("Loading liked posts..."):
            post = liked_posts = semantic_search_posts(
                query=search_text,
                tags=selected_tags,
                limit=limit
            )

            if not liked_posts:
                st.info("No posts matched your filters.")
                return

            for idx, post in enumerate(liked_posts, start=1):
                with st.expander(f"Post #{idx}"):
                    st.write(post["content"])
                    st.markdown(f"**Tags**: `{post['metadata'].get('tag', 'N/A')}`")
                    st.markdown(f"**Subject**: `{post['metadata'].get('subject', 'N/A')}`")
                    
            st.markdown("---")
            st.subheader("⬇️ Download Your Liked Posts")

            col1, col2, col3 = st.columns(3)

            # TXT format
            txt_data = ""
            for idx, post in enumerate(liked_posts, start=1):
                txt_data += f"Post #{idx}\n{post['content']}\nTags: {post['metadata']}\n" + "-" * 50 + "\n"
            with col1:
                st.download_button("📄 Download as TXT", txt_data, "liked_posts.txt", mime="text/plain")

            # JSON format
            json_data = json.dumps(liked_posts, indent=2, ensure_ascii=False)
            with col2:
                st.download_button("🧾 Download as JSON", json_data, "liked_posts.json", mime="application/json")

            # CSV format
            flat_data = [
                {
                    "id": post.get("id", ""),
                    "content": post.get("content", ""),
                    "subject": post["metadata"].get("subject", ""),
                    "tag": post["metadata"].get("tag", ""),
                    "length": post["metadata"].get("length", ""),
                    "language": post["metadata"].get("language", ""),
                    "post_style": post["metadata"].get("post_style", "")
                }
                for post in liked_posts
            ]

            df = pd.DataFrame(flat_data)
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)

            with col3:
                st.download_button("📊 Download as CSV", csv_buffer.getvalue(), "liked_posts.csv", mime="text/csv")

    except Exception as e:
        st.error(f"❌ Error loading posts: {e}")

liked_posts_page()