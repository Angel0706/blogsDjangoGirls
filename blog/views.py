from django.shortcuts import redirect
from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Post
from .forms import PostForm
from datetime import datetime
from rest_framework import viewsets
from .serializer import PostSerializer
import xlsxwriter
import io

# Create your views here.

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html',{'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def get_excel(request, pk):
    output = io.BytesIO()
    post = get_object_or_404(Post, pk=pk)
    fileName = (post.title+'-'+str(post.pk))+'.xlsx'
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    date_format = workbook.add_format({'num_format': 'd "de" mmmm yyyy'})
    bold = workbook.add_format({'bold': True})
    date = datetime.strptime((str(post.published_date.day)+'-'+str(post.published_date.month)+'-'+str(post.published_date.year)), '%d-%m-%Y')
    worksheet.set_column('B:B', 40)
    worksheet.set_column('D:D', 20)
    worksheet.write('A1', 'Titulo', bold)
    worksheet.write('B1', 'Contenido', bold)
    worksheet.write('C1', 'Autor', bold)
    worksheet.write('D1', 'Fecha de publicación', bold)
    worksheet.write('A2', post.title)
    worksheet.write('B2', post.text)
    worksheet.write('C2', str(post.author).capitalize())
    worksheet.write_datetime('D2', date, date_format)
    workbook.close()
    output.seek(0)
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % fileName
    return response

def get_excel_li(request):
    output = io.BytesIO()
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True})
    date_format = workbook.add_format({'num_format': 'd "de" mmmm yyyy'})
    worksheet.write('A1', 'Titulo', bold)
    worksheet.write('B1','Autor', bold)
    worksheet.write('C1','Fecha de publicación', bold)
    fila = 1
    colum = 0
    for p in posts:
        date = datetime.strptime((str(p.published_date.day)+'-'+str(p.published_date.month)+'-'+str(p.published_date.year)), '%d-%m-%Y')
        worksheet.write(fila, colum, p.title)
        worksheet.write(fila, colum+1, str(p.author).capitalize())
        worksheet.write_datetime(fila, colum+2, date, date_format)
        fila+=1
    worksheet.autofit()
    workbook.close()
    output.seek(0)
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % 'Post.xlsx'
    return response

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer