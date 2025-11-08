import streamlit as st
import json
from datetime import datetime
import pandas as pd  # Add this import at the top

# Page config
st.set_page_config(
    page_title="Pocket Mini App",
    page_icon="❤️",
    layout="wide"
)

# Initialize session state
if 'count' not in st.session_state:
    st.session_state.count = 0
if 'notes' not in st.session_state:
    st.session_state.notes = []
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'round' not in st.session_state:
    st.session_state.round = 1

# Header
st.title("Pocket Mini App")
st.markdown("A tiny pack: counter, notes, and more!")

# Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Counter & Notes")
    
    # Counter
    st.write(f"Clicks: {st.session_state.count}")
    if st.button("Increment"):
        st.session_state.count += 1
    if st.button("Reset Counter"):
        st.session_state.count = 0
    
    # Notes
    st.divider()
    note_text = st.text_input("Write a quick note...")
    if st.button("Add Note") and note_text.strip():
        st.session_state.notes.insert(0, {
            'id': datetime.now().timestamp(),
            'text': note_text
        })
    
    if st.session_state.notes:
        for note in st.session_state.notes:
            col1, col2 = st.columns([5,1])
            with col1:
                st.text(note['text'])
            with col2:
                if st.button("Delete", key=f"del_{note['id']}"):
                    st.session_state.notes = [n for n in st.session_state.notes if n['id'] != note['id']]
                    st.rerun()

with col2:
    st.subheader("Score Board")
    st.metric("Current Score", st.session_state.score)
    st.metric("Round", st.session_state.round)
    
    if st.button("Next Round"):
        st.session_state.round += 1
    if st.button("Reset Game"):
        st.session_state.score = 0
        st.session_state.round = 1

# Export section
st.divider()
st.subheader("Share & Export")
if st.button("Export Data"):
    data = {
        "notes": st.session_state.notes,
        "score": st.session_state.score,
        "count": st.session_state.count
    }
    st.download_button(
        "Download JSON",
        data=json.dumps(data, indent=2),
        file_name="pocket-data.json",
        mime="application/json"
    )

st.divider()
st.subheader("File Upload")
uploaded_file = st.file_uploader("Choose a file", type=['csv', 'json', 'txt'])

if uploaded_file is not None:
    # Get file type from extension
    file_type = uploaded_file.name.split('.')[-1].lower()
    
    try:
        if file_type == 'csv':
            # Read CSV file
            df = pd.read_csv(uploaded_file)
            st.write("CSV Data:")
            st.dataframe(df)
            
        elif file_type == 'json':
            # Read JSON file
            data = json.load(uploaded_file)
            st.write("JSON Data:")
            st.json(data)
            
        elif file_type == 'txt':
            # Read text file
            text_contents = uploaded_file.read().decode('utf-8')
            st.write("File Contents:")
            st.text(text_contents)
            
        # Show file details
        st.write(f"Filename: {uploaded_file.name}")
        st.write(f"File size: {uploaded_file.size} bytes")
        
        # Option to save uploaded data
        if st.button("Save to Notes"):
            new_note = {
                'id': datetime.now().timestamp(),
                'text': f"Uploaded from {uploaded_file.name}"
            }
            st.session_state.notes.insert(0, new_note)
            st.success("File contents saved to notes!")
            
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")