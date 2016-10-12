'''This module provides the client page.'''
from direct.gui.DirectButton import DirectButton
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import DirectEntry
from racing.game.engine.gui.page import Page, PageGui
from racing.game.engine.network.client import ClientError
from .carpage import CarPage
from .netmsgs import NetMsgs


class ClientPageGui(PageGui):
    '''This class defines the GUI of the client page.'''

    def __init__(self, mdt, menu):
        PageGui.__init__(self, mdt, menu)
        self.ent = None

    def build(self):
        menu_gui = self.menu.gui
        menu_args = self.menu.gui.menu_args
        self.widgets += [
            OnscreenText(text='', scale=.12, pos=(0, .4),
                         font=menu_gui.font, fg=(.75, .75, .75, 1))]
        PageGui.transl_text(self.widgets[0], _('Client'))
        self.ent = DirectEntry(
            scale=.12, pos=(-.68, 1, .2), entryFont=menu_gui.font, width=12,
            frameColor=menu_args.btn_color,
            initialText='insert the server address')
        self.ent.onscreenText['fg'] = (.75, .75, .75, 1)
        self.widgets += [self.ent]
        self.widgets += [
            DirectButton(
                text=_('Connect'), scale=.2, pos=(0, 1, -.2),
                text_fg=(.75, .75, .75, 1),
                text_font=menu_gui.font, frameColor=menu_args.btn_color,
                command=self.connect, frameSize=menu_args.btn_size,
                rolloverSound=loader.loadSfx('assets/sfx/menu_over.wav'),
                clickSound=loader.loadSfx('assets/sfx/menu_clicked.ogg'))]
        PageGui.build(self)

    def connect(self):
        '''Connects to the server.'''
        try:
            print self.ent.get()
            eng.client.start(self.process_msg, self.ent.get())
            menu_gui = self.menu.gui
            self.widgets += [
                OnscreenText(text=_('Waiting for the server'), scale=.12,
                             pos=(0, -.5), font=menu_gui.font,
                             fg=(.75, .75, .75, 1))]
        except ClientError:
            txt = OnscreenText(_('Error'), fg=(1, 0, 0, 1), scale=.5)
            taskMgr.doMethodLater(
                5.0, lambda tsk: txt.destroy(), 'destroy error text')

    def process_msg(self, data_lst, sender):
        '''Processes a network message.'''
        if data_lst[0] == NetMsgs.track_selected:
            eng.log_mgr.log('track selected: ' + data_lst[1])
            self.menu.track = 'tracks/track_' + data_lst[1]
            self.menu.logic.push_page(CarPage(self.menu))


class ClientPage(Page):
    '''This class models a page.'''
    gui_cls = ClientPageGui
