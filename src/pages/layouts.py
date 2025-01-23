import streamlit as st

st.title("Layouts and Containers Showcase")
st.write("This page demonstrates the usage of different layout and container components in Streamlit.")

# Sidebar
with st.sidebar:
    st.header("Sidebar Example")
    st.write("This is the sidebar.")
    sidebar_option = st.selectbox("Choose a layout to highlight:", ["Columns", "Containers", "Tabs", "Expanders"])
    st.write(f"You selected: {sidebar_option}")

# Columns
st.header("Columns")
vertical_alignment = st.selectbox(
    "Vertical alignment", ["top", "center", "bottom"], index=2
)
col1, col2, col3 = st.columns(3, vertical_alignment=vertical_alignment, border = True)

with col1:
    st.header("A cat")
    st.image("https://static.streamlit.io/examples/cat.jpg")

with col2:
    st.header("A dog")
    st.image("https://static.streamlit.io/examples/dog.jpg")

with col3:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg")

# Container
st.header("Container")
long_text = "Lorem ipsum. " * 1000

with st.container(height=300):
    st.markdown(long_text)

# Modal Dialog (via experimental API)
@st.dialog("Cast your vote")
def vote(item):
    st.write(f"Why is {item} your favorite?")
    reason = st.text_input("Because...")
    if st.button("Submit"):
        st.session_state.vote = {"item": item, "reason": reason}
        st.rerun()

if "vote" not in st.session_state:
    st.write("Vote for your favorite")
    if st.button("A"):
        vote("A")
    if st.button("B"):
        vote("B")
else:
    f"You voted for {st.session_state.vote['item']} because {st.session_state.vote['reason']}"

with st.form("my_form"):
    st.write("Inside the form")
    slider_val = st.slider("Form slider")
    checkbox_val = st.checkbox("Form checkbox")

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("slider", slider_val, "checkbox", checkbox_val)
st.write("Outside the form")



# Empty Placeholder
st.header("Empty Placeholder")
placeholder = st.empty()
if st.button("Update Placeholder"):
    placeholder.text("This text replaced the placeholder.")

# Expander
st.bar_chart({"data": [1, 5, 2, 6, 2, 1]})

with st.expander("See explanation"):
    st.write('''
        The chart above shows some numbers I picked for you.
        I rolled actual dice for these, so they're *guaranteed* to
        be random.
    ''')
    st.image("https://static.streamlit.io/examples/dice.jpg")

# Tabs
st.header("Tabs")
tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])

with tab1:
    st.header("A cat")
    st.image("https://static.streamlit.io/examples/cat.jpg", width=200)
with tab2:
    st.header("A dog")
    st.image("https://static.streamlit.io/examples/dog.jpg", width=200)
with tab3:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg", width=200)

with st.popover("Open popover"):
    st.markdown("Hello World 👋")
    name = st.text_input("What's your name?")

st.write("Your name:", name)
