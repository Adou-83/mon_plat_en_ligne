from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Plat, ProduitMarche, Commande, CommandeItem
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect
from .forms import CommandeForm
from django.contrib.auth.decorators import login_required

def accueil(request):
    return render(request, 'core/accueil.html')

def liste_plats(request):
    plats = Plat.objects.filter(disponible=True).select_related('categorie')
    return render(request, 'core/liste_plats.html', {'plats': plats})

def liste_produits_marche(request):
    produits = ProduitMarche.objects.all()
    return render(request, 'core/liste_produits_marche.html', {'produits': produits})

@require_POST
def ajouter_au_panier(request, type_produit, item_id):
    quantite = int(request.POST.get('quantite', 1))
    panier = request.session.get('panier', {})

    if type_produit not in panier:
        panier[type_produit] = {}

    if str(item_id) in panier[type_produit]:
        panier[type_produit][str(item_id)] += quantite
    else:
        panier[type_produit][str(item_id)] = quantite

    request.session['panier'] = panier

    if type_produit == 'plat':
        item = get_object_or_404(Plat, id=item_id)
    elif type_produit == 'marche':
        item = get_object_or_404(ProduitMarche, id=item_id)
    else:
        messages.error(request, "Type de produit inconnu.")
        return redirect('liste_plats')

    messages.success(request, f"{item.nom} ajouté au panier ({panier[type_produit][str(item_id)]} pcs).")
    return redirect('voir_panier')

def voir_panier(request):
    panier = request.session.get('panier', {})

    plats_ids = panier.get('plat', {}).keys()
    marche_ids = panier.get('marche', {}).keys()

    plats = Plat.objects.filter(id__in=plats_ids)
    produits_marche = ProduitMarche.objects.filter(id__in=marche_ids)

    panier_plats = []
    total_plats = 0
    for plat in plats:
        quantite = panier['plat'].get(str(plat.id), 0)
        total = plat.prix * quantite
        panier_plats.append({
            'item': plat,
            'quantite': quantite,
            'total': total,
        })
        total_plats += total

    panier_marche = []
    total_marche = 0
    for produit in produits_marche:
        quantite = panier['marche'].get(str(produit.id), 0)
        total = produit.prix * quantite
        panier_marche.append({
            'item': produit,
            'quantite': quantite,
            'total': total,
        })
        total_marche += total

    total_general = total_plats + total_marche

    return render(request, 'core/panier.html', {
        'panier_plats': panier_plats,
        'panier_marche': panier_marche,
        'total_plats': total_plats,
        'total_marche': total_marche,
        'total_general': total_general,
    })

@require_POST
def modifier_quantite_panier(request, type_produit, item_id):
    quantite = int(request.POST.get('quantite', 1))
    panier = request.session.get('panier', {})

    if type_produit in panier and str(item_id) in panier[type_produit]:
        panier[type_produit][str(item_id)] = quantite
        request.session['panier'] = panier
        messages.success(request, "Quantité modifiée.")
    else:
        messages.error(request, "Article non trouvé dans le panier.")
    return redirect('voir_panier')

@require_POST
def supprimer_du_panier(request, type_produit, item_id):
    panier = request.session.get('panier', {})
    if type_produit in panier and str(item_id) in panier[type_produit]:
        del panier[type_produit][str(item_id)]
        request.session['panier'] = panier
        messages.success(request, "Article supprimé du panier.")
    else:
        messages.error(request, "Article non trouvé dans le panier.")
    return redirect('voir_panier')

@login_required
def passer_commande(request):
    if request.method == 'POST':
        form = CommandeForm(request.POST)
        if form.is_valid():
            commande = form.save(commit=False)
            commande.utilisateur = request.user
            commande.save()
            form.save_m2m()  # si nécessaire
            return redirect('confirmation_commande')  # Redirige vers confirmation
    else:
        form = CommandeForm()

    return render(request, 'commande/passer_commande.html', {'form': form})


def confirmation_commande(request):
    return render(request, 'commande/confirmation_commande.html')



def valider_commande(request):
    # Logique de validation simple (à améliorer ensuite si tu veux)
    # Par exemple, tu peux afficher un message ou rediriger vers une page de confirmation
    return redirect('confirmation_commande')
