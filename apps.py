from flask import Flask, render_template, request
from main import get_answer


app = Flask(__name__, template_folder="templates")

@app.route('/')
def home():
    return render_template('index.html')

user_requests = []
lucifer_response = []
@app.route('/chat', methods=['GET', 'POST'])
def process_text():
    user_msg = request.form.get('user_message')

    lucifer_gpt = get_answer(user_msg)

    user_requests.append(user_msg)
    lucifer_response.append(lucifer_gpt)

    return render_template('index.html', user=user_requests, gpt=lucifer_response)


if __name__ == '__main__':
    app.run(debug=True)