from app import db

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  nickname = db.Column(db.String(64), index=True)
  email = db.Column(db.String(120), index=True, unique=True)
  notes = db.relationship('Note', backref='author', lazy='dynamic')
  last_seen = db.Column(db.DateTime)

  @staticmethod
  def make_unique_nickname(nickname):
    if User.query.filter_by(nickname=nickname).first() is None:
      return nickname
    version = 2
    while True:
      new_nickname = nickname + str(version)
      if User.query.filter_by(nickname=new_nickname).first() is None:
        break
      version += 1
    return new_nickname

  @property
  def is_authenticated(self):
    return True

  @property
  def is_active(self):
    return True

  @property
  def is_aonymous(self):
    return False

  def get_id(self):
    try:
      return unicode(self.id)
    except NameError:
      return str(self.id)

  def __repr__(self):
    return '<User %r>' % (self.nickname)

class Contact(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  date_created = db.Column(db.DateTime)
  # last_edited = db.Column(db.DateTime)
  first_name = db.Column(db.String(64))
  last_name = db.Column(db.String(64), index=True)
  middle_name = db.Column(db.String(64))
  email = db.Column(db.String(64), index=True)
  phone = db.Column(db.String(64), index=True)
  street_address_1 = db.Column(db.String(64))
  street_address_2 = db.Column(db.String(64))
  city = db.Column(db.String(64), index=True)
  state = db.Column(db.String(64), index=True)
  zip_code = db.Column(db.String(64), index=True)
  company = db.Column(db.String(64), index=True)
  position = db.Column(db.String(64), index=True)
  notes = db.relationship('Note', backref='connect', lazy='dynamic')
  # tags = db.Column(db.String(64))

  def __repr__(self):
    return '<Contact %r>' % (self.first_name)

class Note(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  body = db.Column(db.String(140))
  timestamp = db.Column(db.DateTime)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))

  def __repr__(self):
    return '<Note %r>' % (self.body)