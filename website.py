from configparser import SafeConfigParser
from bottle import route, run, template, static_file, redirect
from pymongo import MongoClient

config = SafeConfigParser()
config.read('config.ini')
db = MongoClient()[config.get('mongodb', 'db_name')]

@route('/')
def index():
    domains = [ d['domain'] for d in db.domains.find({'status': 'inactive'})
                .sort('length').limit(30) ]

    purchased = [ d['domain'] for d in
                  db.domains.find({'purchased_this_week': True}) ]

    return template(
        'index',
        page=1,
        domains=domains,
        purchased=purchased
    )

@route('/<page:re:\d+>')
def page(page):
    index = int(page) - 1

    if index < 0:
        return 'Out of range!'

    domains = [ d['domain'] for d in db.domains.find({'status': 'inactive'})
                .sort('length').skip(index * 30).limit(30) ]

    purchased = [ d['domain'] for d in
                  db.domains.find({'purchased_this_week': True}) ]

    return template(
        'index',
        page=int(page),
        domains=domains,
        purchased=purchased
    )

@route('/register/:domain')
def register(domain):
    # lol
    redirect(config.get('register', '101domain').replace('{{d}}', domain))

@route('/static/<fn>')
def static(fn):
    return static_file(fn, root='static')

def main():
    run(host='localhost', port=3000)

if __name__ == '__main__':
    main()
