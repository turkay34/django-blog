from django import forms
from .models import makale, comment

class IletisimFormu(forms.Form):
    isim = forms.CharField(max_length=50, label='İsminiz :', required=True)
    soyisim = forms.CharField(max_length=50, label='Soyisminiz :', required=True)
    email = forms.EmailField(max_length=100, label='Mailiniz :', required=True)
    icerik = forms.CharField(max_length=1000, label='Konu :', required=True)

    def __init__(self, *args, **kwargs): #init fonksiyonu args kwargs'a override yapılır
        super(IletisimFormu, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'} #formda fields'lara class atanır
        self.fields['icerik'].widget = forms.Textarea(attrs={'class': 'form-control'})

class BlogForm(forms.ModelForm):
    class Meta:
        model = makale
        fields = ['title', 'file', 'content', 'yayin_tipi', 'kategori']

    def __init__(self, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'} #fieldlara class olarak form-control atandı
        self.fields['content'].widget.attrs['rows'] = 10 #fieldlardan content'in rowuna 10 verildi

    def clean_content(self):
        icerik = self.cleaned_data.get('content') #icerik değişkenine postun contentini ata
        if len(icerik) < 250: #karakter sayısı 250'den az ise
            error_message = 'En az 250 karakter giriniz. Girilen karakter sayısı (%s)' % (len(icerik))
            raise forms.ValidationError(error_message)
        return icerik

class PostSorgu(forms.Form):
    taslak_sorgu = forms.ChoiceField(required=False, label='Yayın tipi seçiniz :', widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Aramak için buraya tıklayınız.'}), choices=makale.PUBLISH_CHOICE)

class CommentForm(forms.ModelForm):
    class Meta:
        model = comment
        fields = ['isim', 'soyisim', 'email', 'yorum']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}