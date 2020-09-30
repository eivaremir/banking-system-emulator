from flask import Blueprint
from flask import render_template, request  # render form fields, handle server requests GET & POST
from flask import flash
from flask import redirect, url_for # funciones de redireccionamiento
from flask import abort #lanzar error 404
from .forms import AccountStatementForm, LoginForm, LoanCreationForm

#from .forms import LoginForm, RegisterForm, TaskForm
#from .models import *



from flask_login import login_user, logout_user, login_required, current_user
from .consts import * 
#from .email import *
from . import login_manager



from .functions import *

page = Blueprint('page',__name__)


##############################################################
# DEFINICION DE PROCEDIMIENTOS PARA INICIO Y CERRADO DE SESION
##############################################################

@login_manager.user_loader
def load_user(id):
    return User()


@page.app_errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'),404 # retorna status 200 de exito

@page.route("/login",methods=['GET','POST']) # hablitiar metodos para mostrar y crear sesión
def login():
    # request.form es un tipo de dato Form definido en wtforms (Archivo forms.py) con los valores recibidos de un formulario si esta peticion es de tipo post
    # instancia del formulario, con valores del usuario
    if current_user.is_authenticated:
        return redirect(url_for('.index'))
    form = LoginForm(request.form) 
    
    # if the request to the server is post and validations are correct
    if request.method == 'POST' and form.validate(): 
        user = User()
        if user.verify_password(form.password.data) and user.verify_user(form.username.data):
            login_user(user)
            flash(LOGIN)
            if current_user.is_authenticated:
                return redirect(url_for('.index'))
        else:
            flash(ERROR_USER_PASSWORD,'error')
        #print("Nueva sesión creada con los valores: " + form.username.data +" "+ form.password.data + " resultado: "+str(current_user.is_authenticated))
    print('Auth: '+str(current_user.is_authenticated))
    
    return render_template("login.html",title='Login', form=form, active = 'login')


@page.route("/logout")
def logout():
    print('Auth: '+str(current_user.is_authenticated))
    logout_user()
    print('Auth: '+str(current_user.is_authenticated))
    flash(LOGOUT)
    return redirect(url_for('.login'))

##############################################################
# DEFINICION DE VISTAS
##############################################################

@page.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html',title='Inicio',active='index',user=current_user)
    return render_template('index.html',title='Inicio',active='index')

@page.route("/client/")
@page.route("/client/<id>")
def client(id=0):
    if id == 0:
        
        return render_template('client.html',title="Clientes",active="client",clients=load_clients(),range=range,len=len,Client=Client)
    else:
        client = Client.getClientData(client=id)
        products = Client.getClientProducts(client=id)
        
        return render_template('client.html',title="Clientes",active="client",client=client,id=id,products = products,int = int,Product = Product,range=range,len=len)
@page.route('/statement',methods=['GET','POST'])
def statement():
    form = AccountStatementForm(request.form)
    form.id.data = request.args.get('id')
    found = False
    balance = 0.00
    statement= ''
    if request.method == 'POST' and form.validate():
        found = True
        statement = getAccountStatement(product=int(form.id.data),start=form.From.data,end=form.to.data)
        balance = Product.getProductBalance(id=int(form.id.data))

        return render_template('statement.html',title='Estados de cuenta',active='statement',form=form,balance=balance,found=found,statement=statement, len=len,range=range)
    return render_template('statement.html',title='Estados de cuenta',active='statement',form=form)

@page.route('/create/<product>',methods=['GET','POST'])
def create(product):
    form = LoanCreationForm(request.form)
    table = []
    interests = 0.00
    
    if request.method == 'POST':

        Loan.create_new_loan(Loan(
            id = 2,
            owner = request.args.get('owner'),
            interest_rate = request.args.get('interest_rate'),
            length = request.args.get('length'),
            base = request.args.get('base'),
            balance = request.args.get('amount'),
            From = "DD/MM/YY",
        ))

        return redirect(url_for('.client',id=request.args.get('owner')))

    if request.method == 'GET' and request.args.get('owner'):
        
        l = Loan(owner = request.args.get('owner'), 
                interest_rate = float(request.args.get('interest_rate')),
                base = int(request.args.get('base')),
                balance = float(request.args.get('amount')),
                length = int(request.args.get('length')),
                From = "DD/MM/YY",
                id = 1)
        
        table, interests = l.generate_amortization_table()
        print("Intereses:",interests)
        return render_template('create/amortization.html',title='Tabla de Amortización',loan = l,table=table,interests = interests,range=range,len=len,float=float)
    
            
        
            
            
    return render_template('create/loan.html',title='Crear Préstamo', form = form,table=table,interests = interests)

##############################################################
# FIN
##############################################################
@page.route("/profile")
@login_required
def profile():
    return render_template("profile/view.html",user=current_user)

@page.route("/profile/<int:profile_id>")
@login_required
def profile_id(profile_id):
    user = User.query.get_or_404(profile_id)
    return render_template("profile/view.html",user=user,active='profile')
    



@page.route("/tasks")
@page.route("/tasks/<int:page>")
@login_required
def tasks(page=1,per_page=2):
    
    pagination = current_user.tasks.paginate(page,per_page)
    tasks = pagination.items
    print('Auth: '+str(current_user.is_authenticated))
    return render_template('task/list.html', title="Tasks",tasks=tasks,pagination=pagination, page=page, active='tasks')

@page.route("/tasks/new", methods=['GET','POST'])
@login_required
def new_task():
    form = TaskForm(request.form)
    if request.method == 'POST':
        if form.validate():
            task = Task.create_element(form.title.data,form.description.data,current_user.id)
            if task:
                flash(TASK_CREATED)
    return render_template('task/new.html',title='Nueva Tarea',form=form, active='new_task')

@page.route("/tasks/delete/<int:task_id>")
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    # if the task wasnt created by the user logged in
    if task.user_id != current_user.id:
        abort(404)
    if task.delete_element(task.id):
        flash(TASK_DELETED)
    return redirect(url_for('.tasks'))

@page.route("/tasks/edit/<int:task_id>", methods=['GET','POST'])
@login_required
def edit_task(task_id):
    # obtener la información del task a partir del id
    task = Task.query.get_or_404(task_id)

    # solo el dueño de la tarea puede editar la tarea
    if task.user_id != current_user.id:
        abort(404)

    # instanciar el formulario
    form = TaskForm(request.form,obj=task)
    if request.method == 'POST' and form.validate():
        task = Task.update_element(task.id, form.title.data, form.description.data)
        if task: flash(TASK_UPDATED)
    return render_template("task/edit.html",title="Editar Tarea", form=form)

@page.route("/tasks/show/<int:task_id>")
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    return render_template("task/show.html", methods=['GET','SHOW'],title="Tarea #"+str(task_id),task=task)

@page.route("/register",methods=['GET','POST'])
def register():
    form = RegisterForm(request.form) 
    if request.method == 'POST' and form.validate(): 
        try:
          
            user = User.create_element(form.username.data,form.password.data,form.email.data)
            welcome_mail(user)
            flash(USER_CREATED)
            #print('Usuario '+str(user.id)+' Creado de forma exitosa')
            
            login_user(user)
            
            if current_user.is_authenticated:
                return redirect(url_for('.tasks'))
        except exc.IntegrityError:
            flash(ERROR_USER_DUPLICATE,'error')
        
        
    print('Auth: '+str(current_user.is_authenticated))
    return render_template("register.html",title='Register', form=form, active='register')    

