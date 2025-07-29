from django.db import models
from django.contrib.auth.models import User

class Categorie(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nom

class Plat(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    prix = models.IntegerField()
    quantite_disponible = models.IntegerField()
    temps_preparation = models.IntegerField()
    disponible = models.BooleanField(default=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='plats')
    image = models.ImageField(upload_to='plats/', null=True, blank=True)

    def __str__(self):
        return self.nom

class ProduitMarche(models.Model):
    nom = models.CharField(max_length=100)
    quantite = models.IntegerField()
    unite = models.CharField(max_length=20, default='unités')
    prix = models.IntegerField()  # Utilisation integer pour éviter les décimales compliquées

    def __str__(self):
        return self.nom

class Cuisinier(models.Model):
    nom = models.CharField(max_length=100)
    specialite = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.nom} ({self.specialite})"

class Commande(models.Model):
    nom_client = models.CharField(max_length=255)
    adresse_livraison = models.TextField()
    telephone = models.CharField(max_length=20)
    date_commande = models.DateTimeField(auto_now_add=True)
    total = models.IntegerField(default=0)
    cuisinier = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='commandes_preparees')

    def calculer_total(self):
        total = 0
        for item in self.items.all():
            if item.plat:
                total += item.plat.prix * item.quantite
            elif item.produit_marche:
                total += item.produit_marche.prix * item.quantite
        return total

    def save(self, *args, **kwargs):
        # On n'appelle plus calculer_total ici pour éviter l'erreur
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Commande #{self.id} - {self.nom_client}"

class CommandeItem(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name='items')
    plat = models.ForeignKey(Plat, null=True, blank=True, on_delete=models.CASCADE)
    produit_marche = models.ForeignKey(ProduitMarche, null=True, blank=True, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)

    def __str__(self):
        if self.plat:
            return f"{self.quantite} x {self.plat.nom}"
        elif self.produit_marche:
            return f"{self.quantite} x {self.produit_marche.nom}"
        else:
            return "Item sans produit"
