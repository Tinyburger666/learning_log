from django.shortcuts import render,redirect,get_object_or_404

from .models import Topic,Entry
from .forms import TopicForm,EntryForm

from django.contrib.auth.decorators import login_required
from django.http import Http404

# Create your views here.
def index(request):
    '''学习笔记的主页'''
    return render(request,'learning_logs/index.html')

@login_required
def topics(request):
    '''显示所有的主题'''
    topics=Topic.objects.filter(owner=request.user).order_by('date_added')
    context={'topics':topics}
    return render(request,"learning_logs/topics.html",context)

@login_required
def topic(request,topic_id):
    '''显示单个主题及其所有的条目'''
    topic=Topic.objects.get(id=topic_id)
    #确认请求的主题属于当前用户
    if topic.owner !=request.user:
        raise Http404
    
    entries=topic.entry_set.order_by('-date_added')
    context={'topic':topic,'entries':entries}
    return render(request,'learning_logs/topic.html',context)

@login_required
def new_topic(request):
    '''添加新主题'''
    if request.method !='POST':
        #未提交数据：创建一个新表单
        form=TopicForm()
    else:
        #POST提交的数据：对数据进行处理
        form=TopicForm(data=request.POST) #此中包括用户输入的数据
        if form.is_valid():
            new_topic=form.save(commit=False)
            new_topic.owner=request.user
            new_topic.save()
            return redirect('learning_logs:topics')
        
    #显示空表单或指出表单数据无效
    context={'form':form}
    return render(request,'learning_logs/new_topic.html',context)

@login_required
def new_entry(request,topic_id):
    '''在特定主题中添加新的条目'''
    topic=Topic.objects.get(id=topic_id)

    if request.method !='POST':
        #未提交数据，创建一个新的表单
        form=EntryForm()
    else:
        #POST提交的新数据：对数据进行处理
        form=EntryForm(data=request.POST) #此中包括用户输入的数据
        if form.is_valid():
            new_entry=form.save(commit=False)
            new_entry.topic=topic
            new_entry.topic.owner=topic.owner
            new_entry.save()
            return redirect('learning_logs:topic',topic_id=topic_id)
        else:
            # 输出表单验证错误，方便调试
            print(form.errors)
        
    #显示空表单或指出表单数据无效
    context={'topic':topic,'form':form}
    return render(request,'learning_logs/new_entry.html',context)

@login_required
def edit_entry(request,entry_id):
    '''编辑既有条目'''
    entry=Entry.objects.get(id=entry_id)
    topic=entry.topic
    #确认请求的主题属于当前用户
    if topic.owner !=request.user:
        raise Http404

    if request.method !='POST':
        #初次请求：使用当前条目填充表单
        form=EntryForm(instance=entry)
    else:
        #POST提交的数据：对数据进行处理
        form=EntryForm(instance=entry,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic',topic_id=topic.id)
        
    context={'entry':entry,'topic':topic,'form':form}
    return render(request,'learning_logs/edit_entry.html',context)

@login_required
def delete_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    if request.method == 'POST':
        entry.delete()
        return redirect('learning_logs:topic', topic_id=entry.topic.id)
    return render(request, 'learning_logs/delete_entry.html', {'entry': entry})

@login_required
def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if request.method == 'POST':
        topic.delete()
        return redirect('learning_logs:topics')  # 重定向到主题列表页面
    return render(request, 'learning_logs/delete_topic.html', {'topic': topic})


