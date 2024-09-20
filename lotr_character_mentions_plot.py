
import re
import plotly.express as px
import pandas as pd

# Load the text files (assuming you have them locally)
file_1_path = '01 - The Fellowship Of The Ring.txt'
file_2_path = '02 - The Two Towers.txt'
file_3_path = '03 - The Return Of The King.txt'

# Define the list of important characters
characters = [
    "Frodo", "Sam", "Merry", "Pippin", "Gandalf", "Aragorn", 
    "Legolas", "Gimli", "Boromir", "Sauron", "Gollum", "Saruman"
]

# Read the contents of the three text files
with open(file_1_path, 'r', encoding='latin-1') as file_1,      open(file_2_path, 'r', encoding='latin-1') as file_2,      open(file_3_path, 'r', encoding='latin-1') as file_3:
    text_1 = file_1.read()
    text_2 = file_2.read()
    text_3 = file_3.read()

# Combine all the texts into one
combined_text = text_1 + text_2 + text_3

# Function to find mentions of a character and their positions in the text
def find_mentions(character, text):
    mentions = [m.start() / len(text) * 100 for m in re.finditer(character, text)]
    return mentions

# Function to extract the context around each character mention
def get_context(character, text, context_chars=30):
    context_data = []
    for match in re.finditer(character, text):
        start = max(match.start() - context_chars, 0)
        end = min(match.end() + context_chars, len(text))
        context_data.append(text[start:end].replace('\n', ' ').strip())
    return context_data

# Dictionary to store mentions and contexts for each character
character_mentions = {}
character_contexts = {}

# Loop through each character and find their mentions and contexts in the combined text
for character in characters:
    character_mentions[character] = find_mentions(character, combined_text)
    character_contexts[character] = get_context(character, combined_text)

# Convert the data into a pandas DataFrame for easier manipulation
context_data = []

for character, mentions in character_mentions.items():
    for i, mention in enumerate(mentions):
        context_data.append([character, mention, character_contexts[character][i]])

context_df = pd.DataFrame(context_data, columns=["Character", "Mention Position", "Context"])

# Calculate the approximate start positions for each book
book_starts = {
    "Start of Book I": 0,  # Beginning of the whole text
    "Start of Book II": len(text_1) / len(combined_text) * 100 * 0.5,
    "Start of Book III": len(text_1) / len(combined_text) * 100,
    "Start of Book IV": (len(text_1) + len(text_2) / 2) / len(combined_text) * 100,
    "Start of Book V": (len(text_1) + len(text_2)) / len(combined_text) * 100,
    "Start of Book VI": (len(text_1) + len(text_2) + len(text_3) / 2) / len(combined_text) * 100
}

# Create the interactive plot with context on hover
fig = px.scatter(context_df, x='Mention Position', y='Character', 
                 color='Character',  # Adding color to each character
                 hover_data={'Context': True},  # Show context on hover
                 labels={"Mention Position": "Position in Book (%)", "Character": "Character"}, 
                 title="Character Mentions Across The Lord of the Rings")

# Adding vertical lines for the start of each book
for book, position in book_starts.items():
    fig.add_vline(x=position, line_width=2, line_dash="dash", line_color="red", annotation_text=book, annotation_position="top")

# Save the plot to an HTML file
fig.write_html('lotr_character_mentions_with_hover.html')

print("Plot saved as 'lotr_character_mentions_with_hover.html'")
