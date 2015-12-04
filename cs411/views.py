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
from django.core.paginator import Paginator, InvalidPage, EmptyPage
# Create your views here.
def signup(request):
    return render(request,'signup.html')

def log(request):
    return render(request,'login.html')
def get_data(request):
    try:
        user_name_ = request.GET.get('Username')
        password_ = request.GET.get('Password')
        stu.objects.create(user = user_name_, password=password_, spicy=15, sweet=15, salty=15)
    except IntegrityError as e:
        return HttpResponse('user already existed')

    return _ini_(request)

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
            try:
                comment__.save()

            except:
                return render(request,'exception.html')
        username = request.session.get('username')
        food_ = food.objects.filter(name = request.GET.get('foodname'))
        a,b,c = findremmendation(food_[0])
        print("distance  a "+str(a))
        print("distance  b "+str(b))
        print("distance  c "+str(c))
        comment_form_ = CommentForm()
        comments = comment.objects.filter(name = request.GET.get('foodname'))
        return render_to_response('detail.html', {'foods': food_, "comment":comment_form_, 'username': username, 'cs': comments,'one':a, 'two':b,'three':c})
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
    food_ = food.objects.filter(name__icontains = food_name)
    username = request.session.get('username')
    page_size = 5
    paginator = Paginator(food_, page_size)
    try:
        page = int(request.GET.get('page','1'))
    except:
        page = 1
    try:
        food_page = paginator.page(page)
    except:
        food_page = paginator.page(paginator.num_pages)

    return render_to_response('searchresult.html', {'food_pages': food_page, 'username':username})


def deleteby_name(request):
    if request.session.get("username") is None:
        return render_to_response("login.html",{'info':True})
    food_name = request.GET.get('foodname')
    food_name_list = food.objects.filter(name=food_name)
    food_name_list.delete()
    return render(request,'index.html')

def add_page(request):
    if request.session.get("username") is None:
        return render_to_response("login.html",{'info':True})
    return render(request,'create.html')


def update_render(request):
    if request.session.get("username") is None:
        return render_to_response("login.html",{'info':True})
    retval = urllib.request.unquote(request.GET.get('foodname'))
    return render_to_response('update.html', {'foods':food.objects.filter(name = retval)})

def update(request):
    select = request.GET.get('foodname')
    item = request.GET.get('itemName')
    con = request.GET.get('country')
    cate = request.GET.get('category')
    ingr = request.GET.get('ingredients')
    food_list = food.objects.filter(name = select)

    if(item == ""):
        item = select
    if(con ==""):
        con = food_list[0].country
    if(cate ==""):
        cate = food_list[0].category
    if(ingr ==""):
        ingr = food_list[0].ingredient

    food_list.update(name = item, country = con, category =cate, ingredient=ingr)
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
    username = request.session.get('username')

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
            food_.num_like = 0
            food_.save()
            print("sdfds")
            return _ini_(request)
    else:
        food_form = Foodform()
    return render_to_response('create.html',{'food_form':food_form,'username': username})

from django.http import HttpResponseRedirect
def like(request):
    username = request.session.get("username")
    user_ = stu.objects.filter(user = username)
    if user_[0].num_like > 8:
        return HttpResponse("your likelist is full")
    elif len(likelist.objects.filter(user=username, name=request.GET.get('foodname'))) > 0:
        return render(request,'dialogue.html')
    else:
        temp = user_[0].num_like+1
        user_.update(num_like = temp)
        food_ = food.objects.filter(name=request.GET.get('foodname'))
        tempf = food_[0].num_like+1
        food_.update(num_like=tempf)
        food_ = food.objects.filter(name=request.GET.get('foodname'))[0]
        # user_.update(num_like=temp)
        likelist_ = likelist()
        likelist_.name = request.GET.get('foodname')
        likelist_.user = username
        stu_ = stu.objects.filter(user = username)[0]

        spicy = (9 * stu_.spicy/10 + food_.spicy * 1)/10 * 10
        salty = (9 * stu_.salty/10 + food_.salty * 1)/10 * 10
        sweet = (9 * stu_.sweet/10 + food_.sweet * 1)/10 * 10
        user_.update(salty = salty
        ,sweet = sweet
        ,spicy = spicy)
        likelist_.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

def dislike(request):
    username = request.session.get("username")
    like_ = likelist.objects.filter(user = username,name=request.GET.get('foodname'))
    if len(like_) == 0:
        user_ = stu.objects.filter(user = username)
        food_ = food.objects.filter(name = request.GET.get('foodname'))
        food_ = food_[0]
        stu_ = stu.objects.filter(user = username)[0]
        sp = food_.spicy
        sa = food_.salty
        sw = food_.sweet
        spicy = (stu_.spicy*10/9 - sp * 1)/10 * 10
        salty = (stu_.salty*10/9 - sa * 1)/10 * 10
        sweet = (stu_.sweet*10/9 - sw * 1)/10 * 10
        user_.update(salty = salty
        ,sweet = sweet
        ,spicy = spicy)
        return render(request,"dislike_dialogue.html")
    else:
        user_ = stu.objects.filter(user = username)
        food_ = food.objects.filter(name = request.GET.get('foodname'))
        food__ = food_[0]
        stu_ = stu.objects.filter(user = username)[0]
        sp = food__.spicy
        sa = food__.salty
        sw = food__.sweet
        spicy = (stu_.spicy*10/9 - sp * 1)/10 * 10
        salty = (stu_.salty*10/9 - sa * 1)/10 * 10
        sweet = (stu_.sweet*10/9 - sw * 1)/10 * 10
        num_likeu = stu_.num_like-1
        num_likef = food__.num_like-1
        user_.update(salty = salty
        ,sweet = sweet
        ,spicy = spicy,num_like=num_likeu)
        food_.update(num_like = num_likef)
        food_name = like_[0]
        food_name_list = likelist.objects.filter(name=food_name, user = username)
        food_name_list.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))


def findremmendation2(sp,sa,sw):
    print('findremmendation2')
    foodlist = food.objects.all()
    # print(foodlist.count())
    data_matrix = np.zeros( (foodlist.count() ,2) ,dtype=np.int)

    for i, fd in enumerate(foodlist):
        distance = np.power( fd.spicy - sp/10,2) + np.power( fd.sweet - sw/10,2) +np.power( fd.salty -sa/10,2)
        data_matrix[i][0] = distance
        print(i)
        data_matrix[i][1] = i
    # data_matrix.sort(axis=0)
    # print(data_matrix)
    data_matrix = data_matrix[np.lexsort(np.fliplr(data_matrix).T)]
    b = data_matrix[:3]
    # print("it is")
    return foodlist[int(b[0][1])],foodlist[int(b[1][1])],foodlist[int(b[2][1])]

def profile(request):
    if request.session.get("username") is None:
        return render_to_response("login.html",{'info':True})
    username = request.session.get("username")
    food_ = likelist.objects.filter(user = username)
    food_ = [ food.objects.filter(name = foooo.name)[0] for foooo in food_  ]
    print(food_)
    page_size = 5
    paginator = Paginator(food_, page_size)
    try:
        page = int(request.GET.get('page','1'))
    except:
        page = 1
    try:
        food_page = paginator.page(page)
    except:
        food_page = paginator.page(paginator.num_pages)
    stu_ = stu.objects.filter(user = username)[0]
    a,b,c = findremmendation2(stu_.spicy,stu_.salty,stu_.sweet)
    return render_to_response('profile.html', {'food_pages': food_page, 'username':username,'one':a, 'two':b,'three':c})

def rank(request):
    if request.session.get("username") is None:
        return render_to_response("login.html",{'info':True})
    foodlist = food.objects.all()
    data_matrix = np.zeros( (foodlist.count() ,2) ,dtype=np.int)
    for i, fd in enumerate(foodlist):
        # distance = fd.num_like
        data_matrix[i][0] = fd.num_like
        print(i)
        data_matrix[i][1] = i
    # data_matrix.sort(axis=0)
    # print(data_matrix)
    data_matrix = data_matrix[np.lexsort(np.fliplr(data_matrix).T)]
    print(data_matrix.shape)
    return [  foodlist[int(data_matrix[i][1])] for i in range(data_matrix.shape[0])   ]

def ranking(request):
    tuple_ = rank(request)
    a=tuple_[0]
    b=tuple_[1]
    c=tuple_[2]
    rest = tuple_[3:9]
    # print(a.name)
    # print(b.name)
    # print(c.name)
    return render(request,'rankkk.html',{'a':a, 'b':b,'c':c,'rest':rest})

def contact(request):
    username = request.session.get("username")
    return render_to_response('contact.html', {'username': username})