This file explains how to run the main anonymization system and how to follow the LLM.ipynb and Presidio.ipynb to see how the testing of the models were conducted

##Introduction
This Anonymization system of PII in swedish texts is made in java and must thererfore have python downloaded on your system.
The main system can be found under the PiiAnonymizer directory. It includes a For_tests directory which was used for the tesing of the system not having dummy data generated.

The 'anonymized_texts' directory includes texts anonymized by the models used for testing.
The 'generated_texts' directory used for the testing of all LMMs and final system
The 'generated_texts_presidio' directory used for the testing of the Presidio model (these texts are already marked)
The 'marked texts' directory include the generated texts after they gone through the marking agent, a step in the testing process.


##Installation

###Requirements
1. Python
2. Required libraries listed in 'requirements.txt'

1. Clone the repository using git clone

2. install the required packages:
   pip install -r requirements.txt

3. Create a .env file in the root directory of the project. This file should contain your OpenRouter API key:
    OPENROUTER_API_KEY=your_openrouter_api_key

##Running
1. Ensure all dependencies are installed and the .env file is properly set up.
2. Run the main file from the root with the following command:
    python PiiAnonymizer/Main.py
3. The system will read input text files from the generated_texts directory, process them through the chains, and output the anonymized texts to the        PiiAnonymizer/Anonymized_texts directory.

##Quitting
To stop the system, simply terminate the running file by pressing Ctrl+C.

##Testing
To see if the system works correclty place your text files in the 'generated_texts' folder. At download does it include 100 generated files
run the main file
Verify that the output in the 'PiiAnonymizer/Anonymized_texts' directory has replaced the PII with dummy data.


If you want to follow how the testing for the LLMs was conducted see the LLM.ipynb file as it goes from the generating of syntethic data to the results for each LMM tested.

If you want to see how the testing for the Microsoft Presidio model was conducted see the Presidio.ipynb file.