

import sys
sys.path.insert(0, "../Builtin")

from panda3d.core import *
from panda3d.lui import LUIRegion, LUIInputHandler, LUISprite, LUIObject

from UILabel import UILabel
from UIFrame import UIFrame

load_prc_file_data("", """
    text-minfilter linear
    text-magfilter linear
    text-pixels-per-unit 32
    sync-video #f
    notify-level-lui info
    show-frame-rate-meter #f
    win-size 780 630
    window-title LUI Demo
    win-fixed-size #t
""")

import direct.directbase.DirectStart
from UISkin import UIDefaultSkin
from UILayouts import UIVerticalLayout
from UICheckbox import UICheckbox
from UIFormattedLabel import UIFormattedLabel
from UIButton import UIButton

class DemoFramework:

    """ This is a small helper class to setup common stuff for the demos """

    def __init__(self):
        base.win.set_clear_color(Vec4(0, 0, 0, 1))
        self.skin = UIDefaultSkin()
        self.skin.load()

        # Construct the LUIRegion
        region = LUIRegion.make("LUI", base.win)
        handler = LUIInputHandler()
        base.mouseWatcher.attach_new_node(handler)
        region.set_input_handler(handler)

        self.root = region.root()
        self.constructorParams = []

    def prepare_demo(self, demo_title=u"Some Demo"):

        # Background
        self.background = LUISprite(self.root, "res/DemoBackground.png")

        # Logo
        self.logo = LUISprite(self.root, "res/LUILogo.png")
        self.logo.top = 15
        self.logo.left = 20

        # Title
        self.titleLabel = UILabel(parent=self.root, text=demo_title, font_size=40, font="header")
        self.titleLabel.pos = (120, 20)
        self.subtitleLabel = UILabel(parent=self.root, text="LUI Widget Demo", font_size=14, font="default")
        self.subtitleLabel.pos = (121, 65)
        self.subtitleLabel.color = (1,1,1,0.5)

        # Right bar
        self.rightBar = UIVerticalLayout(parent=self.root, width=350, spacing=20)
        self.rightBar.pos = (410, 120)

        # Constructor parameters
        self.constructorParameters = UIFrame(width=340, style=UIFrame.Sunken)
        self.constructorLabel = UILabel(parent=self.constructorParameters, text=u"Constructor Parameters")
        self.constructorLayout = UIVerticalLayout(parent=self.constructorParameters, spacing=10, use_dividers=True)
        self.constructorLayout.top = 30

        # Public functions
        self.publicFunctions = UIFrame(width=340, style=UIFrame.Sunken)
        self.functionsLabel = UILabel(parent=self.publicFunctions, text=U"Public functions")
        self.functionsLayout = UIVerticalLayout(parent=self.publicFunctions,spacing=10, use_dividers=True)
        self.functionsLayout.top = 30

        # Events
        self.events = UIFrame(width=340,style=UIFrame.Sunken)
        self.eventsLabel = UILabel(parent=self.events, text=U"Additional Events")
        self.eventsLayout = UIVerticalLayout(parent=self.events, spacing=10, use_dividers=True)
        self.eventsLayout.top = 30

        self.rightBar.add_row(self.constructorParameters)
        self.rightBar.add_row(self.publicFunctions)
        self.rightBar.add_row(self.events)

        # Widget
        self.widgetContainer = UIFrame(parent=self.root, width=360, height=250, style=UIFrame.Sunken)
        self.widgetLabel = UILabel(parent=self.widgetContainer, text=u"Widget Demo")
        self.widgetContainer.left = 26
        self.widgetContainer.top = 120

        # Source Code
        self.sourceContainer = UIFrame(parent=self.root, width=360, height=200, style=UIFrame.Sunken)
        self.sourceLabel = UILabel(parent=self.sourceContainer, text=u"Example Source Code")
        self.copyCodeButton = UIButton(parent=self.sourceContainer, 
                text=u"Copy to Clipboard", template="ButtonMagic", 
                right=-5, bottom=-5)
        self.sourceContainer.left = 26
        self.sourceContainer.top = 390
        self.sourceContent = LUIObject(self.sourceContainer)
        self.sourceContent.top = 40


        self.widgetNode = LUIObject(self.widgetContainer, x=0, y=40)

    def add_public_function(self, name, parameters=None, return_type="void"):
        label = UIFormattedLabel()
        label.add_text(text=return_type + " ", color = (102/255.0, 217/255.0, 239/255.0))
        label.add_text(text=name + " ", color = (166/255.0, 226/255.0, 46/255.0))

        label.add_text(text="( ", color=(0.9,0.9,0.9))

        if parameters is not None:
            for index, (pname, ptype) in enumerate(parameters):
                label.add_text(text=pname, color=(255/255.0, 151/255.0, 31/255.0))
                label.add_text(text=" : ", color=(0.9,0.9,0.9))
                label.add_text(text=ptype, color=(102/255.0, 217/255.0, 239/255.0))

                if index < len(parameters) - 1:
                    label.add_text(text=",", color=(0.9,0.9,0.9))
        label.add_text(text=" )", color=(0.9,0.9,0.9))
        self.functionsLayout.add_row(label)
        self.update_layouts()

    def add_constructor_parameter(self, name, default):
        label = UIFormattedLabel()
        label.add_text(text=name, color=(255/255.0, 151/255.0, 31/255.0))
        label.add_text(text=" = ", color=(249/255.0, 38/255.0, 114/255.0))
        label.add_text(text=default, color=(153/255.0, 129/255.0, 255/255.0))
        self.constructorLayout.add_row(label)
        self.constructorParams.append((name, default))
        self.update_layouts()

    def add_event(self, event_name):
        label = UILabel(text=event_name)
        label.color = (1,1,1,0.5)
        self.eventsLayout.add_row(label)
        self.update_layouts()

    def update_layouts(self):
        self.publicFunctions.fit_to_children()
        self.constructorParameters.fit_to_children()
        self.events.fit_to_children()
        self.rightBar.update()

    def construct_sourcecode(self, classname):
        
        self.sourceContent.remove_all_children()
        label = UIFormattedLabel(parent=self.sourceContent)
        label.add_text(text="element ", color=(0.9,0.9,0.9))
        label.add_text(text="= ", color=(249/255.0, 38/255.0, 114/255.0))
        label.add_text(text=classname, color=(166/255.0, 226/255.0, 46/255.0))
        label.add_text(text="(", color=(0.9,0.9,0.9))

        for index, (pname, pvalue) in enumerate(self.constructorParams):
            label.br()
            label.add_text(text=" " * 15)
            label.add_text(text=pname, color=(255/255.0, 151/255.0, 31/255.0))
            label.add_text(text=" = ")
            label.add_text(text=pvalue, color=(153/255.0, 129/255.0, 255/255.0))

            if index < len(self.constructorParams) - 1:
                label.add_text(text=",")

        label.add_text(text=")")

    def get_widget_node(self):
        return self.widgetNode


f = DemoFramework()
f.prepare_demo("UICheckbox")


# Constructor
f.add_constructor_parameter("checked", "False")
f.add_constructor_parameter("label", "'Checkbox'")

# Functions
f.add_public_function("get_checked", [], "bool")
f.add_public_function("set_checked", [("checked", "bool")])
f.add_public_function("get_label", [], "UILabel")

# Events
f.add_event("changed")
f.construct_sourcecode("UICheckbox")

checkbox = UICheckbox()
checkbox.parent = f.get_widget_node()


run()
