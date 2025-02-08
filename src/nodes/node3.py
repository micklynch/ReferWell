from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from utils.console_config import pretty_print_text, print_ruler, print_section_header


def generate_node(state):
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    prompt = ChatPromptTemplate.from_template(
        f"""

You are a primary care physician (PCP) writing a formal referral letter to a medical specialist. Your goal is to provide the specialist with all the necessary information to understand the patient's medical history, current condition, and the reason for the referral. You will be provided with clinical data in the format of {{clinical_data}}. Specialist data {{specialist_data}} Use this data to generate a concise and informative referral letter.

**Guidelines:**

1.  **Letter Format:** Structure the letter with a clear and professional format, including:
    *   Your Name, Practice, Address, Phone Number, and Fax Number from {{referrer_details}}
    *   Date (pick any date in February 2025 as a placeholder)
    *   Specialist's Name, Title, Department, Hospital/Clinic, Address
    *   Salutation (e.g., "Dear Dr. [Specialist's Last Name],")
    *   Body of the Letter (see content guidelines below)
    *   Closing (e.g., "Sincerely,"),
    *   Your Signature (represented as "[PCP's Name], MD")

2.  **Patient Details:**  Start the letter by clearly identifying the patient:
    *   Full Name (including title and preferred name, if different)
    *   Date of Birth
    *   Sex at Birth
    *   Medical Record Number
    *   Full Address and Postcode
    *   Contact Telephone Number(s)
    
3.  **Reason for Referral (Chief Complaint):**  Clearly and concisely state the reason for the referral to be {{reason}}.  Be specific. Use medical terms, even if the reason is written in non-medical language. Examples:
    Example 1: Knee Pain
    * Non-Medical Language: "Patient is experiencing persistent knee pain that's limiting their ability to walk and is not improving despite taking painkillers."
    * Reason for Referral (Chief Complaint): "Referral for evaluation and management of persistent right knee arthralgia and functional limitation despite conservative management with analgesics. Rule out degenerative joint disease requiring orthopedic intervention."
    Explanation & Justification:
        "Arthralgia" replaces "knee pain" for a more medical term.
        "Functional limitation" describes the walking difficulty in medical terms.
        "Conservative management with analgesics" expresses "taking painkillers."
        "Degenerative joint disease" explicitly states the most likely root cause in Medical language.
        "Orthopedic intervention" suggests surgery as a potential end, while refraining from overtly dictating the specialist's treatment.
    
    Example 2: Skin Rash
    * Non-Medical Language: "Patient has a rash that won't go away, and it's very itchy."
    * Reason for Referral (Chief Complaint): "Referral for evaluation and management of a chronic, pruritic (itchy) dermatosis of unknown etiology. Rule out allergic contact dermatitis, eczema, or other inflammatory skin conditions."
    Explanation & Justification:
        "Dermatosis" replaces 'rash" and refers to any skin condition.
        "Pruritic" is the medical term for "itchy."
        "Etiology" is included to specify if the root cause of the dermatosis is known.
        "Allergic contact dermatitis, eczema, or other inflammatory skin conditions" provides specific differential diagnoses.
    
    Example 3: Chronic Cough
    * Non-Medical Language: "Patient has been coughing for several months and it won't go away. They are taking over-the-counter cough medicine."
    * Reason for Referral (Chief Complaint): "Referral for further evaluation of chronic cough, exceeding 8 weeks duration, unresponsive to over-the-counter antitussives. Rule out underlying pulmonary pathology such as post-infectious cough, asthma, or GERD related cough." (Consider infectious causes such as TB if relevant patient factors are present.)
    Explanation & Justification:
        "Chronic cough, exceeding 8 weeks duration" gives a specific medical definition of duration of the symptom.
        "Unresponsive to over-the-counter antitussives" states that cough medicine did not help.
        "Pulmonary pathology" includes lung related root causes.
        "Post-infectious cough, asthma, or GERD related cough" provides specific hypotheses for root causes.
        "Consider infectious causes such as TB" demonstrates how external factors may influence the clinical question or decision making.
    

4.  **Relevant Medical History:** Include only details pertinent to the referral from the following FHIR objects: {{clinical_data}}. Do **NOT** include irrelevant information or placeholders for missing data. If there is no data or missing data fields in {{clinical_data}}, leave it blank and do not create placeholders.
    *   **Active Medical Conditions:** List all current diagnoses relevant to the reason for referral. If no data, remove this line.
    *   **Relevant Resolved Medical Conditions:** Include any previous conditions that might contribute to the present problem. If no data, remove this line.
    *   **Previous Procedures/Surgeries:**  List relevant past procedures and surgeries (date and type). If no data, remove this line.
    *   **Relevant Investigations/Imaging:** Include significant findings from previous relevant imaging or diagnostic tests (date and result summary).  Specify if you're including external radiology reports as separate attachments. If no data, remove this line.
    *   **Medications:** List all current medications the patient is taking that relate to the reason for referral. Include dosages if available in the clinical_data (e.g., blood thinners, relevant pain medication). If no data, remove this line.
    *   **Allergies:**  Specifically list any known allergies, *especially* to medications or materials relevant to potential specialist treatments or tests. Specify allergic reaction type. If no data, remove this line.
    *   **Relevant Social History:** Consider including details on smoking, alcohol, or drug use if pertinent.

5.  **Your Expectations:** Briefly state what you hope the specialist will accomplish.  Examples:
    *   "I would be grateful for your assessment, diagnosis, and recommendations for management."
    *   "I am looking for your guidance on further diagnostic workup and treatment options."
    *   "I request your opinion on whether [Specific intervention, e.g., surgery] is appropriate for this patient."

6. **Tone and Conciseness:** Remain professional and avoid unnecessary jargon. Be concise and to the point. Prioritize key information.

7. **Negative Constraints:**
    *   **Do not include introductory or concluding pleasantries not typically found in formal medical letters.** (e.g. "I hope this letter finds you well," or "It's a pleasure to refer this patient to you.")
    *   **Do not flatter the specialist or mention their expertise in a generic or insincere way.** Focus on the patient's needs.
    *   **Do not invent information not present in the {{clinical_data}}.** If information is missing, leave it empty or do not mention it.

**Example 1 (Simple):**

Patient Name: John Smith, DOB: 1948-03-15, MRN: 1234567
Reason for Referral: Persistent right knee pain despite conservative management.
Relevant History: Osteoarthritis of the right knee for the last 5 years. Tried physical therapy and NSAIDs with limited relief.
Medications: Tylenol 500mg PRN.
Allergies: NKDA

**Desired Output (Example Letter - The LLM is expected to build on this and use the full format defined above):**

[Your Name, Practice, Address, Phone Number, Fax Number]
[Date]

[Specialist's Name, Title, Department, Hospital/Clinic, Address]

Dear Dr. [Specialist's LastName],

I am referring Mr. John Smith (DOB: 1948-03-15, MRN: 1234567) to your care for persistent right knee pain.  He has a 5-year history of osteoarthritis in the right knee and has had limited relief from physical therapy and NSAIDs. He currently takes Tylenol as needed. He has no known drug allergies.

I would appreciate your assessment and recommendations for further management, including consideration for potential surgical intervention.

Sincerely,

[Your Name], MD



**Example 2 (More Complex):**

Patient Name: Jane Doe, DOB: 1972-08-22, MRN: 9876543
Reason for Referral: Evaluate for possible autoimmune etiology of recent onset bilateral hand and wrist pain and swelling.
Relevant History: Diagnosed with hypothyroidism 3 years ago, well-controlled on levothyroxine.  Recent onset (past 2 months) of bilateral MCP and wrist joint pain and swelling.  Reports morning stiffness lasting >1 hour.
Medications: Levothyroxine 100mcg daily, Ibuprofen 200mg PRN
Allergies: Sulfa drugs - hives
Exam Findings: Bilateral MCP and wrist joint swelling and tenderness.  Decreased grip strength bilaterally.
Relevant Investigations:  CBC and CMP within normal limits. ESR elevated at 45 mm/hr.  RF pending.




**Desired Output (Example Letter):**

[Your Name, Practice, Address, Phone Number, Fax Number]
[Date]

[Specialist's Name, Title, Department, Hospital/Clinic, Address]

Dear Dr. [Specialist's Last Name],

I am referring Ms. Jane Doe (DOB: 1972-08-22, MRN: 9876543) to your care for evaluation of recent onset bilateral hand and wrist pain and swelling, possibly secondary to an autoimmune etiology.  She reports morning stiffness lasting greater than 1 hour.

Relevant history includes hypothyroidism, well-controlled on levothyroxine. Exam reveals bilateral MCP and wrist joint swelling and tenderness, and decreased grip strength.  ESR is elevated at 45 mm/hr. RF is pending.  Current medications include levothyroxine and ibuprofen PRN. She reports an allergy to sulfa drugs, causing hives.

I would appreciate your assessment, diagnosis, and recommendations for management.

Sincerely,

[Your Name], MD



**Now, generate the referral letter based on the following clinical data: {{clinical_data}} and reason: {{reason}} from {{referrer_details}}**
IMPORTANT INFORMATION: Do not leave any placeholders. 

""")

    chain = (
            prompt | model | StrOutputParser()
    )
    referral_letter = chain.invoke({
        "clinical_data": state['clinical_data'], 
        "reason": state['reason'],
        "referrer_details": state['referrer_details'] ,
        "specialist_data": state['specialist_data']
        })
    print_ruler()
    print_section_header("GENERATED LETTER", "yellow")
    print_ruler()
    pretty_print_text(referral_letter, panel=True)
    return {"referral_letter":  referral_letter}

