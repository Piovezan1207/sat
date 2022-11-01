from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def API_40_ENIAC():
    #  print(request.json)
    print(request.json)
    return "a"


def main():  
    app.run(debug=False, host='0.0.0.0', port=5678)

main()

