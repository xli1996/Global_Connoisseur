from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponse
from cs411.models import stu
from cs411.models import food
from cs411.models import comment
from cs411.models import likelist
import numpy as np
from django.shortcuts import render_to_response
import urllib.request
from django import forms
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


def findremmendation(target_food):
    foodlist = food.objects.all().exclude(name = target_food.name)
    # print(foodlist.count())
    data_matrix = np.zeros( (foodlist.count() ,2) ,dtype=np.int)

    for i, fd in enumerate(foodlist):
        distance = np.power( fd.spicy - target_food.spicy,2) + np.power( fd.sweet - target_food.sweet,2) +np.power( fd.salty - target_food.salty,2)
        data_matrix[i][0] = distance
        print(i)
        data_matrix[i][1] = i
    # data_matrix.sort(axis=0)
    # print(data_matrix)
    data_matrix = data_matrix[np.lexsort(np.fliplr(data_matrix).T)]
    b = data_matrix[:3]
    # print("it is")
    return foodlist[int(b[0][1])],foodlist[int(b[1][1])],foodlist[int(b[2][1])]

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
        username = request.session.get('username')
        food_ = food.objects.filter(name = request.GET.get('foodname'))
        a,b,c = findremmendation(food_[0])
        print("distance  a "+str(a))
        print("distance  b "+str(b))
        print("distance  c "+str(c))
        comment_form_ = CommentForm()
        comments = comment.objects.filter(name = request.GET.get('foodname'))
        return render_to_response('detail.html', {'foods': food_, "comment":comment_form_, 'username': username, 'cs': comments,'one':a, 'two':b,'three':c})
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


def deleteby_name(request):
    food_name = request.GET.get('foodname')
    food_name_list = food.objects.filter(name=food_name)
    food_name_list.delete()
    return render(request,'index.html')

def add_page(request):
    return render(request,'create.html')


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


class Foodform(forms.Form):
    foodname = forms.CharField()
    countryname = forms.CharField()
    categoryname = forms.CharField()
    ingredientname = forms.CharField()
    spicy = forms.IntegerField()
    sweet = forms.IntegerField()
    salty = forms.IntegerField()
    headImg = forms.FileField()

class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(), )


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

def like(request):
    username = request.session.get("username")
    user_ = stu.objects.filter(user = username)
    if user_[0].num_like > 8:
        return HttpResponse("your likelist is full")
    elif likelist.objects.filter(user=username, name=request.GET.get('foodname')) != None:
        return HttpResponse("you 've already liked this meal")
    else:
        temp = user_[0].num_like+1
        user_.update(num_like = temp)
        # user_.update(num_like=temp)
        likelist_ = likelist()
        likelist_.name = request.GET.get('foodname')
        likelist_.user = username
        likelist_.save()
        return HttpResponse("good")