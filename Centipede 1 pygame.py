import pygame
import math
from pygame.locals import*
from pygame.time import*
from random import randint
pygame.init()

clock = Clock()


speed = 5

HEIGHT = 600
WIDTH = 400
sizeScreen = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption("Modified Atari Centipede")

shooter = pygame.image.load ("otis's better shooter.jpg")

target = pygame.image.load("Target.png")

centipedeHead = pygame.image.load("Otis's cooler centipede head.jpg")

pygame.mouse.set_visible(False)

mushroom = pygame.image.load("otis's cooler mushroom.jpg")

halfMushroom = pygame.image.load("otis's cooler mushroom - Copy.jpg")

quarterMushroom = pygame.image.load("quartermush.jpg")

lives3 = pygame.image.load("lives3.jpg")

mushroomLocations = []
while len(mushroomLocations) < 40:
	x = randint(0,19)
	y = randint(1,28)
	if [x,y,3] not in mushroomLocations:
		mushroomLocations.append([x,y,3])

centipedeLocations = []

def centipedeReset():
	global centipedeLocations
	centipedeLocations = []

	for i in range(12):
		#                             x,y,dir,ydest,atYDest,Up/Down
		centipedeLocations.append([i*20,0,  1,     0,  True,     1])
centipedeReset()

shots = []
lastShot = 0

def main():
	global lastShot
	shooterPosition = [200.0,500.0]
	game = 3
	while game:
		keys = pygame.key.get_pressed()
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				game = 0
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					game = 0
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1 and pygame.time.get_ticks() > lastShot + 250:
					shots.append([shooterPosition[0]+8, shooterPosition[1]- 4])
					lastShot = pygame.time.get_ticks()
		sizeScreen.fill((0,0,0))
		mouseX, mouseY = pygame.mouse.get_pos()
		mouseX = min(mouseX, 380)
		mouseY = min(mouseY, 580)
		# shooterPosition = mouseX, mouseY
		targetPosition = mouseX, mouseY
		sizeScreen.blit(target, targetPosition)

		xDiff = mouseX - shooterPosition[0]
		yDiff = mouseY - shooterPosition[1]
		norm = math.sqrt(xDiff**2+yDiff**2)
		if norm<speed:
			newShooterPosition = [mouseX, mouseY]
		else:
			newShooterPosition = shooterPosition [::]
			newShooterPosition[0] += xDiff*speed/norm
			newShooterPosition[1] += yDiff*speed/norm
		

		for centipedeLocation in centipedeLocations:

			centipedeLocation[4] = centipedeLocation[3] == centipedeLocation[1]

			if not centipedeLocation[4]:
				centipedeLocation[1] += 4 * centipedeLocation[5]
			elif centipedeLocation [2] %2 == 0:
				centipedeLocation[0] -= 4
			else:
				centipedeLocation[0] +=4
		for shotsFired in shots[:]:
			shotsFired[1] -= 5
			pygame.draw.line(sizeScreen, (255,255,255), shotsFired, [shotsFired[0], shotsFired[1] - 10])
			#line(Surface, color, start_pos, end_pos, width=1) -> Rect
			for centipedeLocation in centipedeLocations[:]:
				centipedeRect = pygame.Rect(centipedeLocation[0], centipedeLocation[1], 15,17)
				shotRect = pygame.Rect(shotsFired[0],shotsFired[1],1,10)
				if shotRect.colliderect(centipedeRect):
					if shotsFired in shots:
						shots.remove(shotsFired)
					centipedeLocations.remove(centipedeLocation)
					mushroomLocations.append([round(centipedeLocation[0]/20),round(centipedeLocation[1]/20),3])

		canMoveDiag = True
		canMoveX = True
		canMoveY = True
		for thisMushroom in mushroomLocations:
			shooterRectDiag = pygame.Rect(newShooterPosition[0], newShooterPosition[1], 15,18)
			shooterRectY = pygame.Rect(shooterPosition[0], newShooterPosition[1], 15,18)
			shooterRectX = pygame.Rect(newShooterPosition[0], shooterPosition[1], 15,18)
			thisMushroomRect = pygame.Rect(thisMushroom[0]*20, thisMushroom[1]*20, 15,15)
			if shooterRectDiag.colliderect(thisMushroomRect):
				canMoveDiag = False
			if shooterRectX.colliderect(thisMushroomRect):
				canMoveX = False
			if shooterRectY.colliderect(thisMushroomRect):
				canMoveY = False
			for centipedeLocation in centipedeLocations:
				centipedeRect = pygame.Rect(centipedeLocation[0], centipedeLocation[1], 15,17)
				if centipedeRect.colliderect(thisMushroomRect) and centipedeLocation[4]:
					centipedeLocation[2] += 1
					if centipedeLocation[1] < 460:
						centipedeLocation[5] = 1
					centipedeLocation[3] = centipedeLocation[1] + 20 * centipedeLocation[5]
			for shot in shots[:]:
				# is the shotRect colliding with thisMushroomRect?
				# if so, make mushroom health go down and remove shot
				shotRect = pygame.Rect(shot[0],shot[1],1,10)
				if shotRect.colliderect(thisMushroomRect):
					thisMushroom[2] -= 1
					shots.remove(shot)

		if canMoveDiag:
			shooterPosition = newShooterPosition
		elif canMoveX:shooterPosition[0] = newShooterPosition [0]
		elif canMoveY:shooterPosition[1] = newShooterPosition [1]

		for centipedeLocation in centipedeLocations:
			shooterRect = pygame.Rect(shooterPosition[0], shooterPosition[1], 15,18)
			centipedeRect = pygame.Rect(centipedeLocation[0], centipedeLocation[1], 15,17)
			if centipedeRect.colliderect(shooterRect):
				game -= 1
				centipedeReset()

			if (centipedeLocation[0]<0 or centipedeLocation[0]>380) and centipedeLocation[4]:
					if (centipedeLocation[0] < 0 and  centipedeLocation [2] %2 == 0 or
						centipedeLocation[0] > 380 and  centipedeLocation [2] %2 == 1):
						centipedeLocation[2] += 1
					if centipedeLocation[1] >= 580:
						centipedeLocation[5] = -1
					elif centipedeLocation[1] < 460:
						centipedeLocation[5] = 1
					centipedeLocation[3] = centipedeLocation[1] + 20 * centipedeLocation[5]
					

		if shooterPosition[1]<HEIGHT - 160:
			shooterPosition[1] = HEIGHT - 160
		sizeScreen.blit(shooter, shooterPosition)

		for centipedeLocation in centipedeLocations:
			sizeScreen.blit(centipedeHead, centipedeLocation[:2])

		for i in mushroomLocations[:]:
			drawX = i[0]*20
			drawY = i[1]*20
			if i[2] == 3:
				sizeScreen.blit (mushroom, (drawX,drawY))
			if i[2] == 2:
				sizeScreen.blit(halfMushroom, (drawX,drawY))
			if i[2] == 1:
				sizeScreen.blit(quarterMushroom, (drawX,drawY))
			elif i[2] == 0:
				mushroomLocations.remove(i)

		sizeScreen.blit(lives3, (0,0))


		pygame.display.flip()
		clock.tick(60)

main()