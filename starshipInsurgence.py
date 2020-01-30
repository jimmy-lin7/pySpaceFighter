"""
    Author: Jimmy Lin
    Date: May 28, 2017
    Description: This program is a single-player top-down shooter set in space.
    The player controls a starship with the goal to destroy enemy and avoid getting hit.
    The player wins by reaching a certain amount of points and loses after getting hit enough
    to lose all their life points.
"""

# I - IMPORT AND INITIALIZE
import pygame, starshipInsurgenceSprites, random
pygame.init()
 
     
def main():
    '''This function defines the 'mainline logic' for the game.'''
      
    # DISPLAY
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Starship Insurgence")
     
    # ENTITIES
    background = pygame.Surface(screen.get_size())
    background.fill((0, 255, 255))
    background = background.convert()
    screen.blit(background, (0, 0))

    # Music
    pygame.mixer.music.load("Sounds/music.wav")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)
    # Sound effects
    laser_sound = pygame.mixer.Sound("Sounds/laser.wav")
    laser_sound.set_volume(0.3)
    plasma_sound = pygame.mixer.Sound("Sounds/plasma.wav")
    plasma_sound.set_volume(0.8)
    enemy_plasma_sound = pygame.mixer.Sound("Sounds/enemyPlasma.wav")
    enemy_plasma_sound.set_volume(0.1)
    explosion = pygame.mixer.Sound("Sounds/explosion.wav")
    explosion.set_volume(0.1)

    # Sprites for Wallpaper, score keeper and player
    score_keeper = starshipInsurgenceSprites.ScoreKeeper()
    wallpaper = starshipInsurgenceSprites.Wallpaper(screen)
    player = starshipInsurgenceSprites.Player(screen)
    overlap = starshipInsurgenceSprites.DisplayOverlap()
    # Sprite Groups
    power_up_group = pygame.sprite.Group()
    enemy_boss_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    friendly_plasma_group = pygame.sprite.Group()
    enemy_plasma_group = pygame.sprite.Group()
    friendly_laser_group = pygame.sprite.Group()
    enemy_homing_plasma_group = pygame.sprite.Group()
    allSprites = pygame.sprite.OrderedUpdates(wallpaper, enemy_group, friendly_laser_group, player, power_up_group,
                                              friendly_plasma_group, enemy_plasma_group,enemy_homing_plasma_group, power_up_group, score_keeper, overlap)
    
    # ASSIGN 
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    keepGoing = True

    # Before-game Loop, player can move and read instructions
    overlap.set_display(0)
    # LOOP
    while keepGoing:

        # TIME
        clock.tick(30)

        # EVENT HANDLING: Player uses arrow keys to move, space to fire (hold)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.go_up()
                if event.key == pygame.K_DOWN:
                    player.go_down()
                if event.key == pygame.K_SPACE:
                    keepGoing = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.stop_left()
                if event.key == pygame.K_RIGHT:
                    player.stop_right()
                if event.key == pygame.K_UP:
                    player.stop_up()
                if event.key == pygame.K_DOWN:
                    player.stop_down()

        # REFRESH
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()

    # Main Game loop
    overlap.set_display(-1)
    keepGoing = True
    # LOOP
    while keepGoing:
     
        # TIME
        clock.tick(30)
     
        # EVENT HANDLING: Player uses arrow keys to move, space to fire (hold)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.go_up()
                if event.key == pygame.K_DOWN:
                    player.go_down()
                if event.key == pygame.K_SPACE:
                    player.start_shooting()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.stop_left()
                if event.key == pygame.K_RIGHT:
                    player.stop_right()
                if event.key == pygame.K_UP:
                    player.stop_up()
                if event.key == pygame.K_DOWN:
                    player.stop_down()
                if event.key == pygame.K_SPACE:
                    player.stop_shooting()                

        if player.shoot():
            if player.get_power_up() == 1:
                # Spawns a laser sprite if player is powered up and has not spawned a laser yet
                if not friendly_laser_group:
                    laser = starshipInsurgenceSprites.Laser(screen, player.rect, 0)
                    friendly_laser_group.add(laser)
                    laser_sound.play()
            elif player.get_power_up() == 2:
                # Double Shot
                plasma = starshipInsurgenceSprites.Plasma(screen, player.rect.centerx - 5, player.rect.top, 0)
                friendly_plasma_group.add(plasma)
                plasma = starshipInsurgenceSprites.Plasma(screen, player.rect.centerx + 5, player.rect.top, 0)
                friendly_plasma_group.add(plasma)
                plasma_sound.play()
            elif player.get_power_up() == 0:
                # Normal shots
                plasma = starshipInsurgenceSprites.Plasma(screen, player.rect.centerx, player.rect.top, 0)
                friendly_plasma_group.add(plasma)
                plasma_sound.play()
            allSprites = pygame.sprite.OrderedUpdates(wallpaper, enemy_group, friendly_laser_group, player,
                                                      friendly_plasma_group, enemy_plasma_group,
                                                      enemy_homing_plasma_group, power_up_group, score_keeper, overlap)

        # Randomly spawns enemy grunt ships
        if random.randint(0, 50) == 17:
            enemy = starshipInsurgenceSprites.EnemyShip(screen, 3, 3)
            enemy_group.add(enemy)
            allSprites = pygame.sprite.OrderedUpdates(wallpaper, enemy_group, friendly_laser_group, player,
                                                      friendly_plasma_group, enemy_plasma_group,
                                                      enemy_homing_plasma_group, power_up_group, score_keeper, overlap)
        # Randomly spawns enemy boss ships (max 2 on screen at once)
        if random.randint(0, 400) == 17 and len(enemy_boss_group) < 2:
            enemy_boss = starshipInsurgenceSprites.EnemyShip(screen, 50, 50)
            enemy_boss_group.add(enemy_boss)
            enemy_group.add(enemy_boss_group)
            allSprites = pygame.sprite.OrderedUpdates(wallpaper, enemy_group, friendly_laser_group, player,
                                                      friendly_plasma_group, enemy_plasma_group,
                                                      enemy_homing_plasma_group, power_up_group, score_keeper, overlap)

        # Randomly shoots enemy plasma from all enemy shits
        for enemy in enemy_group:
            if random.randint(0, 60) == 17:
                plasma = starshipInsurgenceSprites.Plasma(screen, enemy.rect.centerx, enemy.rect.bottom, 1)
                enemy_plasma_group.add(plasma)
                allSprites = pygame.sprite.OrderedUpdates(wallpaper, enemy_group, friendly_laser_group, player,
                                                      friendly_plasma_group, enemy_plasma_group,
                                                      enemy_homing_plasma_group, power_up_group, score_keeper, overlap)
                enemy_plasma_sound.play()

        # Randomly shoots enemy plasma and homing plasma in a pattern from boss
        for enemy in enemy_boss_group:
            if random.randint(0, 150) == 17:
                delay = random.randint(25, 40)
                homing_plasma = starshipInsurgenceSprites.HomingPlasma(screen, enemy.rect.centerx, enemy.rect.bottom, delay, -6, 4)
                enemy_homing_plasma_group.add(homing_plasma)
                homing_plasma = starshipInsurgenceSprites.HomingPlasma(screen, enemy.rect.centerx, enemy.rect.bottom, delay, -4, 7)
                enemy_homing_plasma_group.add(homing_plasma)
                homing_plasma = starshipInsurgenceSprites.HomingPlasma(screen, enemy.rect.centerx, enemy.rect.bottom, delay, 4, 7)
                enemy_homing_plasma_group.add(homing_plasma)
                homing_plasma = starshipInsurgenceSprites.HomingPlasma(screen, enemy.rect.centerx, enemy.rect.bottom, delay, 6, 4)
                enemy_homing_plasma_group.add(homing_plasma)
                allSprites = pygame.sprite.OrderedUpdates(wallpaper, enemy_group, friendly_laser_group, player,
                                                      friendly_plasma_group, enemy_plasma_group,
                                                      enemy_homing_plasma_group, power_up_group, score_keeper, overlap)
                enemy_plasma_sound.play()
            if random.randint(0, 60) == 17:
                plasma = starshipInsurgenceSprites.Plasma(screen, enemy.rect.left, enemy.rect.top + 40, 1)
                enemy_plasma_group.add(plasma)
                plasma = starshipInsurgenceSprites.Plasma(screen, enemy.rect.centerx, enemy.rect.bottom, 1)
                enemy_plasma_group.add(plasma)
                plasma = starshipInsurgenceSprites.Plasma(screen, enemy.rect.right, enemy.rect.top + 40, 1)
                enemy_plasma_group.add(plasma)
                allSprites = pygame.sprite.OrderedUpdates(wallpaper, enemy_group, friendly_laser_group, player,
                                                          friendly_plasma_group, enemy_plasma_group,
                                                          enemy_homing_plasma_group, power_up_group, score_keeper, overlap)
                enemy_plasma_sound.play()

        # Changes direction of homing plasma to move towards player if delay is met
        for homing_plasma in enemy_homing_plasma_group:
            homing_plasma.tracking(player.rect.center)

        # Enemy hit detection
        for plasma in friendly_plasma_group:
            enemy_hit_list = pygame.sprite.spritecollide(plasma, enemy_group, False)
            for enemy in enemy_hit_list:
                if enemy.hit():
                    explosion.play()
                    # Guaranteed power ups from dead boss ships
                    if enemy.is_boss():
                        power_up = starshipInsurgenceSprites.PowerUp(screen, enemy.rect, 3)
                        power_up_group.add(power_up)
                        allSprites = pygame.sprite.OrderedUpdates(wallpaper, enemy_group, friendly_laser_group, player,
                                                              friendly_plasma_group, enemy_plasma_group,
                                                              enemy_homing_plasma_group, power_up_group,
                                                              score_keeper, overlap)
                    # Randomly spawns power ups from dead ships
                    score_keeper.player_scored(enemy.get_worth())
                    if random.randint(0, 6) == 3:
                        power_up = starshipInsurgenceSprites.PowerUp(screen, enemy.rect, 1)
                        power_up_group.add(power_up)
                        allSprites = pygame.sprite.OrderedUpdates(wallpaper, enemy_group, friendly_laser_group, player,
                                                                  friendly_plasma_group, enemy_plasma_group,
                                                                  enemy_homing_plasma_group, power_up_group,
                                                                  score_keeper, overlap)
                    elif random.randint(0, 9) == 3:
                        power_up = starshipInsurgenceSprites.PowerUp(screen, enemy.rect, 2)
                        power_up_group.add(power_up)
                        allSprites = pygame.sprite.OrderedUpdates(wallpaper, enemy_group, friendly_laser_group, player,
                                                                  friendly_plasma_group, enemy_plasma_group,
                                                                  enemy_homing_plasma_group, power_up_group,
                                                                  score_keeper, overlap)
                    elif random.randint(0, 5) == 3:
                        power_up = starshipInsurgenceSprites.PowerUp(screen, enemy.rect, 3)
                        power_up_group.add(power_up)
                        allSprites = pygame.sprite.OrderedUpdates(wallpaper, enemy_group, friendly_laser_group, player,
                                                                  friendly_plasma_group, enemy_plasma_group,
                                                                  enemy_homing_plasma_group, power_up_group,
                                                                  score_keeper, overlap)

                # Kills plasma if enemy is not already dead and going through death animation
                if enemy.get_dying_frames() <= 0:
                    plasma.kill()

        # Maintains position of laser sprite, also checks for enemies hit
        for laser in friendly_laser_group:
            laser.move(player.rect)
            enemy_hit_list = pygame.sprite.spritecollide(laser, enemy_group, False)
            for enemy in enemy_hit_list:
                if enemy.hit():
                    score_keeper.player_scored(enemy.get_worth())

        # Player hit detection, deducts points from player health
        for plasma in enemy_plasma_group:
            if pygame.sprite.collide_rect(plasma, player):
                if player.get_hit_frames() == 0:  # Invincibility frames
                    player.hit()
                    score_keeper.player_hit()
                plasma.kill()
        for plasma in enemy_homing_plasma_group:
            if pygame.sprite.collide_rect(plasma, player):  # Invincibility frames
                if player.get_hit_frames() == 0:
                    player.hit()
                    score_keeper.player_hit()
                plasma.kill()

        # Player power up collision detection
        for power_up in power_up_group:
            if pygame.sprite.collide_rect(power_up, player):
                if not power_up.used():  # Prevents excessive healing from a single HP power up during picked up animation
                    if power_up.get_variant() == 3:
                        score_keeper.player_heal()
                    else:
                        player.set_power_up(power_up.get_variant())
                        # Makes sure there aren't two lasers at once
                        if friendly_laser_group:
                            for laser in friendly_laser_group:
                                laser.kill()
                    power_up.picked_up()

        # Check for game over and display appropriate end screen
        if score_keeper.winner():
            overlap.set_display(1)
            keepGoing = False
        if score_keeper.loser():
            overlap.set_display(2)
            keepGoing = False

        
        # REFRESH SCREEN
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()

    # Close the game window with delay and music fadeout
    pygame.mouse.set_visible(True)
    pygame.mixer.music.fadeout(2000)
    pygame.time.delay(2500)
    pygame.quit()
     
# Call the main function
main()    