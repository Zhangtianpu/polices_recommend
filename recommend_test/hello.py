#!/usr/bin/env python
# coding: utf-8




from flask import Flask
from flask import render_template
from flask import request,redirect, url_for, flash, session,send_from_directory,jsonify
from recommend_test.algorithm.recommend import get_result
from recommend_test.algorithm.Utils import get_train_file_name,create_stop_word
app = Flask(__name__)
app.config['MYSTATIC']='../images'
app.config['JSON_AS_ASCII'] = False
app.secret_key = '\xc9ixnRb\xe40\xd4\xa5\x7f\x03\xd0y6\x01\x1f\x96\xeao+\x8a\x9f\xe4'

#fileList=[]
#get_train_file_name("D:\workspace\jupyterWorkspace\政策推荐\policy_data", fileList)
#stopwords, stop_flag = create_stop_word('D:/workspace/PycharmWorkspace/recommend_test/data_polies/stop_words.txt')

app.route('/otherstatic/<filename>')
def otherStatic(filename):
    return send_from_directory(app.config['MYSTATIC'], filename, at_attachment=True)

@app.route('/hello', methods=['post','get'])
def hello_world():
    search_content = request.args.get('search_content')
    policy_content=get_result(search_content)
    return jsonify(policy_content)

@app.route('/polies',methods=['GET', 'POST'])
def get_polies():
    result = None
    result_json=None
    #政策检索
    if request.method == 'POST':
        keywords=request.form['search_content']
        print(keywords)
        if keywords is None:
            return "none"
            #result=get_polies_list()
        else:
            result=get_result("sadfasdf")
            #result=based_tfidf.main_tfidf(keywords)
        result_json=jsonify(result)
    return render_template('政策检索.html', error=result_json)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            flash("成功登录！")
            #session['username'] = request.form.get('username')
            #return redirect(url_for('home'))
            error="登录成功！"
        else:
            error = '错误的用户名或密码！'

    return render_template('login.html', error=error)




def valid_login(username, password):
    if username=='username' and password=='password':
        return True
    else:
        return False

if __name__=="__main__":
    app.run(debug=True)

