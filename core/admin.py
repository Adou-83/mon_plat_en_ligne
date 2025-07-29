from django.contrib import admin
from .models import Plat, Commande, ProduitMarche, Cuisinier, CommandeItem

@admin.register(Plat)
class PlatAdmin(admin.ModelAdmin):
    list_display = ('nom', 'categorie', 'prix', 'disponible')
    list_filter = ('disponible', 'categorie')
    search_fields = ('nom',)

@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ('nom_client', 'get_plats', 'get_quantite_totale', 'date_commande')
    list_filter = ('date_commande',)
    search_fields = ('nom_client',)

    def get_plats(self, obj):
        return ", ".join([item.plat.nom for item in obj.items.all() if item.plat])
    get_plats.short_description = 'Plats'

    def get_quantite_totale(self, obj):
        return sum(item.quantite for item in obj.items.all())
    get_quantite_totale.short_description = 'Quantité totale'

@admin.register(ProduitMarche)
class ProduitMarcheAdmin(admin.ModelAdmin):
    list_display = ('nom', 'quantite', 'unite', 'prix')
    search_fields = ('nom',)

@admin.register(Cuisinier)
class CuisinierAdmin(admin.ModelAdmin):
    list_display = ('nom', 'specialite')
    search_fields = ('nom', 'specialite')
