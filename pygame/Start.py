import pygame
from pygame.locals import Color
from pygame import key
import ControlsScreen

pygame.init()
pygame.font.init()

size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Persona 4 Calendar")

done = False
clock = pygame.time.Clock()
print pygame.display.list_modes()
print pygame.version

scene = ControlsScreen.ControlsScreen(size)
# -------- Main Program Loop -----------
while not done:
    # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
	for event in pygame.event.get(): # User did something
		if event.type == pygame.QUIT:
			done = True
		elif event.type == pygame.KEYDOWN:
            #evt = scene.handle_event(event)
            #TODO: next day, lock until done
			if event.key == pygame.K_RIGHT:
				scene.moveRight()
			elif event.key == pygame.K_LEFT:
				scene.moveLeft()
			pass
	scene.update()
	scene.render(screen)
	clock.tick(60)
     
pygame.quit()
