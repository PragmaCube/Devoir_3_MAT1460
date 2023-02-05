from random import random

# La classe Car contient 3 attributs distincts :
# - Une variable speed de type int avec une vitesse variant 
# entre 1 et 5 (ou 6)
# - Une variable position de type list qui contient 2 int,
# un pour la voie (0 : gauche, 1 : droite) et l'autre pour la
# position sur la voie (entre 0 et 99)
# - Une variable random_deceleration_status de type bool indiquant si la voiture a décéléré
# de manière aléatoire (et ainsi lui empêcher d'accélérer)

class Car:
    # Constructeur de la classe Car
    def __init__(self, initial_speed, initial_position):
        self.speed = initial_speed
        self.position = initial_position
        self.random_deceleration_status = False

    ##############################
    # Méthodes get et set typiques
    def getSpeed(self):
        return self.speed

    def getPosition(self):
        # Ici on veut s'assurer de renvoyer une position inférieure à 100
        return [self.position[0], self.position[1] % 100]

    def getStatus(self):
        return self.random_deceleration_status

    def setPosition(self, position):
        self.position = position

    def setSpeed(self, speed):
        if speed > 5:
            self.speed = 5
        else:
            self.speed = speed
    ########################################

    # On évite de mettre une structure conditionnelle
    # en utilisant l'opérateur %
    def switchWay(self):
        self.position[0] = (self.position[0] + 1) % 2

    ########################################
    # Dans cette section, les méthodes renvoient un
    # booléen. Il s'agit seulement d'une méthode de
    # débogage.
    # Le paramètre way_speed_difference sert seulement à
    # indiquer que sur la voie de gauche la vitesse pour
    # aller jusqu'à 6, et non 5.
    def accelerate(self, way_speed_difference):
        if self.speed < 5 + way_speed_difference:
            self.speed += 1

            return True

        return False

    def requiredDeceleration(self, new_speed):
        if new_speed > 1 and new_speed < 5:
            self.speed = new_speed

        else:
            self.speed = 1

        return False

    def randomDeceleration(self, probability):
        if random() < probability and self.speed > 1:
            self.speed -= 1
            self.random_deceleration_status = True

            return True

        self.random_deceleration_status = False

        return False

    # Méthode appellée seulement lorsqu'une voiture
    # revient sur la voie de droite.
    def rightWayDeceleration(self):
        if self.speed == 6:
            self.speed = 5

            return True

        return False
    ########################################

    def move(self):
        self.position[1] += self.speed