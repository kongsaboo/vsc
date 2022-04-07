from flask import Flask, render_template, jsonify, request
## branch test
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup


from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/memo', methods=['GET'])
def listing():
    data = list(db.alonememo.find({}, {'_id': False}))
    return jsonify({'all_data': data})


## API 역할을 하는 부분
@app.route('/memo', methods=['POST'])
def saving():
    url_receive = request.form['url_give']  # 대괄호 뒤의 명시한 id 가 view의 ajax data의 id와 매핑
    comment_receive = request.form['comment_give']


    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')
    ogtitle = soup.select_one('meta[property="og:title"]')['content']
    ogimage = soup.select_one('meta[property="og:image"]')['content']
    ogdesc = soup.select_one('meta[property="og:description"]')['content']
    doc = {
        'title': ogtitle,
        'url': url_receive,
        'comment': comment_receive,
        'desc' : ogdesc,
        'img' : ogimage
    }
    print(doc)
    db.alonememo.insert_one(doc)
    return jsonify({'msg': 'POST 전달성공!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
