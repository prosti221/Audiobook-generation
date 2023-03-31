import openai
openai.api_key = open('openai_key', 'r').read().strip()

system_content = open('system_content.txt', 'r').read()
assistant_content = open('assistant_content.txt', 'r').read()
user_content = open('user_content.txt', 'r').read()

def transcribe_text(text):
    response = openai.ChatCompletion.create(
               model="gpt-4",
               messages=[
                        {"role": "system", "content": system_content},
                        {"role": "user", "content": user_content},
                        {"role": "assistant", "content": assistant_content},
                        {"role": "user", "content": text}
                    ]
            )
    return response['choices'][0]['message']['content']
