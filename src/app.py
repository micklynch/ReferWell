import streamlit as st
from graphs.my_graph import create_graph
from dotenv import load_dotenv

load_dotenv()

# Set full-width clean UI
st.set_page_config(page_title="ReferWell - Generate Referral Letter", page_icon="📄", layout="centered")

# Custom CSS for styling
st.markdown("""
    <style>
    .app-name {
        font-size: 28px;
        font-weight: bold;
        color: #2c3e50;
        text-align: left;
        margin-bottom: 5px;
    }
    .app-name span {
        color: #3498db; /* Blue */
    }
    .big-title {
        font-size: 28px !important;
        font-weight: bold;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 20px;
    }
    .stTextInput>div>div>input {
        font-size: 18px;
        padding: 10px;
        border-radius: 10px;
        border: 2px solid #3498db;
    }
    .stButton>button {
        border-radius: 10px;
        background-color: #3498db;
        color: white;
        font-size: 18px;
        padding: 12px;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #2980b9;
    }
    .output-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #f8f9fa;
        border-left: 6px solid #3498db;
        font-size: 16px;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Display App Name at the Top Left
st.markdown("<h1 class='app-name'>Refer<span>Well</span></h1>", unsafe_allow_html=True)

# Page Title
st.markdown("<h1 class='big-title'>📄 Generate Referral Letter</h1>", unsafe_allow_html=True)

# Input fields
patient_id = st.text_input("🔹 Enter Patient ID", "")
# specialist = st.text_input("🔹 Specialist", "")
specialist = st.selectbox("Specialist Type", ("Cardiologist", "Orthopedic Surgeon", "Neurologist", "Dermatologist"),placeholder="Choose an option", disabled=False, index=None, label_visibility="visible")
reason = st.text_area("🔹 Reason for Referral", "", height=100)
fake_referring_doctor = """
Dr. Anya Sharma, MD, 
Puget Sound Internal Medicine & Primary Care, 
1200 Madison Street, Suite 100, 
Seattle, WA 98104, 
Phone: (206) 555-2345, 
Fax: (206) 555-6789
"""

# Generate Referral Letter button
if st.button("📝 Generate Referral Letter"):
    if patient_id.strip() and specialist.strip() and reason.strip():
        with st.spinner("Generating referral letter..."):
            inputs = {
                "patient_id": patient_id,
                "specialty_type": specialist,
                "reason": reason,
                "referrer_details": fake_referring_doctor 
            }
            graph = create_graph()
            thread = {"configurable": {"thread_id": 101}}
            result = graph.invoke(inputs, config=thread)

        # Display Referral Letter
        st.markdown("<h3 class='big-title'>📝 Referral Letter</h3>", unsafe_allow_html=True)
        st.write(f"{result.get('referral_letter', 'No data available')}")
    else:
        st.warning("Please fill in all fields.")
