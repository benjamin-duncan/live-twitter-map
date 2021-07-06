from rest_framework import serializers


class StartupSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        return {
            "id": instance.id,
            "text": instance.text,
            "tweet_id": str(instance.tweet_id),
            "lat": instance.lat,
            "lon": instance.lon,
            "timestamp_ms": str(instance.timestamp_ms),
        }


class StatsSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            "total": instance["total"],
            "day": instance["day"],
            "hour": instance["hour"],
            "minute": instance["minute"],
        }


class GraphSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {instance}
