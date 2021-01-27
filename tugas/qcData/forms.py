from django import forms
from django.core.exceptions import ValidationError
from .models import Stasiun, Pegawai, dataStasiun


class FormDaftarStasiunBaru (forms.ModelForm):

  class Meta:
    model = Stasiun
    fields = '__all__'
    labels = {'nama': '', 'alamat': '', 'telepon': '',
              'email': '', 'kepalaStasiun': 'Kepala Stasiun'}
    widgets = {
        'nama': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Stasiun'}),
        'alamat': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Alamat Stasiun'}),
        'telepon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telepon'}),
        'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Stasiun'}),
        'kepalaStasiun': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Kepala Stasiun'}),
    }

  def clean_telepon(self):
    telepon = self.cleaned_data['telepon']
    for x in telepon:
      try:
        int(x)
      except:
        raise ValidationError("Nomor telepon harus angka")
    return telepon


class FormUbahStasiun (forms.ModelForm):

  class Meta:
    model = Stasiun
    fields = '__all__'
    labels = {'nama': '', 'alamat': '', 'telepon': '',
              'email': '', 'kepalaStasiun': ''}
    widgets = {
        'nama': forms.TextInput(attrs={'class': 'form-control', }),
        'alamat': forms.TextInput(attrs={'class': 'form-control', }),
        'telepon': forms.TextInput(attrs={'class': 'form-control', }),
        'email': forms.EmailInput(attrs={'class': 'form-control', }),
        'kepalaStasiun': forms.Select(attrs={'class': 'form-control', }),
    }

  def clean_telepon(self):
    telepon = self.cleaned_data['telepon']
    for x in telepon:
      try:
        int(x)
      except:
        raise ValidationError("Nomor telepon harus angka")
    return telepon


class FormDaftarPegawaiBaru (forms.ModelForm):
  class Meta:
    model = Pegawai
    fields = '__all__'
    labels = {'nip': '', 'nama': '', 'tempatLahir': '',
              'tanggalLahir': '', 'stasiunKerja': 'Stasiun Kerja'}
    widgets = {
        'nip': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'NIP'}),
        'nama': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Lengkap'}),
        'tempatLahir': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tempat Lahir'}),
        'tanggalLahir': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Tanggal Lahir (10/28/2000)'}),
        'stasiunKerja': forms.Select(attrs={'class': 'form-control', }),
    }

  def clean_nip(self):
    nip = self.cleaned_data['nip']
    if len(nip) != 8:
      raise ValidationError("NIP harus 8 digit")
    else:
      for x in nip:
        try:
          int(x)
        except:
          raise ValidationError("NIP harus angka")
      return nip


class FormUbahPegawai (forms.ModelForm):
  class Meta:
    model = Pegawai
    fields = ['nama', 'tempatLahir', 'tanggalLahir', 'stasiunKerja', ]
    labels = {'nama': '', 'tempatLahir': '',
              'tanggalLahir': '', 'stasiunKerja': 'Stasiun Kerja'}
    widgets = {
        'nama': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Lengkap'}),
        'tempatLahir': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tempat Lahir'}),
        'tanggalLahir': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Tanggal Lahir (10/28/2000)'}),
        'stasiunKerja': forms.Select(attrs={'class': 'form-control', }),
    }


class InputDataStasiun(forms.Form):
  tanggal = forms.DateField()
  stasiun = forms.IntegerField()
  tMax = forms.DecimalField(max_digits=3, decimal_places=1)
  tMin = forms.DecimalField(max_digits=3, decimal_places=1)
  t = forms.DecimalField(max_digits=3, decimal_places=1)
  tD = forms.DecimalField(max_digits=3, decimal_places=1)
  rH = forms.DecimalField(max_digits=3, decimal_places=1)
  tekananUdara = forms.DecimalField(max_digits=5, decimal_places=1)
  hujan = forms.DecimalField(max_digits=3, decimal_places=1)


class FormDataMetStasiun (forms.Form):
  choiceTipe = [('mentah', 'Data Mentah'), ('matang', 'Data Matang')]
  choiceTahun = [(2020, '2020'), (1999, '1999'), (2013, '2013')]
  choiceBulan = [(bulan, bulan) for bulan in range(1, 13)]
  tipe = forms.ChoiceField(choices=choiceTipe,
                           widget=forms.Select(attrs={
                               'class': 'form-control', },
                           )
                           )
  tahun = forms.ChoiceField(choices=choiceTahun, widget=forms.Select(attrs={
      'class': 'form-control', },
  ))
  bulan = forms.ChoiceField(choices=choiceBulan, widget=forms.Select(attrs={
      'class': 'form-control', },
  ))
  stasiun = forms.ModelChoiceField(queryset=Stasiun.objects.all(), widget=forms.Select(attrs={
      'class': 'form-control', },
  ))


class FormTambahDataMet (forms.ModelForm):
  class Meta:
    model = dataStasiun
    fields = '__all__'
    labels = {'tanggal': 'Tanggal Pengamatan', 'stasiun': 'Stasiun',
              'tMax': 'Suhu Maks (°C)', 'tMin': 'Suhu Min (°C)',
              't': 'Suhu Rata-Rata (°C)', 'tD': 'Suhu Titik Embun (°C)',
              'rH': 'K. Relatif (%)', 'tekananUdara': 'Tekanan Udara (mbar)',
              'hujan': 'Curah Hujan (mm)'
              }
    widgets = {'tanggal': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'mm/dd/yyyy'}),
               'stasiun': forms.Select(attrs={'class': 'form-control', 'placeholder': ''}),
               'tMax': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
               'tMin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
               't': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
               'rH': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
               'tD': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
               'tekananUdara': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
               'hujan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
               }


class FormUbahDataMet (forms.ModelForm):
  class Meta:
    model = dataStasiun
    fields = ['tMax', 'tMin', 't', 'tD', 'rH', 'tekananUdara', 'hujan', ]
    labels = {'tMax': 'Suhu Maks (°C)', 'tMin': 'Suhu Min (°C)',
              't': 'Suhu Rata-Rata (°C)', 'tD': 'Suhu Titik Embun (°C)',
              'rH': 'K. Relatif (%)', 'tekananUdara': 'Tekanan Udara (mbar)',
              'hujan': 'Curah Hujan (mm)'}
    widgets = {'tMax': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
               'tMin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
               't': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
               'rH': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
               'tD': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
               'tekananUdara': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
               'hujan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
               }
