from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from django.http import HttpResponseBadRequest
from django.contrib import messages
from .models import makale
from .forms import IletisimFormu, BlogForm, PostSorgu, CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#models.py'den gelenler ;


def post_list(request):
    posts = makale.objects.all().order_by('-created_date')  # bütün makaleleri posts değişkeninde tutar ve oluşturulma tarihine göre sıralar
    page = request.GET.get('page', 1) #default sayfa sayısı 1 olarak verildi ve bir değişkene atandı
    keyword = request.GET.get('keyword')
    form = PostSorgu(data=request.GET or None)

    if form.is_valid():
        taslak_sorgu = form.cleaned_data.get('taslak_sorgu', 'hepsi') #formdaki taslak_sorgu değerini değişkene atadık

        if taslak_sorgu and taslak_sorgu != 'hepsi': #eğer değişken değer hepsi değil ise
            posts = posts.filter(yayin_tipi=taslak_sorgu) #postları değişkende ki değere göre filtrele
        if keyword:
            posts = makale.objects.filter(title__contains=keyword)
    paginator = Paginator(posts, 3) #sorgulardan çıktıktan sonra bir sayfada 3 post olacak şekilde belirlendi
    try:
        posts = paginator.page(page) #postlar paginator ile basıldı
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)

    return render(request, 'blog/post-list.html', context={'posts': posts, 'form': form}) #post-list.html'i render eder ve postları yansıtır


def post_detail(request, slug): #slug parametresini istedik
    form = CommentForm()
    article = get_object_or_404(makale, slug=slug) #article değişkenine makalenin sluglaştırılmış title'ını tutturduk
    return render(request, 'blog/post-detail.html', context={'makale': article, 'form': form}) #makale objesine article'i attık ve post-list.html'den argument olarak çektik


def post_update(request, slug):
    article = get_object_or_404(makale, slug=slug)
    form = BlogForm(instance=article, data=request.POST or None, files=request.FILES or None) #BlogForm'unda ki makale.id'sine ait bilgileri getiriyor
    if form.is_valid():
        form.save() #formu kaydeder
        messages.success(request, 'Makaleniz başarılı bir şekilde güncellendi.', extra_tags='info')
        return HttpResponseRedirect(article.get_absolute_url()) #kaydedilmiş makaleye geri dönüş sağlarız
    return render(request, 'blog/post-update.html', context={'form': form, 'article': article})


def post_delete(request, slug):
    article = get_object_or_404(makale, slug=slug)
    article.delete()
    messages.success(request, 'Makaleniz başarılı bir şekilde silindi.', extra_tags='danger')
    return HttpResponseRedirect(reverse('post-list'))



#forms.py'den gelenler ;

mesajlar = []


def iletisim_formu(request):
    form = IletisimFormu(data=request.GET or None) #form'a get requestten gelen bilgilerin datasını atar

    if form.is_valid(): #form tutarlı ve boş gelmedi ise
        isim = form.cleaned_data.get('isim') #formda ki verileri çekmemizi sağlar
        soyisim = form.cleaned_data.get('soyisim')
        email = form.cleaned_data.get('email')
        icerik = form.cleaned_data.get('icerik')

        data = {'isim': isim, 'soyisim': soyisim, 'email': email, 'icerik': icerik} #değişkene bilgleri attık
        mesajlar.append(data) #mesajlar listesinin sonuna data değişkenini atadık

        return render(request, 'iletisim.html', context={'mesajlar': mesajlar, 'form': form})
    return render(request, 'iletisim.html', context={'form': form})



def comment_add(request, slug):
    if request.method == 'GET': #method GET ise
        return HttpResponseBadRequest #hata ver
    post = get_object_or_404(makale, slug=slug) #method GET değil ise makalenin slugunu al ve post değişkenine at
    form = CommentForm(data=request.POST) #form değişkeninde bir CommentForm oluştur ve datasına POST'tan geleni at
    if form.is_valid():
        new_comment = form.save(commit=False) #değişkene form'a gelenleri ata ama saveleme
        print(new_comment)
        new_comment.post = post #değişkende ki değerleri ilgili makaleye attık (.post foreignkey için tutuldu)
        post.save()
        messages.success(request, 'Yorumunuz eklendi.')
        return HttpResponseRedirect(post.get_absolute_url()) #absolute_url ile makaleye geri dönüş yaptı
    messages.error(request, 'Yorumunuz eklenemedi.')

#models.py'den kalıtım alan forms.py'den gelen:

def post_create(request): #models'dan kalıtım alan ModelForm'dan geliyor
    form = BlogForm(data=request.POST, files=request.FILES) #posttan gelenleri BlogForm'un datasına at

    if form.is_valid(): #form valid ise
        blog = form.save() #db'ye kaydet ve blog değişkenine ata
        messages.success(request, 'Makaleniz başarılı bir şekilde oluşturuldu.', extra_tags='success')
        return HttpResponseRedirect(blog.get_absolute_url()) #url değişkenini models.py sayfasında ki get_absolute_url çalıştırılır
    return render(request, 'blog/post-create.html', context={'form': form})