from django.shortcuts import render, get_object_or_404
from .models import Stasiun, Pegawai, dataStasiun, dataStasiunBersih
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .forms import FormDaftarStasiunBaru, FormUbahStasiun, FormDaftarPegawaiBaru, FormDataMetStasiun, FormTambahDataMet, FormUbahDataMet, FormUbahPegawai
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import View


# Create your views here.


def home(request):
    jumlahStasiun = Stasiun.objects.all().count()
    jumlahPegawai = Pegawai.objects.all().count()
    jumlahData = dataStasiun.objects.all().count()
    context = {
        'jumlahStasiun': jumlahStasiun,
        'jumlahPegawai': jumlahPegawai,
        'jumlahData': jumlahData,
    }
    return render(request, 'home.html', context=context)


class daftarStasiun(ListView):
    model = Stasiun
    context_object_name = 'daftarSemuaStasiun'
    template_name = 'Stasiun/daftarStasiun.html'


class daftarStasiun_detail(DetailView):
    model = Stasiun
    template_name = 'Stasiun/daftarStasiun_detail.html'


def daftarStasiunBaru(request):
    judul = "Stasiun"
    if request.method == 'POST':
        form = FormDaftarStasiunBaru(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            stasiunBaru = Stasiun(
                nama=form['nama'], alamat=form['alamat'], telepon=form['telepon'],
                email=form['email'], kepalaStasiun=form['kepalaStasiun'])
            stasiunBaru.save()
            return HttpResponseRedirect(reverse('stasiunLengkap'))
        else:
            return render(request, 'Stasiun/daftarStasiunBaru.html', context={'form': form, 'judul': judul})
    else:
        form = FormDaftarStasiunBaru()
    return render(request, 'Stasiun/daftarStasiunBaru.html', context={'form': form, 'judul': judul})


def ubahDaftarStasiun(request, pk):
    stasiun1 = Stasiun.objects.filter(id=pk)
    stasiun = stasiun1[0]
    if request.method == 'POST':
        form = FormUbahStasiun(request.POST)
        print(form.is_valid())
        print(form.errors)
        if form.is_valid():
            form = form.cleaned_data
            print(form)
            stasiun1.update(nama=form['nama'], alamat=form['alamat'], telepon=form['telepon'],
                            email=form['email'], kepalaStasiun=form['kepalaStasiun'])
            print(stasiun1)
    else:
        form = FormUbahStasiun()
    return render(request, 'Stasiun/ubahStasiun.html', context={'form': form, 'stasiun': stasiun})


def hapusDaftarStasiun(request, pk):
    stasiun = Stasiun.objects.filter(id=pk)
    stasiun.delete()
    return HttpResponseRedirect(reverse('stasiunLengkap'))


class daftarPegawai(ListView):
    model = Pegawai
    template_name = 'Pegawai/daftarPegawai.html'


class daftarPegawaiBaru (View):
    def get(self, request, *args, **kwargs):
        form = FormDaftarPegawaiBaru()
        judul = "Pegawai"
        return render(request, 'Stasiun/daftarStasiunBaru.html', context={'form': form, 'judul': judul})

    def post(self, request, *args, **kwargs):
        form = FormDaftarPegawaiBaru(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            pegawai = Pegawai(nip=form['nip'], nama=form['nama'], tempatLahir=form['tempatLahir'],
                              tanggalLahir=form['tanggalLahir'], stasiunKerja=form['stasiunKerja'])
            pegawai.save()
            print(form)
            return HttpResponseRedirect(reverse('daftarPegawaiLengkap'))
        return render(request, 'Stasiun/daftarStasiunBaru.html', context={'form': form, 'judul': judul})


class daftarPegawai_detail(DetailView):
    model = Pegawai
    template_name = 'Pegawai/daftarPegawai_detail.html'


class ubahDaftarPegawai(View):
    def get(self, request, *args, **kwargs):
        form = FormUbahPegawai()
        pegawai = Pegawai.objects.filter(nip=kwargs['pk'])
        pegawai = pegawai[0]
        return render(request, 'Pegawai/ubahPegawai.html', context={'form': form, 'pegawai': pegawai})

    def post(self, request, *args, **kwargs):
        form = FormUbahPegawai(request.POST)
        pegawai = Pegawai.objects.filter(nip=kwargs['pk'])
        pegawai1 = pegawai.get()
        print(form.errors)
        if form.is_valid():
            form = form.cleaned_data
            try:
                if pegawai1.stasiun != form['stasiunKerja']:
                    return HttpResponse("Tempat Kerja Harus sama dengan Jabatannya Kepala Stasiunnya!! Silahkan kembali")
                else:
                    print(form)
                    pegawai = pegawai.update(nama=form['nama'], tempatLahir=form['tempatLahir'],
                                             tanggalLahir=form['tanggalLahir'], stasiunKerja=form['stasiunKerja'])
            except:
                print(form)
                pegawai = pegawai.update(nama=form['nama'], tempatLahir=form['tempatLahir'],
                                         tanggalLahir=form['tanggalLahir'], stasiunKerja=form['stasiunKerja'])
        return render(request, 'Pegawai/ubahPegawai.html', context={'form': form, 'pegawai': pegawai})


def hapusDaftarPegawai(request, pk):
    pegawai = Pegawai.objects.filter(nip=pk)
    pegawai.delete()
    return HttpResponseRedirect(reverse('daftarPegawaiLengkap'))


def dataMetStasiunHome(request):
    template = 'DataMetStasiun/dataMetStasiun.html'
    jumlahData = dataStasiun.objects.all().count()
    data = dataStasiun.objects.order_by('tanggal')
    awalData = data[0].tanggal
    akhirData = data.reverse()[0].tanggal
    selisihTanggal = akhirData - awalData
    selisihTanggal /= 7
    xAxis = []
    yAxis = []
    for i in range(0, 7):
        xAxis.append(awalData.strftime("%Y-%m-%d"))
        awalData += selisihTanggal
    xAxis.append(akhirData.strftime("%Y-%m-%d"))
    for i in xAxis:
        totalData = dataStasiun.objects.filter(tanggal__lte=i).count()
        yAxis.append(totalData)
    print(yAxis)
    return render(request, template, context={'xAxis': xAxis, 'yAxis': yAxis})


class dataMetStasiunCari (View):
    template = 'DataMetStasiun/cariDataMet.html'
    templateTujuan = 'DataMetStasiun/hasilDataMet.html'

    def get(self, request, *args, **kwargs):
        form = FormDataMetStasiun()
        return render(request, self.template, context={'form': form})

    def post(self, request, *args, **kwargs):
        form = FormDataMetStasiun(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            if form['tipe'] == 'mentah':
                print(form.items())
                data = dataStasiun.objects.filter(
                    stasiun=form['stasiun'], tanggal__year=form['tahun'], tanggal__month=form['bulan']).order_by('tanggal')
                return render(request, self.templateTujuan, context={'data': data, 'form': form})
            else:
                data = dataStasiun.objects.filter(stasiun=form['stasiun'],
                                                  tanggal__year=form['tahun'], tanggal__month=form['bulan']).order_by('tanggal')
                data1 = []
                for i in data:
                    try:
                        data1.append(i.datastasiunbersih)
                    except:
                        pass
                print(data1)
                return render(request, self.templateTujuan, context={'data1': data1, 'form': form})


class dataMetStasiunTambah (View):
    template = 'DataMetStasiun/tambahDataMet.html'

    def get(self, request, *args, **kwargs):
        form = FormTambahDataMet()
        return render(request, self.template, context={'form': form})

    def post(self, request, *args, **kwargs):
        form = FormTambahDataMet(request.POST)
        print(form.errors)

        if form.is_valid():
            form = form.cleaned_data
            data = dataStasiun(tanggal=form['tanggal'], stasiun=form['stasiun'],
                               tMax=form['tMax'], tMin=form['tMin'], t=form['t'], tD=form['tD'],
                               rH=form['rH'], tekananUdara=form['tekananUdara'], hujan=form['hujan'])
            data.save()
            return HttpResponseRedirect(reverse('dataStasiunHome'))
        else:
            peringatan = 'Telah ada data pada tanggal dan stasiun yang sama'
            return render(request, self.template, context={'form': form, 'peringatan': peringatan})


class dataMetStasiunUbah(View):
    template = "dataMetStasiun/ubahDataMet.html"

    def get(self, request, *args, **kwargs):
        form = FormUbahDataMet()
        data = dataStasiun.objects.filter(id=kwargs['pk']).get()
        return render(request, self.template, context={'form': form, 'data': data})

    def post(self, request, *args, **kwargs):
        form = FormUbahDataMet(request.POST)
        data = dataStasiun.objects.filter(id=kwargs['pk'])
        print(form.errors)
        if form.is_valid():
            form = form.cleaned_data
            data = data.update(tMax=form['tMax'], tMin=form['tMin'], t=form['t'], tD=form['tD'],
                               rH=form['rH'], tekananUdara=form['tekananUdara'], hujan=form['hujan'])
            data = dataStasiun.objects.filter(id=kwargs['pk']).get()
            data.tMax = form['tMax']
            data.save()
            return HttpResponse("Data Berhasil Diubah")
        return render(request, self.template, context={'form': form, 'data': data})


class dataMetStasiunHapus(View):
    def get(self, request, *args, **kwargs):
        data = dataStasiun.objects.filter(id=kwargs['pk'])
        data.delete()
        return HttpResponse("Data Berhasil Dihapus")
