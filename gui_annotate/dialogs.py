#!/usr/bin/env python3

from gi.repository import Gtk

from gui_annotate.constants import Constants


def help_dialog(app):
    diag = Gtk.MessageDialog(parent=app,
                             type=Gtk.MessageType.INFO,
                             buttons=Gtk.ButtonsType.OK,
                             message_format=Constants.HELP_DIALOG_MSG)
    diag.format_secondary_markup(Constants.HELP_DIALOG_SECONDARY)
    resp = diag.run()
    if resp:
        diag.destroy()


def about_dialog(app):
    diag = Gtk.AboutDialog(parent=app,
                           website=Constants.WEBSITE,
                           logo=None,
                           program_name=Constants.PROG_NAME,
                           comments=Constants.COMMENTS,
                           copyright=Constants.COPYRIGHT)
    diag.set_authors(Constants.AUTHORS)
    resp = diag.run()
    if resp:
        diag.destroy()
