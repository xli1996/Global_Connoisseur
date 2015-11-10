from django.shortcuts import render
from django.db import IntegrityError
from django.core import exceptions
from django.http import HttpResponse,HttpResponseRedirect
from cs411.models import stu
from cs411.models import food
from django.shortcuts import render_to_response
import urllib.request
from django import forms
from cs411.models import comment
# Create your views here.
def signup(request):
    return render(request,'signup.html')

def log(request):
    return render(request,'login.html')


def get_data(request):
    try:
        user_name_ = request.GET.get('Username')
        password_ = request.GET.get('Password')
        stu.objects.create(user = user_name_, password=password_, spicy=0, sweet=0, salty=0)
    except IntegrityError as e:
        return HttpResponse('user already existed')

    return HttpResponse('cs411')

def login(request):
    user_name_ = request.GET.get('Username')
    password_ = request.GET.get('Password')
    if(user_name_ == ''):
        return render(request,'login.html')
    try:
        stu_get = stu.objects.get(user = user_name_)
    except:
          return render(request,'Login Failure.html')

    if stu_get.password == password_:
        #response = HttpResponseRedirect("index")
        request.session['username']=user_name_
        username = request.session.get('username')
        #response.set_cookie('username',user_name_,3600)
        return render_to_response('index.html',{'username':username})
    else:
        return render(request,'Login Failure.html')

def detail(request):
    if request.session.get("username") is None:
        return render_to_response("login.html",{'info':True})
    if request.method is not "POST":
        food_ = food.objects.filter(name = request.GET.get('foodname'))
        return render_to_response('detail.html',{'foods': food_})


def logout(request):
    del request.session['username']
    return render(request, 'index.html')

def _ini_(request):
    username = request.session.get('username')
    return render_to_response('index.html',{'username':username})

def searchresult_name(request):
    food_name = request.GET.get('food_name')
    food_ = food.objects.filter(name__contains = food_name)
    username = request.session.get('username')
    temp = {'foods': food_, 'username': username}
    return render_to_response('searchresult.html', {'temp': temp})

# def delete_by_name(request):
#

def deleteby_name(request):
    food_name = request.GET.get('foodname')
    food_name_list = food.objects.filter(name=food_name)
    food_name_list.delete()
    return render(request,'index.html')

def add_page(request):
    return render(request,'create.html')

# def add(request):
#     item = request.GET.get('itemName')
#     con = request.GET.get('country')
#     cate = request.GET.get('category')
#     ingr = request.GET.get('ingredients')
#     path = request.GET.get('picturePath')
#     try:
#         food.objects.create(name = item, country = con, category = cate, ingredient = ingr, pic_path = path)
#     except:
#         return HttpResponse("failed!So soory")
#     return render(request,'create2.html')
    # food.objects.filter(name=item)
    # food.objects.filter(country=con)
    # food.objects.filter(category=cate)
    # food.objects.filter(ingredient=ingr)
    # food.objects.filter(pic_path=path).update()
def update_render(request):
    retval = urllib.request.unquote(request.GET.get('foodname'))
    return render_to_response('update.html', {'foods':food.objects.filter(name = retval)})
def update(request):
    select = request.GET.get('foodname')
    item = request.GET.get('itemName')
    con = request.GET.get('country')
    cate = request.GET.get('category')
    ingr = request.GET.get('ingredients')
    path = request.GET.get('picturePath')
    food_list = food.objects.filter(name = select)

    # for a in food_list:
    #     return HttpResponse("size",a.name)
    if(item == ""):
        item = select
    if(con ==""):
        con = food_list[0].country
    if(cate ==""):
        cate = food_list[0].category
    if(ingr ==""):
        ingr = food_list[0].ingredient
    if(path ==""):
        path = food_list[0].pic_path
    food_list.update(name = item, country = con, category =cate, ingredient=ingr, pic_path = path)
    return render_to_response('update2.html',{'foods':food.objects.filter(name =item)})

class UserForm(forms.Form):
    foodname = forms.CharField()
    headImg = forms.FileField()

class Foodform(forms.Form):
    foodname = forms.CharField()
    countryname = forms.CharField()
    categoryname = forms.CharField()
    ingredientname = forms.CharField()
    spicy = forms.IntegerField();
    sweet = forms.IntegerField();
    salty = forms.IntegerField();
    headImg = forms.FileField()

def picture_add(request):
    if request.method == "POST":
        food_form = Foodform(request.POST,request.FILES)
        if food_form.is_valid():

            foodname = food_form.cleaned_data['foodname']
            countryname = food_form.cleaned_data['countryname']
            categoryname = food_form.cleaned_data['categoryname']
            ingredientname = food_form.cleaned_data['ingredientname']
            headImg = food_form.cleaned_data['headImg']
            spicy = food_form.cleaned_data['spicy']
            sweet = food_form.cleaned_data['sweet']
            salty = food_form.cleaned_data['salty']


            food_ = food()
            food_.name = foodname
            food_.spicy = spicy
            food_.sweet = sweet
            food_.salty = salty
            food_.country=countryname
            food_.category=categoryname
            food_.ingredient=ingredientname
            food_.headImg = headImg
            food_.save()

            return HttpResponse("good")
    else:
        food_form = Foodform()
    return render_to_response('create.html',{'food_form':food_form})

# def dislike(request):
#     food_ = food.objects.filter(name = request.GET.get("foodname"))
#     user_ = request.session.get("username")
#     stu.objects.filter()

class CommentForm(forms.Form):
    comment = forms.CharField()
    user = forms.CharField()
    name = forms.CharField()

def detail(request):
    if request.session.get("username") is None:
        return render_to_response("login.html",{'info':True})

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_ = comment_form.cleaned_data['comment']
            food_name_ = request.GET.get('foodname')
            username = request.session.get('username')
            comment__ = comment()
            comment__.name = food_name_
            comment__.context = comment_
            comment__.user = username
            comment__.save()
            return HttpResponse("good")
    else:
        food_ = food.objects.filter(name = request.GET.get('foodname'))
        comment_form_ =CommentForm()
        return render_to_response('detail.html',{'foods': food_,"comment":comment_form_})