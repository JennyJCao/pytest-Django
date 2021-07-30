from django.db import models
from django.utils.timezone import now


class Company(models.Model):
    class CompanyStatus(models.TextChoices):
        # 裁员
        LAYOFFS = "Layoffs"
        HIRING_FREEZE = "Hiring Freeze"
        HIRING = "Hiring"

    name = models.CharField(max_length=30, unique=True)
    status = models.CharField(
        choices=CompanyStatus.choices, default=CompanyStatus.HIRING, max_length=30
    )
    last_update = models.DateTimeField(default=now, editable=True)
    application_link = models.CharField(max_length=100, blank=True)
    notes = models.CharField(max_length=100, blank=True)

    # 为了代码可读性高，标记返回值为str；
    # 本身返回值是一个属性，不是str，将其format就好了
    def __str__(self) -> str:
        return f"{self.name}"
