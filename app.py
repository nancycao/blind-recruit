from flask import Flask #Imports the Flask class from the flask package that we installed
app = Flask(__name__) #Creates an instance of this class

@app.route("/") #Makes index show up when the root folder ("/") of the server is accessed by a user
def index():
    return "home"

if __name__ == "__main__": #Ensures that the app will only start if this file is not being imported from somewhere else but rather being accessed directly
    app.run()
