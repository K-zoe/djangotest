from django.shortcuts import render,redirect,get_object_or_404
from .models import regi_content,User_info
from .forms import RegForm,Index
from datetime import datetime
from datetime import date
from django.utils import timezone
from django.http import HttpResponse

from ipware import get_client_ip

from django.views.decorators.http import require_POST
from django.db.models import Q

from functools import reduce
from operator import and_

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger




now = datetime.today()
today = now.strftime('%Y-%m-%d %H:%M')

def frontpage(request):
    user_data = User_info.objects.all()


    if request.method == "POST":
        form = Index(request.POST)
        print("POST")
        

        if form.is_valid():

            if 'control_id' in form.cleaned_data and form.cleaned_data['control_id']:
                control_id = form.cleaned_data["control_id"]
            else:
                control_id = ""

            if 'f_day' in form.cleaned_data and form.cleaned_data['f_day']:
                f_day = form.cleaned_data["f_day"]
            else:
                f_day =""

            if 'e_day' in form.cleaned_data and form.cleaned_data['e_day']:
                e_day = form.cleaned_data["e_day"]
            else:
                e_day = ""

            if 'name_id' in form.cleaned_data and form.cleaned_data['name_id']:
                name_id = form.cleaned_data['name_id'].user_id
            else:
                name_id = "" # または適切なデフォルト値を設定

            if 'company_name' in form.cleaned_data and form.cleaned_data['company_name']:
                company_name =  form.cleaned_data["company_name"]
            else:
                company_name = ""

            if 'qa_contents' in form.cleaned_data and form.cleaned_data['qa_contents']:
                qa_contents = form.cleaned_data["qa_contents"].split()
                print(qa_contents)
            else:
                qa_contents = ["",""]

            a = form.cleaned_data["order_of_display"]

            print(a)
            regist_content = regi_content.objects.filter(
                                                Q(control_id__contains = control_id)&
                                                Q(first_time__icontains = f_day)&
                                                Q(name_id__contains = name_id)&
                                                Q(company_name__contains = company_name)&

                                                reduce(and_,[Q(q_contents__contains=q) | Q(a_contents__contains=q) for q in qa_contents])
                                                
                                                
                                                ).all().order_by("first_time")
            
            if a == "1":
                regists = regist_content.order_by("first_time")

            else:
                regists = regist_content.order_by("-first_time")

            paginator = Paginator(regists,10)
            page = request.POST.get("page")
            print(page)

            try:
                regist = paginator.page(page)
            except PageNotAnInteger:
                regist = paginator.page(1)
            except EmptyPage:
                regist = paginator.page(paginator.num_pages)



            return render(request, "helpdesktool/frontpage.html", {"regist": regist,"user_data":user_data,"form":form})
        else:
            print("バリデーション失敗")
    else:
        form = Index()
        print("GET通信")

    return render(request, "helpdesktool/frontpage.html", {"user_data":user_data,"form":form})

"""
def frontpage(request):
    user_data = User_info.objects.all()


    if request.method == "POST":
        form = Index(request.POST)
        print("POST")
        

        if form.is_valid():

            if 'control_id' in form.cleaned_data and form.cleaned_data['control_id']:
                control_id = form.cleaned_data["control_id"]
            else:
                control_id = ""

            if 'f_day' in form.cleaned_data and form.cleaned_data['f_day']:
                f_day = form.cleaned_data["f_day"]
            else:
                f_day =""

            if 'e_day' in form.cleaned_data and form.cleaned_data['e_day']:
                e_day = form.cleaned_data["e_day"]
            else:
                e_day = ""

            if 'name_id' in form.cleaned_data and form.cleaned_data['name_id']:
                name_id = form.cleaned_data['name_id'].user_id
            else:
                name_id = "" # または適切なデフォルト値を設定

            if 'company_name' in form.cleaned_data and form.cleaned_data['company_name']:
                company_name =  form.cleaned_data["company_name"]
            else:
                company_name = ""

            if 'qa_contents' in form.cleaned_data and form.cleaned_data['qa_contents']:
                qa_contents = form.cleaned_data["qa_contents"].split()
                print(qa_contents)
            else:
                qa_contents = ["",""]

            a = form.cleaned_data["order_of_display"]

            print(a)
            regist_content = regi_content.objects.filter(
                                                Q(control_id__contains = control_id)&
                                                Q(first_time__icontains = f_day)&
                                                Q(name_id__contains = name_id)&
                                                Q(company_name__contains = company_name)&

                                                reduce(and_,[Q(q_contents__contains=q) | Q(a_contents__contains=q) for q in qa_contents])
                                                
                                                
                                                ).all().order_by("first_time")
            
            if a == "1":
                regist = regist_content.order_by("first_time")

            else:
                regist = regist_content.order_by("-first_time")

            paginator = Paginator(regist,2)
            page = request.GET.get("page")

            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                posts = paginator.page(1)
            except EmptyPage:
                posts = paginator.page(paginator.num_pages)



            return render(request, "helpdesktool/frontpage.html", {"regist": regist,"user_data":user_data,"form":form})
        else:
            print("バリデーション失敗")
    else:
        form = Index()
        print("GET通信")

    return render(request, "helpdesktool/frontpage.html", {"user_data":user_data,"form":form})
    """


def create_form(request):
    if request.method == 'POST':

        form = RegForm(request.POST)

        if form.is_valid():

            f_day = form.cleaned_data['f_day']
            f_time = form.cleaned_data['f_time']
            first_time = datetime.combine(f_day, f_time)
            #終了日時   
            e_day = form.cleaned_data['e_day']
            e_time = form.cleaned_data['e_time']
            end_time = datetime.combine(e_day, e_time)
            #対応合計時間
            total_time = form.cleaned_data['total_time']
            #対応者ID
            name_id = form.cleaned_data['name_id'].user_id 
            #会社名
            company_name = form.cleaned_data['company_name']
            #問い合わせ内容
            q_contents = form.cleaned_data['q_contents']
            #回答内容
            a_contents = form.cleaned_data['a_contents']

            unsolved = form.cleaned_data['unsolved']
            print(unsolved)
        
            # データをデータベースに保存
            new_content=regi_content(
                                    first_time=first_time,
                                    end_time=end_time,
                                    total_time=total_time,
                                    name_id = name_id, 
                                    company_name=company_name,
                                    q_contents=q_contents,
                                    a_contents=a_contents,
                                    unsolved=unsolved,
                                    )
            new_content.save()

            return redirect(nothing)  # データ登録が成功した場合のページにリダイレクト

        else:
            print(form.errors)
    
    else:
        #ipアドレスの取得
        ip_add, second_ip = get_client_ip(request)

        print(ip_add)
        # ユーザーのIPアドレスに合致するUser_infoオブジェクトを取得
        user_infomation = User_info.objects.filter(user_ip=ip_add).first()

        # フォームの初期値としてuser_infoを設定
        if user_infomation:
            initial_id =  user_infomation
        
        else:
            initial_id = {}

        t_day = date.today()
        b = datetime.now().time()
        t_time = b.strftime('%H:%M')
        initial_data = {'f_day': t_day ,'f_time': t_time,'e_day': t_day , 'e_time': t_time , "name_id":initial_id}
        form = RegForm(initial=initial_data)

    return render(request, "helpdesktool/registration.html", {'form': form})



def edit(request, control_id):
    reg_edit = get_object_or_404(regi_content,control_id=control_id)

    # Djangoのデフォルトタイムゾーンを使用
    local_datetime = timezone.localtime(reg_edit.first_time)

    a_day = local_datetime.date()

    a_time = local_datetime.time()

    local_end_datetime = timezone.localtime(reg_edit.end_time)

    e_day = local_end_datetime.date()

    e_time = local_end_datetime.time()

    form = RegForm()
    if request.method == 'POST':
        form = RegForm(request.POST)

        if form.is_valid():
            f_day = form.cleaned_data['f_day']
            f_time = form.cleaned_data['f_time']
            first_time = datetime.combine(f_day, f_time)
            #終了日時   
            e_day = form.cleaned_data['e_day']
            e_time = form.cleaned_data['e_time']
            end_time = datetime.combine(e_day, e_time)
            #対応合計時間
            total_time = form.cleaned_data['total_time']
            #対応者ID
            name_id = form.cleaned_data['name_id'].user_id
            #会社名
            company_name = form.cleaned_data['company_name']
            #問い合わせ内容
            q_contents = form.cleaned_data['q_contents']
            #回答内容
            a_contents = form.cleaned_data['a_contents']

            unsolved = form.cleaned_data['unsolved']

            update_content=regi_content(
                                        control_id=control_id,
                                        first_time=first_time,
                                        end_time=end_time,
                                        total_time=total_time,
                                        name_id = name_id, 
                                        company_name=company_name,
                                        q_contents=q_contents,
                                        a_contents=a_contents,
                                        unsolved = unsolved,
                                    )
            update_content.save()

            return redirect(frontpage)

    else:
        form = RegForm({'f_day':a_day,'f_time':a_time,
                        'e_day':e_day,'e_time':e_time,
                        'total_time':reg_edit.total_time,
                        'name_id':reg_edit.name_id,
                        'company_name':reg_edit.company_name,
                        'q_contents':reg_edit.q_contents,
                        'a_contents':reg_edit.a_contents,
                        'unsolved':reg_edit.unsolved,
                        })
        

        return render(request, "helpdesktool/edit.html",{'form':form,"reg_edit":reg_edit})
    

def copy(request,control_id):
    reg_content = get_object_or_404(regi_content,control_id=control_id)
    form = RegForm()

    if request.method == 'POST':
        form = RegForm(request.POST)

        if form.is_valid():
            f_day = form.cleaned_data['f_day']
            f_time = form.cleaned_data['f_time']
            first_time = datetime.combine(f_day, f_time)
            #終了日時   
            e_day = form.cleaned_data['e_day']
            e_time = form.cleaned_data['e_time']
            end_time = datetime.combine(e_day, e_time)
            #対応合計時間
            total_time = form.cleaned_data['total_time']
            #対応者ID
            name_id = form.cleaned_data['name_id'].user_id
            #会社名
            company_name = form.cleaned_data['company_name']
            #問い合わせ内容
            q_contents = form.cleaned_data['q_contents']
            #回答内容
            a_contents = form.cleaned_data['a_contents']

            unsolved = form.cleaned_data['unsolved']

            copy_content=regi_content(
                                        first_time=first_time,
                                        end_time=end_time,
                                        total_time=total_time,
                                        name_id = name_id, 
                                        company_name=company_name,
                                        q_contents=q_contents,
                                        a_contents=a_contents,
                                        unsolved = unsolved,
                                    )
            copy_content.save()
            
            return redirect(frontpage)
    else:
        ip_add, second_ip = get_client_ip(request)

        print(ip_add)
        # ユーザーのIPアドレスに合致するUser_infoオブジェクトを取得
        user_infomation = User_info.objects.filter(user_ip=ip_add).first()

        # フォームの初期値としてuser_infoを設定
        if user_infomation:
            initial_id =  user_infomation
        
        else:
            initial_id = {}

        t_day = date.today()
        b = datetime.now().time()
        t_time = b.strftime('%H:%M')
        #ここから作成
        initial_data = {'f_day': t_day ,
                        'f_time': t_time,
                        'e_day': t_day , 
                        'e_time': t_time ,
                        "name_id":initial_id,
                        "q_contents":reg_content.q_contents,
                        "a_contents":reg_content.a_contents

                          }
        form = RegForm(initial=initial_data)

        return render(request,"helpdesktool/copy.html",{"form":form})



@require_POST
def delete_data(request, control_id):
    eg_content = get_object_or_404(regi_content,control_id=control_id)
    eg_content.delete()
    return redirect(frontpage)


def nothing(request):
    return render(request,"helpdesktool/nothing.html")




