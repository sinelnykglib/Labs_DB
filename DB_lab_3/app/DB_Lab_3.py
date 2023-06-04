from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import Form, StringField, validators, SubmitField, HiddenField, SelectField, IntegerField, \
    SelectMultipleField, DecimalField
import redis
import random
import string
import math
from __init__ import app_obj, db

app = app_obj()
#app = Flask(__name__)
app.secret_key = 'TeamsecretKey'

#redis_url = 'redis://localhost:6379'

# Redis connection
redis_url = 'redis://redis:6379/0'
redisClient = redis.from_url(redis_url)
CACHELIFETIME = 360

NUM_OF_ENTRIES = 100

# caching
cache = redis.Redis(host='localhost', port=6379, db=0)

# caching with docker
cache = redis.Redis(host='cache', port=6379, password='eYVX7EwVmmxKpCDmwMtyKVge8oLd2t81')



# ORM mapping


class place(db.Model):
    __tablename__ = 'place'

    place_id = db.Column(db.Integer, primary_key=True)
    regname = db.Column(db.String(80), nullable=False)
    areaname = db.Column(db.String(80), nullable=False)
    tername = db.Column(db.String(80), nullable=False)

    schools = db.relationship("school", backref="place", lazy=True, cascade="all, delete-orphan")

class school(db.Model):
    __tablename__ = 'school'

    school_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(400), nullable=False)
    parentname = db.Column(db.String(250))
    place_id = db.Column(db.Integer, db.ForeignKey('place.place_id'), nullable=False)

    students = db.relationship("student", backref = 'school', lazy=True, cascade="all, delete-orphan")
    tests = db.relationship("test", backref="school", lazy=True, cascade="all, delete-orphan")

class student(db.Model):
    __tablename__ = 'student'

    student_id = db.Column(db.String(36), primary_key=True)
    examyear = db.Column(db.SmallInteger, nullable=False)
    birthdate = db.Column(db.SmallInteger, nullable=False)
    sex = db.Column(db.String(10), nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('place.place_id'))
    regtypename = db.Column(db.String(120), nullable=False)
    classprofile = db.Column(db.String(40))
    classlang = db.Column(db.String(40))
    school_id = db.Column(db.Integer, db.ForeignKey('school.school_id'))

    tests = db.relationship("test", backref="student", lazy=True, cascade="all, delete-orphan")

class test(db.Model):
    __tablename__ = 'test'

    subject_id = db.Column(db.Integer, db.ForeignKey('subject.subject_id'), primary_key=True)
    student_id = db.Column(db.String(36), db.ForeignKey('student.student_id'), primary_key=True)
    teststatus = db.Column(db.String(60))
    ball100 = db.Column(db.Numeric(3,2))
    ball12 = db.Column(db.SmallInteger)
    ball = db.Column(db.SmallInteger)
    ukradaptscale = db.Column(db.SmallInteger)
    dpalevel = db.Column(db.String(40))
    school_id = db.Column(db.SmallInteger, db.ForeignKey('school.school_id'))

class subject(db.Model):
    __tablename__ = 'subject'

    subject_id = db.Column(db.Integer, primary_key=True)
    subjectname = db.Column(db.String(400), nullable=False)

    tests = db.relationship("test", backref="subject", lazy=True, cascade="all, delete-orphan")



# Flask forms


class placeForm(FlaskForm):
    place_id = HiddenField()
    regname = StringField('regname', validators=[validators.DataRequired("please enter your field"),
                                                 validators.Length(min=5, max=80)])
    areaname = StringField('areaname', validators=[validators.DataRequired("please enter your field"),
                                                   validators.Length(min=5, max=80)])
    tername = StringField('tername', validators=[validators.DataRequired("please enter your field"),
                                                 validators.Length(min=5, max=80)])
    submit = SubmitField("submit")

class schoolForm(FlaskForm):
    school_id = HiddenField('school_id')
    name = StringField('name', validators=[validators.DataRequired("please enter your field"),
                                           validators.Length(min=5, max=400)])
    parentname = StringField('parentname', validators=[validators.Length(min=0, max=250)])
    place_id = SelectField('place', coerce=int)
    submit = SubmitField("submit")

    def __init__(self, *args, **kwargs):
        super(schoolForm, self).__init__(*args, **kwargs)
        self.place_id.choices = [
            (str(place.place_id), f"{place.regname} {place.areaname} {place.tername}") for place in
            place.query.all()]

    def validate(self):
        if not super(schoolForm, self).validate():
            return False
        place_id = self.place_id.data
        place_ = place.query.get(place_id)
        if not place_:
            self.place_id.errors.append('Invalid place')
            return False
        return True

class studentForm(FlaskForm):
    student_id = HiddenField('student_id')
    examyear = IntegerField('examyear')
    birthdate = IntegerField('birthdate')
    sex = StringField('sex', validators=[validators.DataRequired("please enter your field"),
                                         validators.Length(min=5, max=10)])
    place_id = SelectField('place_id', coerce=int)
    regtypename = StringField('regtypename', validators=[validators.DataRequired("please enter your field"),
                                                         validators.Length(min=5, max=120)])
    classprofile = StringField('classprofile', validators=[validators.Length(min=5, max=40)])
    classlang = StringField('classlang', validators=[validators.Length(min=5, max=40)])
    school_id = SelectField('school_id', coerce=int)
    submit = SubmitField("submit")

    def __init__(self, *args, **kwargs):
        super(studentForm, self).__init__(*args, **kwargs)
        self.place_id.choices = [
            (int(place.place_id), f"{place.regname}, {place.areaname}, {place.tername}") for place in
            place.query.all()]

        self.school_id.choices = [
            (int(school.school_id), f"{school.name}, {school.parentname} {school.place_id}") for school in
            school.query.all()]

    def validate(self):
        if not super(studentForm, self).validate():
            return False
        place_id = self.place_id.data
        place_ = place.query.get(place_id)
        if not place_:
            self.place_id.errors.append('Invalid place')
            return False
        school_id = self.school_id.data
        school_ = school.query.get(school_id)
        if not school_:
            self.school_id.errors.append('Invalid school')
            return False
        return True

class testForm(FlaskForm):
    subject_id = SelectField('subject_id', coerce=int)
    student_id = SelectField('student_id', coerce=str)
    teststatus = StringField('teststatus', validators=[validators.Length(min=5, max=60)])
    ball100 = DecimalField('ball100', validators=[validators.NumberRange(min=100.00, max=200.00, message='Value must be between 100.00 and 200.00'), validators.InputRequired()])
    ball12 = IntegerField('ball12', validators=[validators.NumberRange(min=0, max=12, message='Value must be between 0 and 12')])
    ball = IntegerField('ball', validators=[validators.NumberRange(min=0, max=200, message='Value must be between 0 and 200')])
    ukradaptscale = IntegerField('ukradaptscale', validators=[validators.NumberRange(min=0, max=999, message='Value must be between 0 and 999')])
    dpalevel = StringField('dpaLevel', validators=[validators.Length(min=5, max=40)])
    school_id = SelectField('school', coerce=int)
    submit = SubmitField("submit")

    def __init__(self, *args, **kwargs):
        super(testForm, self).__init__(*args, **kwargs)
        self.subject_id.choices = [
            (int(subject.subject_id), f"{subject.subjectname}") for subject in
            subject.query.all()]

        self.student_id.choices = [
            (str(student.student_id), f"{student.examyear}, {student.birthdate}, {student.sex}, {student.place_id} \n"
                                      f"{student.regtypename}, {student.classprofile}, {student.classlang}, {student.school_id} ")
            for student in student.query.all()]

        self.school_id.choices = [
            (int(school.school_id), f"{school.name}, {school.parentname} {school.place_id}") for school in
            school.query.all()]

    def validate_on_submit(self):
        return True

    def validate(self):
        if not super(testForm, self).validate():
            for field, errors in self.errors.items():
                for error in errors:
                    flash(f"Error in field '{getattr(self, field).label.text}': {error}", 'error')
            #raise Exception(f"Error in field '{getattr(self, field).label.text}': {error}", 'error')
            return False
        subject_id = self.subject_id.data
        subject_ = subject.query.get(subject_id)
        if not subject_:
            self.subject_id.errors.append('Invalid subject')
            #raise Lox_two
            return False
        student_id = self.student_id.data
        student_ = student.query.get(student_id)
        if not student_:
            self.student_id.errors.append('Invalid student')
            #raise Lox_three
            return False
        school_id = self.school_id.data
        school_ = school.query.get(school_id)
        if not school_:
            self.school_id.errors.append('Invalid school')
            #raise Lox_four
            return False
        return True

class subjectForm(FlaskForm):
    subject_id = HiddenField()
    subjectname = StringField('subjectname', validators=[validators.DataRequired("please enter your field"),
                                           validators.Length(min=5, max=400)])
    submit = SubmitField("submit")

class statisticsForm(FlaskForm):
    regname = SelectMultipleField('regionname', validators=[validators.DataRequired()], coerce=str)
    examyear = SelectField('examyear', validators=[validators.DataRequired()], coerce=int)
    subjectname = SelectField('subjectname', validators=[validators.DataRequired()], coerce=str)
    submit = SubmitField('submit')

    def __init__(self, *args, **kwargs):
        super(statisticsForm, self).__init__(*args, **kwargs)

        regions = [(place.regname, place.regname) for place in
                   place.query.with_entities(place.regname).distinct()]
        regions.insert(0, ('all', 'Усі регіони'))
        self.regname.choices = regions

        self.examyear.choices = [(student.examyear, student.examyear) for student in
                                 student.query.with_entities(student.examyear).distinct()]
        self.subjectname.choices = [(subject.subjectname, subject.subjectname) for subject in
                             subject.query.with_entities(subject.subjectname).distinct()]


# Routing

@app.route('/', methods=['GET', 'POST'])
def root():
    return render_template('index.html')

# place

@app.route('/places/<int:page>')
def showplaces(page=1):
    start = (page-1) * NUM_OF_ENTRIES

    # Отримання загальної кількості записів
    total_count = place.query.count()
    last_page = math.ceil(total_count / NUM_OF_ENTRIES)

    # Отримання сторінки записів
    places = place.query.order_by(place.place_id.desc()).limit(NUM_OF_ENTRIES).offset(start).all()

    return render_template('showplaces.html', places=places, last_page=last_page)


@app.route('/places/add', methods=['GET', 'POST'])
def addplace():
    form = placeForm(request.form)

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('formplaces.html', form=form, action='addplace')
        newplace = place (
            regname=form.regname.data,
            areaname=form.areaname.data,
            tername=form.tername.data,
            )
        db.session.add(newplace)
        db.session.commit()
        return redirect(url_for('showplaces', page=1))

    return render_template('formplaces.html', form=form, action='addplace')

@app.route('/places/update', methods=['GET', 'POST'])
def updateplace():
    form = placeForm(request.form)

    if request.method == 'GET':
        place_id = request.args.get('place_id')
        place_ = db.session.query(place).filter(place.place_id == place_id).one()

        form.place_id.data = place_id
        form.regname.data = place_.regname
        form.areaname.data = place_.areaname
        form.tername.data = place_.tername
        return render_template('formplaces.html', form=form, action="updateplace")

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('formplaces.html', form=form, action="updateplace")
        place_ = db.session.query(place).filter(place.place_id == form.place_id.data).one()
        place_.regname = form.regname.data,
        place_.areaname = form.areaname.data,
        place_.tername = form.tername.data,

        db.session.commit()
        return redirect(url_for('showplaces', page=1))


@app.route('/places/delete', methods=['POST'])
def deleteplace():
    place_id = request.form['place_id']
    result = db.session.query(place).filter(place.place_id == place_id).one()

    db.session.delete(result)
    db.session.commit()
    return redirect(url_for('showplaces', page=1))

# school

@app.route('/schools/<int:page>')
def showschools(page=1):
    start = (page - 1) * NUM_OF_ENTRIES
    end = page * NUM_OF_ENTRIES

    # Отримання загальної кількості записів
    total_count = db.session.query(db.func.count(school.school_id)).scalar()
    last_page = math.ceil(total_count / NUM_OF_ENTRIES)

    # Отримання сторінки записів
    schools = school.query.order_by(school.school_id.desc()).slice(start, end)

    return render_template('showschools.html', schools=schools, last_page=last_page)

@app.route('/schools/add', methods=['GET', 'POST'])
def addschool():
    form = schoolForm(request.form)

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('formschools.html', form=form, action='addschool')
        newschool = school(
            name=form.name.data,
            parentname=form.parentname.data,
            place_id=form.place_id.data
        )
        db.session.add(newschool)
        db.session.commit()
        return redirect(url_for('showschools', page=1))

    return render_template('formschools.html', form=form, action='addschool')


@app.route('/schools/update', methods=['GET', 'POST'])
def updateschool():
    form = schoolForm(request.form)

    if request.method == 'GET':
        school_id = request.args.get('school_id')
        print(school_id)
        school_ = db.session.query(school).filter(school.school_id == school_id).one()

        form.school_id.data = school_id
        form.name.data = school_.name
        form.parentname.data = school_.parentname
        form.place_id.data = school_.place_id
        return render_template('formschools.html', form=form, action="updateschool")

    if request.method == 'POST':
        if not form.validate():
            return render_template('formschools.html', form=form, action="updateschool")
        school_ = db.session.query(school).filter(school.school_id == form.school_id.data).one()
        school_.name = form.name.data
        school_.parentname = form.parentname.data
        school_.place_id = form.place_id.data

        db.session.commit()
        return redirect(url_for('showschools', page=1))


@app.route('/schools/delete', methods=['POST'])
def deleteschool():
    school_id = request.form['school_id']
    result = db.session.query(school).filter(school.school_id == school_id).one()

    db.session.delete(result)
    db.session.commit()
    return redirect(url_for('showschools', page=1))


# student

@app.route('/students/<int:page>')
def showstudents(page=1):
    start = (page-1) * NUM_OF_ENTRIES
    end = page * NUM_OF_ENTRIES
    last_page = math.ceil(student.query.count() / NUM_OF_ENTRIES)
    return render_template('showstudents.html', students=student.query[start:end], last_page=last_page)


def generate_random_string():
    random_string = ''.join(random.choices(string.digits + string.ascii_lowercase, k=8))
    random_string += '-' + ''.join(random.choices(string.digits + string.ascii_lowercase, k=4))
    random_string += '-' + ''.join(random.choices(string.digits + string.ascii_lowercase, k=4))
    random_string += '-' + ''.join(random.choices(string.digits + string.ascii_lowercase, k=4))
    random_string += '-' + ''.join(random.choices(string.digits + string.ascii_lowercase, k=12))
    return random_string


@app.route('/students/add', methods=['GET', 'POST'])
def addstudents():
    form = studentForm(request.form)

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('formstudents.html', form=form, action='addstudents')
        while True:
            new_student_id = generate_random_string()
            student_ = student.query.filter_by(student_id=new_student_id).first()
            if student_ is None:
                break

        newstudent = student (
            student_id=new_student_id,
            examyear=form.examyear.data,
            birthdate=form.birthdate.data,
            sex=form.sex.data,
            place_id=form.place_id.data,
            regtypename=form.regtypename.data,
            classprofile=form.classprofile.data,
            classlang=form.classlang.data,
            school_id=form.school_id.data
            )
        db.session.add(newstudent)
        db.session.commit()
        return redirect(url_for('showstudents', page=1))

    return render_template('formstudents.html', form=form, action='addstudents')


@app.route('/students/update', methods=['GET', 'POST'])
def updateStudent():
    form = studentForm(request.form)

    if request.method == 'GET':
        student_id = request.args.get('student_id')
        student_ = db.session.query(student).filter(student.student_id == student_id).one()
        form.student_id.data = student_id
        form.examyear.data = student_.examyear
        form.birthdate.data = student_.birthdate
        form.sex.data = student_.sex
        form.place_id.data = student_.place_id
        form.regtypename.data = student_.regtypename
        form.classprofile.data = student_.classprofile
        form.classlang.data = student_.classlang
        form.school_id.data = student_.school_id

        return render_template('formstudents.html', form=form, action="updateStudent")

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('formstudents.html', form=form, action="updateStudent")
        student_ = db.session.query(student).filter(student.student_id == form.student_id.data).one()
        student_.examyear = int(form.examyear.data)
        student_.birthdate = int(form.birthdate.data)
        student_.sex = form.sex.data
        student_.place_id = form.place_id.data
        student_.regtypename = form.regtypename.data
        student_.classprofile = form.classprofile.data
        student_.classlang = form.classlang.data
        student_.school_id = form.school_id.data
        db.session.commit()
        return redirect(url_for('showstudents', page=1))


@app.route('/students/delete', methods=['POST'])
def deletestudent():
    student_id = request.form['student_id']
    result = db.session.query(student).filter(student.student_id == student_id).one()
    db.session.delete(result)
    db.session.commit()
    return redirect(url_for('showstudents', page=1))

# test

@app.route('/tests/<int:page>')
def showtests(page=1):
    start = (page-1) * NUM_OF_ENTRIES
    end = page * NUM_OF_ENTRIES
    last_page = math.ceil(test.query.count() / NUM_OF_ENTRIES)
    return render_template('showtests.html', tests = test.query[start:end], last_page=last_page)

@app.route('/tests/add', methods=['GET', 'POST'])
def addtests():
    form = testForm(request.form)

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('formtests.html', action='addtests', form=form)
        newtest = test (
            subject_id=form.subject_id.data,
            student_id=form.student_id.data,
            teststatus=form.teststatus.data,
            ball100=form.ball100.data,
            ball12=form.ball12.data,
            ball=form.ball.data,
            ukradaptscale=form.ukradaptscale.data,
            dpalevel=form.dpalevel.data,
            school_id=form.school_id.data
            )
        db.session.add(newtest)
        db.session.commit()
        return redirect(url_for('showtests', page=1))

    return render_template('formtests.html', form=form, action='addtests')



@app.route('/tests/delete', methods=['POST'])
def deletetest():
    student_id = request.form['student_id']
    subject_id = request.form['subject_id']
    result = db.session.query(test).filter(test.student_id == student_id, test.subject_id == subject_id).one()

    db.session.delete(result)
    db.session.commit()

    return redirect(url_for('showtests', page=1))

# subject

@app.route('/subjects/<int:page>')
def showsubjects(page=1):
    start = (page-1) * NUM_OF_ENTRIES
    end = page * NUM_OF_ENTRIES

    # Отримання загальної кількості записів
    total_count = db.session.query(db.func.count(subject.subject_id)).scalar()
    last_page = math.ceil(total_count / NUM_OF_ENTRIES)

    # Отримання сторінки записів
    subjects = subject.query.order_by(subject.subject_id.desc()).slice(start, end)

    return render_template('showsubjects.html', subjects=subjects, last_page=last_page)

@app.route('/subjects/add', methods=['GET', 'POST'])
def addsubjects():
    form = subjectForm(request.form)

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('formsubjects.html', form=form, action='addsubjects')
        newsubject = subject (
            subjectname = form.subjectname.data,
            )
        db.session.add(newsubject)
        db.session.commit()
        return redirect(url_for('showsubjects', page=1))

    return render_template('formsubjects.html', form=form, action='addsubjects')

@app.route('/subjects/update', methods=['GET', 'POST'])
def updateSubject():
    form = subjectForm(request.form)

    print(request.method)
    if request.method == 'GET':
        subject_id = request.args.get('subject_id')
        print(subject_id)
        subject_ = db.session.query(subject).filter(subject.subject_id == subject_id).one()
        form.subject_id.data = subject_id
        form.subjectname.data = subject_.subjectname
        return render_template('formsubjects.html', form=form, action="updateSubject")

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('formsubjects.html', form=form, action="updateSubject")
        subject_ = db.session.query(subject).filter(subject.subject_id == form.subject_id.data).one()
        subject.subjectname = form.subjectname.data,
        db.session.commit()
        return redirect(url_for('showsubjects', page=1))

@app.route('/subjects/delete', methods=['POST'])
def deletesubject():
    subject_id= request.form['subject_id']
    result = db.session.query(subject).filter(subject.subject_id == subject_id).one()

    db.session.delete(result)
    db.session.commit()
    return redirect(url_for('showsubjects', page=1))

# statistics

@app.route('/showstatistics', methods=['GET', 'POST'])
def showstatistics():
    form = statisticsForm(request.form)

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('showstatistics.html', form=form, action='showstatistics')

        selectedRegions = form.regname.data
        if 'all' in selectedRegions:
            selectedRegions = [region[0] for region in form.regname.choices[1:]]
        subjectname = form.subjectname.data
        examYear = form.examyear.data

        statisticsResults = []

        # Getting data from Cache
        regionsTakeFromDB = []
        for region in selectedRegions:
            cacheKey = f"{region}_{subjectname}_{examYear}"
            ball100 = redisClient.get(cacheKey)
            if ball100 is not None and ball100 != -1:
                statisticsResults.append({'regname': region, 'ball100': float(ball100)})
            else:
                regionsTakeFromDB.append(region)

        # Getting data from DB
            if len(regionsTakeFromDB) != 0:
                query = (
                    db.session.query(
                        db.func.round(
                            db.cast(
                                db.func.avg(test.ball100),
                                db.Numeric(precision=10, scale=2)
                            ),
                            2
                        ).label('ball100'),
                        place.regname
                    )
                    .select_from(test)
                    .join(student)
                    .join(place)
                    .join(subject, test.subject_id == subject.subject_id)
                    .filter(
                        test.teststatus == 'Зараховано',
                        subject.subjectname == subjectname,
                        db.cast(student.examyear, db.Integer) == examYear,
                        place.regname.in_(regionsTakeFromDB)
                    )
                )

            query = query.group_by(place.regname)
            regionsFromDB = db.session.execute(query).fetchall()

            for region in regionsFromDB:
                statisticsResults.append(region)
                # Caching data
                cacheKey = f"{region.regname}_{subjectname}_{examYear}"
                redisClient.set(cacheKey, float(region.ball100))
                redisClient.expire(cacheKey, CACHELIFETIME)

        statisticsResults = sorted(statisticsResults, key=lambda x: x['ball100'] if isinstance(x, dict) else x.ball100,
                                   reverse=True)
        return render_template('showstatistics.html', statistics=statisticsResults, form=form)

    return render_template('showstatistics.html', statistics=[], form=form, action='showstatistics')

# Main

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
    db.create_all()
    #run localhost
    #app.run(debug=True)
    #db.create_all()





