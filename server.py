from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('landingPage.html')

@app.route('/Miez-sign-up')
def signUp():
    return render_template('sign-up.html')

@app.route('/sign-in')
def login():
    return render_template('sign-in.html')

@app.route('/miez-membership')
def membership():
    return render_template('membership.html')

@app.route('/dashboard')
def dashboard():
    return render_template('pages/dashboard.html')

@app.route('/profile')
def profile():
   return render_template('pages/profile.html') 


@app.route('/reality')
def reality():
    return render_template('pages/virtual-reality.html')
if __name__ == "__main__":
    app.run(debug=True)