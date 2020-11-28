from flask import Flask, render_template, request, redirect, url_for
from replit import db
from datetime import datetime, timezone, timedelta
tz = timezone(timedelta(hours=+8))

import random

web_site = Flask(__name__)

# Guess The number.
ans = random.randint(1, 10000)
print(ans)


@web_site.route('/', defaults={'num': 0})
def index(num):
    global ans
    num = request.args.get('num')
    result = ''
    if not num or not num.isnumeric():
        num = 0

    num = int(num)

    if num > ans:
        result = 'Too big!🙃'
    elif num == ans:
        result = 'Right! 🎉🎉🎉 \nThe answer has been reset. \nCan you guess it again?'
        ans = random.randint(1, 10000)
        print(ans)

    elif num < ans:
        result = 'Too small!😥'

    comments = db["comments"] if "comments" in db.keys() else []
    

    return render_template(
        'index.html', num=num, result=result, comments=comments)

@web_site.route(
'/comments/<int:comment_id>', methods=['DELETE'])
def delete_comments(comment_id):
    oldComments = db["comments"] if "comments" in db.keys() else []
    if request.method == "DELETE":
            comment_id = int(comment_id)
            newComments = []
            for i, comment in enumerate(oldComments):
                if i == comment_id:
                    continue
                comment = {
                    'author': comment['author'],
                    'content': comment['content'][:100],
                    'create_time': comment['create_time']
                }
                newComments.append(comment)
            db["comments"] = newComments
            # del db['comments']
            return redirect('/admin')

@web_site.route(
    '/comments', methods=['GET', 'POST'])
def comments():
    oldComments = db["comments"] if "comments" in db.keys() else []

   

    author = request.form.get('author')
    content = request.form.get('content')

    author = author[:30]
    content = content[:500]

    newComment = {
        'author': author,
        'content': content,
        'create_time': datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
    }
    oldComments = db["comments"] if "comments" in db.keys() else []
    comments = [newComment] + oldComments
    db["comments"] = comments
    db["comments-bak"] = comments

    return redirect('/')


@web_site.route( '/admin', methods=['GET', 'POST', 'DELETE'])
def admin():
    comments = db["comments"] if "comments" in db.keys() else []

    return render_template(
        'admin.html', comments=comments)

@web_site.route('/bak')
def bak():
   
    comments = db["comments-bak"] if "comments-bak" in db.keys() else []
    
    return render_template(
        'bak.html', comments=comments)


web_site.run(host='0.0.0.0', port=8080)
