# from app.models import BashScript
# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
# @receiver(post_save, sender=BashScript)
# def save_profile(sender, instance, **kwargs):
#     if created:
#         print(instance,sender.name)
#         print("içerde")
#         file = open(os.path.join(MEDIA_URL, '{}'.format(instance.name['name'])), 'w')
#         file.write(instance.script['script'])
#         file.close()