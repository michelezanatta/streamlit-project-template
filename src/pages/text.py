import streamlit as st

st.title("Text Components")

# Header
st.header("Header Component")
st.write("This is an example of a **header**.")

# Subheader
st.subheader("Subheader Component")
st.write("This is an example of a **subheader**.")

# Markdown
st.markdown("### Markdown Component")
st.markdown("""
Markdown allows you to:
- **Bold** text
- *Italicize* text
- Create [links](https://streamlit.io)
- Write inline `code`
- Add lists and more!
""")

# Text
st.text("This is a simple text component.")

# Latex
st.write("### LaTeX Component")
st.latex(r"""
E = mc^2
""")

# Divider
st.write("### Divider Component")
st.divider()

# Echo
st.write("### Echo Component")
with st.echo(code_location='above'):
    st.write("This code will be printed and executed")

    def sum_number(x, y):
        return x + y
    
    st.write(sum_number(2, 3))

# Code
st.write("### Code Component")
st.code("print('Hello, Streamlit!')", language="python")

# Caption 
st.write("### Caption Component")
st.caption("This is an example of a caption.")

# Success
st.write("### Status Components")
st.success("This is a success message.")

# Info
st.info("This is an info message.")

# Warning
st.warning("This is a warning message.")

# Error
st.error("This is an error message.")

# Title with Emoji
st.write("### Title with Emoji")
st.title("Streamlit 🧠 Components")

# Text Input for Demonstration
st.write("### Interactive Text Input")
user_input = st.text_input("Enter some text:", value="Hello, Streamlit!")
st.write(f"You entered: {user_input}")

# Text Area for Demonstration
st.write("### Interactive Text Area")
user_text_area = st.text_area("Enter multiline text:", value="Line 1\nLine 2")
st.write("You entered:")
st.write(user_text_area)