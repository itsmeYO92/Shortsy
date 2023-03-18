import openai

def paragraph_generation(script):
	return script.split('\n\n')


openai.api_key = "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"
model_engine = "text-davinci-003"

genre=input("Whats your genre: ")
prompt = "write me a " + genre + "story"

completion = openai.Completion.create(
	engine=model_engine,
	prompt=prompt,
	max_tokens=1024,
	n=1,
	stop=None,
	temperature=0.5,
) 

response = completion.choices[0].text

p = paragraph_generation(response)
for i in p:
	print("------------")
	print(i) 


