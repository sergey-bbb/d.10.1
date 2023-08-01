from django.urls import reverse_lazy
from django.views import View

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, render, get_object_or_404

from .filters import NewsFilter
from .forms import NewsForm
from datetime import datetime
from .models import News
from .models import Category
from .models import News
from .models import Appointment    # рассылка сообщений
from django.core.mail import mail_admins



class NewsList(ListView):
    model = News
    ordering = 'name'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 2


    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = NewsFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        context['time_now'] = datetime.utcnow()
        return context




class NewDetail(DetailView):

    model = News
    ordering = 'name'
    template_name = 'new.html'
    context_object_name = 'new'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = "Приятного чтения!"
        return context


# Добавляем новое представление для создания товаров.
class NewsCreate(CreateView):
    # Указываем нашу разработанную форму
    form_class = NewsForm
    # модель товаров
    model = News
    # и новый шаблон, в котором используется форма.
    template_name = 'news_edit.html'

class NewsUpdate(UpdateView):
    form_class = NewsForm
    model = News
    template_name = 'news_edit.html'

class NewsDelete(DeleteView):
    model = News
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')



from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='premium')
    if not request.user.groups.filter(name='premium').exists():
        premium_group.user_set.add(user)
    return redirect('/')



class CategoryListView(ListView):
    model = News
    template_name = 'flatpages/category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.news_category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = News.objects.filter(news_category=self.news_category).order_by('-sort_date_of_publication')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.news_category.subscribers.all()
        context['is_subscriber'] = self.request.user in self.news_category.subscribers.all()
        context['category'] = self.news_category
        return context


class AppointmentView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'flatpages/make_appointment.html', {})

    def post(self, request, *args, **kwargs):
        appointment = Appointment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
        )
        appointment.save()



        mail_admins(
            subject=f'{appointment.client_name} {appointment.date.strftime("%d %m %Y")}',
            message=appointment.message,
        )

        return redirect('/appointment/')

def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    message = 'You subscribed to the category: '
    return render(request, 'flatpages/subscribe.html', {'category': category, 'message': message})

def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)
    message = 'You unsubscribed from category: '
    return render(request, 'flatpages/unsubscribe.html', {'category': category, 'message': message})
