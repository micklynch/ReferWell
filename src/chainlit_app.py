import chainlit as cl
from graphs.my_graph import create_graph
from dotenv import load_dotenv
from langgraph.types import Command

load_dotenv()

# Create the graph once
graph = create_graph()

# Store conversation state in local Python variables
conversation_stage = "get_patient_info"
patient_info = {}
specialty_type_options = []
specialist_options = []
selected_specialist = None

fake_referring_doctor = """
Dr. Anya Sharma, MD, 
Puget Sound Internal Medicine & Primary Care, 
1200 Madison Street, Suite 100, 
Seattle, WA 98104, 
Phone: (206) 555-2345, 
Fax: (206) 555-6789
"""

@cl.on_chat_start
async def on_start():
    global conversation_stage
    conversation_stage = "get_patient_info"
    await cl.Message("Welcome to **ReferWell - Generate Referral Letter**!").send()
    await cl.Message("🔹 Please enter the **Patient ID**:").send()

@cl.on_message
async def handle_message(message):
    global conversation_stage, patient_info, specialty_type_options, specialist_options, selected_specialist

    # --------------------------
    # 1️⃣ Collect Patient ID
    # --------------------------
    if conversation_stage == "get_patient_info":
        patient_info["patient_id"] = message.content.strip()
        await cl.Message("🔹 What is the **reason for the referral**?").send()
        conversation_stage = "get_reason"
        return

    # --------------------------
    # 2️⃣ Collect Reason for Referral
    # --------------------------
    if conversation_stage == "get_reason":
        patient_info["reason"] = message.content.strip()

        # Call Graph to Get Specialty Types
        await cl.Message("🔍 Fetching available specialty types... Please wait...").send()
        inputs = {
            "patient_id": patient_info["patient_id"],
            "reason": patient_info["reason"],
            "referrer_details": fake_referring_doctor,
        }
        thread = {"configurable": {"thread_id": 101}}
        state = graph.invoke(inputs, config=thread)
        tasks = graph.get_state(config=thread).tasks
        task = tasks[0]

        # Get Specialty Types
        specialty_list = task.interrupts[0].value.get("specialty_type", [])
        if not specialty_list:
            await cl.Message("❌ No specialty types found. Please restart.").send()
            conversation_stage = "get_patient_info"
            return

        # Store Specialty Options
        specialty_type_options = [
            (i + 1, f"{s['Display Name']}")
            for i, s in enumerate(specialty_list)
        ]

        options_display = "\n".join([f"{num}: {name}" for num, name in specialty_type_options])
        await cl.Message(f"💠 **Available Specialty Types:**\n{options_display}\n\nPlease type the **number** of your choice.").send()
        conversation_stage = "select_specialty_type"
        return

    # --------------------------
    # 3️⃣ Select Specialty Type
    # --------------------------
    if conversation_stage == "select_specialty_type":
        selected_number = message.content.strip()
        try:
            selected_number = int(selected_number)
        except ValueError:
            await cl.Message("❌ Please enter a valid number.").send()
            return

        if selected_number not in [option[0] for option in specialty_type_options]:
            await cl.Message("❌ Invalid choice. Please enter a number from the list.").send()
            return

        patient_info["specialty_type"] = specialty_type_options[selected_number - 1][1]
        await cl.Message(f"✅ You selected: **{patient_info['specialty_type']}**").send()

        # Proceed to Find Specialists
        await cl.Message("🔎 Finding specialists based on your selected specialty...").send()

        thread = {"configurable": {"thread_id": 101}}
        result = graph.invoke(Command(resume=selected_number), config=thread)
        tasks = graph.get_state(config=thread).tasks
        task = tasks[0]

        # Get Specialist List
        specialist_list = task.interrupts[0].value.get("specialist_data", [])
        if not specialist_list:
            await cl.Message("❌ No specialists found. Please restart.").send()
            conversation_stage = "get_patient_info"
            return

        # Store Specialist Options
        specialist_options = [
            (i + 1, f"{s['Doctor Name']} - {s['Specialty']} ({s['Distance']:.2f} miles)")
            for i, s in enumerate(specialist_list)
        ]

        options_display = "\n".join([f"{num}: {desc}" for num, desc in specialist_options])
        await cl.Message(f"👨‍⚕️ **Available Specialists:**\n{options_display}\n\nPlease type the **number** of your choice.").send()
        conversation_stage = "select_specialist"
        return

    # --------------------------
    # 4️⃣ Select Specialist
    # --------------------------
    if conversation_stage == "select_specialist":
        selected_specialist = message.content.strip()
        try:
            selected_specialist = int(selected_specialist)
        except ValueError:
            await cl.Message("❌ Please enter a valid number.").send()
            return

        if selected_specialist not in [option[0] for option in specialist_options]:
            await cl.Message("❌ Invalid choice. Please enter a number from the list.").send()
            return

        await cl.Message("📝 Generating Referral Letter... Please wait...").send()

        # Call Graph to Generate Referral Letter
        thread = {"configurable": {"thread_id": 101}}
        state = graph.invoke(Command(resume=selected_specialist), config=thread)
        referral_letter = state.get("referral_letter", "Referral letter content not found.")

        # Display Referral Letter
        await cl.Message(f"📄 **Referral Letter:**\n\n{referral_letter}").send()

        # End or Restart
        await cl.Message("✅ Process completed! Type `restart` to generate another referral.").send()
        conversation_stage = "restart"
        return

    # --------------------------
    # 🔄 Restart Process
    # --------------------------
    if conversation_stage == "restart" and message.content.strip().lower() == "restart":
        conversation_stage = "get_patient_info"
        patient_info = {}
        specialty_type_options = []
        specialist_options = []
        selected_specialist = None
        await cl.Message("🔄 Restarting... Please enter the **Patient ID**:").send()
        return

    # --------------------------
    # Invalid Input Handling
    # --------------------------
    await cl.Message("⚠️ I did not understand that. Please follow the prompts.").send()