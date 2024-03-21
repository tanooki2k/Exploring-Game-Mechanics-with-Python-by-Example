from game import Game
from mainmenu import MainMenu
from gameplay import Gameplay

game = Game("Space Invader", 800, 700)
main_menu = MainMenu(game.screen)
game_play = Gameplay(game.screen)
main_menu.game_play_scene = game_play
game_play.main_menu = main_menu

game.run(main_menu)
