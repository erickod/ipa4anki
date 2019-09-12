# -*- coding: utf-8 -*-

import os
import re

from anki.hooks import addHook, wrap
from aqt.utils import showInfo
from aqt.editor import Editor
from aqt import mw

from .TranscriptionServices import eng_to_ipa as ipa 

#from . import parse_ipa 


ADDONPATH = os.path.dirname(__file__)
ICONPATH = os.path.join(ADDONPATH, "icons", "button.png")
CONFIG = mw.addonManager.getConfig(__name__)

def clean_text(text): #Verificada
    text = re.sub("^'|^\"|'$|\"$|\‘|\’|;|<i>|</i>|<b>|</b>|<u>|</u>|<br>|<div>|</div>|<p>|</p>|\n", "", text)
    text = re.sub("&nbsp", " ", text)
    return text

def paste_ipa(editor): #Verificada

    note = editor.note
    cleaned_text = clean_text(str(note[CONFIG['WORD_FIELD']]))
    note[CONFIG['IPA_FIELD']] = ipa.convert(cleaned_text)
    editor.loadNote()
    editor.web.setFocus()
    editor.web.eval("focusField(%d);" % editor.currentField)
    
def on_setup_buttons(buttons, editor):
    button = editor.addButton(ICONPATH, "IPA", paste_ipa)
    buttons.append(button)

    return buttons


addHook("setupEditorButtons", on_setup_buttons)
