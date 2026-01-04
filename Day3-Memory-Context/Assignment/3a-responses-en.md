✅ ADK components imported successfully.
✅ API key loaded from .env file
✅ Helper functions defined.

================================================================================
SECTION 2: Stateful Agent with InMemorySessionService
================================================================================
✅ Stateful agent initialized!
   - Application: default
   - User: default
   - Using: InMemorySessionService

 ### Session: stateful-agentic-session

User > Hi, I am Sam! What is the capital of United States?
gemini-2.5-flash-lite >  Hi Sam! The capital of the United States is Washington, D.C.

User > Hello! What is my name?
gemini-2.5-flash-lite >  You told me your name is Sam.

================================================================================
SECTION 3: Persistent Sessions with DatabaseSessionService
================================================================================
✅ Upgraded to persistent sessions!
   - Database: my_agent_data.db
   - Sessions will survive restarts!

 ### Session: test-db-session-01

User > Hi, I am Sam! What is the capital of the United States?
gemini-2.5-flash-lite >  Hello Sam! The capital of the United States is Washington, D.C.

User > Hello! What is my name?
gemini-2.5-flash-lite >  Your name is Sam.

--- Database Contents ---
['app_name', 'session_id', 'author', 'content']
('default', 'test-db-session-01', 'user', '{"parts": [{"text": "Hi, I am Sam! What is the capital of the United States?"}], "role": "user"}')
('default', 'test-db-session-01', 'text_chat_bot', '{"parts": [{"text": "Hello Sam! The capital of the United States is Washington, D.C."}], "role": "model"}')
('default', 'test-db-session-01', 'user', '{"parts": [{"text": "Hello! What is my name?"}], "role": "user"}')
('default', 'test-db-session-01', 'text_chat_bot', '{"parts": [{"text": "Your name is Sam."}], "role": "model"}')

================================================================================
SECTION 4: Context Compaction
================================================================================
/Users/benogren/Desktop/projects/AI-Agents-Intensive-Course/Day-3/day_3a_agent_sessions.py:215: UserWarning: [EXPERIMENTAL] EventsCompactionConfig: This feature is experimental and may change or be removed in future versions without notice. It may introduce breaking changes at any time.
  events_compaction_config=EventsCompactionConfig(
✅ Research App upgraded with Events Compaction!

 ### Session: compaction_demo

User > What is the latest news about AI in healthcare?
gemini-2.5-flash-lite >  I can provide you with a summary of recent developments in AI in healthcare. However, please keep in mind that "latest" news can change very rapidly. To get the absolute most up-to-the-minute information, I would recommend checking reputable technology and healthcare news sources.

Here are some of the key trends and recent developments in AI in healthcare:

**1. Advancements in Diagnostics and Imaging:**

*   **Improved Accuracy:** AI algorithms are becoming increasingly sophisticated at analyzing medical images (X-rays, CT scans, MRIs, pathology slides) to detect diseases like cancer, diabetic retinopathy, and cardiovascular conditions with higher accuracy and often earlier than human interpretation alone.
*   **Faster Analysis:** AI can significantly speed up the review of large volumes of images, helping radiologists and pathologists prioritize critical cases and reduce turnaround times.
*   **New Applications:** Research is expanding to use AI for diagnosing rarer diseases or identifying subtle patterns that might be missed by the human eye.

**2. Drug Discovery and Development:**

*   **Accelerated Research:** AI is being used to identify potential drug targets, predict the efficacy of drug candidates, and optimize clinical trial design, drastically shortening the time and cost of bringing new treatments to market.
*   **Personalized Medicine:** AI can analyze vast datasets of patient genomic, lifestyle, and treatment response data to identify the most effective treatments for individual patients.

**3. Predictive Analytics and Early Intervention:**

*   **Disease Outbreak Prediction:** AI models can analyze public health data, social media trends, and travel patterns to predict and track the spread of infectious diseases.
*   **Patient Risk Stratification:** AI can identify patients at high risk for developing certain conditions (e.g., sepsis, heart failure, readmission) allowing for proactive interventions and personalized care plans.
*   **Early Warning Systems:** AI-powered systems in hospitals can monitor patient vital signs and other data to provide early warnings of deteriorating conditions.

**4. Robotic Surgery and Medical Devices:**

*   **Enhanced Precision:** AI is being integrated into robotic surgical systems to provide surgeons with greater precision, dexterity, and control during complex procedures.
*   **Assisted Decision-Making:** AI can offer real-time guidance and suggestions to surgeons during operations.
*   **Smart Medical Devices:** Wearable devices and implantable sensors powered by AI can continuously monitor patient health, detect anomalies, and alert healthcare providers.

**5. Administrative and Operational Efficiency:**

*   **Streamlining Workflows:** AI is automating administrative tasks like scheduling, billing, and medical record management, freeing up healthcare professionals to focus on patient care.
*   **Optimizing Resource Allocation:** AI can help hospitals manage resources more efficiently, predicting patient flow and staffing needs.
*   **Virtual Assistants and Chatbots:** AI-powered chatbots are being used for patient engagement, answering common questions, booking appointments, and providing preliminary symptom checks.

**6. Challenges and Ethical Considerations:**

Despite the rapid progress, there are ongoing challenges and important ethical considerations:

*   **Data Privacy and Security:** Protecting sensitive patient data is paramount.
*   **Bias in AI Algorithms:** Ensuring that AI models are fair and do not perpetuate existing healthcare disparities is crucial.
*   **Regulatory Approval:** Navigating the complex regulatory landscape for AI-powered medical devices and software is essential.
*   **Clinician Adoption and Trust:** Building trust and ensuring that healthcare professionals are adequately trained to use AI tools effectively.
*   **Explainability and Transparency:** Understanding how AI models arrive at their conclusions is important for clinical decision-making.

**To get the most up-to-date information, I recommend checking sources like:**

*   **Major Tech News Outlets:** TechCrunch, The Verge, Wired, Ars Technica
*   **Healthcare-Specific News:** FierceHealthcare, STAT News, MedCity News
*   **Reputable Medical Journals:** JAMA, The Lancet, Nature Medicine (often publish groundbreaking research)
*   **Major News Organizations with strong science/tech sections:** The New York Times, The Wall Street Journal, BBC News

Is there a specific area of AI in healthcare you're most interested in learning more about? For example, are you curious about AI in cancer detection, drug development, or something else?

 ### Session: compaction_demo

User > Are there any new developments in drug discovery?
gemini-2.5-flash-lite >  Yes, there are **very significant and ongoing developments** in AI-driven drug discovery. This is one of the most impactful areas where AI is transforming healthcare. Here's a breakdown of what's new and exciting:

**1. Accelerated Target Identification:**

*   **Genomic and Proteomic Analysis:** AI is excelling at analyzing massive datasets from genomics, transcriptomics, proteomics, and metabolomics. It can identify novel disease-causing genes, proteins, or pathways that were previously unknown or too complex for traditional analysis. This helps pinpoint the most promising targets for new drugs.
*   **Literature Mining and Knowledge Graphs:** Advanced Natural Language Processing (NLP) models can "read" and synthesize information from millions of scientific papers, patents, and clinical trial reports. This helps researchers uncover hidden connections and identify potential targets much faster than manual review.

**2. Novel Molecule Design and Generation:**

*   **Generative AI Models:** This is a major area of advancement. Models like Variational Autoencoders (VAEs) and Generative Adversarial Networks (GANs) are being used to design entirely new molecular structures with desired properties (e.g., high binding affinity to a target, good solubility, low toxicity).
*   **De Novo Design:** Instead of screening existing libraries, AI can create "from scratch" molecules that have never existed before, potentially leading to more innovative and effective therapies.

**3. Improved Drug Candidate Screening and Optimization:**

*   **Predictive Modeling:** AI can predict how well a potential drug molecule will bind to its target, its absorption, distribution, metabolism, excretion, and toxicity (ADMET) properties, and even its potential side effects. This significantly reduces the number of molecules that need to be synthesized and tested in labs.
*   **Virtual Screening:** AI algorithms can rapidly screen vast virtual libraries of compounds against disease targets, identifying promising candidates for further investigation.
*   **Multi-Objective Optimization:** AI can optimize drug candidates for multiple properties simultaneously, such as efficacy, safety, and manufacturability.

**4. Revolutionizing Clinical Trials:**

*   **Patient Stratification:** AI can analyze patient data to identify subgroups that are most likely to respond to a particular drug. This leads to more efficient and successful clinical trials.
*   **Predicting Trial Success:** AI models are being developed to predict the likelihood of a clinical trial's success, helping companies make better investment decisions.
*   **Designing More Efficient Trials:** AI can help optimize trial protocols, select appropriate endpoints, and identify suitable trial sites.

**5. Repurposing Existing Drugs:**

*   **Finding New Uses:** AI can analyze drug databases and patient data to identify existing drugs that might be effective for treating different diseases. This is a faster and often less expensive route to new therapies.

**Key Players and Recent Trends:**

*   **AI-Native Drug Discovery Companies:** A surge of startups (e.g., Recursion Pharmaceuticals, Exscientia, Atomwise, BenevolentAI) are built from the ground up with AI at their core. Many are forming partnerships with established pharmaceutical giants.
*   **Big Pharma Embracing AI:** Major pharmaceutical companies are heavily investing in AI capabilities, either by building their own teams or collaborating with AI specialists.
*   **Focus on Specific Diseases:** While AI is broadly applicable, there's a strong focus on using it for challenging areas like neurodegenerative diseases (Alzheimer's, Parkinson's), rare diseases, and oncology.
*   **The Rise of "Active Learning" and "Reinforcement Learning":** These AI techniques allow models to learn iteratively from experimental results, continuously improving their predictions and molecule designs.

**Challenges Remain:**

*   **Experimental Validation:** AI predictions still need rigorous experimental validation in the lab and in clinical trials.
*   **Data Quality and Standardization:** The accuracy of AI models heavily relies on high-quality, well-annotated data.
*   **Regulatory Pathways:** While progress is being made, clear regulatory pathways for AI-discovered drugs are still evolving.
*   **"Black Box" Problem:** Understanding *why* an AI model makes a particular prediction can still be challenging, which is important for scientific rigor and regulatory scrutiny.

In summary, AI is no longer just a buzzword in drug discovery; it's becoming an indispensable tool that is fundamentally changing how new medicines are found, designed, and developed. The pace of innovation here is incredibly rapid.

 ### Session: compaction_demo

User > Tell me more about the second development you found.
gemini-2.5-flash-lite >  You're asking about the **second development** I mentioned in my previous answer, which was:

**2. Novel Molecule Design and Generation**

This is a truly groundbreaking aspect of AI in drug discovery. Instead of just *finding* existing molecules that *might* work, AI is now actively **creating entirely new molecular structures** with specific, desired characteristics.

Here's a deeper dive into how this works and why it's so significant:

**How it Works: The Power of Generative AI**

The core technology behind this is **Generative AI**. Think of it like this:

*   **Traditional Machine Learning:** Often focuses on prediction (e.g., predicting if a molecule will bind to a target).
*   **Generative AI:** Focuses on creation (e.g., creating a *new* molecule that *will* bind to a target).

Several types of generative AI models are particularly relevant:

*   **Variational Autoencoders (VAEs):** These models learn a compressed "representation" (a kind of blueprint) of existing molecules. They can then "decode" this representation to generate new molecules that are similar to what they've learned but are still novel.
*   **Generative Adversarial Networks (GANs):** GANs consist of two neural networks: a "generator" that creates new molecules and a "discriminator" that tries to distinguish between real molecules and the ones generated. Through this adversarial process, the generator gets progressively better at creating highly realistic and novel molecules.
*   **Reinforcement Learning (RL) Agents:** These agents can be trained to "explore" the vast chemical space and learn to generate molecules that satisfy specific "rewards," such as high binding affinity, good drug-likeness, or low toxicity.

**Key Capabilities and Outcomes:**

*   **De Novo Design ("From Scratch"):** This is the most revolutionary aspect. AI doesn't just tweak existing drug structures; it can design molecules from the ground up, exploring chemical possibilities that human chemists might not have conceived of.
*   **Targeted Property Optimization:** Researchers can specify the properties they want in a new drug molecule. For example, they might ask the AI to design a molecule that:
    *   **Binds strongly to a specific protein target** (high affinity).
    *   **Has good "drug-likeness"**: This includes factors like solubility, permeability across cell membranes, and stability.
    *   **Minimizes toxicity**: Predicts and avoids common toxic side effects.
    *   **Has a specific "pharmacokinetic" profile**: How the drug is absorbed, distributed, metabolized, and excreted in the body.
*   **Navigating Vast Chemical Space:** The number of possible molecules is astronomically large (estimated to be more than the number of atoms in the universe). AI can efficiently search and navigate this "chemical space" to find promising candidates, something that's impossible to do manually.
*   **Accelerated Design Cycles:** Traditionally, designing and optimizing a drug candidate could take years. AI can condense this process into months or even weeks.

**Why is this so Important?**

*   **Unlocking Novel Therapies:** It allows for the discovery of entirely new classes of drugs that could tackle diseases that are currently untreatable or poorly treated.
*   **Addressing "Undruggable" Targets:** Some disease targets are notoriously difficult to drug with conventional methods. AI's ability to design novel chemical structures can potentially overcome these challenges.
*   **Faster and Cheaper Drug Development:** By creating better drug candidates from the outset, AI can reduce the number of failed experiments and clinical trials, saving immense time and resources.

**Example Scenarios:**

Imagine a researcher is trying to find a drug to inhibit a newly discovered cancer-causing enzyme. Instead of sifting through millions of existing compounds, they can use an AI generative model. They tell the AI: "Design me a molecule that binds tightly to the active site of Enzyme X, is soluble in water, and doesn't interact with known off-target proteins." The AI then generates a list of novel candidate molecules that meet these criteria, ready for synthesis and testing.

This capability of AI to not just analyze but also *create* novel chemical entities is a paradigm shift, opening up a new frontier in the quest for life-saving medicines.

 ### Session: compaction_demo

User > Who are the main companies involved in that?
gemini-2.5-flash-lite >  You're asking about the companies involved in the **Novel Molecule Design and Generation** aspect of AI in drug discovery. This is a dynamic space, and it's important to distinguish between:

1.  **AI-Native Drug Discovery Companies:** These companies were founded with AI as their core technology, specifically for drug discovery.
2.  **Established Pharmaceutical Companies:** These companies are increasingly adopting and investing in AI capabilities, often through partnerships or internal development.

Here are some of the prominent players and their approaches:

**1. Leading AI-Native Drug Discovery Companies:**

These companies are at the forefront of using AI for de novo molecule design and generation:

*   **Exscientia:** A pioneer in the field. They use AI to design molecules with specific properties and have several AI-designed drugs in clinical trials, including for cancer and autoimmune diseases. They are known for their focus on the entire drug discovery process.
*   **Atomwise:** Specializes in using deep learning for small molecule drug discovery. Their AtomNet® platform predicts how well small molecules will bind to target proteins, aiding in the design of new compounds. They often partner with pharmaceutical companies.
*   **Recursion Pharmaceuticals:** While they use AI across many aspects of drug discovery, they are strong in analyzing vast biological and chemical datasets to identify novel drug candidates and understand disease mechanisms, which feeds into their molecule generation efforts.
*   **BenevolentAI:** Focuses on using AI to analyze complex biological data and identify novel drug targets. They then leverage AI for molecule design and optimization to develop new therapies for a range of diseases.
*   **Insilico Medicine:** Known for its end-to-end AI platform that spans target discovery, molecule generation, and clinical trial prediction. They have achieved significant milestones in moving AI-designed drugs from discovery to clinical trials rapidly.
*   **Schrödinger:** While a long-standing player in computational chemistry, Schrödinger has significantly integrated advanced AI and machine learning into its platform, enhancing its capabilities for designing and predicting the properties of novel molecules.
*   **Relay Therapeutics:** Focuses on understanding and targeting protein motion, using a combination of experimental and computational approaches, including AI, to design novel small molecules that modulate protein function.

**2. Major Pharmaceutical Companies Investing Heavily in AI for Molecule Design:**

These large pharmaceutical giants are not developing AI from scratch in the same way the native companies do, but they are integrating advanced AI capabilities into their R&D pipelines, often through collaborations or by building their own internal AI teams.

*   **Pfizer:** Has been actively partnering with AI drug discovery firms and investing in internal AI capabilities for target identification and molecule design.
*   **Merck (MSD):** Like Pfizer, Merck is exploring AI for various stages of drug discovery, including the generation of novel chemical entities.
*   **Novartis:** Has a strong commitment to digital transformation and AI, and they are leveraging these technologies to accelerate drug design and discovery.
*   **AstraZeneca:** Is investing in AI and machine learning to enhance its R&D productivity, including in the area of novel molecule generation.
*   **Johnson & Johnson:** Has various initiatives focused on AI and data science to improve drug discovery and development, including designing new drug candidates.
*   **Roche/Genentech:** Known for its scientific innovation, Roche is incorporating AI to streamline its drug discovery process, from target identification to molecule design.

**Partnerships and Collaborations are Key:**

It's important to note that the landscape is characterized by a lot of **partnerships and collaborations**. AI-native companies often partner with large pharmaceutical companies, bringing their specialized AI expertise to the established players' vast resources, drug development experience, and clinical trial infrastructure.

This dynamic interplay between cutting-edge AI startups and experienced pharmaceutical giants is driving rapid progress in the field of novel molecule design and generation.
--- Searching for Compaction Summary Event ---

✅ SUCCESS! Found the Compaction Event:
  Author: user

 Compacted information: model_version=None content=None grounding_metadata=None partial=None turn_complete=None finish_reason=None error_code=None error_message=None interrupted=None custom_metadata=None usage_metadata=None live_session_resumption_update=None input_transcription=None output_transcription=None avg_logprobs=None logprobs_result=None cache_metadata=None citation_metadata=None invocation_id='2c3343d6-33dd-4654-83a1-da57e8f8d29d' author='user' actions=EventActions(skip_summarization=None, state_delta={}, artifact_delta={}, transfer_to_agent=None, escalate=None, requested_auth_configs={}, requested_tool_confirmations={}, compaction={'start_timestamp': 1763136931.565589, 'end_timestamp': 1763136940.980465, 'compacted_content': {'parts': [{'function_call': None, 'code_execution_result': None, 'executable_code': None, 'file_data': None, 'function_response': None, 'inline_data': None, 'text': 'The user inquired about the latest news in AI in healthcare. The AI agent provided a comprehensive overview of key trends, including advancements in diagnostics, drug discovery, predictive analytics, robotic surgery, and administrative efficiency. It also highlighted the challenges and ethical considerations, such as data privacy, bias, and regulatory approval.\n\nThe user then specifically asked for more information on AI in drug discovery. The AI agent elaborated on this topic, detailing how AI accelerates target identification, enables novel molecule design and generation using generative AI (VAEs, GANs, RL), improves candidate screening, revolutionizes clinical trials through patient stratification and prediction, and aids in drug repurposing. The agent also mentioned the rise of AI-native drug discovery companies and the increasing adoption by big pharma, while acknowledging remaining challenges like experimental validation and data quality.\n\nFinally, the user asked for more details on the "Novel Molecule Design and Generation" development. The AI agent explained this concept further, emphasizing the role of generative AI in creating entirely new molecular structures. It delved into the mechanisms of VAEs, GANs, and RL agents, and outlined the capabilities of de novo design, targeted property optimization, and navigation of chemical space. The agent concluded by explaining the significance of this development in unlocking novel therapies, addressing difficult targets, and accelerating drug development.', 'thought': None, 'thought_signature': None, 'video_metadata': None}], 'role': 'model'}}, end_of_agent=None, agent_state=None, rewind_before_invocation_id=None) long_running_tool_ids=set() branch=None id='0ce1ea05-a480-4bb8-8409-6b2baf184ca8' timestamp=1763136947.390988

================================================================================
SECTION 5: Working with Session State
================================================================================
✅ Agent with session state tools initialized!

 ### Session: state-demo-session

User > Hi there, how are you doing today? What is my name?
gemini-2.5-flash-lite >  Hello! I'm doing well, thank you for asking. I'm not sure what your name is, though. I don't have access to your personal information. If you'd like to tell me your name, I can try to remember it for you!

User > My name is Sam. I'm from Poland.
Warning: there are non-text parts in the response: ['function_call'], returning concatenated text result from text parts. Check the full candidates.content.parts accessor to get the full model response.
gemini-2.5-flash-lite >  Nice to meet you, Sam! I'll be sure to remember that you're from Poland.


User > What is my name? Which country am I from?
gemini-2.5-flash-lite >  I recall that your name is Sam and you are from Poland.
Session State Contents:
{'user:name': 'Sam', 'user:country': 'Poland'}

🔍 Notice the 'user:name' and 'user:country' keys storing our data!

 ### Session: new-isolated-session

User > Hi there, how are you doing today? What is my name?
gemini-2.5-flash-lite >  Hello! I'm doing great, thank you for asking. I'd love to tell you your name, but I don't have access to that information. My memory is fresh with every conversation. If you'd like, you can tell me your name, and I'll remember it for our current chat!
✅ Cleaned up old database files