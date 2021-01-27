from django.db import models
from django.db.models import Q, F
from django.urls import reverse

# Create your models here.


class Stasiun (models.Model):
    nama = models.CharField(max_length=80)
    alamat = models.CharField(max_length=80)
    telepon = models.CharField(max_length=80)
    email = models.EmailField(max_length=80)
    kepalaStasiun = models.OneToOneField(
        'Pegawai',
        on_delete=models.SET_NULL,
        null=True, )

    class Meta:
        db_table = "daftarStasiun"

    def __str__(self):
        return self.nama

    def getAbsoluteUrl(self):
        return reverse('stasiun-detail', args=[self.id])


class Pegawai (models.Model):
    nip = models.CharField(max_length=18, primary_key=True)
    nama = models.CharField(max_length=80)
    tempatLahir = models.CharField(max_length=80, null=True, blank=True)
    tanggalLahir = models.DateField(null=True, blank=True)
    stasiunKerja = models.ForeignKey(
        Stasiun,
        on_delete=models.SET_NULL,
        null=True,)

    class Meta:
        db_table = 'daftarPegawai'

    def __str__(self):
        return f"({self.nip}) {self.nama}"

    def getAbsoluteUrl(self):
        return reverse('pegawai-detail', args=[self.nip])


class dataStasiun (models.Model):
    tanggal = models.DateField()
    stasiun = models.ForeignKey(Stasiun, on_delete=models.PROTECT)
    tMax = models.DecimalField(max_digits=3, decimal_places=1)
    tMin = models.DecimalField(max_digits=3, decimal_places=1)
    t = models.DecimalField(max_digits=3, decimal_places=1)
    tD = models.DecimalField(max_digits=3, decimal_places=1)
    rH = models.DecimalField(max_digits=3, decimal_places=1)
    tekananUdara = models.DecimalField(max_digits=5, decimal_places=1)
    hujan = models.DecimalField(max_digits=3, decimal_places=1)

    class Meta:
        db_table = 'dataStasiun'
        constraints = [
            models.UniqueConstraint(
                fields=['tanggal', 'stasiun'], name='unique_waktudantempat'),
        ]

    def __str__(self):
        return f"{self.stasiun}, {self.tanggal} = > ({self.tMax}, {self.tMin},{self.t},{self.tD}) derajatCelcius,{self.rH},{self.tekananUdara},{self.hujan}."

    def getAbsoluteUrl(self):
        return reverse("ubahDataMet", args=[str(self.id), ])


class dataStasiunBersih (models.Model):
    data = models.OneToOneField(dataStasiun, on_delete=models.CASCADE)
    tMaxClean = models.DecimalField(
        max_digits=3, decimal_places=1, null=True, blank=True)
    tMinClean = models.DecimalField(
        max_digits=3, decimal_places=1, null=True, blank=True)
    tClean = models.DecimalField(
        max_digits=3, decimal_places=1, null=True, blank=True)
    tDClean = models.DecimalField(
        max_digits=3, decimal_places=1, null=True, blank=True)
    rHClean = models.DecimalField(
        max_digits=3, decimal_places=1, null=True, blank=True)
    tekananUdaraClean = models.DecimalField(
        max_digits=5, decimal_places=1, null=True, blank=True)
    hujanClean = models.DecimalField(
        max_digits=3, decimal_places=1, null=True, blank=True)

    class Meta:
        db_table = 'dataStasiunBersih'

    def __str__(self):
        pesan = "{self.data} = > ({self.tMaxClean}, {self.tMinClean}, {self.tClean}, {self.tDClean}) derajatCelcius,"
        pesan += "{self.rHClean}, {self.tekananUdaraClean}, {self.hujanClean}."
        return f"{self.data.tanggal} = > ({self.tMaxClean}, {self.tMinClean}, {self.tClean}, {self.tDClean}) derajatCelcius, {self.rHClean}, {self.tekananUdaraClean}, {self.hujanClean}."

    def getAbsoluteUrl(self):
        return reverse()


from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=dataStasiun)
def myhandler(sender, **kwargs):
    data = []
    data.append(kwargs['instance'].id)
    data.append(kwargs['instance'].tMax)
    data.append(kwargs['instance'].tMin)
    data.append(kwargs['instance'].t)
    data.append(kwargs['instance'].tD)
    data.append(kwargs['instance'].rH)
    data.append(kwargs['instance'].tekananUdara)
    data.append(kwargs['instance'].hujan)
    x = 0
    for item in data:
        if x == 0:
            x += 1
        elif 0 < x <= 3:
            if -80 <= item <= 60:
                x += 1
            else:
                data[x] = None
                x += 1
        elif x == 4:
            if -80 <= item <= 35:
                x += 1
            else:
                data[x] = None
                x += 1
        elif x == 5:
            if 0 <= item <= 100:
                x += 1
            else:
                data[x] = None
                x += 1
        elif x == 6:
            if 500 <= item <= 1100:
                x += 1
            else:
                data[x] = None
                x += 1
        elif x == 7:
            if 0 <= item <= 40:
                x += 1
            else:
                data[x] = None
                x += 1
    print(data)
    data1 = dataStasiunBersih(data=kwargs['instance'], tMaxClean=data[1], tMinClean=data[2],
                              tClean=data[3], tDClean=data[4], rHClean=data[5], tekananUdaraClean=data[6], hujanClean=data[7])
    try:
        data1.save()
    except:
        data1 = dataStasiunBersih.objects.filter(data=kwargs['instance'])
        data1 = data1.update(tMaxClean=data[1], tMinClean=data[2],
                             tClean=data[3], tDClean=data[4], rHClean=data[5], tekananUdaraClean=data[6], hujanClean=data[7])
        print("Loncatin")
    print("QC telah dilakukan")
