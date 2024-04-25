from django.shortcuts import render, redirect
from crud.models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.


new_user = {}

def register_auth(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        user = User.objects.filter(username = username)
        if (user.exists()):
            messages.info(request, "Username is already taken. Try another one.")
            return redirect("/register/user-auth/")

        else:
            new_user["username"] = username
            new_user["email"] = email
            new_user["password"] = password

            # for a, b in new_user.items():
                # print(a, b)
            return redirect("/register/user-info/")

    return render(request, "register1.html")





def register_info(request):

    if new_user.get("username", "none") == "none":
        return redirect("/")

    if request.method == "POST":
        fullname = request.POST.get("fullname")
        age = request.POST.get("age")
        bio = request.POST.get("bio")
        sex = request.POST.get("sex")
        image = request.FILES.get("image")

        new_user["fullname"] = fullname
        new_user["age"] = age
        new_user["bio"] = bio
        new_user["sex"] = sex
        new_user["image"] = image

        # for a, b in new_user.items():
        #     print(a, b)
        
        user = User(username = new_user.get("username"),
                     email = new_user.get("email"))
        user.set_password(new_user.get("password"))
        user.save()

        user_info = UserProfile(user = user,
                                fullname = new_user.get("fullname"),
                                age = new_user.get("age"),
                                sex = new_user.get("sex"),
                                bio = new_user.get("bio"))
        if new_user.get("image") != None:
            user_info.image = new_user.get("image")
        user_info.save()

        db_pointer = DBPointer(db_pointer = 0, preference = 'a')
        db_pointer.user = user
        db_pointer.save()

        login(request, user)

        return redirect("/profile-page/")
    
    return render(request, "register2.html")



@login_required(login_url = "/login/")
def del_account(request):

    username = request.user
    if request.method == "POST":
        password = request.POST.get("password")
        user = authenticate(username = username, password = password)
        if user is None:
            messages.error(request, "Password is incorrect.")
            return redirect("/delete-account/")
        else:
            user.delete()
            return redirect("/login/")
    
    return render(request, "del_account.html")



def login_page(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not User.objects.filter(username = username).exists():
            messages.error(request, "Username doesn't exist.")
            return redirect("/login/")
        
        user = authenticate(username = username, password = password)
        if user is None:
            messages.error(request, "Password is incorrect.")
            return redirect("/login/")
        else:
            login(request, user)
            return redirect("/profile-page/")

    return render(request, "login.html")



@login_required(login_url = "/login/")
def logout_page(request):
    logout(request)
    return redirect("/login/")






def validate(id, have_seen):
    length = have_seen.count()
    lo = 0
    hi = length - 1
    while lo <= hi:
        mid = lo + (hi-lo) // 2
        if have_seen[mid].user_seen_id == id:
            return True
        elif have_seen[mid].user_seen_id < id:
            lo = mid + 1
        else:
            hi = mid - 1
    return False





@login_required(login_url = "/login/")
def profile_page(request):
    
    record = UserProfile.objects.filter(user__username = request.user)[0]
    user = {
        "fullname": record.fullname,
        "age": record.age,
        "sex": record.sex,
        "bio": record.bio,
        "image": record.image,
        "score": record.score
    }

    male_records = UserProfile.objects.filter(sex = "male")
    paginator_male = Paginator(male_records, 20)
    m_page_no = request.GET.get("mpage", 1)
    male_page_obj = paginator_male.get_page(m_page_no)

    female_records = UserProfile.objects.filter(sex = "female")
    paginator_female = Paginator(female_records, 20)
    f_page_no = request.GET.get("fpage", 1)
    female_page_obj = paginator_female.get_page(f_page_no)


    user["male_records"] = male_page_obj
    user["female_records"] = female_page_obj


    user["flag"] = False
    have_seen = UserSeen.objects.filter(user__username = request.user)
    user_prefer = DBPointer.objects.filter(user__username = request.user)[0]


    if user_prefer.preference == 'a':
        user_records = UserProfile.objects.all()
    elif user_prefer.preference == 'm':
        user_records = UserProfile.objects.filter(sex = "male")
    else:
        user_records = UserProfile.objects.filter(sex = "female")

    if request.GET.get("preference"):
        preference = request.GET.get("preference")
        
        if preference == "male":
            user_prefer.preference = "m"
            user_records = UserProfile.objects.filter(sex = "male")
        elif preference == "female":
            user_prefer.preference = "f"
            user_records = UserProfile.objects.filter(sex = "female")
        else:
            user_prefer.preference = "a"
            user_records = UserProfile.objects.all()
        user_prefer.save()

    user["prefer"] = user_prefer.preference

    length = user_records.count()

    CUR_POINTER = user_prefer.db_pointer
    CYCLES = 0

    while user["flag"] != True:

        if CUR_POINTER >= length:
            CUR_POINTER = 0

        if CUR_POINTER == user_prefer.db_pointer:
            CYCLES += 1
            if CYCLES >= 2:
                break
   

        cur_user = user_records[CUR_POINTER]
        # refering to same user
        same_user =  record.id == cur_user.id
           
        # current user has already seen this other user 
        if have_seen.exists():
            has_already_seen = validate(cur_user.id, have_seen)
        else:
            has_already_seen = False
            
        if same_user == False and has_already_seen == False:
            user["flag"] = True
            user["next_user_id"] = cur_user.id
            user["next_user_fn"] = cur_user.fullname
            user["next_user_age"] = cur_user.age
            user["next_user_sex"] = cur_user.sex
            user["next_user_bio"] = cur_user.bio
            user["next_user_img"] = cur_user.image
            break

        CUR_POINTER = 1 + CUR_POINTER
    
    user_prefer.db_pointer = int(CUR_POINTER)
    user_prefer.save()

    return render(request, "user_page.html", context=user)





@login_required(login_url = "/login/")
def update_page(request):

    record = UserProfile.objects.filter(user__username = request.user)[0]

    user = {
        "fullname": record.fullname,
        "age": record.age,
        "sex": record.sex,
        "bio": record.bio,
        "image": record.image
    }


    if request.method == "POST":
        record.fullname = request.POST.get("fullname")
        record.age = request.POST.get("age")
        record.sex = request.POST.get("sex")
        record.bio = request.POST.get("bio")

        if request.FILES.get("image") != None:
            record.image = request.FILES.get("image")
        
        record.save()
        return redirect("/profile-page/")

    return render(request, "update_page.html", context=user)





@login_required(login_url = "/login/")
def smash_user(request, id):
    
    cur_user = User.objects.filter(username = request.user)[0]

    smashed_user = UserProfile.objects.filter(id = id)[0]
    smashed_user.score += 1
    smashed_user.save()

    record = UserSeen(user_seen_id = id)
    record.user = cur_user
    record.save()
  

    return redirect("/profile-page/")




@login_required(login_url = "/login/")
def pass_user(request, id):

    cur_user = User.objects.filter(username = request.user)[0]
    
    record = UserSeen(user_seen_id = id)
    record.user = cur_user
    record.save()


    return redirect("/profile-page/")




# ----------------------------------------------------------------------------------------------------






























# def user_profile(request):
#     if request.method == "POST":
#         fullname = request.POST.get("fullname")
#         age = request.POST.get("age")
#         bio = request.POST.get("bio")
#         # print("asd")
#         image = request.FILES.get("picture")
#         # print("lala")
#         # print(fullname)
#         # print(age)
#         # print(bio)
#         # print(image)
#         data = {
#             "fullname": fullname,
#             "age": age,
#             "bio": bio
#         }
#         if image != None:
#             data["image"] = image
#         new_record = UserProfile(**data)
#         new_record.save()
#         return redirect("/user-profile/")
    
#     records = UserProfile.objects.all()

#     if request.GET.get("key"):
#         key = request.GET.get("key")
#         records = UserProfile.objects.filter(fullname__icontains = key)
#     return render(request, "user_profile.html", context={"records": records})


# def increase_score(request, id):
#     user = UserProfile.objects.get(id = id)
#     user.score += 10
#     user.save()
#     return redirect("/user-profile/")

# def delete_user(request, id):
#     UserProfile.objects.get(id = id).delete()
#     return redirect("/user-profile/")


# def update_user(request, id):
#     record = UserProfile.objects.get(id = id)
#     if request.method == "POST":
#         fullname = request.POST.get("fullname")
#         age = request.POST.get("age")
#         bio = request.POST.get("bio")
#         image = request.FILES.get("picture")
        
#         record.fullname = fullname
#         record.age = age
#         record.bio = bio

#         if image != None:
#             record.image = image
#         record.save()
#         return redirect("/user-profile/")

    
#     return render(request, "update.html", context= {"record": record})