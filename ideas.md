
använd existernade open source modeller API man behöver inte köra detta lokalt då jag använder dummy data men om man skulle vilja så kör man det lokalt. använd llamav3 för att generera data, en agent för att kolla den genererade datan så att den endast innehåller text stycken och inte text som förklaringar gjord av chatbotten, en agent markerar datan, en agent dubbelkolla datan. osv.

Att ta upp på möte

jag har använt LLm för att generera och markera text som används för att testa modellen. Jag skulle kunna köra en LLm lokalt och byta ut all markerad text som ett anonymizerings system.






###Roadmap
1. Project setup
   - Set up a Jupyter Notebook environment that can interact with LLMs
2. Data preperation
    - Define what categorises as sensitive information
3. Model selection
    - Use existing LLMs to detect sensitive information
    - The chosen LLM is Microsoft Persudio next points will be for tuning it.
4. Label PPI in a documnet and test the model see what it dosnt pick up on and go back to tuning it by implementing rule based systems like regex.
5. 


add imgae recognition to presidio


https://cookbook.openai.com/examples/sdg1

https://learn.microsoft.com/en-us/azure/ai-services/language-service/personally-identifiable-information/concepts/conversations-entity-categories

Langchain, Pinecone, OpenAI
Presudio? add different language.


open source?? istället för openai

with more time could i implement image recognition to presidio




Roadmap NLP

##Machine learning
Cleaning the input -Tokeniazation, Lemmatization
Input text -> vectors - Bow, TF IDF
Input -> vectors - Word2Vec, AvgWord2Vec

Librarys for ML - NLTK, Spacy

##Deep learning
Neural n/w - RNN, LSTM RNN, GRU RNN
Word embedding
BERT

LDA
tokenaziation
LLM







###Notes for Report
- new environment for the project
- 



Frågor att ställa :
kostnads effektivitet

 youtube videos/ forums som referenser?




##Refereces
https://www.youtube.com/watch?v=ENLEjGozrio&t=1s&ab_channel=KrishNaik

https://www.youtube.com/watch?v=aywZrzNaKjs&t=359s&ab_channel=Rabbitmetrics

https://www.youtube.com/watch?v=oUAYZPY-tw8&ab_channel=MG

for improving presidio
https://github.com/microsoft/presidio/discussions/767

spacy
https://spacy.io/models/sv/

