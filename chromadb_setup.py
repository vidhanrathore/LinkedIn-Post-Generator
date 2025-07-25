from chromadb import PersistentClient
from myLogging.logger_config import setup_logger
from chromadb.errors import ChromaError
import hashlib

logger = setup_logger(__name__)
logger.info("Starting the ChromaDB File...")

try:
    # Initialize Chroma Client with persistent storage
    client = PersistentClient(path="./chroma_db")
    collection_name = "linkedin_posts"

    # Create or get existing collection
    collection = client.get_or_create_collection(name=collection_name)
    logger.info(f"Chroma collection '{collection_name}' loaded successfully.")

except ChromaError as e:
    logger.exception(f"ChromaDB initialization failed: {e}")
    raise

except Exception as e:
    logger.exception(f"Unexpected error during ChromaDB setup: {e}")
    raise


def save_post_to_chroma(generated_post, tag="growth", length="short", language="english", subject="", post_style=""):
    post_id = generate_post_id(subject, post_style, tag, length, language, generated_post)

    try:
        collection.add(
            documents=[generated_post],
            metadatas=[{
                "subject": subject,
                "post_style": post_style,
                "tag": tag,
                "length": length,
                "language": language
            }],
            ids=[post_id]
        )

        logger.info(f"Post saved with ID: {post_id}")

    except ChromaError as e:
        logger.error(f"Failed to save post to ChromaDB: {e}")

    except Exception as e:
        logger.exception(f"Unexpected error while saving post: {e}")


def search_existing_post(subject, post_style, tag, length, language):
    post_id = generate_post_id(subject, post_style, tag, length, language)

    try:
        results = collection.get(ids=[post_id], include=["documents"])

        if results and results.get("documents"):
            logger.info(f"Post found for query ID: {post_id}")
            return results["documents"][0]

        logger.info(f"No post found for query ID: {post_id}")
        return None

    except ChromaError as e:
        logger.error(f"ChromaDB query failed: {e}")
        return None

    except Exception as e:
        logger.exception(f"Unexpected error during post search: {e}")
        return None
    
    
def query_similar_posts_by_text(text_query: str, top_k: int = 5, metadata_filter: dict = None):
    """
    Perform a semantic search over saved posts using text query and optional metadata filtering.
    
    Args:
        text_query (str): The user's search text.
        top_k (int): Number of similar results to retrieve.
        metadata_filter (dict): Optional metadata to filter results (e.g., {"tag": "Motivation"}).

    Returns:
        List[str]: Top matching post texts, or an empty list.
    """
    try:
        query_params = {
            "query_texts": [text_query],
            "n_results": top_k,
            "include": ["documents", "metadatas"]
        }
        if metadata_filter:
            query_params["where"] = metadata_filter

        results = collection.query(**query_params)
        # return results
        # Combine each result's document, metadata, and id into a list of dicts
        posts = []
        for i in range(len(results["documents"][0])):
            posts.append({
                "document": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "id": results["ids"][0][i]
            })

        return posts[0]['document']
        # if only documnet needed
        # return results.get("documents", [[]])[0]
    except Exception as e:
        logger.error(f"ChromaDB Query Error: {e}")
        return []



def generate_post_id(subject, post_style, tag, length, language, generated_post=None):
    base_string = f"{subject}|{post_style}|{tag}|{length}|{language}"
    # If post text is provided, include it to avoid duplicate ID with different content
    if generated_post:
        base_string += f"|{generated_post}"
    post_id = hashlib.sha256(base_string.encode()).hexdigest()[:16]
    return post_id 

def delete_all_posts(key="123"):
    try:
        if key == "123123":
            # Fetch all IDs in the collection
            all_data = collection.get(include=["ids"])
            all_ids = all_data.get("ids", [])

            if all_ids:
                collection.delete(ids=all_ids)
                logger.info(f"✅ Deleted {len(all_ids)} posts from ChromaDB.")
            else:
                logger.info("ℹ️ No posts found to delete.")
        else:
            logger.warning("You Don't have right to delete the post.")
    except Exception as e:
        logger.error(f"❌ Failed to delete posts: {e}")
        
        
def get_all_posts():
    """
    Fetch all posts from the collection.
    """
    try: 
        results = collection.get(include=["documents", "metadatas"])
        posts = [
            {
                "id": id_,
                "content": doc,
                "metadata": meta
            }
            for id_, doc, meta in zip(results["ids"], results["documents"], results["metadatas"])
        ]
        logger.info(f"Post found: {posts}")
        
        return posts
    except ChromaError as e:
        logger.error(f"ChromaDB Get method failed: {e}")
        return None

    except Exception as e:
        logger.exception(f"Unexpected error during Get all Post: {e}")
        return None

if __name__ == "__main__":
    get_all_posts()
    
    # sample_post = """🌱 Organic Growth: The Path to Sustainable Success
    # In today's fast-paced world, organic growth isn't just a buzzword; it's a necessity. Unlike quick fixes, it focuses on long-term strategies that build a strong foundation. Whether it's scaling your business, enhancing your skills, or fostering relationships, organic growth ensures stability and resilience. It’s about nurturing what you have and letting it flourish naturally. Embrace the journey, and remember, patience and consistent effort are key. What organic growth strategies have you implemented that have led to sustainable success? Share your experiences below! 🌟 #OrganicGrowth #SustainableSuccess #LongTermStrategies #ConsistentEffort"""

    # save_post_to_chroma(
    #     generated_post=sample_post,
    #     tag="growth",
    #     length="short",
    #     language="english",
    #     subject="",
    #     post_style=""
    # )
    # result = query_similar_posts_by_text("Organic Growth")
    # print(result)
    # delete_all_posts("123123")
    