import sys
import cfg
import pygame
import random
import os

class SkierClass(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.direction = 0
        self.imagepaths = cfg.SKIER_IMAGE_PATHS[:-1]
        self.image = pygame.image.load(self.imagepaths[self.direction])
        self.rect = self.image.get_rect()
        self.rect.center = [320, 100]
        self.speed = [self.direction, 6 - abs(self.direction) * 2]
        self.flag_count = 0  # Counter for collecting flags
        self.score = 0

    def turn(self, num):
        self.direction += num
        self.direction = max(-2, self.direction)
        self.direction = min(2, self.direction)
        center = self.rect.center
        self.image = pygame.image.load(self.imagepaths[self.direction])
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speed = [self.direction, 6 - abs(self.direction) * 2]
        return self.speed

    def move(self):
        self.rect.centerx += self.speed[0]
        self.rect.centerx = max(20, self.rect.centerx)
        self.rect.centerx = min(620, self.rect.centerx)

    def setFall(self):
        self.image = pygame.image.load(cfg.SKIER_IMAGE_PATHS[-1])

    def setForward(self):
        self.direction = 0
        self.image = pygame.image.load(self.imagepaths[self.direction])


class ObstacleClass(pygame.sprite.Sprite):
    def __init__(self, img_path, location, attribute):
        pygame.sprite.Sprite.__init__(self)
        self.img_path = img_path
        self.image = pygame.image.load(self.img_path)
        self.location = location
        self.rect = self.image.get_rect()
        self.rect.center = self.location
        self.attribute = attribute
        self.passed = False

    def move(self, num):
        self.rect.centery = self.location[1] - num


def createObstacles(s, e, num=10):
    obstacles = pygame.sprite.Group()
    locations = []
    for i in range(num):
        row = random.randint(s, e)
        col = random.randint(0, 9)
        location = [col * 64 + 20, row * 64 + 20]
        if location not in locations:
            locations.append(location)
            if i % 4 == 0:
                attribute = "tree"  # Distribute trees
            elif i % 4 == 1:
                attribute = "stone"  # Distribute stones
            else:
                attribute = "flag"  # Distribute flags
            img_path = cfg.OBSTACLE_PATHS[attribute]
            obstacle = ObstacleClass(img_path, location, attribute)
            obstacles.add(obstacle)
    return obstacles


def AddObstacles(obstacles0, obstacles1):
    obstacles = pygame.sprite.Group()
    for obstacle in obstacles0:
        obstacles.add(obstacle)
    for obstacle in obstacles1:
        obstacles.add(obstacle)
    return obstacles

def showScore(screen, score, pos=(10, 10)):
    font = pygame.font.Font(cfg.FONTPATH, 30)
    score_text = font.render("Score: %s" % score, True, (0, 0, 0))
    screen.blit(score_text, pos)


def ShowStartInterface(screen, screensize):
    screen.fill((255, 255, 255))
    tfont = pygame.font.Font(cfg.FONTPATH, screensize[0] // 5)
    cfont = pygame.font.Font(cfg.FONTPATH, screensize[0] // 20)
    title = tfont.render(u'Skier Game', True, (255, 0, 0))
    content = cfont.render(u'Press any key to START.', True, (0, 0, 255))
    trect = title.get_rect()
    trect.midtop = (screensize[0] / 2, screensize[1] / 5)
    crect = content.get_rect()
    crect.midtop = (screensize[0] / 2, screensize[1] / 2)
    screen.blit(title, trect)
    screen.blit(content, crect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                return
        pygame.display.update()


def updateFrame(screen, obstacles, skier):
    screen.fill((255, 255, 255))
    obstacles.draw(screen)
    screen.blit(skier.image, skier.rect)
    showScore(screen, skier.score)
    pygame.display.update()


def main():
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(cfg.BGMPATH)
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)

    screen = pygame.display.set_mode(cfg.SCREENSIZE)
    pygame.display.set_caption('Skier Game')

    ShowStartInterface(screen, cfg.SCREENSIZE)

    while True:
        skier = SkierClass()

        obstacles0 = createObstacles(20, 29, num=15)  # Decrease number of trees and stones
        obstacles1 = createObstacles(10, 19, num=15)  # Decrease number of trees and stones
        obstaclesflag = 0
        obstacles = AddObstacles(obstacles0, obstacles1)

        clock = pygame.time.Clock()

        distance = 0

        restart = False  # Variable to track whether the game should restart or quit

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        skier.turn(-1)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        skier.turn(1)
                    elif event.key == pygame.K_q:  # Press 'q' to quit the game
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_r:  # Press 'r' to restart the game
                        restart = True

            if restart:
                break  # Exit the inner loop to restart the game

            skier.move()
            distance += skier.speed[1]
            if distance >= 640 and obstaclesflag == 0:
                obstaclesflag = 1
                obstacles0 = createObstacles(20, 29, num=15)  # Decrease number of trees and stones
                obstacles = AddObstacles(obstacles0, obstacles1)

            if distance >= 1280 and obstaclesflag == 1:
                obstaclesflag = 0
                distance -= 1280
                for obstacle in obstacles0:
                    obstacle.location[1] = obstacle.location[1] - 1280
                obstacles1 = createObstacles(10, 19, num=15)  # Decrease number of trees and stones
                obstacles = AddObstacles(obstacles0, obstacles1)

            for obstacle in obstacles:
                obstacle.move(distance)

            hitted_obstacles = pygame.sprite.spritecollide(skier, obstacles, False)
            if hitted_obstacles:
                if hitted_obstacles[0].attribute == "tree" and not hitted_obstacles[0].passed:
                    skier.score -= 5  # Decrease score by 5 when hitting a tree
                    skier.setFall()
                    skier.speed[1] = 2  # Decrease skier's speed
                    updateFrame(screen, obstacles, skier)
                    pygame.time.delay(1000)
                    skier.setForward()
                    skier.speed[1] = 6  # Reset skier's speed
                    hitted_obstacles[0].passed = True
                elif hitted_obstacles[0].attribute == "stone" and not hitted_obstacles[0].passed:
                    skier.score -= 10  # Decrease score by 10 when hitting a stone
                    skier.setFall()
                    skier.speed[1] = 2  # Decrease skier's speed
                    updateFrame(screen, obstacles, skier)
                    pygame.time.delay(1000)
                    skier.setForward()
                    skier.speed[1] = 6  # Reset skier's speed
                    hitted_obstacles[0].passed = True
                elif hitted_obstacles[0].attribute == "flag" and not hitted_obstacles[0].passed:
                    skier.score += 10  # Increase score by 10 when collecting a flag
                    skier.flag_count += 1
                    if skier.flag_count >= 10:  # Increase speed after collecting 10 flags
                        skier.speed[1] = 8
                    obstacles.remove(hitted_obstacles[0])

            updateFrame(screen, obstacles, skier)
            if skier.score < 0:  # Check if score is negative
                screen.fill((255, 255, 255))
                font = pygame.font.Font(cfg.FONTPATH, 40)
                game_over_text = font.render("Game Over", True, (255, 0, 0))
                prompt_text = font.render("Press 'r' to restart or 'q' to quit.", True, (0, 0, 255))
                game_over_rect = game_over_text.get_rect(center=(cfg.SCREENSIZE[0] // 2, cfg.SCREENSIZE[1] // 2))
                prompt_rect = prompt_text.get_rect(center=(cfg.SCREENSIZE[0] // 2, cfg.SCREENSIZE[1] // 2 + 50))
                screen.blit(game_over_text, game_over_rect)
                screen.blit(prompt_text, prompt_rect)
                pygame.display.update()

                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_r:  # Press 'r' to restart the game
                                restart = True
                            elif event.key == pygame.K_q:  # Press 'q' to quit the game
                                pygame.quit()
                                sys.exit()

                    if restart:
                        break  # Exit the inner loop to restart the game

            clock.tick(cfg.FPS)

        if not restart:
            break  # Exit the outer loop if the game should quit


if __name__ == '__main__':
    main()
