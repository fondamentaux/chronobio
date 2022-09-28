from chronobio.game.game import Game

game = Game()
game.add_player("Vincent")
game.add_player("Benjamin")

for _ in range(100):
    print("New day")
    print(f" - Greenhouse gas: {game.greenhouse_gas}")
    game.new_day()
    for farm in game.farms:
        if farm.name:
            print(f" - {farm.name}: {farm.score}")