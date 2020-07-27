from django.db import models
from django.shortcuts import reverse
from unidecode import unidecode
from django.template.defaultfilters import slugify
from uuid import uuid4
from ckeditor.fields import RichTextField
import os

# Create your models here.

def upload_to(instance, filename):
    extension = filename.split('.')[-1] #dosyalarda noktadan sonra ki uzantıyı almak için
    new_name = "%s.%s" % (str(uuid4()), extension) #yeni dosya ismini unique id ve dosya uzantısı olarak alır
    unique_id = instance.unique_id #dosyanın unique_id'sini çeker
    return os.path.join('blog', unique_id, new_name) #upload_to fonksiyonu çalıştığında blog adında bir klasör açar ve altına o postun unique_id'si ile bir başka klasör açar ve içine dosyanın yeni adını atar.

class kategori(models.Model):
    isim = models.CharField(max_length=30, verbose_name='Kategori İsimi :')

    class Meta:
        verbose_name_plural = 'Kategoriler'

    def __str__(self):
        return self.isim

class makale(models.Model):

    PUBLISH_CHOICE = (('hepsi', 'Hepsi'), ('yayin', 'Yayın'), ('taslak', 'Taslak'))

    title = models.CharField(max_length=50, verbose_name="Başlık giriniz :", help_text="Makalenizin başlığını yazınız.", blank=False, null=True)
    file = models.FileField(default='default/default.jpg', verbose_name='Medya Dosyası', upload_to=upload_to, null=True, help_text='Medya dosyanızı ekleyiniz.', blank=True)
    content = RichTextField(max_length=5000, verbose_name="İçerik giriniz :", help_text="Makalenizin içeriğini yazınız.", blank=False, null=True)
    created_date = models.DateField(auto_now_add=True)
    kategori = models.ManyToManyField(to=kategori,blank=True, null=True) #manytomany bağlantısı kurulacak ilişki
    yayin_tipi = models.CharField(choices=PUBLISH_CHOICE, max_length=6, default='yayin')
    slug = models.SlugField(null=True, unique=True, editable=False)
    unique_id = models.CharField(max_length=100, editable=False, null=True)


    def __str__(self):
        return self.title #fonksiyonun görünecek özelliği

    def get_yayin_tipi(self):
        if self.yayin_tipi == 'yayin': #makalenin yayin tipi yayin ise
            return '<span class="badge badge-success">{0}</span>'.format(self.get_yayin_tipi_display()) #ilgili alana bunu
        return '<span class="badge badge-danger">{0}</span>'.format(self.get_yayin_tipi_display()) #değil ise bunu

    def get_file(self):
        if self.file:
            return self.file.url
        else:
            return '/media/default/default.jpg'

    def get_absolute_url(self):
        return reverse('detail', kwargs={'slug': self.slug}) #detail nameview'ında ki html çalıştırılır ve id olarak oluşturulan makalenin id'sini otomatik alır

    def get_unique_slug(self):
        sayi = 0
        slug = slugify(unidecode(self.title)) #slug değişkenine title'ı slugify ederek atadık

        if makale.objects.filter(slug=slug).exists(): #makalede girilen slug diğer makalalerde var ise
            sayi += 1 #sayiyi bir arttir
            slug = "%s-%s" % (slug, sayi) #yeni bir slug hazırla ve bunu slug-sayi olarak yaz ve slug değişkenine ata
        return slug #slug'a return et

    def save(self, *args, **kwargs): #viewsda ki save çalıştığın da burası çalışacak
        if self.id is None:
            new_unique_id = str(uuid4())
            self.unique_id = new_unique_id
            self.slug = self.get_unique_slug() #slug'a yukarıda ki döngüyü verdik
        else:
            slug_address = slugify(makale.objects.get(slug=self.slug)) #new_slug değişkenine makalenin şu an ki slugunu attık
            slug_title = slugify(self.title)
            if slug_address != slug_title: #makale_slug ile title aynı değilse
                self.slug = self.get_unique_slug() #uniqueslug çalıştır ve makale ile title'ı aynı yap
        super(makale, self).save(*args, **kwargs) #kayıt ettik

    def get_post_comment(self):
        return self.comment_set.all()

class comment(models.Model):
    post = models.ForeignKey(makale, null=True, on_delete=models.CASCADE) #post değişkeni altında makale classından ForeignKey çektirdik
    isim = models.CharField(blank=True, null=True, default='Anonim', verbose_name='İsim', max_length=50)
    soyisim = models.CharField(blank=True, null=True, verbose_name='Soyisim', max_length=50)
    email = models.EmailField(blank=True, null=True, verbose_name='Email')
    yorum = RichTextField(null=True, blank=False, verbose_name='Yorum', help_text='Yorumunuzu yazınız...', max_length=500)
    comment_date = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name_plural = 'Yorumlar' #admin panelinde görülecek isim

    def __str__(self):
        return "%s %s %s" % (self.isim, self.soyisim, self.post)