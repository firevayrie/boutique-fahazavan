"""Les produits et les contacts de la boutique.

Modifiez ce fichier pour changer un prix, une description, un stock...
Ensuite, lancez :  python reinitialiser_produits.py
(les demandes reçues via les formulaires sont conservées).
"""

# Numéros affichés pour passer commande par téléphone
CONTACTS = [
    {"affiche": "034 89 884 39", "tel": "0348988439"},
    {"affiche": "032 64 015 59", "tel": "0326401559"},
]

# (nom, description, prix en Ar, stock, catégorie, image dans static/produits/)
# Stock = nombre d'unités disponibles ; 0 = "Indisponible" sur le site.
PRODUITS = [
    (
        "Vinaigre de cidre – 1 L",
        "Vinaigre de cidre non pasteurisé et non filtré, en bouteille d'un litre. "
        "Pour assaisonner salades, sauces et marinades, ou en boisson rafraîchissante.",
        10000, 20, "Vinaigres de fruits", "vinaigre-cidre.jpg",
    ),
    (
        "Vinaigre de fruits Cidre & Fraise – 1 L",
        "Vinaigre de fruits cidre et fraise, non pasteurisé et non filtré, en bouteille d'un litre.",
        10000, 20, "Vinaigres de fruits", "vinaigre-fraise.jpg",
    ),
    (
        "Vinaigre de fruits Cidre & Goyave – 1 L",
        "Vinaigre de fruits cidre et goyave, non pasteurisé et non filtré, en bouteille d'un litre.",
        10000, 20, "Vinaigres de fruits", "vinaigre-goyave.jpg",
    ),
    (
        "Vinaigre de fruits Cidre & Mangue – 1 L",
        "Vinaigre de fruits cidre et mangue, non pasteurisé et non filtré, en bouteille d'un litre.",
        10000, 20, "Vinaigres de fruits", "vinaigre-mangue.jpg",
    ),
    (
        "Vinaigre de fruits Cidre & Ananas – 1 L",
        "Vinaigre de fruits cidre et ananas, non pasteurisé et non filtré, en bouteille d'un litre.",
        10000, 20, "Vinaigres de fruits", "vinaigre-ananas.jpg",
    ),
    (
        "Confiture de goyave",
        "Confiture de goyave en bocal.",
        8000, 20, "Confitures", "confiture-goyave.jpg",
    ),
    (
        "Pâte de fruits à la goyave",
        "Pâtes de fruits à la goyave, en boîtes de plusieurs tailles.",
        5000, 20, "Confiseries", "pate-de-fruits.jpg",
    ),
    (
        "Gingembre confit",
        "Gingembre confit, en boîtes de plusieurs tailles.",
        5000, 20, "Confiseries", "gingembre-confit.jpg",
    ),
]
