import Box2D
from Box2D.b2 import world, polygonShape, staticBody, dynamicBody
import pygame
from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE)
import time

# Pygame setup
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PPM = 20.0  # Pixels per meter
TARGET_FPS = 60
TIME_STEP = 1.0 / TARGET_FPS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("PyBox2D Physics Simulation")
    clock = pygame.time.Clock()

    # Box2D world setup
    world = Box2D.b2World(gravity=(0, -10), doSleep=True)

    # Ground body
    ground_body = world.CreateStaticBody(
        position=(0, 0),  # Adjust ground to align with the bottom of the screen
        shapes=polygonShape(box=(50, 1))  # The ground is wide, extending across the screen
    )

    # Dynamic body (falling box)
    dynamic_body1 = world.CreateDynamicBody(position=(10, 15))
    dynamic_body2 = world.CreateDynamicBody(position=(10, 12))
    box = dynamic_body1.CreatePolygonFixture(box=(1, 2), density=1, friction=0.3)
    box = dynamic_body2.CreatePolygonFixture(box=(1, .1), density=1, friction=0.3)

    # Define the anchor point where the bodies will be 'pinned'
    anchor_point = (10, 15)

    # Create a revolute joint (pin joint)
    joint = world.CreateRevoluteJoint(
        bodyA=dynamic_body1,
        bodyB=dynamic_body2,
        anchor=anchor_point
    )

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False
                
        #dynamic_body1.ApplyTorque(500, wake=True)
        #dynamic_body2.ApplyTorque(-500, wake=True)

        # Clear screen
        screen.fill(WHITE)

        # Draw ground
        ground_vertices = [(v[0] * PPM, SCREEN_HEIGHT - v[1] * PPM)
                           for v in ground_body.fixtures[0].shape.vertices]
        pygame.draw.polygon(screen, GREEN, ground_vertices)

        # Draw dynamic body (falling box)
        for fixture in dynamic_body1.fixtures:
            shape = fixture.shape
            vertices = [(dynamic_body1.transform * v) * PPM for v in shape.vertices]
            vertices = [(v[0], SCREEN_HEIGHT - v[1]) for v in vertices]
            pygame.draw.polygon(screen, RED, vertices)
        
        # Draw dynamic body (falling box)
        for fixture in dynamic_body2.fixtures:
            shape = fixture.shape
            vertices = [(dynamic_body2.transform * v) * PPM for v in shape.vertices]
            vertices = [(v[0], SCREEN_HEIGHT - v[1]) for v in vertices]
            pygame.draw.polygon(screen, RED, vertices)

        # Step simulation
        world.Step(TIME_STEP, 10, 10)

        # Update display
        pygame.display.flip()
        clock.tick(TARGET_FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
