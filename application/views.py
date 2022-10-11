from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Tasks,List,User
from flask import render_template,request,redirect,url_for,session,flash
from . import db
from sqlalchemy import func
from datetime import datetime
from datetime import date
import matplotlib.pyplot as plt
import numpy as np
import os
import json


views = Blueprint('views',__name__)

@views.route('/')
@login_required
def home():
    user_id = current_user.id
    data = {}
    lists = db.session.query(List).filter(List.username == user_id)
    for list in lists:
        tasks = db.session.query(Tasks).filter((Tasks.username == user_id) & (Tasks.status == list.id))
        task_data = []
        for task in tasks:
            task_data.append(task)
        data[list.list_name] = task_data
    db.session.commit()
    return render_template("home.html",user=current_user,data=data)

@views.route('/addlist', methods=['GET', 'POST'])
@login_required
def addlist():
    if request.method == 'GET':
        return render_template("addlist.html" , user = current_user )
    elif request.method == 'POST':
        list = db.session.query(List).filter((List.list_name == request.form['listname']) & (List.username == current_user.id)).first()
        if not list:
            list = List(
                username = current_user.id,
                list_name = request.form['listname']
            )
            db.session.add(list)
            db.session.commit()
            return redirect('/') 
        else:
            flash('list name already exists',category='error')
            return redirect('/addlist')

@views.route('/addtask', methods=['GET', 'POST'])
@login_required
def addtask():
    if request.method == 'GET':
        lists = db.session.query(List).filter(List.username == current_user.id).all()
        return render_template('addtask.html' , user = current_user,lists=lists)
    elif request.method == 'POST':
        list = db.session.query(List).filter((List.username == current_user.id) & (List.id == request.form['Status'])).first()
        
        if (request.form['completed'] == 'true'):
            completed_date = datetime.now()
        else:
            completed_date =  None
        tasks = Tasks(
                username = request.form['user'],
                task = request.form['Task-description'],
                title = request.form['Task-title'],
                status = list.id,
                due_date = datetime.strptime(request.form['Due'], '%Y-%m-%d'),
                completed = request.form['completed'],
                completed_date = completed_date)
        db.session.add(tasks)
        db.session.commit()
        return redirect('/')

@views.route('/<listname>/editlist', methods=['GET', 'POST'])
@login_required
def edit_list(listname):
    if request.method == 'GET':
        list_name = db.session.query(List).filter((List.username == current_user.id) & (List.list_name == listname)).first()
        return render_template('editlist.html', listname = list_name,user = current_user)
    elif request.method == 'POST':
        list = db.session.query(List).filter((List.username == current_user.id) & (List.id == request.form['id'])).first()
        list2 = db.session.query(List).filter((List.username == current_user.id) & (List.list_name == request.form['listname'])).first()
        if list2:
            flash('List name already exists',category='error')
            return render_template('editlist.html', listname = list,user = current_user)
        
        list.list_name = request.form['listname']
        db.session.commit()
        return redirect('/')

@views.route('/<task_id>/edit_task', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    if request.method == 'GET':
        task = db.session.query(Tasks).filter((Tasks.username == current_user.id) & (Tasks.id == task_id)).first()
        list_name = db.session.query(List).filter((List.username == current_user.id) & (List.id == task.status)).first()
        lists = db.session.query(List).filter((List.username == current_user.id)).all()

        return render_template('edittask.html' , task = task , user = current_user , lists = lists,list_name=list_name)
    elif request.method == 'POST':
        list = db.session.query(List).filter((List.username == current_user.id) & (List.list_name == request.form['status'])).first()
        task = db.session.query(Tasks).filter((Tasks.username == current_user.id) & (Tasks.id == request.form['id'])).first()
        if (request.form['completed'] == 'true'):
            completed_date = datetime.today()
        else:
            completed_date =  None

        task.task = request.form['Task-description']
        task.title = request.form['Task-title']
        task.status = list.id
        task.due_date = datetime.strptime(request.form['Due'], '%Y-%m-%d')
        task.completed = request.form['completed']
        task.completed_date = completed_date
        db.session.commit()
        return redirect('/')



@views.route('/<task_id>/deletetask', methods=['GET'])
@login_required
def delete_task(task_id):
    if request.method == 'GET':
        task = db.session.query(Tasks).filter((Tasks.username == current_user.id) & (Tasks.id == task_id)).first()
        lists = db.session.query(List).filter((List.username == current_user.id) & (Tasks.id == task.id)).first()
        return render_template('deletetask.html',Tasks = task,list = lists, user=current_user)

@views.route('<task_id>/deletetask/yes', methods=['GET'])
@login_required
def delete_task_yes(task_id):
    if request.method == 'GET':
        task = db.session.query(Tasks).filter((Tasks.username == current_user.id) & (Tasks.id == task_id)).first()
        db.session.delete(task)
        db.session.commit()
        return redirect('/')

@views.route('<listname>/deletelist', methods=['GET'])
@login_required
def delete_list(listname):
    if request.method == 'GET':
        list_name = db.session.query(List).filter((List.username == current_user.id) & (List.list_name == listname)).first()
        tasks = db.session.query(Tasks).filter((Tasks.username == current_user.id) & (Tasks.status == list_name.id)).all()
        return render_template('deletelist.html', list = list_name, user = current_user, tasks = tasks)

@views.route('/<listname>/deletelist/yes', methods=['GET'])
@login_required
def delete_list_yes(listname):
    if request.method == 'GET':
        list_name = db.session.query(List).filter((List.username == current_user.id) & (List.list_name == listname)).first()
        tasks = db.session.query(Tasks).filter((Tasks.username == current_user.id) & (Tasks.status == list_name.id)).all()
        for task in tasks:
            db.session.delete(task)
        db.session.delete(list_name)
        db.session.commit()
        return redirect('/')

@views.route('/summary')
@login_required
def summary():
    task_counts = db.session.query(Tasks).filter((Tasks.username == current_user.id)).count()
    if (task_counts > 0 ):
        tasks = db.session.query(Tasks).filter((Tasks.username == current_user.id)).all()
        lists = db.session.query(List).filter((List.username == current_user.id)).all()
        datas = {}
        due = {}
        for list in lists:
            listname = list.list_name
            task_count = db.session.query(Tasks).filter((Tasks.username == current_user.id) & (Tasks.status == list.id)).count()
            task_due_date_over = db.session.query(Tasks).filter((Tasks.username == current_user.id) & (Tasks.status == list.id) & (func.date(Tasks.due_date) <  date.today())).count()
            task_done = db.session.query(Tasks).filter((Tasks.username == current_user.id) & (Tasks.status == list.id) & (Tasks.completed == 'true')).count()
            if (task_count > 0):
                datas[listname] = task_count
                data = np.array([task_due_date_over,task_count-task_due_date_over])
                my_label = ['Deadline Passed','Deadline not Passed']
                plt.bar(my_label,data)
                path = 'application/static/' + listname + '.jpg'
                if(os.path.exists(path=path)):
                    os.remove(path)
                plt.savefig(path)
                plt.close()
                data = np.array([task_done,task_count-task_done])
                my_label = ['Done','Pending']
                plt.pie(data,labels=my_label)
                plt.legend()
                path = 'application/static/' + listname + 'done.jpg'
                if(os.path.exists(path=path)):
                    os.remove(path)
                plt.savefig(path)
                plt.close()
        tasks_completed = db.session.query(Tasks).filter((Tasks.username == current_user.id) & (Tasks.completed == 'true')).count()
        data = np.array([tasks_completed,task_counts-tasks_completed])
        my_labels = ['done','pending']
        plt.pie(data,labels=my_labels)
        plt.legend()
        path = 'application/static/percentagecompleted.jpg'
        if(os.path.exists(path=path)):
            os.remove(path)
        plt.savefig(path)
        plt.close()
        task_due_date_over = db.session.query(Tasks).filter((Tasks.username == current_user.id) & (func.date(Tasks.due_date) <  date.today())).count()
        data = np.array([task_due_date_over,task_counts-task_due_date_over])
        my_label = ['Deadline Passed','Deadline not Passed']
        plt.bar(my_label,data)
        path = 'application/static/deadline.jpg'
        if(os.path.exists(path=path)):
            os.remove(path)
        plt.savefig(path)
        plt.close()

        data = []
        values = []
        for task in tasks:
            dates = str(task.due_date)
            if dates in data:
                index = data.index(dates)
                values[index] = values[index] + 1
            else:
                data.append(dates) 
                values.append(1)
        dat = values
        keys = data
        plt.plot_date(keys,dat,linestyle = 'solid')
        path = 'application/static/graph.jpg'
        if(os.path.exists(path=path)):
            os.remove(path)
        plt.savefig(path)
        plt.close()

        plt.pie(dat,labels=keys)
        path = 'application/static/graph-pie.jpg'
        if(os.path.exists(path=path)):
            os.remove(path)
        plt.savefig(path)
        plt.close()
        return render_template('summary.html',data = datas,user=current_user)
    else:
        flash('Create Lists and tasks to view summary',category='error')
        return redirect('/')
