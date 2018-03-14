from django.db import models


# Create your models here.

class Area(models.Model):
	name = models.CharField(max_length=10)

	def __str__(self):
		return self.name

class Candidate(models.Model):
	name = models.CharField(max_length=10)
	introduction = models.TextField()
	# area = models.CharField(max_length=15)
	area = models.ForeignKey('Area', on_delete=models.CASCADE)
	party_number = models.IntegerField(default=1)

	def __str__(self):
		return self.name


class Poll(models.Model):
	start_date = models.DateTimeField()
	end_date = models.DateTimeField()
	# area = models.CharField(max_length=15)
	area = models.ForeignKey('Area', on_delete=models.CASCADE)

	def __str__(self):
		return "여론조사지역: " + self.area.name


class Choice(models.Model):
	poll = models.ForeignKey('Poll', on_delete=models.CASCADE)
	candidate = models.ForeignKey('Candidate', on_delete=models.CASCADE)
	votes = models.IntegerField(default=0)

	def __str__(self):
		return "후보자: {}, 득표수: {}".format(self.candidate.name, self.votes)
