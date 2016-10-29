from racing.game.game import Game
from racing.game.dictfile import DictFile
from racing.game.engine.configuration import Configuration
from .logic import _Logic
from .event import _Event
from .fsm import _Fsm
from .audio import _Audio


class Yorg(Game):
    logic_cls = _Logic
    event_cls = _Event
    fsm_cls = _Fsm
    audio_cls = _Audio

    def __init__(self):
        default_opt = {
            'settings': {
                'lang': 'en',
                'volume': 1,
                'fullscreen': 0,
                'resolution': '1280 720',
                'aa': 0,
                'open_browser_at_exit': 1},
            'development': {
                'multithreaded_render': 0,
                'ai': 0,
                'submodels': 1,
                'split_world': 1,
                'laps': 3,
                'fps': 1,
                'car': '',
                'track': ''}}
        self.options = DictFile('options.yml', default_opt)
        conf = Configuration(
            fps=self.options['development']['fps'], win_title='Yorg',
            win_size=self.options['settings']['resolution'],
            fullscreen=self.options['settings']['fullscreen'],
            antialiasing=self.options['settings']['aa'],
            lang=self.options['settings']['lang'],
            mt_render=self.options['development']['multithreaded_render'],
            lang_domain='yorg')
        Game.__init__(self, conf)