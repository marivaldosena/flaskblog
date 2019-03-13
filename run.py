import os
from flask import Flask, render_template
app = Flask(__name__)

posts = [
    {
        'author': 'Marivaldo Sena',
        'title': 'Quisque lacinia ultricies ipsum sed consectetur',
        'content': '''
            Quisque lacinia ultricies ipsum sed consectetur. Donec ultrices tincidunt tempus. Donec sed consectetur elit. Curabitur quis commodo ex. Phasellus consequat sagittis condimentum. Phasellus sollicitudin felis a ullamcorper mattis. Sed erat nisi, luctus quis ipsum ut, volutpat tempus felis. Fusce gravida tincidunt risus, sit amet dictum lorem iaculis quis.
        ''',
        'date_posted': '2019-03-12'
    },
    {
        'author': 'Marivaldo Sena',
        'title': 'Donec nec diam vitae enim feugiat pretium',
        'content': '''
            Phasellus hendrerit interdum tincidunt. Quisque aliquam aliquet lectus, eu pellentesque eros eleifend at. Suspendisse nisi tortor, scelerisque ut tellus id, vestibulum bibendum arcu. Maecenas molestie iaculis odio, ac tincidunt mauris lobortis vel. Praesent sit amet metus vel elit ornare auctor. Vestibulum nec augue et diam ullamcorper cursus. Nam viverra consequat ornare. Pellentesque ut purus non elit dignissim efficitur. Aenean posuere diam felis, vitae lacinia ipsum semper eu. Aliquam mi erat, imperdiet a fringilla id, ultricies in nulla. Integer condimentum ultrices ante, ac pharetra dolor venenatis et. Sed pharetra, metus ac sagittis accumsan, mi purus pretium tellus, eu sodales metus libero quis enim. Nullam vulputate rutrum purus, sed dictum tortor cursus eu. Aenean id aliquet dolor, et tempor lorem. Nulla facilisi.
        ''',
        'date_posted': '2019-03-12'
    }
]

app.secret_key = os.getenv('APP_SECRET_KEY') or '3676a9fc1001dca88437094cc3b1610b'

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')
    

if __name__ == '__main__':
    app.run()