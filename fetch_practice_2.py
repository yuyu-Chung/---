

from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import String, Integer

app = Flask(__name__)

user = "YUYU"
password = "422924Qq"
host = "localhost"
port = 3306
schema = "practice_1"

engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{schema}")


@app.route("/")
def index():
    return send_from_directory("static", "fetch_practice_2.html")

@app.route("/add_data_practice_2", methods=["POST"])
def add_data():
    data = request.get_json()
    print("收到前端資料", data)

    df = pd.DataFrame([data])
    df.to_sql("receieved_from_front", con=engine, if_exists="append", index=False,
                dtype={
                    "name":String(50),
                    "careeryear":Integer,
                    "professional":String(50)
                })

    print("成功寫入MySQl")
    return jsonify({"status":"success", "received":data})

@app.route("/get_data", methods=["GET"])
def read_data():
    querry = "SELECT *FROM receieved_from_front"
    df = pd.read_sql(querry, con=engine)

    html_output = ""
    for _, row in df.iterrows():
        html_output += f"姓名: {row['name']    }    職業年資: {row['careeryear']}  專業: {row['professional']} <br>"

    return html_output

if __name__ =="__main__":
    app.run(debug=True)