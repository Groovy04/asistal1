from flask import Flask, render_template, flash, request, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms import validators
from wtforms.validators import DataRequired, Email, ValidationError, InputRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

from flask_login import UserMixin
from flask_login import login_user, current_user, logout_user, login_required

from flask_login import LoginManager

#from A_bokeh1 import script, div  #Arrange these in the file


#////////bokeh test libraries
import random
from bokeh.models.tools import Toolbar
import pandas
import numpy as np
import pandas as pd
import pandas

from bokeh.layouts import layout
from bokeh.models.glyphs import Circle
from bokeh.models.sources import ColumnDataSource
from bokeh.plotting import figure, output_file, save
from bokeh.io import curdoc, show
from numpy import source

from bokeh.sampledata.iris import flowers
from bokeh.models import Range1d, PanTool, ResetTool, HoverTool, Band, Toggle, Div
from bokeh.models.annotations import Label, LabelSet, Span, BoxAnnotation, ToolbarPanel
from bokeh.models.widgets import Select, Slider, RadioButtonGroup
from bokeh.layouts import gridplot, row, column
from bokeh.io import curdoc
from bokeh.transform import dodge
from bokeh.resources import CDN
from math import pi

from bokeh.embed import server_document, components

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine


#////////bokeh test libraries



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://tansubaktiran:Avz9p9&9Dgsu_099@193.111.73.99/tansubaktiran"

#Secret key
app.config['SECRET_KEY'] = "MYSUPERKEY"
#Initialize the adatabase
db = SQLAlchemy(app)

#Setting up user login parts
login_manager = LoginManager(app)
login_manager.login_view = 'login' #Name of the route in charge of logging in
login_manager.login_message_category = 'info'


#ADDED FOR TESTING USER LOGIN - 27.10.21
@login_manager.user_loader
def load_user(id):
    return Users_db.query.get(int(id)) #DB table name to be updated!!!! ////////////


#DATABASE MODELS TO BE UPDATED - 
#AUTHORIZED USERS, SALESMTPLANNED, SALESMTACTUAL, CUSTOMERS, ... OTHERS?
class Users_db(db.Model, UserMixin): #TO BE UPDATED!!!
    id = db.Column(db.Integer, primary_key=True)
    name_db = db.Column(db.String(200), nullable=False)
    email_db = db.Column(db.String(120), nullable=False, unique=True)
    password_db = db.Column(db.String(120), nullable=False)
    role_db = db.Column(db.String(20), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<Name %r>' % self.name

#OTHER DATABASES TO BE INCLUDED HERE - 
#////////////////////////////////////////////////////////////
class SALESMTPLANNED_db(db.Model): #MT Planned db - 
    id = db.Column(db.Integer, primary_key=True)
    month_planned_db = db.Column(db.String(15), nullable=False)
    month_order_db = db.Column(db.Integer(), nullable=False, default=0)
    year_planned_db = db.Column(db.Integer(), nullable=False)
    month_unique_db = db.Column(db.String(20), nullable=False)
    tot_vol_planned_db = db.Column(db.Integer, nullable=False, default=0)
    tot_mf_planned_db = db.Column(db.Integer, nullable=False, default=0)
    tot_anodize_planned_db = db.Column(db.Integer, nullable=False, default=0)
    tot_powder_coat_planned_db = db.Column(db.Integer, nullable=False, default=0)
    tot_wood_finish_planned_db = db.Column(db.Integer, nullable=False, default=0)
    tot_crimping_planned_db = db.Column(db.Integer, nullable=False, default=0)
    tot_EUR_planned_db = db.Column(db.Integer, nullable=False, default=0)
    new_customers_planned_db = db.Column(db.Integer, nullable=False, default=0)
    date_added_db = db.Column(db.DateTime, default=datetime.utcnow)
        
    def __repr__(self):
        return '<Entry No: %r>' % self.id

#////////////////////////////////////////////////////////////
#NEW TABLE
class SALESMTACTUAL_db(db.Model): #MT actual db - 
    id = db.Column(db.Integer, primary_key=True)
    month_actual_db = db.Column(db.String(15), nullable=False)
    month_order_db = db.Column(db.Integer(), nullable=False, default=0)
    year_actual_db = db.Column(db.Integer(), nullable=False)
    month_unique_db = db.Column(db.String(20), nullable=False)
    tot_vol_actual_db = db.Column(db.Integer, nullable=False, default=0)
    tot_mf_actual_db = db.Column(db.Integer, nullable=False, default=0)
    tot_anodize_actual_db = db.Column(db.Integer, nullable=False, default=0)
    tot_powder_coat_actual_db = db.Column(db.Integer, nullable=False, default=0)
    tot_wood_finish_actual_db = db.Column(db.Integer, nullable=False, default=0)
    tot_crimping_actual_db = db.Column(db.Integer, nullable=False, default=0)
    tot_EUR_actual_db = db.Column(db.Integer, nullable=False, default=0)
    new_customers_actual_db = db.Column(db.Integer, nullable=False, default=0)
    date_added_db = db.Column(db.DateTime, default=datetime.utcnow)
        
    def __repr__(self):
        return '<Entry No: %r>' % self.id

#NEW TABLE
#////////////////////////////////////////////////////////////




#FORMS HERE
#FORMS TO BE INCLUDED - USERS, SALESMTPLANNED, SALESMTACTUAL, CUSTOMERS, ... OTHERS?
#////////////////////////////////////////////////////////////
class Login(FlaskForm):
    email = StringField("Enter your email please..", validators=[DataRequired(), Email()]) #Check if true
    password = StringField("Enter your password please..", validators=[DataRequired()])
    submit = SubmitField("For Entering System")


class SalesMTPlanned(FlaskForm): #Will be transformed to a form structure.. check also integer vaidations..
    month_planned = SelectField(label='Month', choices=[("Jan", "Jan"), 
                    ("Feb", "Feb"), ("Mar", "Mar"), ("Apr", "Apr"), ("May", "May"), ("Jun", "Jun")
                    , ("Jul", "Jul"), ("Aug", "Aug"), ("Sep", "Sep"), ("Oct", "Oct"), ("Nov", "Nov")
                    , ("Dec", "Dec") ], validators=[InputRequired()])
    year_planned = IntegerField("Year", validators=[InputRequired()]) #Is integer?1
    #period_planned = StringField("Enter the relevant period please", validators=[DataRequired()])
    tot_vol_planned = IntegerField("Total Sales Volume in MT", validators=[InputRequired()]) #Is integer?
    tot_mf_planned = IntegerField("Total Volume in MT in MF phase", validators=[InputRequired()])
    tot_anodize_planned = IntegerField("Total Volume in MT in ANODIZE phase", validators=[InputRequired()])
    tot_powder_coat_planned = IntegerField("Total Volume in MT in POWDER COATING phase", validators=[InputRequired()])
    tot_wood_finish_planned = IntegerField("Total Volume in MT in WOOD FINISH phase", validators=[InputRequired()])
    tot_crimping_planned = IntegerField("Total Volume in MT in CRIMPING phase", validators=[InputRequired()])
    tot_EUR_planned = IntegerField("Total EUR AMOUNT planned", validators=[InputRequired()])
    new_customers_planned = IntegerField("Total number of new customers planned", validators=[InputRequired()])
    submit = SubmitField("Save This Entry")
    

#////////////////////////////////////////////////////////////
#NEW FORM
class SalesMTActual(FlaskForm): #Will be transformed to a form structure.. check also integer vaidations..
    month_actual = SelectField(label='Month', choices=[("Jan", "Jan"), 
                    ("Feb", "Feb"), ("Mar", "Mar"), ("Apr", "Apr"), ("May", "May"), ("Jun", "Jun")
                    , ("Jul", "Jul"), ("Aug", "Aug"), ("Sep", "Sep"), ("Oct", "Oct"), ("Nov", "Nov")
                    , ("Dec", "Dec") ], validators=[InputRequired()])
    year_actual = IntegerField("Year", validators=[InputRequired()]) #Is integer?1
    #period_actual = StringField("Enter the relevant period please", validators=[DataRequired()])
    tot_vol_actual = IntegerField("Total Sales Volume in MT", validators=[InputRequired()]) #Is integer?
    tot_mf_actual = IntegerField("Total Volume in MT in MF phase", validators=[InputRequired()])
    tot_anodize_actual = IntegerField("Total Volume in MT in ANODIZE phase", validators=[InputRequired()])
    tot_powder_coat_actual = IntegerField("Total Volume in MT in POWDER COATING phase", validators=[InputRequired()])
    tot_wood_finish_actual = IntegerField("Total Volume in MT in WOOD FINISH phase", validators=[InputRequired()])
    tot_crimping_actual = IntegerField("Total Volume in MT in CRIMPING phase", validators=[InputRequired()])
    tot_EUR_actual = IntegerField("Total EUR AMOUNT actual", validators=[InputRequired()])
    new_customers_actual = IntegerField("Total number of new customers actual", validators=[InputRequired()])
    submit = SubmitField("Save This Entry")





#////////////////////////////////////////////////////////////

"""#////////////////First example
class MyForm(FlaskForm):
    name = StringField('Name', [InputRequired()])
    def validate_name(form, field):
        if len(field.data) > 50:
            raise ValidationError('Name must be less than 50 characters')
#////////////////Second example
def my_length_check(form, field):
    if len(field.data) > 50:
        raise ValidationError('Field must be less than 50 characters')
class MyForm(Form):
    name = StringField('Name', [InputRequired(), my_length_check])"""


#////////////////////////////////////////////////////////////END-OF FORMS

#ROUTES
@app.route('/')
@app.route('/index')
def index():
    name="TEST"
    number = 10
    return  render_template("index.html", name=name, number=number)


#OTHER ROUTES HERE...
#////////////////////////////////////////////////////////////
@app.route('/sales_planned_entry', methods=["GET", "POST"])
@login_required
def sales_planned_entry(): #Add user - ALSO TO DATABASE!!!
    name = None #For sending to "please enter your name/credentials page on html - if statement"
    form = SalesMTPlanned()
    #Validation of our form
    if form.validate_on_submit():
        #name = form.name_field.data
        #For arranging a code disabling multiple entries for same month/period
        month_unique_temporary = form.month_planned.data + str(form.year_planned.data)
        unique_month = SALESMTPLANNED_db.query.filter_by(month_unique_db=month_unique_temporary).first()
        if unique_month is None:
            #DB MONTH SIRALAMA SCRIPTI. HEMEN ALTINDA DA DATABASE'E ATIYOR.
            month_order ={"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, 
                            "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
            month_order_no = month_order[form.month_planned.data]
            month_unique = form.month_planned.data + str(form.year_planned.data)
            print(month_unique)
            month = SALESMTPLANNED_db(month_planned_db = form.month_planned.data, 
            month_order_db = month_order_no,
            year_planned_db = form.year_planned.data, 
            month_unique_db = month_unique,
            tot_vol_planned_db = form.tot_vol_planned.data, 
            tot_mf_planned_db = form.tot_mf_planned.data, 
            tot_anodize_planned_db = form.tot_anodize_planned.data, 
            tot_powder_coat_planned_db = form.tot_powder_coat_planned.data, 
            tot_wood_finish_planned_db = form. tot_wood_finish_planned.data, 
            tot_crimping_planned_db = form. tot_crimping_planned.data, tot_EUR_planned_db = form. tot_EUR_planned.data, 
            new_customers_planned_db = form. new_customers_planned.data)
                        
            db.session.add(month)
            db.session.commit()
            flash("Entry recorded successfully! Thank you!", "success")
        #name = form.name_field.data #For sending to "hello -name-"" page on html. Otherwise will keep asking the name/credentials.
        #form.name_field.data = ""
        #form.email_field.data = ""
        else:
            flash("Entry for this month was recorded before! Please update chosen month or choose another month for recording!", 'error')
        
    #User.query.order_by(User.popularity.desc(), User.date_created.desc()).limit(10).all()
    all_records = SALESMTPLANNED_db.query.order_by(SALESMTPLANNED_db.year_planned_db, SALESMTPLANNED_db.month_order_db)
    return  render_template("sales_planned_entry.html", form=form, name=name, all_records=all_records)


#//////////////////////NEW FUNCTION
@app.route('/sales_actual_entry', methods=["GET", "POST"])
@login_required
def sales_actual_entry(): #Add user - ALSO TO DATABASE!!!
    name = None #For sending to "please enter your name/credentials page on html - if statement"
    form = SalesMTActual()
    #Validation of our form
    if form.validate_on_submit():
        #name = form.name_field.data
        #For arranging a code disabling multiple entries for same month/period
        month_unique_temporary = form.month_actual.data + str(form.year_actual.data)
        unique_month = SALESMTACTUAL_db.query.filter_by(month_unique_db=month_unique_temporary).first()
        if unique_month is None:
            #DB MONTH SIRALAMA SCRIPTI. HEMEN ALTINDA DA DATABASE'E ATIYOR.
            month_order ={"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, 
                            "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
            month_order_no = month_order[form.month_actual.data]
            month_unique = form.month_actual.data + str(form.year_actual.data)
            print(month_unique)
            month = SALESMTACTUAL_db(month_actual_db = form.month_actual.data, 
            month_order_db = month_order_no,
            year_actual_db = form.year_actual.data, 
            month_unique_db = month_unique,
            tot_vol_actual_db = form.tot_vol_actual.data, 
            tot_mf_actual_db = form.tot_mf_actual.data, 
            tot_anodize_actual_db = form.tot_anodize_actual.data, 
            tot_powder_coat_actual_db = form.tot_powder_coat_actual.data, 
            tot_wood_finish_actual_db = form. tot_wood_finish_actual.data, 
            tot_crimping_actual_db = form. tot_crimping_actual.data, tot_EUR_actual_db = form. tot_EUR_actual.data, 
            new_customers_actual_db = form. new_customers_actual.data)
                        
            db.session.add(month)
            db.session.commit()
            flash("Entry recorded successfully! Thank you!", "success")
        #name = form.name_field.data #For sending to "hello -name-"" page on html. Otherwise will keep asking the name/credentials.
        #form.name_field.data = ""
        #form.email_field.data = ""
        else:
            flash("Entry for this month was recorded before! Please update chosen month or choose another month for recording!", 'error')
        
    #User.query.order_by(User.popularity.desc(), User.date_created.desc()).limit(10).all()
    all_records = SALESMTACTUAL_db.query.order_by(SALESMTACTUAL_db.year_actual_db, SALESMTACTUAL_db.month_order_db)
    return  render_template("sales_actual_entry.html", form=form, name=name, all_records=all_records)

#//////////////////////NEW FUNCTION

#NEREDE KALDIK? -  AŞAĞIDAKİ UPDATE FONKSİYONUNA TEKRAR BAKILACAK...!
#Update tests-001
@app.route('/update_planned_entry/<int:id>', methods=["GET", "POST"])
@login_required
def update_planned(id):
    #id = None
    form = SalesMTPlanned()
    entry_to_update = SALESMTPLANNED_db.query.get_or_404(id)
    #print(entry_to_update)
    if request.method == "POST": #burayı daha iyi anlamalıyız!!! 
        #- yani eğer update.html üzerinden post edilen bir işlem var ise mi demek istiyor? Buna bakmaya devam...
        print("Yes this is a POST attempt")
        entry_to_update.tot_vol_planned_db = request.form["tot_vol_planned"] #Check here out!! Buraya da bakalım..!!
        entry_to_update.tot_mf_planned_db = request.form["tot_mf_planned"]
        entry_to_update.tot_anodize_planned_db = request.form["tot_anodize_planned"]
        entry_to_update.tot_powder_coat_planned_db = request.form["tot_powder_coat_planned"]
        entry_to_update.tot_wood_finish_planned_db = request.form["tot_wood_finish_planned"]
        entry_to_update.tot_crimping_planned_db = request.form["tot_crimping_planned"]
        entry_to_update.tot_EUR_planned_db = request.form["tot_EUR_planned"]
        entry_to_update.new_customers_planned_db = request.form["new_customers_planned"]
        # Açıklaması için https://stackoverflow.com/questions/10434599/get-the-data-received-in-a-flask-request
        try:
            db.session.commit()
            flash("Your update process is successful", "success")
            return render_template("update_planned_entry.html", form=form, entry_to_update=entry_to_update, id=id)
            
        except:
            db.session.commit()
            flash("Update process failed! Please inform your administrator..", "success")
            return render_template("update_planned_entry.html", form=form, entry_to_update=entry_to_update, id=id)
    else:
        print("NO this is NOT a POST attempt")
        return render_template("update_planned_entry.html", form=form, entry_to_update=entry_to_update, id=id)

#//////////////////////NEW FUNCTION

@app.route('/update_actual_entry/<int:id>', methods=["GET", "POST"])
@login_required
def update_actual(id):
    #id = None
    form = SalesMTActual()
    entry_to_update = SALESMTACTUAL_db.query.get_or_404(id)
    #print(entry_to_update)
    if request.method == "POST": #burayı daha iyi anlamalıyız!!! 
        #- yani eğer update.html üzerinden post edilen bir işlem var ise mi demek istiyor? Buna bakmaya devam...
        print("Yes this is a POST attempt")
        entry_to_update.tot_vol_actual_db = request.form["tot_vol_actual"] #Check here out!! Buraya da bakalım..!!
        entry_to_update.tot_mf_actual_db = request.form["tot_mf_actual"]
        entry_to_update.tot_anodize_actual_db = request.form["tot_anodize_actual"]
        entry_to_update.tot_powder_coat_actual_db = request.form["tot_powder_coat_actual"]
        entry_to_update.tot_wood_finish_actual_db = request.form["tot_wood_finish_actual"]
        entry_to_update.tot_crimping_actual_db = request.form["tot_crimping_actual"]
        entry_to_update.tot_EUR_actual_db = request.form["tot_EUR_actual"]
        entry_to_update.new_customers_actual_db = request.form["new_customers_actual"]
        # Açıklaması için https://stackoverflow.com/questions/10434599/get-the-data-received-in-a-flask-request
        try:
            db.session.commit()
            flash("Your update process is successful", "success")
            return render_template("update_actual_entry.html", form=form, entry_to_update=entry_to_update, id=id)
            
        except:
            db.session.commit()
            flash("Update process failed! Please inform your administrator..", "success")
            return render_template("update_actual_entry.html", form=form, entry_to_update=entry_to_update, id=id)
    else:
        print("NO this is NOT a POST attempt")
        return render_template("update_actual_entry.html", form=form, entry_to_update=entry_to_update, id=id)



#Route for deleting our entries - NEW!! :) PLANNED!!!
@app.route('/delete_planned_entry/<int:id>', methods=["GET", "POST"])
@login_required
def delete_planned(id):
    entry_to_delete = SALESMTPLANNED_db.query.get_or_404(id)
    name = None #For sending to "please enter your name/credentials page on html - if statement"
    form = SalesMTPlanned()
    try:
        db.session.delete(entry_to_delete)
        db.session.commit()
        flash("Entry deleted. Thank you", "success")
        print("Entry deleted.. now should be re-routing to form2??")
        all_records = SALESMTPLANNED_db.query.order_by(SALESMTPLANNED_db.date_added_db)
        return redirect(url_for("sales_planned_entry")) #Orjinal codemy videsounda bu satır yok. 
        # Bunun yerine aşağıdaki satır yazılmış ama delete/n urlinde kalıyordu. 
        # Dolayısı ile sildikten sonra yeni giriş hata veriyordu.
        #return  render_template("form2.html", form=form, name=name, our_users=our_users)
    except:
        flash("There seems to be a problem. Please inform your administrator", 'error')
        return  render_template("sales_planned_entry.html", form=form, name=name, all_records=all_records)


#//////////////////////NEW FUNCTION

#Route for deleting our entries - NEW!! :) ACTUAL!!!
@app.route('/delete_actual_entry/<int:id>', methods=["GET", "POST"])
@login_required
def delete_actual(id):
    entry_to_delete = SALESMTACTUAL_db.query.get_or_404(id)
    name = None #For sending to "please enter your name/credentials page on html - if statement"
    form = SalesMTActual()
    try:
        db.session.delete(entry_to_delete)
        db.session.commit()
        flash("Entry deleted. Thank you", "success")
        print("Entry deleted.. now should be re-routing to form2??")
        all_records = SALESMTACTUAL_db.query.order_by(SALESMTACTUAL_db.date_added_db)
        return redirect(url_for("sales_actual_entry")) #Orjinal codemy videsounda bu satır yok. 
        # Bunun yerine aşağıdaki satır yazılmış ama delete/n urlinde kalıyordu. 
        # Dolayısı ile sildikten sonra yeni giriş hata veriyordu.
        #return  render_template("form2.html", form=form, name=name, our_users=our_users)
    except:
        flash("There seems to be a problem. Please inform your administrator", 'error')
        return  render_template("sales_actual_entry.html", form=form, name=name, all_records=all_records)


@app.route("/login", methods=['GET', 'POST'])
def login():
    name=None
    if current_user.is_authenticated:
        print("User is ALREADY LOGGED IN")
        return redirect(url_for('index'))
    form = Login()
    if form.validate_on_submit():
        print("Form validated")
        user = Users_db.query.filter_by(email_db=form.email.data).first()
        password = user.password_db
        print("passcheck", password)
        password_check = form.password.data
        print("passcheck", password_check)
        
        #name=form.name.data
        print(form.email.data)
        if user and (password==password_check):
            print("/////////Found this user and his password is correct!!!//////")
            login_user(user)
            #name=form.name_field.data
            print("User seems to be logged in beybisi..")
            flash('Login Successful. Have a nice day!!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'error')
    return render_template('login.html', title='Login', form=form, name=name)


@app.route("/logout")
def logout():
    logout_user()
    print("The user should have been LOGGED OUT NOW!!!")
    flash('Logout successful. Thank you for using the system', 'success')
    return redirect(url_for('index'))




@app.route('/performance_graph')
@login_required
def performance_graph():
    #//////////////////////////////
    #//////////////////////////////BOKEH TEST REGION

    # Connecting to MySQL server using mysql-python DBAPI 
    engine = create_engine("mysql+pymysql://tansubaktiran:Avz9p9&9Dgsu_099@193.111.73.99/tansubaktiran")
    dbconnection = engine.connect()

    planned_data = pandas.read_sql("select * from SALESMTPLANNED_db", dbconnection)
    actual_data = pandas.read_sql("select * from SALESMTACTUAL_db", dbconnection)
    myfilter = planned_data["year_planned_db"]==2021
    planned_data.sort_values(by='month_order_db', ascending=True, inplace=True)
    filtered_planned_data = planned_data[myfilter]

    source1 = ColumnDataSource(filtered_planned_data)
    source2 = ColumnDataSource(actual_data)

    circle_size=10
    bar_width=.5

    f = figure(x_range=filtered_planned_data["month_unique_db"], title ="Planned and Actual Total Volume (in MT)")
    f.circle(x="month_unique_db", y="tot_vol_planned_db", size=circle_size, fill_alpha=.4, color="navy", source=source1)
    f.vbar(x="month_unique_db", top="tot_vol_actual_db", width=bar_width, color="orangered", fill_alpha=.4, source=source2)

    f2 = figure(x_range=filtered_planned_data["month_unique_db"], title ="Planned and Actual MF (in MT)")
    f2.circle(x="month_unique_db", y="tot_mf_planned_db", size=circle_size , fill_alpha=.4, color="navy", source=source1)
    f2.vbar(x="month_unique_db", top="tot_mf_actual_db", width=bar_width, color="blue", fill_alpha=.4, source=source2)

    f3 = figure(x_range=filtered_planned_data["month_unique_db"], title ="Planned and Actual ANODIZE (in MT)")
    f3.circle(x="month_unique_db", y="tot_anodize_planned_db", size=circle_size, fill_alpha=.4, color="navy", source=source1)
    f3.vbar(x="month_unique_db", top="tot_anodize_actual_db", width=bar_width, color="gold", fill_alpha=.4, source=source2)

    f4 = figure(x_range=filtered_planned_data["month_unique_db"], title ="Planned and Actual POWDER COATING (in MT)")
    f4.circle(x="month_unique_db", y="tot_powder_coat_planned_db", size=circle_size, fill_alpha=.4, color="navy", source=source1)
    f4.vbar(x="month_unique_db", top="tot_powder_coat_actual_db", width=bar_width, color="purple", fill_alpha=.4, source=source2)

    f5 = figure(x_range=filtered_planned_data["month_unique_db"], title ="Planned and Actual WOOD FINISH (in MT)")
    f5.circle(x="month_unique_db", y="tot_wood_finish_planned_db", size=circle_size, fill_alpha=.4, color="navy", source=source1)
    f5.vbar(x="month_unique_db", top="tot_wood_finish_actual_db", width=bar_width, color="green", fill_alpha=.4, source=source2)

    f6 = figure(x_range=filtered_planned_data["month_unique_db"], title ="Planned and Actual CRIMPING (in MT)")
    f6.circle(x="month_unique_db", y="tot_crimping_planned_db", size=circle_size, fill_alpha=.4, color="navy", source=source1)
    f6.vbar(x="month_unique_db", top="tot_crimping_actual_db", width=bar_width, color="turquoise", fill_alpha=.4, source=source2)

    f7 = figure(x_range=filtered_planned_data["month_unique_db"], title ="Planned and Actual Total Revenues (in EUR)")
    f7.circle(x="month_unique_db", y="tot_EUR_planned_db", size=circle_size, fill_alpha=.4, color="navy", source=source1)
    f7.vbar(x="month_unique_db", top="tot_EUR_actual_db", width=bar_width, color="gold", fill_alpha=.4, source=source2)

    f8 = figure(x_range=filtered_planned_data["month_unique_db"], title ="Number of Planned and Actual New Customers")
    f8.circle(x="month_unique_db", y="new_customers_planned_db", size=circle_size, fill_alpha=.4, color="navy", source=source1)
    f8.vbar(x="month_unique_db", top="new_customers_actual_db", width=bar_width, color="lightblue", fill_alpha=.4, source=source2)

    figure_list = [f,f2,f3,f4,f5,f6,f7,f8]
    for fig in figure_list:
        fig.xaxis.major_label_orientation = pi/4

    lay_out = gridplot([[f,f2,f3], [f4,f5,f6],[f7,f8]],plot_width=400, plot_height=400)
    #show(column(Div(text="<h2>Asistal - CRM Dashboard - Test-1 05.11.21 </h2></br><h3>Year 2021 Records</h3></br><h3>Circles are targets, bars are actual values</h3>"), lay_out))
    #show(f)
    script, div = components(lay_out)
    dbconnection.close()

    #IMPROVE THE ABOVE    
    #//////////////////////////////
    #//////////////////////////////BOKEH TEST REGION

    return  render_template("performance_graph.html", script=script, div=div)


if __name__ == "__main__":
    app.run(debug=True)