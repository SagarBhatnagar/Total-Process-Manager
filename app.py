from flask import Flask, render_template, url_for, redirect, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_wtf import FlaskForm
from flask_table import Table, Col
import os

#App
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#initialize database
db = SQLAlchemy(app)
#marshmallow
ma = Marshmallow(app)

#DATA STRUCTURE
class Item(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    ref_id=db.Column(db.String(100), unique = True)
    project_name=db.Column(db.String(100))
    task=db.Column(db.String(100))
    channel=db.Column(db.String(100))
    ticket=db.Column(db.String(100))
    priority=db.Column(db.String(100))
    start_date=db.Column(db.String(100))
    end_date=db.Column(db.String(100))
    gtin=db.Column(db.Integer)
    vendor_id=db.Column(db.Integer)
    action_required=db.Column(db.Text)
    action_taken=db.Column(db.Text)
    assigned_to=db.Column(db.String(100))
    reviewer=db.Column(db.String(100))
    project_manager=db.Column(db.String(100))
    project_lead=db.Column(db.String(100))
    status=db.Column(db.Text)
    review=db.Column(db.Text)


    def __init__(self, ref_id, project_name, task, channel, ticket, priority, start_date, end_date, gtin, vendor_id):
        self.ref_id = ref_id
        self.project_name = project_name
        self.task = task
        self.channel = channel
        self.ticket = ticket
        self.priority = priority
        self.start_date = start_date
        self.end_date = end_date
        self.gtin = gtin
        self.vendor_id = vendor_id

#ItemSchema
class ItemSchema(ma.Schema):
    class Meta:
        fields = ('id', 'ref_id', 'project_name', 'task', 'channel',  'ticket', 'priority', 'start_date', 'end_date', 'gtin', 'vendor_id')
#Init Schema
item_schema = ItemSchema()
items_schema = ItemSchema(many=True)



app.secret_key = "super secret key"

#Table
class ItemTable(Table):
    ref_id = Col('Unique Reference Number')
    project_name = Col('Project Name')
    task = Col('Task')
    channel = Col('How we receive')
    ticket = Col('JIRA ticket number')
    priority = Col('Priority')
    start_date = Col('Recieved Date')
    end_date = Col('Resolved Date')
    gtin = Col('GTIN')
    vendor_id = Col('Vendor ID')

#Master Page
@app.route('/', methods = ['GET', 'POST'])
def home():
    #Fetching Search Parameters
    if request.method == 'POST':
        project_name = request.form.get('project_name')
        ticket = request.form.get('ticket')
        gtin = request.form.get('gtin')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        priority = request.form.get('priority')
        project_manager = request.form.get('project_manager')
        reviewer = request.form.get('reviewer')
        ref_id = request.form.get('Ref_ID')
        query = Item.query
        #Search Filter
        if project_name:
            query = query.filter(Item.project_name == project_name)
        if ticket:
            query = query.filter(Item.ticket == ticket)
        if gtin:
            query = query.filter(Item.gtin == gtin)
        if start_date:
            query = query.filter(Item.start_date == start_date)
        if end_date:
            query = query.filter(Item.end_date == end_date)
        if priority:
            query = query.filter(Item.priority == priority)
        if project_manager:
            query = query.filter(Item.project_manager == project_manager)
        if reviewer:
            query = query.filter(Item.reviewer == reviewer)
        if ref_id:
            query = query.filter(Item.ref_id == ref_id)
        #Generated Result
        result = query.all()
        table = ItemTable(result)
            # print(table.__html__())
        #Show Results Page
        return render_template('search_results.html', table=table)
    return render_template('home.html')

#Work Induction
@app.route('/workInd', methods = ['GET', 'POST'])
def workInd():
    #get data from form
    if request.method == 'POST':
        project_name = request.form.get('project_name')
        task = request.form.get('task')
        channel = request.form.get('channel')
        ticket = request.form.get('ticket')
        priority = request.form.get('priority')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        gtin = request.form.get('gtin')
        vendor_id = request.form.get('vendor_id')
        
        
        #check for new or repeat
        found_vendor = Item.query.filter_by(vendor_id = vendor_id).first()
        found_gtin = Item.query.filter_by(gtin = gtin).first()
        
        #get code for reference id
        if project_name:
            if project_name == 'WM Support':
                a = 'WMS'
            elif project_name == 'RCT Support':
                a = 'RCT'
            elif project_name == 'JoW':
                a = 'JOW'
        if task:
            if task == 'Item Maintenance':
                b = 'IM'
            elif task == 'Item Setup':
                b = 'IS'
            elif task == 'Miscellaneous':
                b = 'M'
        #set new or repeat
        c = 'N'
        if found_vendor and found_gtin:
            c = 'R'
        else:
            c = 'N'

        ref_id = a
        #create the item in database
        item = Item(ref_id, project_name, task, channel, ticket, priority, start_date, end_date, gtin, vendor_id)
        db.session.add(item)
        db.session.commit()
        
        #generate reference id for an item
        item.ref_id = a + '-' + str(item.id) + '-' + b + '-' +  c 
        db.session.commit()

        flash('Added new item with Reference id : {}'.format(item.ref_id))
    return render_template('workInduction.html')

#Delete
@app.route('/delete', methods = ["GET", "POST"])
def delete_item():
    if request.method == 'POST':
        Ref_ID = request.form.get('Ref_ID')
        found_item = Item.query.filter_by(ref_id = Ref_ID).first()
        if found_item:
            Item.query.filter_by(ref_id = Ref_ID).delete()
            db.session.commit()
            flash('Successfully deleted')
        else:
            flash('Item not found') 
    return render_template("delete.html")

#Work Info
@app.route('/workInfo', methods = ["GET", "POST"])
def workInfo():
    if request.method == "POST": 
        #get the values from form
        Ref_ID = request.form.get('Ref_ID')
        end_date = request.form.get('end_date')
        action_required = request.form.get('action_required')
        action_taken = request.form.get('action_taken')
        assigned_to = request.form.get('assigned_to')
        reviewer = request.form.get('reviewer')
        project_manager = request.form.get('project_manager')
        project_lead = request.form.get('project_lead')
        #edit values obtained
        found_item = Item.query.filter_by(ref_id = Ref_ID).first()
        if found_item:
            if end_date:
                found_item.end_date = end_date
            if action_required:
                found_item.action_required = action_required
            if action_taken:
                found_item.action_taken = action_taken
            if assigned_to:
                found_item.assigned_to = assigned_to
            if reviewer:
                found_item.reviewer = reviewer
            if project_manager:
                found_item.project_manager = project_manager
            if project_lead:
                found_item.project_lead = project_lead
            db.session.commit()
            flash('updated item : {}'.format(Ref_ID))
        else:
            flash('Item Not Found')
    return render_template('workInfo.html')

@app.route('/qms', methods = ["GET", "POST"])
def qms():
    if request.method == 'POST':
        Ref_ID = request.form.get('Ref_ID')
        found_item = Item.query.filter_by(ref_id = Ref_ID).first()
        if found_item:
            return redirect(url_for('status', Ref_ID = Ref_ID))
            flash('Found')
        else:
            flash('Item not found')
    return render_template('qms.html')

@app.route('/status', methods = ["GET", "POST"])
def status():
    Ref_ID = request.args['Ref_ID']    
    item = Item.query.filter_by(ref_id = Ref_ID)
    item = item[0]
    List = [item.gtin, item.assigned_to, item.reviewer]
    if request.method == 'POST':
        status = request.form.get('status')
        action_required = request.form.get('action_required')
        if item.status:
            item.status = item.status+', '+status
        else:
            item.status = status
        if action_required:
            item.action_required = item.action_required+','+action_required
        else:
            item.action_required = action_required
        db.session.commit()
        flash('done')

    return render_template('status.html', List = List)

if __name__ == '__main__':
    app.run(debug = True)