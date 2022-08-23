from unicodedata import name
from django.shortcuts import render
from tracker_app.models import login,amoundspen

# Create your views here.
def home(request):
    return render(request,"home.html")

def home2(request):
    return render(request,"login.html")

#registration
def registration(request):
    message={}
    try:
        lname=request.POST['name']
        lamount=request.POST['payment']
        lpassword=request.POST['password']
        lconpassword=request.POST['con_password']
        #validation
        if lname=="" or lamount=="" or lpassword=="":
            if lname=="":
                message['msg1']="Empty field"
            if lamount=="":
                message['msg2']="Empty field"
            if lpassword=="":
                message['msg3']="Empty field"
            if lconpassword=="":
                message['msg4']="Empty field"
            return render(request,"login.html",message)
        elif lpassword!=lconpassword:
            message['msg4']="password not match"
            return render(request,"login.html",message)
        else:
            print ("lname")
            che=login.objects.filter(name=lname)
            if che.exists():
                message['msg5']="Name already entered"
            else:
                emp=login(name=lname,amount=lamount,password=lpassword)
                emp.save()
                message['msg5']="Registration completed"
                return render(request,"login.html",message)
    except Exception as e:
        print(e)
        message['msg5']="Failed"
        return render(request,"login.html",message)

# login user
def login_acc(request):
    message={}
    try:
        loginname=request.POST['login_name']
        loginpassword=request.POST['login_password']
        if loginname=="" or loginpassword=="":
            message['msg6']="Empty fields"
            return render(request,"login.html",message)
        else:
            request.session['username']=loginname
            che=login.objects.filter(name=loginname,password=loginpassword)
            if che.exists():
                return display(request)
            else:
                message['msg6']="login failed"
                return render(request,"login.html",message)
    except Exception as e:
        print(e)
        message['msg6']="Failed"
        return render(request,"login.html",message)

# display 
def display(request):
    cart = request.session.get('username')
    emp1=login.objects.filter(name=cart)

    # user namer dispaly
    data=cart.upper()
   

    #  add amount thing is travel
    emp2=amoundspen.objects.values_list('price',flat=True).filter(thing="travel",nname=cart)
    lens = (list(emp2))
    sum=0
    for i in range(len(lens)):
        
        sum = sum+int(lens[i])

    # add amount thing is food
    emp3=amoundspen.objects.values_list('price',flat=True).filter(thing="food",nname=cart)
    print(emp3)
    lens1 = (list(emp3))
    sum1=0
    for j in range(len(lens1)):
        sum1 = sum1+int(lens1[j])
    print(sum1)

    # add amount thing is stay
    emp4=amoundspen.objects.values_list('price',flat=True).filter(thing="Stay",nname=cart)
   
    lens2 = (list(emp4))
    sum2=0
    for k in range(len(lens2)):
        sum2 = sum2+int(lens2[k])
        
    # add total amound spend
    sum3=sum+sum1+sum2
    
    # conditions for display
    if 'add_matter' in request.POST:
        return render(request,"index.html",{'contactdetail':emp1,'data':data,'msg':"Details added",'sum':sum,'sum1':sum1,'sum2':sum2,'sum3':sum3})
    if 'add_wallet' in request.POST:
        return render(request,"index.html",{'contactdetail':emp1,'data':data,'msg':"Amount added",'sum':sum,'sum1':sum1,'sum2':sum2,'sum3':sum3})
    if 'sub' in request.POST:
        return render(request,"index.html",{'contactdetail':emp1,'data':data,'sum':sum,'sum1':sum1,'sum2':sum2,'sum3':sum3})
    return render(request,"index.html",{'contactdetail':emp1,'data':data,'sum':sum,'sum1':sum1,'sum2':sum2,'sum3':sum3})


def wallet_add(request):
    message={}
    # add wallet amount
    if 'add_wallet' in request.POST:
        try:
            price=request.POST['walletadd']
            if price=="":
                message['msg']="Empty field"
                return render(request,"index.html",message)
            else:
                cart = request.session.get('username')
                emp=login.objects.values_list('amount',flat=True).filter(name=cart)
                for value in emp:
                    new_amount=int(value)+int(price)
                che=login.objects.filter(name=cart)
                che.update(amount=new_amount)
                return display(request)
        except Exception as e:
            print(e)
            message['msg2']="Amount not added"
            return render(request,"index.html",message)

    # add matter and amount
    if 'add_matter' in request.POST:
        try:
            cart = request.session.get('username')
            emp=login.objects.values_list('amount',flat=True).filter(name=cart)
            c=(list(emp))
            matter=request.POST['matter']
            spend=request.POST['spend']
            if matter=="" or spend=="":
                message['msg']="empty field"
                return render(request,"index.html",message)
            else:
                if (int(spend))<=(int(c[0])):
                    che=amoundspen(nname=cart,thing=matter,price=spend)
                    che.save()
                    # update wallet balance
                    new_amount=int(c[0])-int(spend)
                    emp1=login.objects.filter(name=cart)
                    emp1.update(amount=new_amount)
                    msg2="Details Added"
                    return display(request) 
                else:
                    message['msg']="insfficent balance"
            return render(request,"index.html",message)
        except Exception as e:
            print(e)
            message['msg']="Amount not added"
            return render(request,"index.html",message)

#logout session
def logout(request):
    request.session.clear()    
    request.session.flush()
    return render(request,"login.html")






