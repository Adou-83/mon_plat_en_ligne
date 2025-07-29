from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('plats/', views.liste_plats, name='liste_plats'),
    path('marche/', views.liste_produits_marche, name='liste_produits_marche'),
    path('panier/', views.voir_panier, name='voir_panier'),
    path('', views.liste_plats, name='liste_plats'),
    path('marche/', views.liste_produits_marche, name='liste_produits_marche'),

    path('panier/', views.voir_panier, name='voir_panier'),

    path('panier/ajouter/<str:type_produit>/<int:item_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('panier/modifier/<str:type_produit>/<int:item_id>/', views.modifier_quantite_panier, name='modifier_quantite_panier'),
    path('panier/supprimer/<str:type_produit>/<int:item_id>/', views.supprimer_du_panier, name='supprimer_du_panier'),

    path('commande/valider/', views.valider_commande, name='valider_commande'),
    path('commande/confirmation/', views.confirmation_commande, name='confirmation_commande'),
    path('commande/passer/', views.passer_commande, name='passer_commande'),

]
