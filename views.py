from flask import Blueprint, render_template

views = Blueprint(__name__, "views")


@views.route('/')
def homePage():
    return render_template('homepage.html')

@views.route('/projects.html')
def projectPage():
    return render_template('projects.html')

@views.route('/designManifesto.html')
def projectListPage():
    return render_template('designManifesto.html')

@views.route('/project1.html')
def projectPage1():
    return render_template('project1.html')

@views.route('/project2.html')
def projectPage2():
    return render_template('project2.html')

@views.route('/project3.html')
def projectPage3():
    return render_template('project3.html')

@views.route('/project4.html')
def projectPage4():
    return render_template('project4.html')

@views.route('/project5.html')
def projectPage5():
    return render_template('project5.html')

@views.route('/projectwordle.html')
def projectwordlePage():
    return render_template('projectwordle.html')

@views.route('/AboutMe.html')
def aboutme():
    return render_template('AboutMe.html')

@views.route('/spotivibe.html')
def spotivibe():
    return render_template('spotivibe.html')

@views.route('/reciMe.html')
def recimePage():
    return render_template('reciMe.html')

@views.route('/clony.html')
def clonyPage():
    return render_template('clony.html')

@views.route('/lingomates.html')
def lingomatesPage():
    return render_template('lingomates.html')