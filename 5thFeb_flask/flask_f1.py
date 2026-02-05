from flask import Flask,render_template,request,redirect,url_for,jsonify

app = Flask(__name__)

@app.route("/",methods=["GET"])
def welcome():
   return "<h1>Welcome to Flask F1</h1>"

@app.route("/index",methods=["GET"])
def index():
    return "Welcome to index app"

@app.route("/success/<int:score>")
def success(score):
    return "The person is pass and score is :" + str(score)

@app.route("/fail/<int:score>")
def fail(score):
    return "The person is fail and score is :" + str(score)

@app.route("/form", methods=["GET","POST"])
def form():
    if request.method == "GET":
        return render_template("form.html")
    else:
        maths = float(request.form['maths'])
        science = float(request.form['science'])
        history = float(request.form['history'])

        average_marks = (maths + science + history) / 3
        res = ""
        if average_marks >= 50:
            res = "success"
        else:
            res = "fail"
        return redirect(url_for(res,score=average_marks))

@app.route("/api",methods=["POST"])
def calculate_sum():
    data = request.get_json()
    a_val = float(dict(data)['a'])
    b_val = float(dict(data)['b'])
    return jsonify(a_val + b_val)
if __name__ == "__main__":
        app.run(debug=True)
