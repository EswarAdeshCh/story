import streamlit as st
import google.generativeai as genai

def generate_story(hints, genre, length):
    """Generates a story based on given parameters.

    Args:
        hints: Hints or keywords to be included in the story.
        genre: The genre of the story.
        length: The desired length of the story.

    Returns:
        A string containing the story, or None if an error occurs.
    """

    try:
        # Debugging: Check if the API key is retrieved correctly
        api_key = st.secrets.get("api_key", None)
        if api_key is None:
            st.error("API key not found in secrets.")
            return None

        genai.configure(api_key=api_key)

        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
            system_instruction="You are an expert storyteller. Create engaging and immersive stories based on the user's hints, genre, and desired length.",
        )

        prompt = f"Create a {length} story in the {genre} genre that includes the following hints: {hints}."

        response = model.generate_content(prompt)
        story_text = response.text

        return story_text

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Streamlit app
st.set_page_config(page_icon="🧾", page_title="AI Story Generator")

hints = st.text_input("Enter hints for the story:")
genre = st.selectbox("Select the genre of the story:", ["Fantasy", "Science Fiction", "Mystery", "Romance", "Horror", "Adventure"])
length = st.selectbox("Select the desired length of the story:", ["short", "medium", "long"])

if st.button("Generate Story"):
    story = generate_story(hints, genre, length)
    if story:
        st.subheader("Generated Story:")
        st.write(story)
    else:
        st.error("Failed to generate story.")
