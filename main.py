"""
Escape game : quête dans le château au sommet du Python des Neiges
Auteur : Kino Saliba
Date début : 2020-11-13
Date de fin : 2020-11-15
Ce jeu est un escape game/un labyrinthe vue de dessus avec des objets à ramasser qui vous aideront
à répondre à des énigmes pour pouvoir progresser vers la but final.

Convention pour le système de coordonnées du module turtle, les indices de la matrice, et certaines variables :

*Le système de coordonnées du module turtle est (x, y) où x augmente de gauche à droite et y de bas en haut.
*Les indices de la matrice sont (i, j) où i augmente de haut en bas et représente les lignes de la matrice,
tandis que j augmente de gauche à droite et représente les colonnes de la matrice.

*Je choisis de terminer le nom des variables qui représentent un couple d'indice par '_mm',donc pour les matrices
*Je choisis de terminer le nom des variables qui représentent un couple de coordonnées par '_pp',
donc pour les pixels turtle.
*Je N'applique PAS ces conventions pour les variables fournies par le module CONFIGS.
Par exemple case_mm correspond aux indices dans la matrice d'une case du labyrinthe.

"""


import turtle
from CONFIGS import *


VIDE = 0
MUR = 1
BUT = 2
PORTE = 3
OBJET = 4


def creer_dictionnaire_des_objets(fichier_des_objets):
    """(fichier_des_objets : .txt) -> dict
    Renvoie le dictionnaire des objets et des questions à partir d'un fichier TXT et
    """

    dictionnaire = {}

    for line in open(fichier_des_objets, encoding='utf-8'):
        
        # Récupère les informations de la ligne lue avec eval, on suppose que la ligne peut être transformée en tuple.
        a, b = eval(line)
        # Ajoute la valeur b dans le dictionnaire avec la clé a,
        # a étant un tuple de int correspondant à la place dans la matrice de b qui est l'objet ou la question.
        dictionnaire[a] = b

    return dictionnaire


def lire_matrice(fichier):
    """(fichier : .txt) -> liste de listes de int
    Lis un fichier TXT encodant le plan du chateau et rend une matrice où la j-eme composante de la i-eme
    ligne de la matrice correspont au j-eme entier de la i-eme ligne du fichier.

    Hypothèses :
    *Chaque ligne du fichier contient le même nombre d'entiers
    *Les entiers sont séparé par des espaces.
    *Les entiers sont 0, 1, 2, 3, 4 et rien d'autre
    """
    # Ne pas oublier de refermer le fichier après coup avec with
    with open(fichier) as opened_file:
        result = [[int(i) for i in line.split()] for line in opened_file]
    return result


def calculer_pas(matrice):
    """(matrice : liste de listes de int) -> int
    Rend la longueur en pixel turtle du côté d'une case du plan du chateau en fonction de la taille de la matrice reçue.
    Etant donné qu'il y a 2 réponses, rend la taille minimal pour que le plan rentre dans la zone prévue.
    """

    return min((ZONE_PLAN_MAXI[1] - ZONE_PLAN_MINI[1]) // len(matrice),
               (ZONE_PLAN_MAXI[0] - ZONE_PLAN_MINI[0]) // len(matrice[0]))


def coordonnees(case_mm, cote_carre):
    """(case_mm : (int, int), cote_carre : int) -> (int, int)
    Calcul les coordonnées en pixels turtle du coin inférieur gauche d'une case du chateau,
    en fonction de case_mm : coordonnées de la case dans la matrice et cote_carre : taille du côté d'une case.
    """

    # Prend en compte la position point inférieur gauche du chateau pour calculer le point inférieur gauche d'une case.
    return ZONE_PLAN_MINI[0] + case_mm[1] * cote_carre, ZONE_PLAN_MAXI[1] - (case_mm[0] + 1) * cote_carre


def coordonnees_centre(case_mm, cote_carre):
    """(case_mm : (int, int), cote_carre : int) -> (int, int)
    Fait la même chose que la fonction coordonnees(), sauf qu'elle rend le couple de pixel turtle coorespondant au
    centre du carrée et non son coin inférieur gauche.
    """

    return coordonnees(case_mm, cote_carre)[0] + cote_carre // 2, coordonnees(case_mm, cote_carre)[1] + cote_carre // 2


def tracer_case(case_mm, couleur, cote_carre):
    """(case_mm : (int, int), couleur, cote_carre) -> None
    Trace une case selon sa position dans le plan et la couleur donnée.
    """

    turtle.goto(coordonnees(case_mm, cote_carre))  # on va là où l'argument case_mm demande.
    turtle.color(couleur)
    turtle.begin_fill()  # remplissage
    
    for i in range(4):  # Trace les contours du carré. La tortue doit toujours faire 0° avec l'axe des x avant le for.
        turtle.forward(cote_carre)
        turtle.left(90)

    turtle.end_fill()


def afficher_plan(matrice):
    """(matrice : liste de listes de int) : -> None
    Fonction qui trace le plan à partir de la matrice et du code couleur provenat de la lsite COULEURS du module
    CONFIGS.
    """
    
    n_lignes = len(matrice)
    n_colonnes = len(matrice[0])
    
    for i in range(n_lignes):

        for j in range(n_colonnes):

            # la convention i : lignes et j : colonnes est respectée par la fonction tracer_case.

            # my_pas la taille en pixels turtle du côté des cases est calculé une seule fois en début du code principal.
            # matrice[i][j] donne un int (0 à 4) donne la nature de la case.
            tracer_case((i, j), COULEURS[matrice[i][j]], my_pas)


def next_posi_its_type(matrice, mouvement_mm):
    """(matrice : liste de listes de int, mouvement_mm : couple de lint) -> (couple de int, int ou None)
    Renvoie la prochaine position couple de int selon la flèche pressée et le type de la
    case (vide, mur, but, porte, objet ou None) None pour le cas où on sort de la matrice.
    """
    
    next_posi_mm = [my_posi_mm[k] + mouvement_mm[k] for k in range(2)]  # Hypothétique prochaine position.

    # Vérifie si on sort pas de la matrice
    if 0 <= next_posi_mm[0] < len(matrice) and 0 <= next_posi_mm[1] < len(matrice[0]):

        # Si oui on récupère le type de la prochaine position.
        next_posi_type = matrice[next_posi_mm[0]][next_posi_mm[1]]

    # Si non on assigne la valeur None pour ne rien faire dans la fonction deplacer()
    else:
        next_posi_type = None

    return next_posi_mm, next_posi_type


def deja_vue_and_move_player(mouvement_mm):
    """(mouvement_mm : couple de int) -> None
    Déplace le personnage, marque la case précédente comme déjà-vue incrémente les composantes de my_position_mm
    par les composantes respectives de mouvement_mm.
    Mettre un nom plus explicite.
    """
    
    # Marque qu'on est déjà passé par là (efface le personnage,les portes et les objets de l'affichage du même coup).
    tracer_case(my_posi_mm, COULEUR_VUE, my_pas)

    my_posi_mm[0] += mouvement_mm[0]  # Change notre position.
    my_posi_mm[1] += mouvement_mm[1]

    turtle.goto(coordonnees_centre(my_posi_mm, my_pas))  # Tortue va à la nouvelle position.
    turtle.dot(my_size, COULEUR_PERSONNAGE)  # Replace le personnage.


def deplacer(matrice, mouvement_mm):
    """(matrice : liste de listes de int, mouvement_mm : couple de int) -> None
    Fonction qui déplace le personnage.
    Elle est appelée par les 4 fonctions qui captent si les flèches du clavier sont pressées ou pas.
    mouvement_mm est la direction de mouvement souhaitée.

    Si le mouvement souhaité fait :
    *sortir le personnage du plan, il ne se passe rien.
    *avancer le personnage vers un mur, il ne se passe rien.
    *avancer le personnage vers un objet, récupère l'objet.
    *avancer le personnage vers une porte, pose une question, si la réponse est correcte ouvre la porte et
    la fait disparaitre, si non ne fait rien.
    *avancer le personnage vers la case victoire et si le personnage a tous les objets,
    alors le but est atteint, si non dit au joueur de collecter tous les objets.
    """

    # Prochaine position et son type (VIDE, MUR, BUT, PORTE, OBJET ou None), None pour en dehors de la matrice.
    next_posi_mm, type_next_case = next_posi_its_type(matrice, mouvement_mm)

    # Important de NE PAS avoir de else au niveau du if ci-dessus, car les cas où on a mur/None ne sont pas traité.
    if type_next_case in (VIDE, OBJET):

        deja_vue_and_move_player(mouvement_mm)

        if type_next_case == OBJET:  # Sous-cas avec objet.

            ramasser_objet()  # Change matrice, récupère objet, l'annonce et met à jour l'inventaire
    
    elif type_next_case == BUT:

        if len(my_inv) == len(my_obj_dict):  # Impose de collecter tous les objets pour gagner.

            annonce('case jaune', 'victoire', None)  # Victoire et annonce.
            deja_vue_and_move_player(mouvement_mm)

        else:
            annonce('case jaune', 'pas tous les objets', None)  # Pas victoire et invite à rammasser tous les objets.

    elif type_next_case == PORTE:

        if poser_question(next_posi_mm):  # Si réponse correcte.

            annonce('porte', 'correcte', None)  # Annonce ouverture porte.

            deja_vue_and_move_player(mouvement_mm)  # Déplace le personnage.

            my_matrix[my_posi_mm[0]][my_posi_mm[1]] = 0  # Enlève la porte de la matrice.

        else:  # Si fausse réponse.
            annonce('porte', 'faux', None)  # Annonce fausse réponse.


def deplacer_gauche():
    """Fonction qui appel la fonction deplacer() avec comme argument pour mouvement_mm (0, -1),
    ce qui revient à ne pas changer de ligne dans la matrice, mais à reculer d'une colonne.
    """

    turtle.onkeypress(None, 'Left')  # Arrête la fenêtre Turtle d'écouter le clavier.
    deplacer(my_matrix, (0, -1))
    turtle.onkeypress(deplacer_gauche, 'Left')  # Remet la fenêtre Turtle sur écoute du clavier.


def deplacer_droite():
    """Même chose que pour deplacer_gauche(), sauf qu'on avance d'une colonne."""

    turtle.onkeypress(None, 'Right')
    deplacer(my_matrix, (0, 1))
    turtle.onkeypress(deplacer_droite, 'Right')


def deplacer_haut():
    """Même chose que pour deplacer_gauche(), sauf qu'on recule d'une ligne dans la matrice,
    mais on monte le personnage dans la fenêtre Turtle."""

    turtle.onkeypress(None, 'Up')
    deplacer(my_matrix, (-1, 0))
    turtle.onkeypress(deplacer_haut, 'Up')


def deplacer_bas():
    """Même chose que pour deplacer_gauche(), sauf qu'on avance d'une ligne dans la matrice,
    mais on descend le personnage dans la fenêtre Turtle."""
    
    turtle.onkeypress(None, 'Down')
    deplacer(my_matrix, (1, 0))
    turtle.onkeypress(deplacer_bas, 'Down')


def effacement_annonce():
    """ -> None
    Efface l'annonce en cours pour laisser place à la nouvelle annonce.
    """

    x_pp, y_pp = POINT_AFFICHAGE_ANNONCES
    delta_x_pp = 900
    delta_y_pp = 20
    
    turtle.goto(x_pp - 10, y_pp + delta_y_pp)  # Haut gauche zone affichage annonces.
    # Le -10 est pour prendre de la marge pour bien tout effacer.
    turtle.color('white')
    
    turtle.begin_fill()  # on efface l'annonce précédente en l'encadrant et avec une commande de remplissage.
    turtle.goto(x_pp + delta_x_pp, y_pp + delta_y_pp)  # Haut droite zone affichage annonces.
    turtle.goto(x_pp + delta_x_pp, y_pp - delta_y_pp)  # Bas droite zone affichage annonces.
    turtle.goto(x_pp - 10, y_pp - delta_y_pp)  # Bas gauche zone affichage annonces.
    turtle.end_fill()
    
    turtle.goto(x_pp, y_pp)  # on se met en position d'écriture.


def ramasser_objet():
    """ -> None
    Fonction qui rammasse l'objet et modifie la matrice pour l'en enlever et met à jour l'inventaire
    et les annonces.
    """

    my_matrix[my_posi_mm[0]][my_posi_mm[1]] = 0  # Remplace la case objet de la matrice par une case vide.

    objet_trouve = my_obj_dict[(my_posi_mm[0], my_posi_mm[1])]  # Trouve quel objet correspond à notre position acutelle
 
    my_inv.add(objet_trouve)  # Ajoute l'objet trouvé à l'inventaire.

    afficher_inventaire(objet_trouve)  # Fonctions d'affichage : inventaire et annonces
    annonce('objet', None, objet_trouve)


def afficher_inventaire(objet_trouve):
    """-> None
    Affiche l'objet qui vient de s'ajouter à l'invetaire.
    """

    # chaque commande write se faire à 30 pixel turtle de la précédente,
    # car la fonction est appelée à chaque fois que l'iventaire est mis à jour.
    turtle.goto(POINT_AFFICHAGE_INVENTAIRE[0], POINT_AFFICHAGE_INVENTAIRE[1] - 10 - 30 * len(my_inv))

    turtle.color('black')
    turtle.write('* ' + objet_trouve, font=('Consolas', 10, 'italic bold'))


def poser_question(next_posi_mm):
    """(next_posi_mm : couple de int) -> bool
    Fonction qui gère les annonces et les textinput en rapport aux portes.
    Elle renvoie True si le joueur répond correctement, False autrement
    """
    
    annonce('porte', 'fermée', None)
    
    # Demande de répondre à my_questions[tuple(next_posi_mm)][0]. my_question est un dictionnaire
    # de clés tuple (int, int) et de valeurs listes [questions, réponses].
    reponse = turtle.textinput('Question pour ouvrir la porte :', my_questions[tuple(next_posi_mm)][0])

    turtle.listen()  # Relance l'écoute du clavier après turtle.textinput

    return reponse == my_questions[tuple(next_posi_mm)][1]


def annonce(type_annonce, sous_type_annonce, objet_trouve):
    """(type_annonce : str, sous_type_annonce : str ou None, objet_trouve : str ou None) -> None
    Affiche les annonces lorsqu'on trouve un objet, veut franchir/franchit une porte, veut gagner/gagne.

    type_annonce désigne le type des annonces, sous_type_annonce si il existe est un sous-cas de type_annonce.
    objet_trouve si n'est pas None alors on met à jour l'inventaire.
    """

    effacement_annonce()  # Efface l'annonce qui est en place et se met en position annonces.
    turtle.color('#000000')  # Couleur noir pour écrire.
    
    if type_annonce == 'objet':  # Si on trouve un objet.
        turtle.write('Vous avez trouvé un nouvel objet : ' + objet_trouve, font=('Consolas', 10, 'bold'))

    elif type_annonce == 'porte':  # Si on veut franchir une porte.

        if sous_type_annonce == 'fermée':  # Si la porte est fermée.
            turtle.write('Cette porte est fermée !', font=('Consolas', 10, 'bold'))

        elif sous_type_annonce == 'correcte':  # Si la réponse à la question est correcte.
            turtle.write('Bonne réponse, la porte s\'ouvre !', font=('Consolas', 10, 'bold'))

        elif sous_type_annonce == 'faux':  # Si la réponse à la question est mauvaise.
            turtle.write('Mauvaise réponse !', font=('Consolas', 10, 'bold'))

    elif type_annonce == 'case jaune':  # Si on atteint l'objectif.

        if sous_type_annonce == 'victoire':  # Si on a tous les objets on gagne.
            turtle.write('Félicitation, vous avez gagné !', font=('Consolas', 14, 'bold '))

        elif sous_type_annonce == 'pas tous les objets':  # Si non.
            turtle.write('Vous devez rassembler tous les objets pour gagner !', font=('Consolas', 10, 'bold '))


# Définitions des variables nécessaires.
my_matrix = lire_matrice(fichier_plan)  # Matrice du plan
my_posi_mm = list(POSITION_DEPART)  # Position du personnage en terme de my_matrix
my_pas = calculer_pas(my_matrix)  # Dimension du côté des carrées en pixel turtle
my_size = my_pas * RATIO_PERSONNAGE  # Taille du personnage en pixel turtle
my_obj_dict = creer_dictionnaire_des_objets(fichier_objets)  # Dictionnaire des objets à trouver
my_inv = set()  # Inventaire du joueur qui contiendra les objets trouvés
my_questions = creer_dictionnaire_des_objets(fichier_questions)  # Dictionnaire des questionse et réponses


# Mise en place de la tortue.
turtle.tracer(0)  # Vitesse "instantanée".
turtle.up()  # Pas besoin de baisser la plume pour autre chose que le traçage.
turtle.hideturtle()


# Affiche la 1e annonce.
turtle.goto(POINT_AFFICHAGE_ANNONCES)
turtle.write('Menez votre personnage à l\'objectif en jaune', font=('Consolas', 12, 'bold'))


# Début de l'affichage de l'inventaire.
turtle.goto(70, 200)
turtle.write('Votre inventaire :', font=('Consolas', 12, 'bold'))


# Dessin du plan et du personnage
afficher_plan(my_matrix)
turtle.goto(coordonnees_centre(my_posi_mm, my_pas))  # Place le personnage au milieu de la case de départ.
turtle.dot(my_size, COULEUR_PERSONNAGE)


# Le joueur prend les commandes
turtle.listen()  # Déclenche l’écoute du clavier

turtle.onkeypress(deplacer_gauche, "Left")  # Associe à la touche Left ie flèche gauche la fonction deplacer_gauche.
turtle.onkeypress(deplacer_droite, "Right")  # Important que les fonctions appelées dans onkeypress n'aient pas de ().
turtle.onkeypress(deplacer_haut, "Up")
turtle.onkeypress(deplacer_bas, "Down")

turtle.mainloop()  # Place le programme en position d’attente d’une action du joueur
