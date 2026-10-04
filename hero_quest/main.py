from time import *
class hero():
    def __init__(self,name,health,armor,power,weapon):
        self.name=name
        self.health=health
        self.armor=armor
        self.power=power
        self.weapon=weapon
    def print_info(self):
        print('Поприветсвуйте героя-', self.name)
        print('Уровень здоровья-',self.health)
        print('Класс брони-',self.armor)
        print('Сила атаки-',self.power)
        print('Оружие:',self.weapon)
    def strike(self,enemy):
        print(self.name,'атакует',enemy.name,'с силой',str(self.power),'используя',self.weapon+'\n')
        enemy.armor -= self.power
        if enemy.armor<0:
            enemy.health += enemy.armor
            enemy.armor=0
    def fight(self,enemy):
        while self.health and enemy.health>0:
            self.strike(enemy)
            if enemy.health<=0:
                print(enemy.name,'Пал в этом нелёгком бою!\n')
                break
            sleep(2)
            enemy.strike(self)
            if self.health<=0:
                print(self.name,'Пал в этом нелёгком бою!\n')
                break
            sleep(2)
        if knight.health >0:
            knight.healt=100
            knight.power*=2
            knight.armor=10*2
            print(knight.name,'стал сильнее и опытнее.Теперь его сила:',str(knight.power),',а его класс брани:',str(knight.armor))            
print('Средиземье в опасности!В королевстве буйствуйт разбойники и драконы.На помощь королевству спешит рыцарь...')
knight=hero('Ричард',100,20,20,'меч')
knight.print_info()
print('Ричард бредёт по лесу.По всюду туман.Нечего не видно.Из-за угла его атакует бандит!')
vilian=hero('Борис',25,10,7,'нож')
vilian.print_info()
knight.fight(vilian)
print('Выйдя из лесу Ричард увидел дракона и его логово')
dragon=hero('Дракон',100,35,30,'пламя')
dragon.print_info()
knight.fight(dragon)
print('После победы над драконом в королевстве настал покой...')





#####





from time import sleep

class Hero():
    #конструктор класса
    def __init__(self, name, health, armor):
        self.name = name
        self.health = health #число
        self.armor = armor #строка
    #печать параметров персонажа
    def print_info(self):
        print('Уровень здоровья:', self.health)
        print('Класс брони:', self.armor, '\n')
class Warrior(Hero):
    def __init__(self, name, health, armor,power):
        super().__init__(name,health,armor,)
        self.power=30
    def hello(self):
        print('Верхом на коне появился бравый воин по имени', self.name)
        self.print_info()
        sleep(4)
    def attack(self,enemy):
        print('Удар! Храбрый воин',self.name,'атакует',enemy.name,'мечом!')
        print('Страшный ударобрушился на противника')
        enemy.armor -= self.power
        if enemy.armor<0:
            enemy.health += enemy.armor
            enemy.armor=0
        print('Теперь его броня упала до-',enemy.armor,'a его здоровье-',enemy.health)
war=Warrior('Остин',100,50,30)
war.hello()
class Wizzard(Hero):
    def __init__(self, name, health, armor,power):
        super().__init__(name,health,armor,)
        self.power=50
    def hello(self):
        print('Откуда ни возмись появился искусстный волшебник ', self.name)
        self.print_info()
        sleep(4)
    def attack(self,enemy):
        print('Удар! Ловкий маг',self.name,'атакует',enemy.name,'накладывая заклинание!')
        print('Мощное заклинание истезает противника')
        enemy.armor -= self.power
        if enemy.armor<0:
            enemy.health += enemy.armor
            enemy.armor=0
        print('Теперь его броня упала до-',enemy.armor,'a его здоровье-',enemy.health)
mag=Wizzard('Гарольд',85,35,50)
mag.hello()
war.attack(mag)
