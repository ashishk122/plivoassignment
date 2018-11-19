from api import db_modal

CREATEPHONEBOOK = db_modal.create_phone_book()

def storeData(data_number):
    # check data is already present
    email = data_number["email"]
    name = data_number["name"]
    number = str(data_number["number"])
    resp = db_modal.db.session.query(
            CREATEPHONEBOOK.number).filter_by(email=email).all()
    if len(resp) != 0:
        return False
    data = CREATEPHONEBOOK(name, email, number)
    try:
        db_modal.db.session.add(data)
        try:
            db_modal.db.session.commit()
        except:
            db_modal.db.session().rollback()
    except:  # pylint: disable = W0702
        db_modal.db.session.close()
    return True

def deletedata(data_number):
    number = data_number["number"]
    resp = db_modal.db.session.query(
            CREATEPHONEBOOK.number).filter_by(number=number).all()
    if len(resp) == 0:
        return False
    CREATEPHONEBOOK.db.session.query().filter_by(number=number).delete()
    return True

def editdata(data_number):
    number = data_number["number"]
    flag = ""
    data_update = data_number["data_tobe_updated"]
    try:
        data_tobe_updated = data_update["name"]
        flag = "number"
        db_modal.db.session.query(
                    AUTHTABLE).filter_by(
                        number=number).update(
                            {"name": data_tobe_updated})
    except:
        pass
    try:
        data_tobe_updated = data_update["email"]
        db_modal.db.session.query(
                    AUTHTABLE).filter_by(
                        number=number).update(
                            {"email": data_tobe_updated})
    except:
        pass
    try:
        data_tobe_updated = data_update["number"]
        db_modal.db.session.query(
                    AUTHTABLE).filter_by(
                        number=number).update(
                            {"number": data_tobe_updated})
    except:
        pass
    try:
        try:
            db_modal.db.session.commit()
        except:
            db_modal.db.session().rollback()
    except:  # pylint: disable = W0702
        db_modal.db.session.close()
        return False
    return True



def searchdata(start, data, flag):
    limit = 10
    if flag:
        resp = db_modal.db.session.query(CREATEPHONEBOOK.number, CREATEPHONEBOOK.email, CREATEPHONEBOOK.name).filter_by(email=data).limit(limit).offset(start*limit).all()
    else:
        resp = db_modal.db.session.query(CREATEPHONEBOOK.number, CREATEPHONEBOOK.email, CREATEPHONEBOOK.name).limit(limit).offset(start*limit).filter_by(name=data).all()

    print resp
    if len(resp) != 0:
        return True
    else:
        return False
