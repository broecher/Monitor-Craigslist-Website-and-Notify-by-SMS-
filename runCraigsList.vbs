option explicit

dim wshShell

Set wshShell = WScript.CreateObject("WSCript.shell")
wshshell.run """Z:\Data\Scripts\CraigsListFree\CraigsListFree.py""", False

set wshshell = nothing
