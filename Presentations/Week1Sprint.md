### ReferWell 

Doctors routinely refer patients to specialists. 

---
#### The process
In order to make the referral, the doctor needs to 
1. Identify the most appropriate specialist,
2. Collect relevant information from the patient's health record
3. Inform the patient about the referral

---
#### The Pain Point

Existing EHR-based referral systems generate generic letters that lack personalization, leading to inefficiencies (e.g., mismatched specialists, incomplete data), patient confusion, and administrative burden.

---
#### Solution Direction
ReferWell is a multi-agent referral management system designed to streamline the healthcare referral process. The initial focus is on simplifying the **identification of appropriate specialists**, **generating a referral report** with key data tailored to the specialist’s needs, and **creating a personalized letter for patients** explaining the reason for the referral.

---

### Sprint 1 Progress update
1. Team formed 🙌
2. First draft of PRD completed & Reviewed
3. Process mapped
4. E2E Langflow created

---
### Team Members
- Viraf Bankwalla
- Bharath Thippireddy
- Omid Geysar
- Michael Lynch

---
### PRD Draft
Initial draft of PRD with feedback from Amir
![](Pasted%20image%2020250126115908.png)

---
### Process Mapped
Version 1
**![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXciB34QqKS6mqGSoADB7J4tLCIcihJfeFl17VOSOo2XaPq3w_S_rtb1d7oGyqdIyn1UuZdfvI4liLabrd9Ca_L-6KiZVWnBYbvSVGV0WzQ_8vlGma4N892CQhosLY192OM-zQz9?key=nexpwaZSeQrInT_-zkEblMli)**
Version 2
**![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXcXicNAXoHnLrzC7Pg1pEHo_E_FSwW2Z3EnDAYRS5K-ayHpbhpVY4qDKYqD_ibTtt6Iydls3Zn2ZEhFLJuIFZCNlQlwR3a4EFpvS5UNSr9h3U4Tgkx4-2sARRim_ij3l_0owo2KKg?key=nexpwaZSeQrInT_-zkEblMli)**

---
### Langflow Implementation
![](Pasted%20image%2020250126120102.png)

---
### Next Steps
1. Validate with real data
	1. 10GB of Provider data (name, address, specialty)
	2. Publicly available Patient data server (FHIR standard)
2. Move implementation from Langflow to Langgraph