# Snake le jeu vidéo 02/05/2020
# Author : Kevin Dufour (Pardival)

from tkinter import *
import random

# Variables
hx = 0 			# Position x de base du serpent (int) 
hy = 0 			# Position y de base du serpent (int)

x = 10			# Mouvement du serpent sur l'abscise (vers la droite par defaut) (int)
y = 0			# Mouvement du serpent sur l'ordonnée (int)

x_food = 150	# Position x de la nourriture 
y_food = 150	# Position y de la nouriture

score = 0		# Score du joueur

direction = 3 	# Définit la direction du serpent (0 => bas, 1 => haut, 2 => gauche, 3 => droite) (int)

snake_body_position = []	# On stock les position du corps du serpent
snake_head_position = []	# On stock la position de la tête du serpent
snake_body = []				# On stock les rectangle déssiné

# Création de mon interface avec config de base
master = Tk()
master.title("Snake")
master.geometry("400x400")
master.minsize(720,480)
master.iconbitmap("zukzuk.ico")
master.config(background="#000000")

# Création du canvas
canvas = Canvas(master, width=720, height=480, bg="black")
canvas.pack()

# Création du serpent
head = canvas.create_rectangle(0,0,10,10)
canvas.itemconfig(head, fill='red')
snake_body.append(head)

# Création de la nourriture du serpent
food = canvas.create_rectangle(150,150,160,160)
canvas.itemconfig(food, fill='blue')

#====================================================================#

label_score = Label(canvas, fg="green", text=score, bg="black", font=("Arial",20))
canvas.create_window(690,30, window=label_score)

#====================================================================#

# Anime le deplacement du serpent 
def deplacement(x,y) :
	# On récupère les variables de postions
	global hx, hy, score
	hx = hx + x
	hy = hy + y

	# deplacement de la tête du serpent
	canvas.coords(head, hx, hy, hx + 10, hy + 10)

	# On construit la queu du serpent
	i = 0
	e = len(snake_body)
	j = len(snake_body_position)

	while i < score :
		i+=1
		canvas.coords(snake_body[e-i], snake_body_position[j-i][0], snake_body_position[j-i][1], 
			snake_body_position[j-i][0]+10, snake_body_position[j-i][1]+10 )

	# On stock la position de la tête du serpent à chaque deplacement
	snake_head_position = []
	snake_head_position.append(hx)
	snake_head_position.append(hy)
	snake_body_position.append(snake_head_position)

# Mouvement vers le haut
def move_up(event) :
	global direction, x, y

	# Si le serpent n'avance pas dans la direction opposé 
	if direction != 1 :
		# On change les variable de diretion 
		direction = 0
		x = 0
		y = -10

# Mouvement vers le bas
def move_down(event) :
	global direction, x, y

	# Si le serpent n'avance pas dans la direction opposé 
	if direction != 0 :
		# On change les variable de diretion 
		direction = 1
		x = 0
		y = 10

# Mouvement vers la gauche
def move_left(event) :
	global direction, x, y

	# Si le serpent n'avance pas dans la direction opposé 
	if direction != 3 :
		# On change les variable de diretion 
		direction = 2
		x = -10
		y = 0

# Mouvement vers la droite
def move_right(event) :
	global direction, x, y

	# Si le serpent n'avance pas dans la direction opposé 
	if direction != 2 :
		# On change les variable de diretion 
		direction = 3
		x = 10
		y = 0

# Créer la nourriture du serpent
def create_food() :
	global food, x_food, y_food

	rand_number_x = random.randint(0, 71) * 10
	rand_number_y = random.randint(0, 48) * 10
	x_food = rand_number_x
	y_food = rand_number_y

	# On supprime la nourriture stocké
	canvas.delete(food)

	# On recréee la nourriture
	food = canvas.create_rectangle(rand_number_x, rand_number_y, rand_number_x + 10, rand_number_y + 10)
	canvas.itemconfig(food, fill='blue')

# Détecte si le serpent mange la nourriture
def collision_food() : 
	global x_food, y_food, hy, hx, score

	# On observe la detection d'une collision avec la nourriture 
	if (hx < x_food + 10 and
	hx + 10 > x_food and
	hy < y_food + 10 and
	hy + 10 > y_food) :
		create_food()
		add_body()
		score+=1
		label_score.configure(text=score) 

# Détecte si le serpent se mange ou prend un mur
def collision() :
	# Collision avec le serpent
	i = 0
	j = len(snake_body_position) - 1	# On soustrait un pour que la tête ne soit pa prise en compte
	while i < score :
		i+=1
		if (hx < snake_body_position[j-i][0] + 10 and
			hx + 10 > snake_body_position[j-i][0] and
			hy < snake_body_position[j-i][1] + 10 and
			hy + 10 > snake_body_position[j-i][1]) :
			print("collision corps")
			return True

	# Collision avec les murs
	if (hx + 10 > 720 or
		hx < 0 or
		hy + 10 > 480 or
		hy < 0) :
		print("collision mur")
		return True
			

# On permet de faire agrandir le corps du serpent
def add_body() :
	length = len(snake_head_position)
	last_head_position_x = snake_body_position[length-2][0]
	last_head_position_y = snake_body_position[length-2][1]

	body = canvas.create_rectangle(last_head_position_x, last_head_position_y, last_head_position_x + 10, last_head_position_y + 10)
	canvas.itemconfig(body, fill='red')
	snake_body.append(body)

def recall() :
	global hx, x_food
	deplacement(x,y)
	collision_food()
	if collision() :
		reset() 
	master.after(100, recall)

# Permet de reset le jeu
def reset() :
	global x, y, snake_body, snake_body_position, snake_head_position
	global hx,hy,direction, score, head

	for cube in snake_body :
		canvas.delete(cube)

	score = 0
	x = 10
	y = 0
	snake_body = []
	snake_body_position = []
	snake_head_position = []
	hx = 0
	hy = 0
	direction = 3

	head = canvas.create_rectangle(0,0,10,10)
	canvas.itemconfig(head, fill='red')
	snake_body.append(head)
	label_score.configure(text=score) 

# On lie les touches du clavier ax fonctions de déplacmaster.bind("<Down>", move_down)
master.bind("<Up>", move_up)
master.bind("<Left>", move_left)
master.bind("<Right>", move_right)
master.bind("<Down>", move_down)

# On appel les fonctions nécéssaire au fonctionnement du jeu
recall()

master.mainloop()