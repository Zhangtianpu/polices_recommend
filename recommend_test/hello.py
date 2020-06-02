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
app.route('/otherstatic/<filename>')

@app.route('/hello', methods=['post','get'])
def hello_world():
    search_content = request.args.get('search_content')
    policy_content=get_result(search_content)
    return jsonify(policy_content)

if __name__=="__main__":
    app.run(debug=True)

