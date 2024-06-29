import streamlit as st
import requests

# Function to get book recommendations from Open Library API
def get_book_recommendations(genre, num_books=100):
    url = f"https://openlibrary.org/subjects/{genre}.json?limit={num_books}"
    response = requests.get(url)
    data = response.json()
    books = data.get("works", [])
    return books

# Streamlit app
st.title("Top Book Recommendations")

# Step 1: Ask user for genre and get top 100 books
genre = st.text_input("Enter a genre (e.g., fiction, mystery, fantasy):")
if st.button("Get Top 100 Books"):
    if genre:
        top_100_books = get_book_recommendations(genre, num_books=100)
        st.session_state['top_100_books'] = top_100_books
        st.session_state['genre'] = genre
        st.write(f"Top 100 Books in {genre.capitalize()}")
        for i, book in enumerate(top_100_books, 1):
            st.write(f"{i}. {book['title']} by {book.get('authors', [{'name': 'Unknown'}])[0]['name']}")
    else:
        st.write("Please enter a genre.")

# Step 2: Allow user to get top 10 books from the top 100
if 'top_100_books' in st.session_state and len(st.session_state['top_100_books']) > 0:
    if st.button("Get Top 10 Books"):
        top_10_books = st.session_state['top_100_books'][:10]
        st.session_state['top_10_books'] = top_10_books
        st.write(f"Top 10 Books in {st.session_state['genre'].capitalize()}")
        for i, book in enumerate(top_10_books, 1):
            st.write(f"{i}. {book['title']} by {book.get('authors', [{'name': 'Unknown'}])[0]['name']}")

# Step 3: Allow user to select 1 book from the top 10
if 'top_10_books' in st.session_state and len(st.session_state['top_10_books']) > 0:
    selected_book_index = st.number_input("Select a book number from the top 10:", min_value=1, max_value=10)
    if st.button("Select Book"):
        selected_book = st.session_state['top_10_books'][selected_book_index - 1]
        st.session_state['selected_book'] = selected_book
        st.write(f"You selected: {selected_book['title']} by {selected_book.get('authors', [{'name': 'Unknown'}])[0]['name']}")

# Step 4: Conclude the task with a thank you message
if 'selected_book' in st.session_state:
    if st.button("Conclude"):
        st.write("Thank you for using the book recommendation agent!")
        st.session_state.clear()  # Clear the session state for new interactions
