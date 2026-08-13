1. Token

Token is piece of text.Sometimes tokens are words or subwords.
Like: 'I','love','AI'
Models use their own dictionary to convert text in tokens.Because all models have different dictionary.
Newer models have updated dictionary of tokens.
For example: 'I am studying at Islamia University of Bahawalpur'
In GPT 5 it shows 11 tokens(Bahawalpur with 3 tokens)
but in older GPT 4 it shows 12 tokens(Bahawalpur with 4 tokens).

2. Context Window

Context Window is amount of tokens that a LLM can use at one time.
It is the working memory of a model that it can see previous chats,new messages,system instructions with in the interaction.
Once it's memory filled new messages will give error or drop older chats.
Once old memory deleted,it don't know any previous context.
In simple words it is like a memory card which only store 8 gb data once it fill you have to delete old data to add new one.
Same LLM has limited tokens.

3. Temperature

Temperature is like a setting which control the creativity and predictability of a model
Typical range of temperature is 0 to 1.In advanced APIs it goes upto 2.
Low range(0 to 0.3) make predictable response.
Medium range(0.4 to 0.7) makes balance approach.
High range(0.8 to 1+) makes random/creative response.
For example: This tree  is ___.(big/tall/short/green/dry).

4. Top-p

Top-p control the next output word of the model.Sometimes it use along the Temperature.
It ranges from 0 to 1.It works with threshold.If you set threshold 0.4.
So it combine the probability of top probability words unless reaches 40%.These words added in pool and then model select next output word.
Remaining words rejected from model.
For example: Car is ___.(Big(25%),(Small(10%),(Blue(7),(Dirty(4%))

5. System Prompt

System Prompt is the set of instruction or rule given to models before the user message.
It defines how the model respond to user message.
By defining the system prompt model will give consistent responses
For example: 'You are my teacher and give answer only in one line'

6. Embedding

Embedding is the method to convert text into list of numbers because computer system can't understand text directly.
It understand numbers.It also used to identify the text of similar meaning.
For example: The sun is bright/The sun is hot/Computer is on.
In these sentences first two has kind of similar numerics but 3rd has different.

7. Hallucination

Hallucination is the effect that LLM generate while giving wrong information that is not in reality.
In this model make false and made up information in a confident way that user can trust
For example: If we ask "What Quaid e Azam said in 1951 in Lahore?"
SO model check "Quaid e Azam","speech","time","Place".
and match the patterns and model respond in made up speech by different previous speeches.

8. Fine Tuning

Fine tuning is the process in which we take pre trained LLM and further train it on the specific dataset for specific responses.
By this we set the model on specific way that it gave answer on that style.
For example: We finetune a model for a clinic assistant so model respond as a clinic employee.It book appointments,guide the patient etc.

9. Inference

Inference is the process of model to generate answers,predictions.
In this trained model is used.In inference model will not learn some thing new only make decisions on previous training
There is two main phases for model:
i.Training: Model trained by the data.
ii.Inference: Model generate the answer on the training.


----------------------------------------------------------------------------------------------------------------------------------------------------------------------------


Base Model vs Instruction tuned Model:

Base model:

Base model is trained on raw internet text,books,dataset.
These models predict the next most likely word of text.They can't able to give direct answers.
For example: 'Capital of America?'
it will response predict answer like , capital has white house,it has highest court.

Instruction tuned model:

Instruction tuned model is the also a base model but with extra training.So,it can give answers directly on point,
rather than randomly predict them.
In response of america capital? It will directly say,
'Capital of America is Washington D.C."


-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------


Why LLM predicts?

i.   LLM is a statistical pattern matching engine.
ii.  It does not have a database of facts.
iii. It predict the next most likely words based on its training.if it trained on wrong database it will respond wrong answer in confident way(Hallucination).



