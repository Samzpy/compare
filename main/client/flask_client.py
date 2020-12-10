# -*- coding:utf-8 -*-
 ######################################################
#        > File Name: flask_client.py
#      > Author: GuoXiaoNao
 #     > Mail: 250919354@qq.com 
 #     > Created Time: Mon 20 May 2019 11:52:00 AM CST
 ######################################################

from flask import Flask, send_file

app = Flask(__name__)
#127.0.0.1:5000/index  u
@app.route('/index')
def index():
    #首页
    return send_file('templates/index.html')
@app.route('/mylist')
def mylist():
    #追蹤清單
    return send_file('templates/mylist.html')
#127.0.0.1:5000/login  u
@app.route('/login')
def login(): 
    #登录
    return send_file('templates/login.html')
@app.route('/search')
def search(): 
    #登录
    return send_file('templates/search.html')
#127.0.0.1:5000/register  u
@app.route('/register')
def register():
    #注册
    return send_file('templates/register.html')

@app.route('/sort/<topics>')
def sort_detail(topics):
    #商品分類
    return send_file('templates/com.html')
@app.route('/detail/<name>')
def com_detail(name):
    #商品細項
    return send_file('templates/detail.html')


if __name__ == '__main__':
    app.run(debug=True)

