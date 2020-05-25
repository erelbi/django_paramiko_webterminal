from app.models import BashScript,WordsPoint
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import collections

@receiver(post_save, sender=BashScript)
def save_profile(sender, instance, created,**kwargs):
    if created:
        words = instance.script
        total=0
        script_in_word = WordsPoint.objects.values_list('word', flat=True)
        words_split = words.split()
        word_counts = collections.Counter(words_split)
        for word, count in sorted(word_counts.items()):
            if str(word) in script_in_word:
                p = WordsPoint.objects.filter(word=word).values('point').first()
                total += (int(p['point']) * int(count))
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "point", {"type": "bash.script",
                       "event": "bashscript",
                        "name": instance.name,
                       "point": total})