from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class regi_content(models.Model):
    #管理番号
    control_id = models.AutoField(primary_key=True)
    #初回受付日時
    first_time = models.DateTimeField()
    #終了日時   
    end_time = models.DateTimeField()
    #対応合計時間
    total_time = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    #対応者ID
    name_id = models.IntegerField(default=0)
    #会社名
    company_name = models.CharField(max_length=255) 
    #問い合わせ内容
    q_contents = models.TextField()
    #回答内容
    a_contents = models.TextField()

    #未解決
    unsolved = models.IntegerField()



class User_info(models.Model):
    user_id = models.IntegerField(primary_key=True)

    user_name = models.CharField(max_length=30)

    user_ip = models.GenericIPAddressField(unique=True)

    def __str__(self):
        return self.user_name

    
    

