from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Plat, ProduitMarche
from django.contrib.auth.decorators import login_required
from .models import Commande, CommandeItem

def accueil(request):
    return render(request, 'core/accueil.html')

def liste_plats(request):
    query = request.GET.get('q', '')
    if query:
        plats = Plat.objects.filter(nom__icontains=query, disponible=True)
    else:
        plats = Plat.objects.filter(disponible=True)
    return render(request, 'core/liste_plats.html', {'plats': plats, 'query': query})

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
        return redirect('accueil')

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
            'plat': plat,
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
            'nom': produit.nom,
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

 
def passer_commande(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        telephone = request.POST.get('telephone')
        adresse = request.POST.get('adresse')

        if nom and telephone and adresse:
            panier = request.session.get('panier', {})
            if not panier:
                messages.error(request, "Votre panier est vide.")
                return redirect('voir_panier')

            commande = Commande.objects.create(
                nom_client=nom,
                telephone=telephone,
                adresse_livraison=adresse,
                total=0,
                cuisinier=None
            )

            total_commande = 0

            for plat_id, quantite in panier.get('plat', {}).items():
                plat = get_object_or_404(Plat, id=plat_id)
                CommandeItem.objects.create(
                    commande=commande,
                    plat=plat,
                    quantite=quantite
                )
                total_commande += plat.prix * quantite

            for produit_id, quantite in panier.get('marche', {}).items():
                produit = get_object_or_404(ProduitMarche, id=produit_id)
                CommandeItem.objects.create(
                    commande=commande,
                    produit_marche=produit,
                    quantite=quantite
                )
                total_commande += produit.prix * quantite

            commande.total = total_commande
            commande.save()

            request.session['panier'] = {}
            messages.success(request, "Commande enregistrée avec succès ✅")
            return redirect('accueil')

        else:
            messages.error(request, "Veuillez remplir tous les champs ❌")
            # Redessine le formulaire rempli, si besoin tu peux aussi renvoyer les données saisies
            return render(request, "commande/passer_commande.html")

    # 👉 Manquait ce return pour les requêtes GET
    return render(request, "commande/passer_commande.html")
