from flask import Flask, request, jsonify
import openai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

openai.api_key = ""

conversation = []
initial_prompt = ""

def ai_initial_message(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        ai_message = response['choices'][0]['message']['content']
        return ai_message
    except Exception as e:
        return str(e)


@app.route('/send_message', methods=['POST'])
def send_message():
    global conversation

    human_message = request.json.get('message')
    role = request.json.get('role')

    if not human_message and role == "Party 2":  
        ai_message = ai_initial_message(initial_prompt)
        conversation.append(f"AI (Party 1): {ai_message}")
        return jsonify({'response': ai_message, 'conversation': conversation}), 200

    elif human_message and role == "Party 2":
        conversation.append(f"Human (Party 2): {human_message}")

        prompt = f"The conversation so far: {' '.join(conversation)}. Party 2 said: {human_message}. How should Party 1 respond?"
        
        try:
            ai_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            ai_message = ai_response['choices'][0]['message']['content']

            conversation.append(f"AI (Party 1): {ai_message}")

            return jsonify({'response': ai_message, 'conversation': conversation}), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    initial_prompt = input("Enter a general prompt to start the AI conversation: ")
    app.run(debug=True)