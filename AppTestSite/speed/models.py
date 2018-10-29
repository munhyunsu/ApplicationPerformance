from django.db import models
from django.utils import timezone


class AppInformation(models.Model):
    app_title = models.CharField('application title', max_length=50)
    package_name = models.CharField('package name', max_length=50)
    star_score = models.FloatField('star rate')

    def __str__(self):
        return self.app_title


class SpeedInformation(models.Model):
    package_name = models.CharField('package name', max_length=50)
    exp_date = models.DateField('experimented date')
    scene_num = models.IntegerField('scene number')
    speed_index = models.IntegerField('speed index')
    tcp_num = models.IntegerField('tcp connections')
    rtt_max = models.FloatField('max rtt')
    rtt_avg = models.FloatField('avg rtt')
    ret_pm = models.FloatField('retransmission per minute')
    layout_num = models.IntegerField('layout number')
    image_num = models.IntegerField('image number')
    ads_num = models.IntegerField('ads number')
    tra_vol = models.FloatField('traffic volume')
    servers = models.TextField('Server list')

    def __str__(self):
        return '{0} - {1} by {2}'.format(self.package_name, self.scene_num, self.exp_date)
