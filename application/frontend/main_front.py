from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/record')
def record():
    return render_template('record_data.html')


@app.route('/view')
def view():
    # Supondo que você tenha algum dado a ser passado para o template record_data.html
    # data = {"example_data": "Some data to display"}
    # return render_template('record_data.html', data=data)
    return render_template('view_data.html')


if __name__ == '__main__':
    app.run(port=5001, debug=True)
