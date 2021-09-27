from django.db import models

class Conversation(models.Model):
    content = models.TextField()
    num = models.PositiveIntegerField()

    def __str__(self):
        return f"Conversation {self.num}"

class Client(models.Model):
    client_id = models.PositiveIntegerField(primary_key=True)
    name = models.TextField()

    def __str__(self):
        return f"{self.client_id}"

class Infor(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    age = models.PositiveSmallIntegerField()
    sex = models.TextField()
    cough = models.BinaryField()
    fever = models.BinaryField()
    sore_throat = models.BinaryField()
    shortness_breath = models.BinaryField()
    headache = models.BinaryField()
    test_indicator = models.BinaryField()

    def __str__(self):
        return f"{self.client}"

