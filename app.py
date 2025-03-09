from flask import Flask, request, render_template, redirect, url_for
import os
import time
from module.create_image import create_image,create_image_sdx
from module.gpt_4o_mini import make_nikki_from_image,create_image_prompt
from module.make_word import make_word
import glob
from dotenv import load_dotenv
load_dotenv()

OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")

UPLOAD_FOLDER = './uploads'

app = Flask(__name__)

@app.route('/')
def root_func_get():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def root_func_post():
    print("POST")
    result = ""
    if 'text1' in request.form and request.form['text1'] != "":
        print("has text in form") # textはここにある
        print(request.form['text1'])
        result=request.form['text1']
        prompt=create_image_prompt(request.form['text1'])
        create_image_sdx(prompt,device)
    elif 'img_name' in request.files: # ここにある
        print(request.files)
        #フォルダーの中身を削除
        files = os.listdir(UPLOAD_FOLDER)
        for file in files:
            os.remove(os.path.join(UPLOAD_FOLDER, file))
        files = request.files.getlist('img_name')
        print(files, "files")
        for file in files:
            file.save(os.path.join(UPLOAD_FOLDER, file.filename))
        file=glob.glob("./uploads/*")[0]
        print(file)
        create_image(file,device)
        result = make_nikki_from_image(file,OPEN_AI_API_KEY)
    if 'img_name' in request.form:
        print("has img_name in form") # img_nameはここには無い

    make_word(result)
    time.sleep(2)
    return redirect(url_for('static', filename='sample2.pdf'))


if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    global device
    device="mps" #NOTE: もしAppleシリコンのMacを使っている場合は`mps`に変更してください
    app.run(debug=True)