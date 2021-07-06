from django.db import models


class Tweet(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField()
    tweet_id = models.TextField()
    lat = models.FloatField()
    lon = models.FloatField()
    timestamp_ms = models.BigIntegerField()

    class Meta:
        db_table = "tweets"
