from flask import jsonify, Flask, request
from functools import wraps
from flask import jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy

APPS = Flask(__name__)

def check_auth(username, password):
    return username == 'plivo' and password == 'ashish@123'

def authenticate():
    response = jsonify({"status": False, "msg":"authentication failed"})
    response.status_code = 401
    return response

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@APPS.route('/plivo/v1/createphonebook', methods=["GET", "POST", "DELETE", "PUT"])
@requires_auth
def createphone():
    if request.method == "PUT":
        data = request.get_json(force=True)
        print data
        res = storeData(data)
        if res:
            response = jsonify({"status": "success", "message": "successfull create"})
            response.status_code = 200
            return response
        else:
            response = jsonify({"status": "failure", "message": "already present"})
            response.status_code = 409
            return response

    else:
        response = jsonify({"status": False, "message": "method type error"})
        response.status_code = 405
        return response

@APPS.route('/plivo/v1/deletecontact', methods=["GET", "POST", "DELETE", "PUT"])
@requires_auth
def deletecontact():
    if request.method == "DELETE":
        data = request.get_json(force=True)
        res = deletedata(data)
        if res:
            response = jsonify({"status": "success", "message": "successfull deleted"})
            response.status_code = 200
            return response
        else:
            response = jsonify({"status": "failure", "message": "not found"})
            response.status_code = 404
            return response
    else:
        response = jsonify({"status": False, "message": "method type error"})
        response.status_code = 405
        return response

@APPS.route('/plivo/v1/editcontact', methods=["GET", "POST", "DELETE", "PUT"])
@requires_auth
def editcontact():
    if request.method == "POST":
        data = request.get_json(force=True)
        res = editdata(data)
        if res:
            response = jsonify({"status": "success", "message": "successfull updated"})
            response.status_code = 200
            return response
        else:
            response = jsonify({"status": "failure", "message": "not found"})
            response.status_code = 404
            return response
    else:
        response = jsonify({"status": False, "message": "method type error"})
        response.status_code = 405
        return response

@APPS.route('/plivo/v1/searchcontact', methods=["GET", "POST", "DELETE", "PUT"])
@requires_auth
def searchcontact():
    if request.method == "GET":
        email = request.args.get('email')
        name = request.args.get('name')
        start = request.args.get('start')
        if email:
            resp = searchdata(start, email, flag = True)
        elif name:
            resp = searchdata(start, name, flag = False)
        else:
            response = jsonify({"status": False, "message": "no searchign query found"})
            response.status_code = 400
            return response
        if resp:
            response = jsonify({"status":"succes", "result":resp})
            response.status_code = 200
            return response
        else:
            response = jsonify({"status": "failure", "message": "not found"})
            response.status_code = 404
            return response
    else:
        response = jsonify({"status": False, "message": "method type error"})
        response.status_code = 405
        return response


APPS.config['SQLALCHEMY_DATABASE_URI'] = \
    'mysql://root:artifacia@localhost/plivophonebook'
db = SQLAlchemy(APPS)
db.create_all()

def create_phone_book():
    class PHONEBOOK(db.Model):
        __tablename__ = 'phonebook'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100))
        email = db.Column(db.String(100), unique=True)
        number = db.Column(db.String(100))

        __table_args__ = (db.UniqueConstraint(
            email, number), {'extend_existing': True})

        def __init__(self, name, email, number):
            self.name = name
            self.email = email
            self.number = number


        def __repr__(self):
            return '(%r, %r, %r)' % (self.email, self.name, self.number)
    return PHONEBOOK


CREATEPHONEBOOK = create_phone_book()

def storeData(data_number):
    # check data is already present
    email = data_number["email"]
    name = data_number["name"]
    number = str(data_number["number"])
    resp = db.session.query(
            CREATEPHONEBOOK.number).filter_by(email=email).all()
    if len(resp) != 0:
        return False
    data = CREATEPHONEBOOK(name, email, number)
    try:
        db.session.add(data)
        try:
            db.session.commit()
        except:
            db.session().rollback()
    except:  # pylint: disable = W0702
        db.session.close()
    return True

def deletedata(data_number):
    number = data_number["number"]
    resp = db.session.query(
            CREATEPHONEBOOK.number).filter_by(number=number).all()
    if len(resp) == 0:
        return False
    db.session.query(CREATEPHONEBOOK).filter(CREATEPHONEBOOK.number==number).delete()
    try:
        db.session.commit()
    except:
        db.session().rollback()
    return True

def editdata(data_number):
    number = data_number["number"]
    flag = ""
    data_update = data_number["data_tobe_updated"]
    resp = db.session.query(
            CREATEPHONEBOOK.number).filter_by(number=number).all()
    if len(resp) == 0:
        return False
    try:
        data_tobe_updated = data_update["name"]
        print "hello"
        db.session.query(
                    CREATEPHONEBOOK).filter_by(
                        number=number).update(
                            {"name": data_tobe_updated})
    except:
        pass
    try:
        data_tobe_updated = data_update["email"]
        db.session.query(
                    CREATEPHONEBOOK).filter_by(
                        number=number).update(
                            {"email": data_tobe_updated})
    except:
        pass
    try:
        data_tobe_updated = data_update["number"]
        db.session.query(
                    CREATEPHONEBOOK).filter_by(
                        number=number).update(
                            {"number": data_tobe_updated})
    except:
        pass
    try:
        try:
            db.session.commit()
        except:
            db.session().rollback()
    except:  # pylint: disable = W0702
        db.session.close()
        return False
    return True



def searchdata(start, data, flag):
    limit = 10
    search_q = data[:2]
    print flag
    print search_q
    if flag:
        resp = db.session.query(CREATEPHONEBOOK.number, CREATEPHONEBOOK.email, CREATEPHONEBOOK.name).filter(CREATEPHONEBOOK.email.like(search_q+"%")).limit(limit).offset(limit*start).all()
    else:
        resp = db.session.query(CREATEPHONEBOOK.number, CREATEPHONEBOOK.email, CREATEPHONEBOOK.name).filter(CREATEPHONEBOOK.name.like(search_q+"%")).limit(limit).all()

    print resp
    if len(resp) != 0:
        return resp
    else:
        return False


if __name__ == '__main__':
    APPS.run(host="localhost", port=8000)
