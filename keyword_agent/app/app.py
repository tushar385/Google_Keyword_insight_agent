import streamlit as st
import os

# Path to your insights directory
# insights_dir = "/home/latitude/Documents/tap/keyword_agent/insights"
insights_dir = "./insights"  # Adjusted to be relative to the working directory

# Function to read file content
def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Dynamically generate options from file names
txt_files = [f for f in os.listdir(insights_dir) if f.endswith(".txt")]
options = [os.path.splitext(f)[0].replace("insights_", "").capitalize() for f in txt_files]
file_mapping = dict(zip(options, txt_files))

# Page description
st.title("Insights Analysis")
st.write("Insight Analysis for Keyword Agent.")

# Dropdown selection
selected_option = st.selectbox("Choose an option:", options)

# Trigger button
if st.button("Trigger Action"):
    if selected_option in file_mapping:
        file_name = file_mapping[selected_option]
        content = read_file(os.path.join(insights_dir, file_name))
        st.write(f"### Content from {file_name}:")
        st.write(content)
    else:
        st.write("Please select a valid option.")





# import streamlit as st
# import os

# # Manual options list
# options = ["Dentist", "Furniture", "Lawyer", "Mechanic"]  # Add more manually
# selected_option = st.selectbox("Choose an option:", options)

# # File path pattern (assumes consistent naming)
# insights_dir = "/home/latitude/Documents/tap/keyword_agent/insights"

# # Create a dynamic file name based on the selected option
# file_name = f"{selected_option}.txt"  # Construct the file name directly from the selected option
# file_path = os.path.join(insights_dir, file_name)

# # Page description
# st.title("Insights Analysis")
# st.write("Insight Analysis for Keyword Agent.")

# # Trigger button (always works dynamically for selected option)
# if st.button("Trigger Action"):
#     if os.path.exists(file_path):
#         with open(file_path, 'r') as f:
#             content = f.read()
#         st.write(f"### Content from {file_name}:")
#         st.write(content)
#     else:
#         st.warning(f"No file found for `{selected_option}`.")


