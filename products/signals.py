import pusher
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product

pusher_client = pusher.Pusher(
    app_id="1",                   # Identifiant arbitraire, doit être numérique
    key="public-key-1234",        # Clé publique
    secret="private-key-5678",    # Clé secrète
    cluster="mt1",                # Cluster 'mt1'
    ssl=False                     # False si HTTP
)

@receiver(post_save, sender=Product)
def product_created(sender, instance, created, **kwargs):
    if created:
        pusher_client.trigger('notifications', 'product-added', {
            'message': f"A new product '{instance.name}' has been added."
        })
