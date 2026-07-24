from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET'])
def main():
    # if request.method == 'POST':
    #     name = request.form['username']
    #     return f"Hello {name}, POST request received"
    return render_template('index.html')

if __name__ == '__main__':
    app.run()