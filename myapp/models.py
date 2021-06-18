from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum, Avg


# class Biaya(models.Model):
# 	nama = models.CharField(max_length=200, null=True)
# 	status = models.CharField(max_length=200, null=True)
# 	created_at = models.DateTimeField(auto_now_add=True, null=True)
# 	updated_at = models.DateTimeField(auto_now=True, null=True)

# 	# class Meta:
# 	# 	ordering = ['nama']

# 	def __str__(self):
# 		return '%s' % (self.nama)

class Pegawai(models.Model):
	GOLONGAN = (
			('IIA', 'IIA'),
			('IIB', 'IIB'),
			('IIC', 'IIC'),
			('IID', 'IID'),
			('IIIA', 'IIIA'),
			('IIIB', 'IIIB'),
			('IIIC', 'IIIC'),
			('IIID', 'IIID'),
			('IVA', 'IVA'),
			('IVB', 'IVB'),
			('IVC', 'IVC'),
			)

	STATUS_PEGAWAI = (
			('PNS', 'PNS'),
			('PPPK', 'PPPK'),
			('HONORER', 'HONORER'),
			)

	nip = models.CharField(max_length=200, null=True)
	nama = models.CharField(max_length=200, null=True)
	# skpd = models.CharField(max_length=200, null=True)
	pangkat = models.CharField(max_length=200, null=True)
	golongan = models.CharField(max_length=200, null=True, choices=GOLONGAN)
	jabatan = models.CharField(max_length=200, null=True)
	status_pegawai = models.CharField(max_length=200, null=True ,choices=STATUS_PEGAWAI)
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True)

	def __str__(self):
		return self.nama

class Instansi(models.Model):
	nama = models.CharField(max_length=200, null=True)
	alamat = models.CharField(max_length=200, null=True)
	telepon = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	situs = models.CharField(max_length=200, null=True)
	logo = models.ImageField(default="pemda.png", null=True, blank=True)
	# status = models.CharField(max_length=200, null=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True)

	class Meta:
		ordering = ['nama']

	def __str__(self):
		return self.nama


class Surat_perintah(models.Model):
	nomor = models.CharField(max_length=200, null=True)
	uraian = models.CharField(max_length=200, null=True)
	tanggal = models.DateField(null=True)
	penanggung_jawab = models.ForeignKey(Pegawai, on_delete=models.CASCADE)
	koordinator = models.ForeignKey(Pegawai, on_delete=models.CASCADE, related_name='+')
	pengikut = models.ManyToManyField(Pegawai, blank=True, null=True, related_name="surat_perintahs")
	# status = models.CharField(max_length=200, null=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True)

	class Meta:
		ordering = ['nomor']

	def __str__(self):
		return self.nomor


class Sppd(models.Model):
	nomor = models.CharField(max_length=200, null=True)
	tempat_berangkat = models.CharField(max_length=200, null=True)
	tempat_tujuan = models.CharField(max_length=200, null=True)
	tanggal_berangkat = models.DateField(null=True)
	tanggal_kembali = models.DateField(null=True)
	keterangan = models.CharField(max_length=200, null=True)
	# instansi = models.ForeignKey(Instansi, on_delete=models.CASCADE)
	surat_perintah = models.OneToOneField(Surat_perintah, null=True, on_delete=models.CASCADE)

	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True)

	class Meta:
		ordering = ['nomor']

	def __str__(self):
		return '%s' % (self.nomor)

class Rincian(models.Model):

	SATUAN = (
			('Hari', 'Hari'),
			('Minggu', 'Minggu'),
			('Bulan', 'Bulan'),
			('Tahun', 'Tahun'),
			)

	uraian = models.CharField(max_length=200, null=True)
	# biaya = models.OneToOneField(Biaya, null=True, on_delete=models.CASCADE)
	kuantitas = models.PositiveIntegerField()
	satuan = models.CharField(max_length=200, null=True, choices=SATUAN)
	harga = models.IntegerField()
	jumlahnya = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True)

	def save(self, *args, **kwargs):
		self.jumlahnya = self.harga * self.kuantitas
		super(Rincian, self).save(*args, **kwargs)

	# class Meta:
	# 	ordering = ['uraian']
	
	# @property
	# def jumlahnya(self):
	# 	return self.harga * self.kuantitas

	def __str__(self):
		return self.uraian



class Pengeluaran(models.Model):
	nomor_bukti_pengeluaran = models.CharField(max_length=200, null=True)
	sumber_dana = models.CharField(max_length=200, null=True)
	keperluan = models.CharField(max_length=200, null=True)
	tanggal = models.DateField(null=True)
	keterangan = models.CharField(max_length=200, null=True)
	sppd = models.ForeignKey(Sppd, on_delete=models.CASCADE)
	pegawai = models.ForeignKey(Pegawai, on_delete=models.CASCADE)
	rincian = models.ManyToManyField(Rincian)
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True)

	# class Meta:
	# 	ordering = ['nomor_bukti_pengeluaran']

	def __str__(self):
		return '%s' % (self.nomor_bukti_pengeluaran)

	@property
	def total_nya(self):
		return self.rincian.aggregate(Sum('jumlahnya'))


class Anggaran(models.Model):
	
	PERIODE = (
			('Murni', 'Murni'),
			('Perubahan', 'Perubahan'),)
			

	tahun = models.CharField(max_length=200, null=True)
	dana = models.CharField(max_length=200, null=True)
	periode = models.CharField(max_length=200, null=True, choices=PERIODE)
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True)

	# class Meta:
	# 	ordering = ['nama']

	def __str__(self):
		return '%s' % (self.tahun)

# simpan otomatis one to one
@receiver(post_save, sender=Surat_perintah)
def create_sppd(sender, instance, created, **kwargs):
	if created:
		# group = Group.objects.get(name='customer')
		# instance.groups.add(group)
		Sppd.objects.create(
			surat_perintah=instance,
			# name=instance.username,
			)
		print('sppd create!')

@receiver(post_save, sender=Surat_perintah)
def update_sppd(sender, instance, created, **kwargs):
	if created == False:
		instance.sppd.save()
		print('sppd update')