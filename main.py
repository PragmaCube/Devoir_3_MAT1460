# Programmé par 20244742
# Équipe 20244742, 20243840, 20256966, 20128333

# Pour bien comprendre le programme, il est important
# de lire les commentaires qui apportent de précieuses
# informations. À noter que le programme est écrit en
# anglais pour respecter les standards d'industrie.

# La simulation consiste en 500 itérations montrant les
# voitures se déplaçant en fonction des règles du modèle.


from road import *

# On importe random pour générer de manière aléatoire
# la position des voitures.
from random import random

cars = []

# Au sujet des collisions et de la génération des positions
# des voitures.
# Le modèle évite les collisions lorsqu'elles ne sont pas 
# présentes initialement. Dans le cas contraire, cela dépend
# des densités de voiture sur la route et de la disposition
# des voitures :
# - En cas de faible densité de trafic (< 27 voitures), il 
# est préférable que les voitures aient entre 4/5 et 7/8 cases 
#d'écart pour éviter les collisions en début de simulation. 
# C'est correct puisque dans la réalité ce cas ne constitue 
#pas de réel trafic et les voitures gardent souvent une 
# certaine distance entre elles.
# - En cas de forte densité (27 < voitures < 75), il est 
# préférable que les voitures aient 3/4 cases d'écart pour
# éviter les collisions (attention, vers 75 cela commence à
# être très aléatoire). C'est aussi correct et pour la même
# raison (mais dans l'autre sens).
# - En cas de très fortes densités (75 < voitures < 127), le
# modèle ne permet pas d'éviter les collisions immédiatement,
# mais après un certain nombre d'itérations (qui dépend
# directement de la densité) le modèle permet aux voitures de
# se déplacer sans collision.
# - En cas d'extrême densité (> 127 voitures), le modèle ne 
# permet pas d'éviter sufisamment de collisions (les voitures
# sont en collisions dès l'itération 1).

while True:
    for i in range(35):
        cars.append(Car(round((random() * 10) % 5 + 1), [round(random() * 10) % 2, 3 * i + 1]))
    
    road = Road(cars)

    # On s'assure de commencer le programme en ayant aucune collisions.
    if not (road.checkCollision()):
        break
    
road.applyPosition()
road.mainloop()