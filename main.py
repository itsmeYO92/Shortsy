import openai

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
print(response)

