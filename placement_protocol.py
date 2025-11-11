import curses
import time
import threading
from event_bus import EventBus
from ecs_core import ECSManager, PlayerComponent, HealthComponent, ScoreComponent
from analytics_stream import AnalyticsServer
from profiler import Profiler


class GameState:
    MENU = "menu"
    PLAYING = "playing"
    GAME_OVER = "game_over"


class PlacementProtocolGame:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.state = GameState.MENU
        self.event_bus = EventBus()
        self.ecs = ECSManager(self.event_bus)
        self.profiler = Profiler()
        self.analytics_server = AnalyticsServer(self.ecs, self.profiler)

        self.player_name = ""
        self.max_y, self.max_x = self.screen.getmaxyx()
        curses.curs_set(0)
        self.screen.nodelay(True)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

    def run(self):
        self.analytics_server.start()
        self.profiler.start()
        while self.running:
            if self.state == GameState.MENU:
                self.render_menu()
            elif self.state == GameState.PLAYING:
                self.render_game()
            elif self.state == GameState.GAME_OVER:
                self.render_game_over()
            time.sleep(0.05)
        self.shutdown()

    def render_menu(self):
        self.screen.clear()
        self.screen.addstr(self.max_y//2 - 2, self.max_x//2 - 10, "🧠 Placement Protocol", curses.color_pair(1))
        self.screen.addstr(self.max_y//2, self.max_x//2 - 10, "Enter your name: " + self.player_name)
        self.screen.refresh()

        try:
            ch = self.screen.getch()
            if ch == 10 and self.player_name:
                self.start_game()
            elif ch == 27:
                self.running = False
            elif ch != -1:
                if ch in range(32, 127):
                    self.player_name += chr(ch)
                elif ch in [8, 127]:
                    self.player_name = self.player_name[:-1]
        except:
            pass

    def start_game(self):
        self.state = GameState.PLAYING
        player = self.ecs.create_entity()
        self.ecs.add_component(player, PlayerComponent(self.player_name))
        self.ecs.add_component(player, HealthComponent(100))
        self.ecs.add_component(player, ScoreComponent(0))
        self.event_bus.post("GAME_START", {"player": self.player_name})

    def render_game(self):
        self.screen.clear()
        player = self.ecs.get_player()
        if not player:
            self.state = GameState.GAME_OVER
            return

        self.screen.addstr(1, 2, f"Player: {player.name}", curses.color_pair(1))
        self.screen.addstr(2, 2, f"Health: {player.health}", curses.color_pair(2))
        self.screen.addstr(3, 2, f"Score: {player.score}", curses.color_pair(2))
        self.screen.addstr(5, 2, "[A] Solve Challenge | [Q] Quit", curses.color_pair(3))

        ch = self.screen.getch()
        if ch in [ord('a'), ord('A')]:
            player.score += 5
            player.health -= 3
            self.event_bus.post("CHALLENGE_SOLVED", {"player": player.name, "score": player.score})
        elif ch in [ord('q'), ord('Q')]:
            self.state = GameState.GAME_OVER

        if player.health <= 0:
            self.state = GameState.GAME_OVER

        self.profiler.update()
        self.screen.addstr(self.max_y-2, 2, f"FPS: {self.profiler.fps:.1f} | Clients: {len(self.analytics_server.clients)}")
        self.screen.refresh()

    def render_game_over(self):
        self.screen.clear()
        self.screen.addstr(self.max_y//2 - 1, self.max_x//2 - 10, "💀 GAME OVER 💀", curses.color_pair(3))
        self.screen.addstr(self.max_y//2, self.max_x//2 - 10, f"Final Score: {self.ecs.get_player().score}")
        self.screen.addstr(self.max_y//2 + 2, self.max_x//2 - 10, "[R]estart | [Q]uit")
        self.screen.refresh()

        ch = self.screen.getch()
        if ch in [ord('r'), ord('R')]:
            self.__init__(self.screen)
        elif ch in [ord('q'), ord('Q')]:
            self.running = False

    def shutdown(self):
        self.analytics_server.stop()
        self.profiler.stop()
        curses.endwin()


def main(stdscr):
    game = PlacementProtocolGame(stdscr)
    game.run()


if __name__ == "__main__":
    curses.wrapper(main)
