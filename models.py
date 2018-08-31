from django.db.models import Model, ManyToManyField, DateTimeField, CharField, PositiveSmallIntegerField, TextField, ForeignKey, CASCADE
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from blog.models import Title
from medium.models import Medium

class Tug(Model):
	title=ForeignKey(Title, related_name='title_tug', on_delete=CASCADE)
	media=ManyToManyField(Medium, related_name='media_tug')
	tugger=ManyToManyField(settings.AUTH_USER_MODEL, related_name='tugger_tug')
	description=TextField()
	coordinate=CharField(max_length=50)
	datetime=DateTimeField()
	max=PositiveSmallIntegerField()
	timestamp=DateTimeField(auto_now=True)
	def __str__(self):return ' '.join([self.title.title, self.description])
	@property
	def tug_launcher(self): return self.media.last().user.last()
	@property
	def initiator(self): return self.tugger.latest('-timestamp')
	@property
	def tuggers(self):return [user for user in self.tugger.all()]
	class Meta: db_table='tug'
