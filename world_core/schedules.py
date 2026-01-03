def daily_routine(bot, world):
    if bot.role == "dad":
        if world.time_of_day < 8:
            bot.location = "home"
        elif world.time_of_day < 18:
            bot.location = "work"
        else:
            bot.location = "home"