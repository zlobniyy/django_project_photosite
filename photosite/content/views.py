from django.contrib import auth
from django.core.exceptions import ValidationError
from .models import *
from .forms import *
from usermanage.forms import *
from usermanage.models import *
from main.forms import *
from main.models import *
from django.http import Http404, JsonResponse
from django.template import loader
from django.template.context_processors import csrf
from django.contrib.auth.decorators import user_passes_test
import time, datetime
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

# @user_passes_test(lambda user: user.is_superuser, login_url='/main/')
def images_list(request):
    imagelist = Imagemodel.objects.all()
    form = ImageForm()
    return render(request, 'admin_images.html', {'imagelist': imagelist, 'form': form})


# List of items + Paginator
def listimg(request, id):
    title = get_object_or_404(Categorymodel, id=id)
    image_list = Imagemodel.objects.filter(category_id=id)
    paginator = Paginator(image_list, 4)
    page = request.GET.get('page')
    try:
        imagelist = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        imagelist = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        imagelist = paginator.page(paginator.num_pages)

    return render(request, 'album.html',
                  {"imagelist": imagelist, 'image_list': image_list, 'page': page, 'title': title})


def admin_image_create(request):
    print('========admin_image_add==========')
    print('POST=' + str(request.POST))
    title = 'Добавить картинку'
    if request.method == 'POST':
        form = ImageFormChange(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/admin/lists/')
        context = {'form': form}
        return render(request, 'admin_image_create.html', context, {'title': title})
    context = {'form': ImageFormChange()}
    return render(request, 'admin_image_create.html', context, {'title': title})


# представление для добавления изображения пользователем
@user_passes_test(lambda user: user.is_authenticated, login_url='/oops/')
def album_image_create(request):
    author = auth.get_user(request).pk
    print('========album_image_add==========')
#    print('POST=' + str(request_new))
    title = 'Добавить картинку в альбом'
    if request.method == 'POST':
        # form = ImageFormChange(request.POST, request.FILES,initial={'author': str(author)})
        request_new=request.POST.copy()
        #request_new['author']=str(author)
        request_new.update({'author':str(author)})
        #request_new.update({'image_orig':request['image']})
        print(request_new)
        form = ImageFormChange(request.POST, request.FILES)
        form1 = ImageFormChange(request_new, request.FILES)
        # здесь переопределяем автора на текущего пользователя
        #form1.data['author'] = str(author)
        print(type(request_new))
        print(type(author))
        print(type(form1.data['author']))
        print('current_author===' + str(author))
        print('form1_author===' + form1.data['author'])
        print('form===' + str(form1))
        print('POST=' + str(request_new))
        if form1.is_valid():
            form1.save()
            return HttpResponseRedirect('/list/' + request_new['category'] + '?page=999999999999999')
        else:
            print("========WTF========")
        context = {'form': form1}
        return render(request, 'album.html', context, {'title': title, 'author': author})
    context = {'form': ImageFormChange()}
    return render(request, 'album.html', context, {'title': title, 'author': author})


@user_passes_test(lambda user: user.is_authenticated, login_url='/oops/')
def album_image_delete(request, id_cat, id_image):
    image = get_object_or_404(Imagemodel, id=id_image)
    if image.author.id == request.user.id:
        image.delete()
        return HttpResponseRedirect('/list/' + id_cat)
    else:
        return HttpResponseRedirect('/oops/')

@user_passes_test(lambda user: user.is_superuser, login_url='/oops/')
def adm_album_image_delete(request, id_cat, id_image):
    image = get_object_or_404(Imagemodel, id=id_image)
    image.delete()
    return HttpResponseRedirect('/list/' + id_cat)
