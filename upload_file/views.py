import math
import json
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from .forms import UploadForm
from collections import defaultdict, Counter
from .models import Upload


class Home(CreateView):
    model = Upload
    form_class = UploadForm
    template_name = 'base.html'
    success_url = reverse_lazy('result')
    context_object_name = 'docs'


    def setup(self, request, *args, **kwargs):
        self.docs_list= [] # получам список списков
        self.file =request.FILES  # файлы текущего пользолвателя\
        self.text = [] #список слов текущего файла
        self.text_tf = None # объект collections.Counter
        self.docs = Upload.objects.all()
        for i in self.docs:
            self.docs_list.append(i.doc_list) # получаем список списков всех загруженных файлов

        return super().setup(request, *args, **kwargs)
    #
    def compute_idf(self, word, corpus):
        # на вход берется слово, для которого считаем IDF
        # и корпус документов в виде списка списков слов
        # количество документов, где встречается искомый термин считается как генератор списков
        try :
            ss = math.log10(len(corpus) / sum([1.0 for i in corpus if word in i ]))
        except ZeroDivisionError:
            ss = 0
        return  ss


    def form_valid(self, form):
        list_f = self.file['file'] # достаем загруженный файл
        for i in list_f.read().lower().split():
            self.text.append(i.decode("utf-8")) # Добавляем слова в список для теккущего файла
        tf_idf_list = defaultdict(list)
        tf_text = Counter(self.text)
        for i in tf_text:
            tf_text[i] = tf_text[i] / float(len(self.text))
            tf_idf_list[i].append(tf_text[i])
            tf_idf_list[i].append(self.compute_idf(i, self.docs_list))

        self.text_tf = json.dumps( tf_idf_list) # кодирование JSON полученного стловаря со списком списков
        form.instance.json = self.text_tf # Сохраняем кодированный JSON словарь со список списков
        form.instance.doc_list = self.text #сохряняем спиcок слов файла
        return super(Home, self).form_valid(form)



class Result(ListView):
    template_name = 'upload_file/result.html'
    context_object_name = 'doc_file'


    def get_queryset(self):
        obj = Upload.objects.order_by('-created_at').first()
        object_json = obj.json
        object_json = json.loads(object_json)
        object_json = dict((sorted(object_json.items(), key=lambda x: x[1][1], reverse =True))[0:50])
        return object_json
