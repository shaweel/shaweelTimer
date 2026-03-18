import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk


def onActivate(application):
	global installImage, installLabel
	window = Adw.ApplicationWindow(application=application)
	window.set_resizable(False)
	css = Gtk.CssProvider()
	css.load_from_data(b".colon { font-size: 40px; font-weight: 800; }")
	Gtk.StyleContext.add_provider_for_display(window.get_display(), css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

	mainOverlay = Gtk.Overlay()

	mainBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
	mainBox.set_margin_top(10)
	mainBox.set_margin_bottom(10)
	mainBox.set_margin_start(20)
	mainBox.set_margin_end(20)

	title = Gtk.Label(label="shaweelTimer installer")
	title.add_css_class("title-2")

	currentVersion = Gtk.Label(label="Current shaweelTimer version: None")
	currentVersion.set_halign(Gtk.Align.START)

	installButton = Gtk.Button()
	installButtonHorizontalBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
	installButtonHorizontalBox.set_halign(Gtk.Align.CENTER)
	installButtonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
	installButtonBox.set_halign(Gtk.Align.CENTER)


	installLabel = Gtk.Label(label="Install")
	installImage = Gtk.Image(icon_name="folder-download-symbolic")

	installButtonHorizontalBox.append(installImage)
	installButtonHorizontalBox.append(installLabel)

	installButtonBox.append(installButtonHorizontalBox)
	installButtonBox.append(Gtk.Label(label="Install shaweelTimer on your computer", css_classes=))

	installButton.set_hexpand(False)
	installButton.set_size_request(160, 0)
	installButton.set_halign(Gtk.Align.CENTER)

	installButton.set_child(installButtonBox)
	def onInstallButtonClicked():
		pass

	installButton.connect("clicked", lambda _: onInstallButtonClicked())
		
	mainBox.append(title)
	mainBox.append(currentVersion)
	mainBox.append(installButton)

	buttonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
	buttonBox.set_halign(Gtk.Align.END)
	buttonBox.set_valign(Gtk.Align.START)
	buttonBox.set_margin_end(5)
	buttonBox.set_margin_top(5)

	quitButton = Gtk.Button(icon_name="window-close-symbolic")
	quitButton.set_size_request(20, 20)
	quitButton.set_hexpand(False)
	quitButton.set_vexpand(False)
	quitButton.add_css_class("destructive-action")
	quitButton.connect("clicked", lambda button: application.quit())

	buttonBox.append(quitButton)

	mainOverlay.set_child(mainBox)
	mainOverlay.add_overlay(buttonBox)

	handle = Gtk.WindowHandle()
	handle.set_child(mainOverlay)

	window.set_content(handle)

	window.present()

application = Adw.Application()
application.connect("activate", onActivate)
application.run()