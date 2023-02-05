from car import Car

# On a importé sleep pour mettre, si on le souhaite,
# un délai entre chaque mise à jour de l'écran.
from time import sleep

# On a importé system pour pouvoir nettoyer la console
# à chaque mise à jour.
from os import system

road_lenght = 100
deceleration_probability = 0.1

# La classe Road contient 3 attributs utilisés et 2 peu utilisés :
# - Une variable cars de type list qui contient l'ensemble des voitures
# - Une variable road de type list qui contient les données d'affichage
# de la route. Un point signifie qu'il n'y a pas de voiture, un X l'inverse
# Une variable collisions de type int qui contient le nombre de collisions
# produites par le modèle. Elle est là comme preuve de son efficacité.
# ------
# - Une variable right_way de type list servant à initialiser la variable
# road en moins de ligne.
# - Une variable left_way de type list servant à initialiser la variable
# road en moins de ligne.

class Road:
    # Constructeur de la classe Road
    def __init__(self, car_list):
        self.cars = car_list
        self.right_way = ['.' for i in range(road_lenght)]         
        self.left_way = ['.' for i in range(road_lenght)]
        self.road = [self.left_way, self.right_way]
        self.collisions = 0

    # On récupère la voiture (notamment pour sa vitesse) à partir de sa position
    def getCarByPosition(self, position):
        for car in self.cars:
            if car.getPosition() == position:
                return car
        
        return False
    
    # On récupère la distance entre la voiture actuelle et la voiture la plus
    # proche en avant
    def getDistanceNearestCarOnWay(self, way, car):
        for i in range(car.getPosition()[1], car.getPosition()[1] + 8):
            if self.road[way][(i + 1) % road_lenght] == 'X':
                return ((i - car.getPosition()[1]) % road_lenght)
        
        return road_lenght

    # On récupère la distance entre la voiture actuelle et la voiture la plus
    # proche en avant
    def getDistanceNearestCarOnWayBack(self, way, car):
        for i in range(car.getPosition()[1],  car.getPosition()[1] + 8):
            if self.road[way][(car.getPosition()[1] - i - 1) % road_lenght] == 'X':
                return (i - car.getPosition()[1]) % road_lenght
        
        return road_lenght

    # On applique les positions (à faire après l'appel du constructeur)
    def applyPosition(self):
        for i in range(len(self.cars)):
            if self.cars[i].getPosition()[0] == 0:
                self.road[0][self.cars[i].getPosition()[1]] = 'X'
            
            elif self.cars[i].getPosition()[0] == 1:
                self.road[1][self.cars[i].getPosition()[1]] = 'X'

    # On regarde si au moins une collision s'est produite lors de l'itération.
    # Pour se faire, on range les positions des voitures dans des listes (une
    # pour chaque voie) et on utilise la fonction set qui enlève n'autorise
    # que les valeurs en unique exemplaire. On compare ensuite la taille des
    # listes.
    def checkCollision(self):
        right_dup = []
        left_dup = []

        for car in self.cars:
            if car.getPosition()[0] == 0:
                left_dup.append(car.getPosition()[1] % 100)
            else:
                right_dup.append(car.getPosition()[1] % 100)

        if len(right_dup) != len(set(right_dup)):
            return True

        if len(left_dup) != len(set(left_dup)):
            return True

        return False

    # On met à jour la route en appliquant les règles de notre modèle. Pour se faire,
    # on sépare d'abord les voitures en fonction de leur voie, puis on leur applique
    # les règles en fonction des cas.
    def update(self):
        self.lastRoad = ''.join(['|', ''.join(self.road[0]), '|\n|', ''.join(self.road[1]), '|']) +'\n' + (' ' * 49 ) + '50'
        for i in range(len(self.cars)):
            # On commence par remplacer tous les caractères de la route par des points,
            # puis on applique la possible réduction de vitesse. Si elle n'a pas lieu,
            # on accélère par défaut.
            self.road[self.cars[i].getPosition()[0]][self.cars[i].getPosition()[1]] = '.'
            self.cars[i].randomDeceleration(deceleration_probability)

            if not self.cars[i].getStatus():
                self.cars[i].accelerate(0)

            # Séparation des voitures selon leur voie.
            if self.cars[i].getPosition()[0] == 1:
                # On regarde si la vitesse de la voiture à droite est trop élevée par
                # rapport à la distance qui la sépare de la voiture la plus proche en avant.
                # Si la condition est remplie, une condition doit être évitée.
                if self.cars[i].getSpeed() >= self.getDistanceNearestCarOnWay(1, self.cars[i]):
                    # Si oui, on regarde s'il y a de la place direcetement à gauche pour un possible dépassement.
                    if self.road[0][self.cars[i].getPosition()[1]] == '.':
                        # On regarde si la voiture peut accélérer à gauche (donc si elle en a l'espace)
                        if 6 >= self.getDistanceNearestCarOnWay(0, self.cars[i]):
                            # Si la condition n'est pas remplie, la voiture décélère.
                            self.cars[i].requiredDeceleration(self.getDistanceNearestCarOnWay(self.cars[i].getPosition()[0], self.cars[i]))

                        else:
                            # Si la condition est remplie, la voiture change de voie et accélère.
                            self.cars[i].switchWay()
                            self.cars[i].setSpeed(6)

                    else:
                        # Si la condition n'est pas remplie, la voiture décélère.
                        self.cars[i].requiredDeceleration(self.getDistanceNearestCarOnWay(self.cars[i].getPosition()[0], self.cars[i]))
                # Si la condition n'est pas remplie (c'est-à-dire que la voiture en avant est assez loin),
                # alors toutes les actions ont déjà été posées.

            else:    
                # Après un dépassement, une voiture cherche à revenir sur la voie de droite.
                if self.road[1][self.cars[i].getPosition()[1]] == '.':
                    # On regarde si la vitesse de la voiture est trop élevée pour revenir sur la voie de droite.
                    if self.cars[i].getSpeed() >= self.getDistanceNearestCarOnWay(1, self.cars[i]):
                        # Si la distance entre la voiture actuelle et celle de devant est inférieure ou égale à la
                        # vitesse de la première, il faut décélérer.
                        if self.cars[i].getSpeed() >= self.getDistanceNearestCarOnWay(0, self.cars[i]):
                            self.cars[i].requiredDeceleration(self.getDistanceNearestCarOnWay(self.cars[i].getPosition()[0], self.cars[i]))

                    # On regarde si la voiture a suffisament d'espace en avant et en arrière d'elle (à droite) pour changer de voie
                    else:
                        if self.cars[i].getSpeed() > self.getDistanceNearestCarOnWayBack(1, self.cars[i]) or self.getDistanceNearestCarOnWayBack(1, self.cars[i]) > 5:
                            self.cars[i].switchWay()
                            self.cars[i].rightWayDeceleration()

                        # Dans ce cas, la voiture ne peut que décélérer.
                        else:
                            if self.cars[i].getSpeed() >= self.getDistanceNearestCarOnWay(0, self.cars[i]):
                                self.cars[i].requiredDeceleration(self.getDistanceNearestCarOnWay(self.cars[i].getPosition()[0], self.cars[i]))

                else:
                    # Dans ce cas, la voiture ne peut que décélérer.
                    if self.cars[i].getSpeed() >= self.getDistanceNearestCarOnWay(0, self.cars[i]):
                        self.cars[i].requiredDeceleration(self.getDistanceNearestCarOnWay(self.cars[i].getPosition()[0], self.cars[i]))                  

            # On fait bouger les voitures et on met à jour leur position.
            self.cars[i].move()
            self.road[self.cars[i].getPosition()[0]][self.cars[i].getPosition()[1]] = 'X'
            
        if self.checkCollision():
            self.collisions += 1

    # On affiche efficacement la route.
    def display(self):
        print(''.join(['|', ''.join(self.road[0]), '|\n|', ''.join(self.road[1]), '|']) +'\n' + (' ' * 49 ) + '50')

    # Fonction permettant la simulation.
    def mainloop(self):
        for i in range(500):
            print('Itération  : ' + str(i))
            self.display()
            self.update()
            self.display()
            # On met cette ligne au besoin si l'on veut bien observer le
            # mouvement des voitures
            # sleep(0.05)
            system('cls')

            print('Collisions : ' + str(self.collisions))