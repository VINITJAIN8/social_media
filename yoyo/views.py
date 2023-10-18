from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile,User,Post,Comment,LikePost,Connection

def front_page(request):
    return render(request,'base.html')



@login_required
def index(request):
    post=Post.objects.all()
    return render(request,'index.html',{'post':post}) 


@login_required
def delete_post(request,id):
    post=Post.objects.get(id=id)
    
    check_post=Post.objects.filter(id=id,user=request.user.id)
    if check_post:
        post.delete()
        return HttpResponse(("<h2>Post deleted Successfully</h2>"))
    return HttpResponse("<h2>Sorry You Cant delete the post</h2>") 
    # return redirect('index')  

    
def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                #create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model)
                new_profile.save()
                return redirect('signin')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
        
    else:
        return render(request, 'signup.html')

def signin(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            # return render(request,'profile.html')
            return redirect('create_profile')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')

    else:
        return render(request, 'signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def upload(request):
    if request.method=="POST":
        # user=request.user.username
        # image=request.FILES.get('image_upload')
        caption=request.POST['caption']
        new_profile = Profile.objects.get(user_id = request.user.id)
        print(new_profile)
        # new_p = new_profile.user_id
        new_post=Post(user_id = new_profile.id,caption=caption)
        new_post.save()
        return render(request,'upload_post.html')
    else:
        return render(request,'upload_post.html')   

@login_required(login_url='signin')
def do_comment(request,id):
    post=get_object_or_404(Post,id=id)
    comment=Comment.objects.filter(post_commented=id)
    if not comment:
        return HttpResponse('comment not found')
    return render(request, 'comment.html', {'comment': comment})

# this is not working
@login_required(login_url='signin')
def delete_comment(request,id):
    del_comment=Comment.objects.get(id=id)
    del_comment.delete()
    return redirect('index')

@login_required(login_url='signin')
def add_comment(request,id):
    if request.method=='POST':
        post=Post.objects.get(id=id)
        user=User.objects.get(id=request.user.id)
        content=request.POST['content']
        cmnt=Comment(post_commented=post,content=content,user_commented=user)
        cmnt.save()
        
        return HttpResponse('comment added sucessfully')
    return HttpResponse('Coment show')


@login_required(login_url='signin')
def create_profile(request):
    check_user=Profile.objects.filter(user=request.user.id)
    print(check_user)

    if check_user.exists():
        return redirect('index')
    
    if request.method=='POST':

        # we need value from the form 
        # then se have to save it to profile model
        bio = request.POST['bio']
        location = request.POST['location']
        work = request.POST['work']
        relationship = request.POST['relationship']
        dob = request.POST['dob']
        contact_no = request.POST['contact_no']
        profile=Profile(user=request.user,bio=bio,location=location,work=work,relationship=relationship,dob=dob,contact_no=contact_no)
        if profile is not None:
            profile.save()
            return render(request,'create_profile.html')
    else:
        return render(request,'create_profile.html') 
    
@login_required(login_url='signin')
def edit_profile(request):
    profile = Profile.objects.filter(user=request.user.id).first()
    if not profile:
        # Handle the case where the profile doesn't exist
        return HttpResponse('Profile does not exist')

    if request.method=='POST':
        bio = request.POST['bio']
        location = request.POST['location']
        work = request.POST['work']
        relationship = request.POST['relationship']
        dob = request.POST['dob']
        contact_no = request.POST['contact_no']

        profile.bio = bio
        profile.location = location
        profile.work = work
        profile.relationship = relationship
        profile.dob = dob
        profile.contact_no = contact_no
        profile.save()
        return HttpResponse('successfully updated')
    else:
        return render(request,'edit_profile.html') 
    
@login_required(login_url='signin')
def like_post(request,id):
    print(id)
    post=Post.objects.get(id=id)
    print(post)
    user=User.objects.get(id=request.user.id)
    like_post=LikePost.objects.filter(post_id=id,username=user).exists()
    if like_post:
        return HttpResponse('already liked')
    new_like=LikePost(post_id=post,username=user)
    new_like.save()
    return redirect('index')

@login_required(login_url='signin')
def see_who_liked(request,id):
    people_liked=LikePost.objects.filter(post_id=id)
    counts=LikePost.objects.filter(post_id=id).count()
    return render(request,'like.html',{'people_liked':people_liked,'counts':counts})

@login_required(login_url='signin')
def del_like(request,id):
    ins=LikePost.objects.filter(post_id=id,username=request.user.id)
    if ins:
        ins.delete()
        return HttpResponse('Disliked')
    return HttpResponse('not liked yet')

@login_required(login_url='signin')
def logout_user(request):
    logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def list_connection(request):
    user=request.user
    users=User.objects.exclude(username=user)
    print(users)
    connected=Connection.objects.all()
    print(connected)
    return render(request,'connection.html',{'users':users})


@login_required(login_url='signin')
def est_connection(request,id):
    if request.method=='POST':
        user=User.objects.get(id=request.user.id)
        connect=User.objects.get(id=id)
        connect_exists=Connection.objects.filter(user=user,follow_list=connect)
        if connect_exists:
            return HttpResponse('already exits')
        con=Connection(user=user,follow_list=connect)
        print(con)
        con.save()
        return redirect('list_connection')
    else:
        return HttpResponse('couldnt')

@login_required(login_url='signin')
def my_connected_list(request):
    my_list=Connection.objects.filter(user=request.user.id)
    return render(request,'my_connected_list.html',{'my_list':my_list})

    
    
@login_required(login_url='signin')
def del_connection(request,id):
    print(id)
    con=Connection.objects.filter(id=id)
    print(con)
    if con:
        con.delete()
        return redirect('my_connected_list')
    else:
        return HttpResponse('couldnt')