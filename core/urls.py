from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('plats/', views.liste_plats, name='liste_plats'),
    path('marche/', views.liste_produits_marche, name='liste_produits_marche'),
    path('panier/', views.voir_panier, name='voir_panier'),
    path('panier/ajouter/<str:type_produit>/<int:item_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('passer-commande/', views.passer_commande, name='passer_commande'),
]
