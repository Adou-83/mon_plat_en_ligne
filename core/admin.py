from django.contrib import admin
from .models import Categorie, Plat, ProduitMarche, Cuisinier, Commande, CommandeItem

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)

@admin.register(Plat)
class PlatAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prix', 'quantite_disponible', 'disponible', 'categorie')
    list_filter = ('disponible', 'categorie')
    search_fields = ('nom', 'description')
    readonly_fields = ()
    
@admin.register(ProduitMarche)
class ProduitMarcheAdmin(admin.ModelAdmin):
    list_display = ('nom', 'quantite', 'unite', 'prix')
    search_fields = ('nom',)

@admin.register(Cuisinier)
class CuisinierAdmin(admin.ModelAdmin):
    list_display = ('nom', 'specialite', 'telephone')
    search_fields = ('nom', 'specialite')

class CommandeItemInline(admin.TabularInline):
    model = CommandeItem
    extra = 1

@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom_client', 'date_commande', 'total', 'cuisinier')
    list_filter = ('date_commande', 'cuisinier')
    search_fields = ('nom_client', 'adresse_livraison', 'telephone')
    inlines = [CommandeItemInline]

@admin.register(CommandeItem)
class CommandeItemAdmin(admin.ModelAdmin):
    list_display = ('commande', 'plat', 'produit_marche', 'quantite')
    search_fields = ('plat__nom', 'produit_marche__nom')
