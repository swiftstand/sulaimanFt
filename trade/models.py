from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from utils.updated_mixin import UpdatedCreatedMixin
import uuid

class Portfolio(UpdatedCreatedMixin):
    user = models.IntegerField(unique=True) # to store user primary key
    amount = models.IntegerField() # will store amount in base unit in our case $100 * 100 = 10000 cents
    portfolio_code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, ) # unique identifier    
    loss_count_dict = models.TextField(default="{}")
    profit_count_dict = models.TextField(default="{}")



class PortfolioTrade(models.Model):
    portfolio = models.UUIDField(editable=False) #to connect a trade to its respective portfolio
    amount_traded = models.IntegerField() # base unit
    closing_amount = models.IntegerField() # base unit
    start_time = models.DateTimeField(null=True)
    closing_time = models.DateTimeField(null=True)
