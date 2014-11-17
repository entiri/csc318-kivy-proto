import os
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.properties import ObjectProperty, StringProperty, \
     NumericProperty, ListProperty
from functools import partial

class AppScreen(FloatLayout):
    app = ObjectProperty(None)

class MainMenu(AppScreen):
    pass

class SettingScreen(TabbedPanel):
    app = ObjectProperty(None)

    def back_to_main(self):
        '''
        Direct the user back to the main page
        '''
        self.app.goto_screen("menu")

class CSCGroupNineApp(App):
    data = StringProperty('')
    searchHistory = StringProperty('')
    
    # (ignore/saved)List are used to store instances in for saved/ignore tabs.
    ignoreList = ListProperty([])
    historyList = ListProperty([])

    def build(self):
        self.screens = {}
        self.screens["settings"] = SettingScreen(app=self)
        self.screens["menu"] = MainMenu(app=self)
        self.root = FloatLayout()
        self.goto_screen("menu")
        return self.root
 
    def goto_screen(self, screen_name):
        self.root.clear_widgets()
        self.root.add_widget(self.screens[screen_name])
        
    def results(self, query):
        '''
        Return a list of all search results for index in fle
        '''

        # If the user had previously made a search, delete the result.
        for child in self.screens["menu"].ids.search.children:
            if child.id in ['noResults', 'tooManyResults', 'scroll']:
                self.screens["menu"].ids.search.remove_widget(child)

        '''
        for option in ['noResults', 'tooManyResults', 'scroll']:
            if option in self.screens["menu"].ids.search.children : 
                self.screens["menu"].ids.search.remove_widget(option)'''

        #Assume the text is all lowercase words, change the first letter
        # of each word to upper case (change to title case)
        query = query.title()
        
        #Troubleshoot - for various errors
        if len(query) <= 1:
            return "Sorry, your search has to be longer than a few words!"

        #open file
        fle = open('C:/Users/USER/My Documents/GitHub/csc318-kivy-proto/idioms.txt',\
                   'r')

        queryRslt = []

        #The toggle is only flipped when lines are to be added to queryRslt
        toggle = False
        for line in fle:
            #Toggle to append next line
            if toggle == True:
                queryRslt[-1].append(line)
                #Set the toggle to false so that the next line isnt added
                toggle = False

            # If it exists in file as an idiom, append the phrase to 
            # the list (without the ending!)
            if line.find(query) != -1 and line[-3] == ":":
                if line[0:-3] not in self.ignoreList:
                    queryRslt.append([line[0:-3]])
                    #Set toggle to true to append the next line
                    toggle = True

        # If the search was successful, add the search to Saved data
        if len(queryRslt) > 1 and len(queryRslt) < 100:
            self.addToHistory(query)

        #Add the results to the result screen
        self.stringResults(queryRslt)

    def stringResults(self, res):
        '''
        Return a scrollable set of search results to be
        displayed in the app.
        '''
        # If there are less than one, or more than 50 results for a search,
        # return an error (as a label)
        if len(res) < 1:
            noResults = Label(text="Sorry, your search turned up no results.", size_hint_y=None, height=200)
            self.screens["menu"].ids.search.add_widget(noResults)
        elif len(res) > 100:
            tooManyResults = Label(text="The search returned too many results!", size_hint_y=None, height=200)
            self.screens["menu"].ids.search.add_widget(tooManyResults)
        # Return a series of buttons in a scrollable list. 
        else:
            gridlayout = GridLayout(cols=1, spacing=10, size_hint_y=None)
            #Make sure the height is such that there is something to scroll.
            gridlayout.bind(minimum_height=gridlayout.setter('height'))
            # Create a button for each item in the list; add it to GridLayout
            for item in res:
                # Create button, bind to grid layout 
                resButton = Button(text=item[0], size_hint_y=None, height=40)
                
                # The use of lambda feels like a callback to 324. Learning is cool.
                resButton.bind(on_press = lambda widget: self.resultDefinitionPage ( item ))
                gridlayout.add_widget(resButton)

            # Create Scrollable widget, add grid layout
            scroll = ScrollView(id='scroll', size_hint=(None, None), size=(400, 200), \
                pos_hint={'center_x':.5, 'center_y':.45})
            scroll.add_widget(gridlayout)

            # Add the scrollable widget to the results page.
            self.screens["menu"].ids.search.add_widget(scroll)

    def resultDefinitionPage(self, res):
        '''
        Given result res, return both the result and its given definition
        '''

        #If the user had made a previous search, remove the results,
        # otherwise the values will stil be in the screen
        for child in self.screens["menu"].ids.definition.children:
            if child.id in ['phrase', 'meaning']:
                self.screens["menu"].ids.definition.remove_widget(child)

        # Create label for query result, add it to screen
        result = Label(id = 'phrase', text = res[0], size_hint_y=None, height=40, \
            pos_hint={'center_x':.5, 'center_y':.8})
        self.screens["menu"].ids.definition.add_widget(result)
        
        # Create label for result definition, add it to screen
        definition = Label(id = 'meaning', text = res[1], size_hint_y=None, height=40, \
            pos_hint={'center_x':.5, 'center_y':.5})
        self.screens["menu"].ids.definition.add_widget(definition)

        #navigate to the next page
        self.screens["menu"].ids.manager.current = 'Definition'

    def addToIgnore(self, obj):
        '''
        Add obj to list of objects to ignore in future searches.
        '''
        if obj not in self.ignoreList:
            self.ignoreList.append(obj)
        self.showIgnore(self.ignoreList)

    def removeFromIgnore(self, obj):
        '''
        Remove obj from list of ignored searches
        '''
        if obj in self.ignoreList:
            self.ignoreList.remove(obj)

    def showIgnore(self, lst):
        '''
        Show list of ignored items
        '''
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        #Make sure the height is such that there is something to scroll.
        layout.bind(minimum_height=layout.setter('height'))
        for i in lst:
            item = Label(text=i, size_hint_y=None, height=40)
            layout.add_widget(item)
        scroll = ScrollView(size=(400, 200), size_hint=(None, None), \
            pos_hint={'center_x':.5, 'center_y':.45})
        scroll.add_widget(layout)

        self.screens["settings"].ids.ignorebox.add_widget(scroll)

    def addToHistory(self, obj):
        '''
        Add obj to list of objects to ignore in future searches.
        '''
        if obj not in self.historyList:
            self.historyList.append(obj)
        self.showHistory(self.historyList)

    def showHistory(self, lst):
        '''
        Show Search history as scrollable label
        '''
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        #Make sure the height is such that there is something to scroll.
        layout.bind(minimum_height=layout.setter('height'))
        for i in lst:
            item = Label(text=i, size_hint_y=None, height=40)
            layout.add_widget(item)
        scroll = ScrollView(size=(400, 200), size_hint=(None, None), \
            pos_hint={'center_x':.5, 'center_y':.45})
        scroll.add_widget(layout)

        self.screens["menu"].ids.history.add_widget(scroll)

if __name__ == '__main__':
    CSCGroupNineApp().run()