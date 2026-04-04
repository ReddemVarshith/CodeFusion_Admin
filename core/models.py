# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Team(models.Model):
    id = models.BigAutoField(primary_key=True)
    team_name = models.CharField(unique=True, max_length=100)
    team_size = models.IntegerField()
    payment_proof = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField()
    utr_id = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'registrations_team'

    def __str__(self):
        return self.team_name


class TeamMember(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=20)
    college_code = models.CharField(max_length=20)
    college_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    email = models.CharField(max_length=254)
    tshirt_size = models.CharField(max_length=5)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')

    class Meta:
        managed = False
        db_table = 'registrations_teammember'

    def __str__(self):
        return f"{self.name} ({self.team.team_name})"
