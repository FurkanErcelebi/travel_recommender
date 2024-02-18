from django.db import models

# class Ranges(models.Model):
	
# 	id = models.AutoField(unique=True,primary_key=True)
# 	type = models.IntegerField()
# 	label = models.CharField(max_length=10)


# class BookingType(models.Model):

# 	id = models.AutoField(unique=True,primary_key=True)
# 	type = models.CharField(max_length=10)
# 	label = models.CharField(max_length=20)

# class Stars(models.Model):

# 	id = models.AutoField(unique=True,primary_key=True)
# 	type = models.FloatField(null=False)
# 	label = models.CharField(max_length=20)


class Amenities(models.Model):

	id = models.AutoField(unique=True,primary_key=True)
	type = models.CharField(max_length=10)
	label = models.CharField(max_length=30)
	description = models.CharField(max_length=40, null=True)


class Property(models.Model):

	id = models.AutoField(unique=True,primary_key=True)
	type = models.IntegerField(null=False)
	label = models.CharField(max_length=40)
	description = models.CharField(max_length=120, null=True)
 

class Rooms(models.Model):

	id = models.AutoField(unique=True,primary_key=True)
	type = models.IntegerField(null=False)
	label = models.CharField(max_length=20)
	description = models.CharField(max_length=120, null=True)
 
class Hotels(models.Model):
	
	id = models.AutoField(unique=True,primary_key=True)
	type = models.IntegerField(null=False)
	label = models.CharField(max_length=20)
	description = models.CharField(max_length=120, null=True)

class Meals(models.Model):
	
	id = models.AutoField(unique=True,primary_key=True)
	type = models.IntegerField(null=False)
	label = models.CharField(max_length=20)
	description = models.CharField(max_length=120, null=True)

class Market(models.Model):
	
	id = models.AutoField(unique=True,primary_key=True)
	type = models.IntegerField(null=False)
	label = models.CharField(max_length=20)
	description = models.CharField(max_length=120, null=True)

class Distribution(models.Model):
	
	id = models.AutoField(unique=True,primary_key=True)
	type = models.IntegerField(null=False)
	label = models.CharField(max_length=20)
	description = models.CharField(max_length=120, null=True)

class Deposit(models.Model):
	
	id = models.AutoField(unique=True,primary_key=True)
	type = models.IntegerField(null=False)
	label = models.CharField(max_length=20)
	description = models.CharField(max_length=120, null=True)

class Customer(models.Model):
	
	id = models.AutoField(unique=True,primary_key=True)
	type = models.IntegerField(null=False)
	label = models.CharField(max_length=20)
	description = models.CharField(max_length=120, null=True)

		
		
