from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Teacher_login_informa, Student_login_informatn, store_email_teach_new, store_email_stu_new, Student_courses_with_Teacher_name, Grade_Student, Teacher_Assignment_upload_File, Student_Submit_Assignment_pro, Assignment_Comments
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import authenticate, login, logout
from .forms import chg_pass, chg_pass_stu
from django.core.files.storage import FileSystemStorage
from .templatetags import get_dict




def index(request):

    return render(request, 'index.html')


def login_func(request):
    if request.method == 'POST':
        log_ID = request.POST['log_ID']
        log_password = request.POST['log_password']

        stu_matching= Student_login_informatn.matching_loging_stu(log_ID)
        teacher_matching= Teacher_login_informa.matching_loging_teacher(log_ID)

        if stu_matching:

            if stu_matching.Student_pass == log_password:
                request.session['Stu_id'] = stu_matching.Student_ID
                request.session['Stu_name'] = stu_matching.Student_Name

                return redirect('index')

            else:
                messages.error(request, "Password is incorrect")
                return render(request, 'login.html')

        elif teacher_matching:
            if teacher_matching.Teacher_pass == log_password:
                request.session['Teacher_id'] = teacher_matching.Teacher_ID
                request.session['Teacher_name'] = teacher_matching.Teacher_Name
                request.session['Teacher_pass'] = teacher_matching.Teacher_pass

                return redirect('index')

            else:
                messages.error(request, "Password is incorrect")
                return render(request, 'login.html')

        else:
            messages.error(request, "User ID is incorrect")
            return render(request, 'login.html')

    else:
        return render(request, 'login.html')


def profile(request):
    if request.method == "POST":
        get_id_show= request.POST.get('get_id_show')


        check_user_id = store_email_teach_new.matching_show_teacher(get_id_show)
        check_user_id_stu = store_email_stu_new.matching_show_stu(get_id_show)

        if check_user_id:
            profile_email = check_user_id.Teacher_email
            d1 = {'profile_email': profile_email}
            return render(request, 'profile.html', d1)

        elif check_user_id_stu:
            profile_email = check_user_id_stu.Student_email
            d1 = {'profile_email': profile_email}
            return render(request, 'profile.html', d1)

        else:

            no_email="No Email Added !! Go to Settings to add email or click here."
            d2 = {'no_email': no_email}
            return render(request, 'profile.html', d2)
    else:
        return render(request, 'profile.html')


def settings(request):
    if request.method == "POST":
        # get some values
        add_email_user_id = request.POST.get('add_email_user_id')
        add_email_user_pass = request.POST.get('add_email_user_pass')
        add_email_user_email = request.POST.get('add_email_user_email')

        # get login userID
        user_id_uniq = request.POST.get('user_id_uniq')

        # if main password and given passwords are same
        if user_id_uniq==add_email_user_id:
            # chech if already added a email
            check_email = store_email_teach_new.matching_show_teacher(add_email_user_id)

            check_email_stu = store_email_stu_new.matching_show_stu(add_email_user_id)

            if check_email:
                messages.error(request, "Oh !! You Already Added your Email !! No need to add email. Go to your Profile. ")
                return redirect('settings')

            elif check_email_stu:
                messages.error(request,"Oh !! You Already Added your Email !! No need to add email. Go to your Profile. ")
                return redirect('settings')

            else:
                # matching user id to login informations
                teacher_matching_add_email = Teacher_login_informa.matching_loging_teacher(add_email_user_id)
                stu_matching_ID = Student_login_informatn.matching_loging_stu(add_email_user_id)

                if teacher_matching_add_email:
                    # matching email to login info
                    if teacher_matching_add_email.Teacher_pass == add_email_user_pass:

                        storing_email_teach = store_email_teach_new(Teacher_ID=add_email_user_id,
                                                                    Teacher_email=add_email_user_email)
                        storing_email_teach.save()
                        messages.success(request, "Weldone, Your Email has been successfully added to your profile !!")
                        return redirect('settings')

                    else:
                        messages.error(request, "Password is incorrect")
                        return render(request, 'settings.html')

                elif stu_matching_ID:
                    if stu_matching_ID.Student_pass == add_email_user_pass:

                        storing_email_stud = store_email_stu_new(Student_ID=add_email_user_id,
                                                                    Student_email=add_email_user_email)
                        storing_email_stud.save()
                        messages.success(request, "Weldone, Your Email has been successfully added to your profile !!")
                        return redirect('settings')

                    else:
                        messages.error(request, "Password is incorrect")
                        return render(request, 'settings.html')

                else:
                    messages.error(request, "Your User ID is Invalid !! ")
                    return render(request, 'settings.html')

        else:
            messages.error(request, "This is not Your ID !! ")
            return render(request, 'settings.html')

    else:
        return render(request, 'settings.html')


def check_user(request):
    if request.method=="POST":
        get_id_teach= request.POST.get('get_id_teach')
        context = {'get_id_teach':get_id_teach}
        return render(request, 'check_user.html', context)
    else:
        return redirect('/')


def check_user_password(request):
    if request.method=="POST":
        check_id=request.POST.get('check_id')
        check_pass=request.POST.get('check_pass')

        get_id_teacher=request.POST.get('get_id_teacher')
        # get_id_student=request.POST.get('get_id_student')


        get_pass_teach = Teacher_login_informa.objects.get(Teacher_ID=get_id_teacher)
        teacher_pass_match = get_pass_teach.Teacher_pass

        if get_id_teacher==check_id:
            if check_pass==teacher_pass_match:
                return render(request, 'change_pass.html')
            else:
                messages.error(request, "Your Password is Incorrect !!")
                return redirect('/')

        else:
            messages.error(request, "It is not Your User ID or Valid User ID !!")
            return redirect('/')

    else:
        return redirect('/')


def check_user_password_student(request):
    if request.method=="POST":
        check_id=request.POST.get('check_id')
        check_pass=request.POST.get('check_pass')

        get_id_student=request.POST.get('get_id_student')
        print(check_id, check_pass, get_id_student)

        get_pass_stu = Student_login_informatn.objects.get(Student_ID=get_id_student)
        teacher_pass_match = get_pass_stu.Student_pass

        if get_id_student==check_id:
            if check_pass==teacher_pass_match:
                return render(request, 'change_pass_student.html')
            else:
                messages.error(request, "Your Password is Incorrect !!")
                return redirect('/')

        else:
            messages.error(request, "It is not Your User ID or Valid User ID !!")
            return redirect('/')

    else:
        return redirect('/')


def check_user_student(request):
    if request.method=="POST":
        get_id_stu= request.POST.get('get_id_stu')
        print(get_id_stu)
        context = {'get_id_stu':get_id_stu}
        return render(request, 'check_user_stu.html', context)
    else:
        return redirect('/')



def update_change_password(request, pk):
    teach = Teacher_login_informa.objects.get(Teacher_ID=pk)

    form = chg_pass(instance=teach)

    if request.method == 'POST':
        form = chg_pass(request.POST, instance=teach)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request, 'change_password.html', context)


def update_change_password_stu(request, pk):
    stu_pas_ch = Student_login_informatn.objects.get(Student_ID=pk)

    form = chg_pass_stu(instance=stu_pas_ch)

    if request.method == 'POST':
        form = chg_pass_stu(request.POST, instance=stu_pas_ch)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request, 'change_password.html', context)


def stu_course(request):
    if request.method == "POST":
        stu_course_id=request.POST.get('stu_course_id')
        get_course_name = Student_login_informatn.objects.get(Student_ID=stu_course_id)
        get_course_name_id = get_course_name.id
        get_student_name = get_course_name.Student_Name
        get_student_course = get_course_name.course
        # print(get_student_course)

        get_grade_of_my_grade = Grade_Student.objects.filter(Student_ID=stu_course_id)
        # print(get_grade_of_my_grade)

        get_submit_assignment_stu = Student_Submit_Assignment_pro.objects.filter(Student_ID=stu_course_id)
        # print(get_submit_assignment_stu)

        stu_id_page_username = get_course_name.course
        # print(stu_id_page_username)

        teacher_id_course = Student_courses_with_Teacher_name.objects.get(course=stu_id_page_username)
        # print(teacher_id_course.Teacher_ID)
        # print(teacher_id_course.id)

        get_id_course_stud = teacher_id_course.id

        get_assignmet_for_stu = Teacher_Assignment_upload_File.objects.filter(course=stu_id_page_username)
        # print(get_assignmet_for_stu)

        teacher_ns_interface = teacher_id_course.Teacher_ID

        teacher_name_course = Teacher_login_informa.objects.get(Teacher_ID=teacher_ns_interface)
        # print(teacher_name_course.Teacher_Name)

        teacher_ns_interface12 = teacher_name_course.Teacher_Name

        #comments
        get_assignment12 = Teacher_Assignment_upload_File.objects.filter(course=get_student_course).first()
        print(get_assignment12)

        get_all_comments = Assignment_Comments.objects.filter(post=get_assignment12, parent=None)
        replies = Assignment_Comments.objects.filter(post=get_assignment12).exclude(parent=None)
        print(get_all_comments, replies)

        repDict = {}
        for reply in replies:
            if reply.parent.serial_no not in repDict.keys():
                repDict[reply.parent.serial_no] = [reply]

            else:
                repDict[reply.parent.serial_no].append(reply)

        context = {'stu_id_page_username':stu_id_page_username, 'teacher_ns_interface': teacher_ns_interface12, 'get_assignmet_for_stu': get_assignmet_for_stu, 'get_submit_assignment_stu': get_submit_assignment_stu, 'get_grade_of_my_grade':get_grade_of_my_grade, 'stu_course_id':stu_course_id, 'get_student_name':get_student_name, 'get_all_comments':get_all_comments, 'get_assignment12':get_assignment12, 'repDict':repDict}

        return render(request, 'stu_course.html', context)

    else:
        return redirect('/')


def sir_course(request):
    if request.method == "POST":
        teach_course_id=request.POST.get('teach_course_id')
        # print(teach_course_id)

        get_id_teach = Teacher_login_informa.objects.get(Teacher_ID=teach_course_id)
        # print(get_id_teach.id)

        get_id_teach_id = get_id_teach.id

        get_course_name_th = Student_courses_with_Teacher_name.objects.filter(Teacher_ID=get_id_teach_id)
        # print(get_course_name_th)

        context1 = {'get_course_name_t_cours':get_course_name_th}

        return render(request, 'teacher_page.html', context1)

    else:
        return redirect('/')


def assignment_page(request):
    if request.method == "POST":
        get_course_name = request.POST.get('get_course_name')
        # print(get_course_name)

        get_id_course = Student_courses_with_Teacher_name.objects.get(course=get_course_name)
        # print(get_id_course.id)

        get_id_course_id = get_id_course.id


        get_id_course_id_teach_id = get_id_course.Teacher_ID
        # print(get_id_course_id_teach_id)

        get_id_course_id_teach_name = Teacher_login_informa.objects.get(Teacher_ID=get_id_course_id_teach_id)
        # print(get_id_course_id_teach_name)

        get_grade_all_stu_course = Grade_Student.objects.filter(course=get_id_course)
        # print(get_grade_all_stu_course)


        get_id_course_course_name = get_id_course.course
        # print(get_id_course_course_name)

        stu_course_all_stu = Student_login_informatn.objects.filter(course=get_id_course_id)
        # print(stu_course_all_stu)

        get_assignment = Teacher_Assignment_upload_File.objects.filter(course=get_course_name)
        # print(get_assignment)

        get_submit_ass_fs_tt = Student_Submit_Assignment_pro.objects.filter(course=get_course_name)
        # print(get_submit_ass_fs_tt)


        get_assignment12 = Teacher_Assignment_upload_File.objects.filter(course=get_course_name).first()
        print(get_assignment12)

        # get_assignment12_total_grade=get_assignment12.Out_Of_Grade

        get_all_comments = Assignment_Comments.objects.filter(post=get_assignment12, parent=None)
        replies = Assignment_Comments.objects.filter(post=get_assignment12).exclude(parent=None)
        print(get_all_comments, replies)

        repDict = {}
        for reply in replies:
            if reply.parent.serial_no not in repDict.keys():
                repDict[reply.parent.serial_no] = [reply]

            else:
                repDict[reply.parent.serial_no].append(reply)


        context2 = {'stu_course_all_stu':stu_course_all_stu, 'get_assignment':get_assignment, 'get_id_course_course_name': get_id_course_course_name, 'get_submit_ass_fs_tt':get_submit_ass_fs_tt, 'get_grade_all_stu_course':get_grade_all_stu_course, 'get_course_name':get_course_name, 'get_id_course_id_teach_name':get_id_course_id_teach_name, 'get_all_comments':get_all_comments, 'get_assignment12':get_assignment12, 'repDict':repDict}

        return render(request, 'assignment_page.html', context2)

    else:
        return redirect('/')


def grading_page(request):
    if request.method == "POST":
        stu_id_grade = request.POST.get('stu_id_grade')
        stu_course_grade = request.POST.get('stu_course_grade')
        stu_ass_name_grade = request.POST.get('stu_ass_name_grade')
        # print(stu_id_grade, stu_course_grade, stu_ass_name_grade)

        stu_total_grade=request.POST.get('stu_total_grade')
        print(stu_total_grade)

        dict1122 = {'stu_id_grade':stu_id_grade, 'stu_course_grade': stu_course_grade, 'stu_ass_name_grade':stu_ass_name_grade, 'stu_total_grade':stu_total_grade}

        return render(request, 'grading_page.html', dict1122)
    else:
        return redirect('/')


def grading_submit(request):
    if request.method=="POST":

        grade_field_stu_id = request.POST.get('grade_field_stu_id')
        grade_field_course_name = request.POST.get('grade_field_course_name')
        grade_field_assignment_name = request.POST.get('grade_field_assignment_name')
        grade_field = request.POST.get('grade_field')
        out_grade_filed = request.POST.get('out_grade_filed')

        print(grade_field, grade_field_stu_id, grade_field_course_name, grade_field_assignment_name, out_grade_filed)

        Grade_Student_data= Grade_Student (Student_ID = grade_field_stu_id,course = grade_field_course_name, Assignment_name = grade_field_assignment_name, Grade = grade_field, Out_Of_Grade = out_grade_filed)

        Grade_Student_data.save()

        messages.success(request, "You Successfully Grade a student!")

        return redirect('assignment_page')
    else:
        return redirect('/')



def add_assignment(request):
    if request.method=="POST":

        get_course_name_cors = request.POST.get('get_course_name_cors')
        print(get_course_name_cors)

        context2 = {'get_course_name_cors': get_course_name_cors}
        return render(request, 'add_assignment.html', context2)

    else:
        return redirect('/')



def add_assignment_up_page(request):
    if request.method=="POST":
        attachment_ass_up = request.FILES['attachment_ass_up']
        # print(attachment_ass_up.name)
        # print(attachment_ass_up.size)
        fs = FileSystemStorage()
        filename = fs.save(attachment_ass_up.name, attachment_ass_up)
        url_file = fs.url(filename)
        # print(url_file)

        ass_name = request.POST.get('ass_name')
        course_ass_up = request.POST.get('course_ass_up')
        date_ass_up = request.POST.get('date_ass_up')
        due_date_ass_up = request.POST.get('due_date_ass_up')
        title_ass_up = request.POST.get('title_ass_up')
        details_ass_up = request.POST.get('details_ass_up')

        resource_ass_up = request.POST.get('resource_ass_up')
        posts_ass_up = request.POST.get('posts_ass_up')
        grade_ass_up = request.POST.get('grade_ass_up')


        print(ass_name, course_ass_up, date_ass_up, due_date_ass_up, title_ass_up,  details_ass_up, attachment_ass_up, resource_ass_up, posts_ass_up)

        Teacher_Assignment_upload_file_data = Teacher_Assignment_upload_File(Assignment_name=ass_name, course=course_ass_up, date=date_ass_up, due_date=due_date_ass_up, title=title_ass_up, Details=details_ass_up, attachment=url_file, resource=resource_ass_up, posts=posts_ass_up, Out_Of_Grade=grade_ass_up)

        Teacher_Assignment_upload_file_data.save()
        messages.success(request, "Successfully added Assignment")


        return redirect('/')


def submit_assignment_student(request):
    if request.method == "POST":
        ass_name_stu_submit1 = request.POST.get('ass_name_stu_submit1')
        cor_name_stu_submit1 = request.POST.get('cor_name_stu_submit1')
        stu_id_stu_submit1 = request.POST.get('stu_id_stu_submit1')
        print(ass_name_stu_submit1, cor_name_stu_submit1, stu_id_stu_submit1)

        attachment_ass_sub = request.FILES['attachment_ass_sub']
        print(attachment_ass_sub.name)

        fss = FileSystemStorage()
        filename1 = fss.save(attachment_ass_sub.name, attachment_ass_sub)
        url_file1 = fss.url(filename1)
        # print(url_file1)

        Student_Submit_Assignment_pro_data = Student_Submit_Assignment_pro(attachment =url_file1, course=cor_name_stu_submit1, Student_ID=stu_id_stu_submit1, Assignment_name=ass_name_stu_submit1)

        Student_Submit_Assignment_pro_data.save()
        messages.success(request, "You have Successfully submit your Assignment")


        return redirect('/')

    else:
        return redirect('/')


def stu_id_details(request):
    if request.method=="POST":
        get_id_stu_details = request.POST.get('get_id_stu_details')
        print(get_id_stu_details)

        get_details_stu = Student_login_informatn.objects.get(Student_ID=get_id_stu_details)
        print(get_details_stu)

        context3= {'get_details_stu':get_details_stu}

        return render(request, 'stu_id_details.html', context3)

    else:
        return redirect('/')


def submit_assignment(request):
    if request.method=="POST":

        ass_name_stu_submit = request.POST.get('ass_name_stu_submit')
        cor_name_stu_submit = request.POST.get('cor_name_stu_submit')
        stu_id_stu_submit = request.POST.get('stu_id_stu_submit')
        # print(ass_name_stu_submit, cor_name_stu_submit, stu_id_stu_submit)

        dictnary12 = {'ass_name_stu_submit':ass_name_stu_submit, 'cor_name_stu_submit':cor_name_stu_submit, 'stu_id_stu_submit':stu_id_stu_submit}

        return render(request, 'submit_assignment.html', dictnary12)

    else:
        return redirect('/')


def postComments(request):
    if request.method == "POST":
        comment_ass = request.POST.get('comment_ass')
        comment_username = request.POST.get('comment_username')
        user = comment_username
        ass_id = request.POST.get('ass_id')
        postId = ass_id

        post = Teacher_Assignment_upload_File.objects.get(id=postId)
        print(post)

        serial_no= request.POST.get('serial_no')
        print(serial_no)

        if serial_no == "":
            Assignment_Comments_data = Assignment_Comments(comment=comment_ass, user=user, postID=postId, post=post)
            Assignment_Comments_data.save()

            messages.success(request, "Your Comment is Successfully Posted !!")

        else:
            parent = Assignment_Comments.objects.get(serial_no=serial_no)
            Assignment_Comments_data = Assignment_Comments(comment=comment_ass, user=user, postID=postId, post=post , parent=parent)
            Assignment_Comments_data.save()

            messages.success(request, "Your Reply is Successfully Posted !!")

    return redirect(f'/')


def logout_func(request):
    request.session.clear()
    return redirect('login')


