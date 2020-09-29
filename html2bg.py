#!/usr/bin/python
import PyQt5
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWebKitWidgets import QWebView , QWebPage
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtNetwork import *
import sys
import os

class MyBrowser(QWebPage):
	''' Settings for the browser.'''
    
	def userAgentForUrl(self, url):
		return "Roemchens AppleWebKit/537.36 (KHTML, like Gecko)"

class Browser(QWebView):
	def __init__(self):
		# QWebView
		self.view = QWebView.__init__(self)
		#self.view.setPage(MyBrowser())
		self.setWindowTitle( sys.argv[0] + " as GUI" )
		self.sNAME = sys.argv[0].split(".")
		
		self.sNAME.pop()
		self.sNAME = str(".").join(self.sNAME)
		
		self.loadFinished.connect( self.on_load_finnished )
		#super(Browser).connect(self.ui.webView,QtCore.SIGNAL("titleChanged (const QString&amp;)"), self.adjustTitle)
	def save( self ):
		pic = self.grab()
		sFILE = os.getenv("HOME") + "/" + os.path.basename(self.sNAME) + ".jpg" 
		pic.save( sFILE , "png" ) 
		os.system( "/usr/bin/gsettings get org.gnome.desktop.background picture-uri >> " + self.sNAME + ".stdout" )
		f=open( self.sNAME + ".stdout" , "r")
		sDCONF = f.read()
		f.close()
		os.system( "chmod 0755 " + sFILE )
		
		if sDCONF != sFILE:
			os.system( "gsettings set org.gnome.desktop.background picture-uri " + sFILE )
			os.system( "gsettings set org.gnome.desktop.background picture-options stretched" )
		os.system("zenity --notification --text=\"" + sys.argv[1] + " ==> | background(" + sFILE + ")\"")

	def on_load_finnished( self , ok ):
		self.save()
		self.close()

	def disableJS(self):
		settings = QWebSettings.globalSettings()
		settings.setAttribute(QWebSettings.JavascriptEnabled, False)

	def enableJS(self):
		settings = QWebSettings.globalSettings()
		settings.setAttribute(QWebSettings.JavascriptEnabled, True )

	def toggleFullScreen(self):
		if self.isFullScreen():
			self.showNormal()
		else:
			self.showFullScreen()
			
	def load( self , url ):
		self.setUrl(QUrl(url))

	def acceptNavigationRequest( self , url, NavigationType , isMainFrame ):
		if url == "about:screenshot":
			self.save()
			return False
		if url == "about:exit":
			self.save()
			self.close()
			return False

		self.load(QUrl(url))
		return True

if len( sys.argv ) > 1:
	app = QApplication(sys.argv)
	view = Browser()
	view.showFullScreen()
	#view.setVisible( False )
	if os.path.isfile( sys.argv[1] ):
		view.load( "file://" + urllib.parse.quote( sys.argv[1] ) )
	else:
		view.load( sys.argv[1] )
	app.exec_()
else:
	print( "usage:" )
	print( sys.argv[0] + " [html]" )

