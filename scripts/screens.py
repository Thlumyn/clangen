from .clan import *
from .events import *
from math import ceil, floor


# SCREENS PARENT CLASS
class Screens(object):
    game_screen = screen
    game_x = screen_x
    game_y = screen_y
    all_screens = {}
    last_screen = ''  # store the screen that the user will go back to after clicking 'back' button

    def __init__(self, name=None):
        self.name = name
        if name is not None:
            self.all_screens[name] = self
            game.all_screens[name] = self

    def on_use(self):
        pass

    def screen_switches(self):
        pass


# SCREEN CHILD CLASSES
class StartScreen(Screens):
    def on_use(self):
        # layout
        verdana_big.text('Welcome to CLAN GENERATOR.', ('center', 100))
        example_cat.draw_big((350, 150))

        # buttons
        if game.clan is not None:
            buttons.draw_button(('center', 300), text='Continue >', cur_screen='clan screen')
            buttons.draw_button(('center', 350), text='Switch Clan >', cur_screen='switch clan screen')
        else:
            buttons.draw_button(('center', 300), text='Continue >', available=False)
            buttons.draw_button(('center', 350), text='Switch Clan >', available=False)
        buttons.draw_button(('center', 400), text='Make New >', cur_screen='make clan screen')
        buttons.draw_button(('center', 450), text='Settings & Info >', cur_screen='settings screen')

    def screen_switches(self):
        if game.clan is not None:
            key_copy = tuple(cat_class.all_cats.keys()) 
            for x in key_copy:
                if x not in game.clan.clan_cats:
                    game.clan.remove_cat(x)

        # SAVE cats
        if game.clan is not None:
            cat_class.save_cats()
            game.clan.save_clan()

        # LOAD settings
        game.load_settings()

class SwitchClanScreen(Screens):
    def on_use(self):
        verdana_big.text('Switch Clan:', ('center', 100))
        verdana.text('Note: this will close the game. When you open it next, it should have the new clan.', ('center', 150))
        game.switches['read_clans']=True 

        y_pos=200

        for i in range(len(game.switches['clan_list'])):
            if len(game.switches['clan_list'][i])>1 and i<9:
                buttons.draw_button(('center', 50*i+y_pos), text=game.switches['clan_list'][i] + 'clan', switch_clan=game.switches['clan_list'][i])


        buttons.draw_button((50, 50), text='<< Back to Main Menu', cur_screen='start screen')

class SettingsScreen(Screens):
    text_size = {'0': 'small', '1': 'medium', '2': 'big'}  # How text sizes will show up on the screen
    bool = {True: 'Yes', False: 'No', None: 'None'}

    def on_use(self):
        # layout
        buttons.draw_button((330, 100), text='Settings', available=False)
        buttons.draw_button((-340, 100), text='Info', cur_screen='info screen')
        verdana.text("Change the setting of your game here.", ('center', 130))

        # Setting names
        verdana.text("Text size: (unavailable)", (100, 200))
        verdana.text("Allow couples to have kittens despite same-sex status:", (100, 230))

        verdana.text("Allow unmated cats to have offspring:", (100, 260))

        # Setting values
        verdana.text(self.text_size[game.settings['text size']], (-170, 200))
        buttons.draw_button((-80, 200), text='SWITCH', setting='text size', available=False)
        verdana.text(self.bool[game.settings['no gendered breeding']], (-170, 230))
        buttons.draw_button((-80, 230), text='SWITCH', setting='no gendered breeding')
        verdana.text(self.bool[game.settings['no unknown fathers']], (-170, 260))
        buttons.draw_button((-80, 260), text='SWITCH', setting='no unknown fathers')

        # other buttons
        buttons.draw_button((50, 50), text='<< Back to Main Menu', cur_screen='start screen')
        if game.settings_changed:
            buttons.draw_button(('center', -150), text='Save Settings', save_settings=True)
        else:
            buttons.draw_button(('center', -150), text='Save Settings', available=False)


class InfoScreen(Screens):
    def on_use(self):
        # layout
        buttons.draw_button((330, 100), text='Settings', cur_screen='settings screen')
        buttons.draw_button((-340, 100), text='Info', available=False)
        verdana.text("Welcome to Warrior Cats clan generator!", ('center', 140))
        verdana.text("This is fan-made generator for the Warrior Cats -book series by Erin Hunter.", ('center', 175))
        verdana.text("Create a new clan in the 'Make New' section. That clan is saved and can be", ('center', 195))
        verdana.text("revisited until you decide the overwrite it with a new one.", ('center', 215))
        verdana.text("You're free to use the characters and sprites generated in this program", ('center', 235))
        verdana.text("as you like, as long as you don't claim the sprites as your own creations.", ('center', 255))
        verdana.text("Contact me @ just-some-cat.tumblr.com .", ('center', 275))

        verdana.text("Updates 0.2:", ('center', 320))
        verdana.text("- Time can now go forward; clan cats grow older now when 'timeskip' is used", ('center', 350))
        verdana.text("- Cats can be paired together and have litters of kittens", ('center', 370))
        verdana.text("- Starclan has been added for dead cats", ('center', 390))
        verdana.text("- Cats can die (but only of old age at around 200 moons)", ('center', 410))
        verdana.text("- A list page for the clan cats has been added for a more organized view", ('center', 430))
        verdana.text("- Minor additions to fur patterns etc.", ('center', 450))

        verdana.text("Thank you for playing!!", ('center', 550))

        # other buttons
        buttons.draw_button((50, 50), text='<< Back to Main Menu', cur_screen='start screen')


class ClanScreen(Screens):
    def on_use(self):
        # layout
        verdana_big.text(game.clan.name + 'Clan', ('center', 30))
        verdana.text('Leader\'s Den', game.clan.cur_layout['leader den'])
        verdana.text('Medicine Cat Den', game.clan.cur_layout['medicine den'])
        verdana.text('Nursery', game.clan.cur_layout['nursery'])
        verdana.text('Clearing', game.clan.cur_layout['clearing'])
        verdana.text('Apprentices\' Den', game.clan.cur_layout['apprentice den'])
        verdana.text('Warriors\' Den', game.clan.cur_layout['warrior den'])
        verdana.text('Elders\' Den', game.clan.cur_layout['elder den'])

        for x in game.clan.clan_cats:
            if not cat_class.all_cats[x].dead:
                buttons.draw_button(cat_class.all_cats[x].placement, image=cat_class.all_cats[x].sprite, cat=x,
                                    cur_screen='profile screen')

        # buttons
        buttons.draw_button((290, 70), text='EVENTS', cur_screen='events screen')
        buttons.draw_button((370, 70), text='CLAN', available=False)
        buttons.draw_button((430, 70), text='STARCLAN', cur_screen='starclan screen')
        buttons.draw_button((50, 50), text='< Back to Main Menu', cur_screen='start screen')
        buttons.draw_button((-70, 50), text='List Cats', cur_screen='list screen')
        buttons.draw_button(('center', -50), text='Save Clan', save_clan=True)

    def screen_switches(self):
        cat_profiles()
        game.switches['cat'] = None

        p = game.clan.cur_layout
        game.clan.leader.placement = choice(p['leader place'])
        game.clan.medicine_cat.placement = choice(p['medicine place'])

        # print 'SECOND SCREEN SWITCH, GAME.CLAN.CLAN_CATS:'
        # print game.clan.clan_cats
        for x in game.clan.clan_cats:
            i = randint(0, 20)
            if cat_class.all_cats[x].status == 'warrior':
                if i < 15:  # higher chance for warriors to end up in warriors den or the clearing
                    cat_class.all_cats[x].placement = choice([choice(p['warrior place']), choice(p['clearing place'])])
                else:
                    cat_class.all_cats[x].placement = choice([choice(p['nursery place']), choice(p['leader place']),
                                                              choice(p['elder place']), choice(p['medicine place']),
                                                              choice(p['apprentice place'])])
            elif cat_class.all_cats[x].status == 'kitten':
                if i < 13:
                    cat_class.all_cats[x].placement = choice(p['nursery place'])
                elif i == 19:
                    cat_class.all_cats[x].placement = choice(p['leader place'])
                else:
                    cat_class.all_cats[x].placement = choice([choice(p['clearing place']), choice(p['warrior place']),
                                                              choice(p['elder place']), choice(p['medicine place']),
                                                              choice(p['apprentice place'])])
            elif cat_class.all_cats[x].status == 'elder':
                cat_class.all_cats[x].placement = choice(p['elder place'])
            elif cat_class.all_cats[x].status == 'apprentice':
                if i < 13:
                    cat_class.all_cats[x].placement = choice([choice(p['apprentice place']),
                                                              choice(p['clearing place'])])
                elif i >= 19:
                    cat_class.all_cats[x].placement = choice(p['leader place'])
                else:
                    cat_class.all_cats[x].placement = choice([choice(p['nursery place']), choice(p['warrior place']),
                                                              choice(p['elder place']), choice(p['medicine place'])])
            elif cat_class.all_cats[x].status == 'medicine cat apprentice':
                cat_class.all_cats[x].placement = choice(p['medicine place'])
            elif cat_class.all_cats[x].status == 'medicine cat':
                cat_class.all_cats[x].placement = choice(p['medicine place'])
                                                              


class StarClanScreen(Screens):
    def on_use(self):
        # layout
        verdana_big.text(game.clan.name + 'Clan', ('center', 30))
        verdana.text('StarClan Cat List', ('center', 100))

        #make a list of just dead cats
        dead_cats = [game.clan.instructor]
        for x in range(len(cat_class.all_cats.values())):
            the_cat = list(cat_class.all_cats.values())[x]
            if the_cat.dead and the_cat.ID != game.clan.instructor.ID:
                dead_cats.append(the_cat)

        # pages
        all_pages = 1  # amount of pages
        if len(dead_cats) > 24:
            all_pages = int(ceil(len(dead_cats)/24.0))

        # dead cats
        pos_x = 0
        pos_y = 0
        cats_on_page = 0  # how many are on page already
        for x in range(len(dead_cats)):
            if (x + (game.switches['list_page']-1)*24)>len(dead_cats):
                game.switches['list_page']=1
            
            the_cat = dead_cats[x + (game.switches['list_page']-1)*24]
            if the_cat.dead:
                buttons.draw_button((130 + pos_x, 180 + pos_y), image=the_cat.sprite, cat=the_cat.ID,
                                    cur_screen='profile screen')
                # name length
                name_len = verdana.text(str(the_cat.name))
                verdana.text(str(the_cat.name), (155 + pos_x - name_len/2, 240 + pos_y))
                cats_on_page += 1
                pos_x += 100
                if pos_x >= 600:
                    pos_x = 0
                    pos_y += 100

                if cats_on_page >= 24 or x + (game.switches['list_page']-1)*24 == len(dead_cats)-1:
                    break

        # page buttons
        verdana.text('page ' + str(game.switches['list_page']) + ' / ' + str(all_pages), ('center', 600))
        if game.switches['list_page'] > 1:
            buttons.draw_button((300, 600), text='<', list_page=game.switches['list_page'] - 1)
        if game.switches['list_page'] < all_pages:
            buttons.draw_button((-300, 600), text='>', list_page=game.switches['list_page'] + 1)


            
    # def on_use(self):

        
    #     # layout
    #     verdana_big.text(game.clan.name + 'Clan', ('center', 30))
    #     verdana.text('You are visiting StarClan.', ('center', 100))

    #     # instructor cat
    #     buttons.draw_button(('center', 120), image=game.clan.instructor.sprite, cat=game.clan.instructor.ID,
    #                         cur_screen='profile screen')
    #     verdana.text(str(game.clan.instructor.name), ('center', 170))

    #     # dead cats
    #     pos_x = 0
    #     pos_y = 0
    #     for x in game.clan.starclan_cats:
    #         if x != game.clan.instructor.ID:  # Instructor has their own spot in starclan
    #             buttons.draw_button((100 + pos_x, 250 + pos_y), image=cat_class.all_cats[x].sprite, cat=x,
    #                                 cur_screen='profile screen')
    #             verdana.text(str(cat_class.all_cats[x].name), (90 + pos_x, 310 + pos_y))
    #             pos_x += 100
    #             if pos_x >= 500:
    #                 pos_x = 0
    #                 pos_y += 100

        # buttons
        buttons.draw_button((290, 70), text='EVENTS', cur_screen='events screen')
        buttons.draw_button((370, 70), text='CLAN', cur_screen='clan screen')
        buttons.draw_button((430, 70), text='STARCLAN', available=False)
        buttons.draw_button((50, 50), text='< Back to Main Menu', cur_screen='start screen')
        buttons.draw_button((-70, 50), text='List Cats', cur_screen='list screen')


class MakeClanScreen(Screens):
    def first_phase(self):
        # layout
        verdana_big.text('NAME YOUR CLAN!', ('center', 150))
        self.game_screen.blit(game.naming_box, (310, 200))
        verdana.text(game.switches['naming_text'], (315, 200))
        verdana.text('-Clan', (455, 200))
        verdana.text('Max ten letters long. Don\'t include "Clan" in it.', ('center', 250))

        # buttons
        verdana_small.text('Note: going back to main menu resets the generated cats.', (50, 25))
        buttons.draw_button((50, 50), text='<< Back to Main Menu', cur_screen='start screen', naming_text='')
        writer.draw((290, 300))
        buttons.draw_button(('center', 500), text='Name Clan', clan_name=game.switches['naming_text'])

    def second_phase(self):
        # LAYOUT
        verdana.text(game.switches['clan_name']+'Clan', ('center', 90))
        verdana.text('These twelve cats are your potential clan members.', ('center', 115))
        verdana.text('Some of them will be left behind.', ('center', 135))
        verdana.text('First, pick your leader from them:', ('center', 160))

        # cat buttons / small sprites
        for u in range(6):
            buttons.draw_button((50, 150 + 50*u), image=game.choose_cats[u].sprite,
                                cat=u)
        for u in range(6, 12):
            buttons.draw_button((screen_x - 100, 150 + 50*(u-6)), image=game.choose_cats[u].sprite,
                                cat=u)

        # cat profiles
        if game.switches['cat'] is not None and 12 > game.switches['cat'] >= 0:
            game.choose_cats[game.switches['cat']].draw_large((320, 200))
            verdana.text(str(game.choose_cats[game.switches['cat']].name) + ' --> ' +
                             game.choose_cats[game.switches['cat']].name.prefix + 'star', ('center', 360))
            verdana_small.text(str(game.choose_cats[game.switches['cat']].gender), (330, 385))
            verdana_small.text(str(game.choose_cats[game.switches['cat']].age), (330, 405))
            if game.choose_cats[game.switches['cat']].age == 'kitten':
                verdana_baby.text(str(game.choose_cats[game.switches['cat']].trait), (330, 425))
            else:
                verdana_small.text(str(game.choose_cats[game.switches['cat']].trait), (330, 425))

            if game.choose_cats[game.switches['cat']].age in ['kitten', 'adolescent']:
                verdana_red.text('Too young to become leader.', ('center', 490))
            else:
                buttons.draw_button(('center', 490), text='Grant this cat their nine lives',
                                    leader=game.switches['cat'])

        # buttons
        verdana_small.text('Note: going back to main menu resets the generated cats.', (50, 25))
        buttons.draw_button((50, 50), text='<< Back to Main Menu', cur_screen='start screen', naming_text='')
        buttons.draw_button((-50, 50), text='< Last step', clan_name='', cat=None)

    def third_phase(self):
        # LAYOUT
        verdana.text(game.switches['clan_name'] + 'Clan', ('center', 90))
        verdana.text('Second, pick your medicine cat:', ('center', 120))

        # cat buttons / small sprites
        for u in range(6):
            if game.switches['leader'] == u:
                game.choose_cats[u].draw((screen_x/2 - 25, 550))
            else:
                buttons.draw_button((50, 150 + 50 * u), image=game.choose_cats[u].sprite,
                                    cat=u)
        for u in range(6, 12):
            if game.switches['leader'] == u:
                game.choose_cats[u].draw((screen_x/2 - 25, 550))
            else:
                buttons.draw_button((screen_x - 100, 150 + 50 * (u - 6)), image=game.choose_cats[u].sprite,
                                    cat=u)

        # cat profiles
        if 12 > game.switches['cat'] >= 0 and game.switches['cat'] != game.switches['leader']:
            game.choose_cats[game.switches['cat']].draw_large((320, 200))
            verdana.text(str(game.choose_cats[game.switches['cat']].name), ('center', 360))
            verdana_small.text(str(game.choose_cats[game.switches['cat']].gender), (330, 385))
            verdana_small.text(str(game.choose_cats[game.switches['cat']].age), (330, 405))
            verdana_small.text(str(game.choose_cats[game.switches['cat']].trait), (330, 425))

            if game.choose_cats[game.switches['cat']].age == 'kitten':
                verdana_red.text('Too young to become medicine cat.', ('center', 490))
            else:
                buttons.draw_button(('center', 490), text='This cat will take care of the clan',
                                    medicine_cat=game.switches['cat'])

        # buttons
        verdana_small.text('Note: going back to main menu resets the generated cats.', (50, 25))
        buttons.draw_button((50, 50), text='<< Back to Main Menu', cur_screen='start screen', naming_text='')
        buttons.draw_button((-50, 50), text='< Last step', leader=None, cat=None)

    def fourth_phase(self):
        # LAYOUT
        verdana.text(game.switches['clan_name'] + 'Clan', ('center', 90))
        verdana.text('Finally, recruit from 4 to 7 more members to your clan.', ('center', 120))
        verdana.text('Choose wisely...', ('center', 150))

        # cat buttons / small sprites
        for u in range(6):
            if game.switches['leader'] == u:
                game.choose_cats[u].draw((screen_x / 2 - 50, 550))
            elif game.switches['medicine_cat'] == u:
                game.choose_cats[u].draw((screen_x / 2, 550))
            elif u in game.switches['members']:
                game.choose_cats[u].draw((screen_x / 2 - 50*(u+2), 550))
            else:
                buttons.draw_button((50, 150 + 50 * u), image=game.choose_cats[u].sprite,
                                    cat=u)
        for u in range(6, 12):
            if game.switches['leader'] == u:
                game.choose_cats[u].draw((screen_x / 2 - 50, 550))
            elif game.switches['medicine_cat'] == u:
                game.choose_cats[u].draw((screen_x / 2, 550))
            elif u in game.switches['members']:
                game.choose_cats[u].draw((screen_x / 2 + 50*(u-5), 550))
            else:
                buttons.draw_button((screen_x - 100, 150 + 50 * (u - 6)), image=game.choose_cats[u].sprite,
                                    cat=u)

        # cat profiles
        if 12 > game.switches['cat'] >= 0 and \
                game.switches['cat'] not in [game.switches['leader'], game.switches['medicine_cat']]\
                and game.switches['cat'] not in game.switches['members']:
            game.choose_cats[game.switches['cat']].draw_large((320, 200))
            verdana.text(str(game.choose_cats[game.switches['cat']].name), ('center', 360))
            verdana_small.text(str(game.choose_cats[game.switches['cat']].gender), (330, 385))
            verdana_small.text(str(game.choose_cats[game.switches['cat']].age), (330, 405))
            verdana_small.text(str(game.choose_cats[game.switches['cat']].trait), (330, 425))

            if len(game.switches['members']) < 7:
                buttons.draw_button(('center', 490), text='Recruit', members=game.switches['cat'], add=True)

        verdana_small.text('Note: if you have more than 8 clans, clicking done deletes the least recently used clan.', ('center', 660))

        # buttons
        verdana_small.text('Note: going back to main menu resets the generated cats.', (50, 25))
        buttons.draw_button((50, 50), text='<< Back to Main Menu', cur_screen='start screen', naming_text='')
        buttons.draw_button((-50, 50), text='< Last step', medicine_cat=None, members=[], cat=None)
        if len(game.switches['members']) > 3:
            buttons.draw_button(('center', 630), text='Done', cur_screen='clan created screen')
        else:
            buttons.draw_button(('center', 630), text='Done', available=False)

    def on_use(self):
        if len(game.switches['clan_name']) == 0:
            self.first_phase()
        elif len(game.switches['clan_name']) > 0 and game.switches['leader'] is None:
            self.second_phase()
        elif game.switches['leader'] is not None and game.switches['medicine_cat'] is None:
            self.third_phase()
        else:
            self.fourth_phase()

    def screen_switches(self):
        game.switches['clan_name'] = ''
        writer.upper = True
        game.switches['leader'] = None
        game.switches['cat'] = None
        game.switches['medicine_cat'] = None
        game.switches['members'] = []
        example_cats()


class ClanCreatedScreen(Screens):
    def on_use(self):
        # LAYOUT
        verdana.text('Your clan has been created and saved!', ('center', 50))
        game.clan.leader.draw_big((screen_x/2 - 50, 100))

        # buttons
        buttons.draw_button(('center', 250), text='Continue', cur_screen='clan screen')

    def screen_switches(self):
        game.clan = Clan(game.switches['clan_name'], game.choose_cats[game.switches['leader']],
                         game.choose_cats[game.switches['medicine_cat']])
        """for i in cat_class.all_cats.values():
            not_found = True
            for x in game.switches['members']:
                if i == game.choose_cats[x]:
                    game.clan.add_cat(i)
                    not_found = False
            if i != game.choose_cats[game.switches['leader']] and i != game.choose_cats[game.switches['medicine_cat']]\
                    and not_found:
                game.clan.remove_cat(i.ID)
                i.example = True
        cat_class.save_cats()
        game.clan.save_clan()

        # give thoughts/actions to cats
        cat_class.thoughts()"""
        game.clan.create_clan()


class EventsScreen(Screens):
    def on_use(self):
        # LAYOUT
        verdana_big.text(game.clan.name + 'Clan', ('center', 30))
        verdana.text('Check this page to see which events are currently happening at the clan.', ('center', 100))
        verdana.text('(currently unavailable)', ('center', 130))
        verdana.text('Clan age: ' + str(game.clan.age) + ' moons', ('center', 160))

        if game.switches['events_left'] == 0:
            buttons.draw_button(('center', 200), text='TIMESKIP ONE MOON', timeskip=True)
            if game.switches['timeskip']:
                game.cur_events_list = []
        else:
            buttons.draw_button(('center', 200), text='TIMESKIP ONE MOON', available=False)
        cat_class.one_moon()
        verdana_red.text('Remember to save - the game doesn\'t save automatically.', ('center', 230))

        if game.cur_events_list is not None and game.cur_events_list != []:
            a=0
            for x in range(len(game.cur_events_list)):
                verdana.text(game.cur_events_list[x], ('center', 270 + a*30))
                a += 1
            

        #"""a = 0
        #if len(game.cur_events) > 0:
        #    for x in game.cur_events.keys():
        #        events_class.all_events[x].news(('center', 150 + a))
        #        screen_buttons['event'].draw_button(('center', 200 + a))
        #        screen_buttons['event'].check()
        #        a += 150"""

        # buttons
        buttons.draw_button((50, 50), text='< Back to Main Menu', cur_screen='start screen')
        buttons.draw_button((290, 70), text='EVENTS', available=False)
        buttons.draw_button((370, 70), text='CLAN', cur_screen='clan screen')
        buttons.draw_button((430, 70), text='STARCLAN', cur_screen='starclan screen')


class ProfileScreen(Screens):
    def on_use(self):
        # use this variable to point to the cat object in question
        the_cat = cat_class.all_cats[game.switches['cat']]
        # use these attributes to create differing profiles for starclan cats etc.
        is_instructor = False
        if the_cat.dead:
            if game.clan.instructor.ID == the_cat.ID:
                is_instructor = True

        # Info in string
        cat_name = str(the_cat.name)  # name
        cat_thought = the_cat.thought  # thought
        if the_cat.dead:
            cat_name += " (dead)"  # A dead cat will have the (dead) sign next to their name
        if is_instructor:
            cat_thought = "Hello. I am here to guide the dead cats of " + game.clan.name + "Clan into StarClan."

        # LAYOUT
        verdana_big.text(cat_name, ('center', 70))  # NAME
        the_cat.draw_large(('center', 100))  # IMAGE
        verdana.text(cat_thought, ('center', 300))  # THOUGHT / ACTION
        verdana_small.text(the_cat.gender, ('center', 330))  # SEX / GENDER
        verdana_small.text(the_cat.status, ('center', 345))  # STATUS
        verdana_small.text(the_cat.age, ('center', 360))  # AGE
        verdana_small.text(the_cat.trait, ('center', 375))  # CHARACTER TRAIT
        verdana_small.text(the_cat.skill, ('center', 390))  # SPECIAL SKILL
        verdana_small.text('eyes: ' + the_cat.eye_colour.lower(), ('center', 405))  # EYE COLOR
        verdana_small.text('pelt: ' + the_cat.pelt.name.lower(), ('center', 420))  # PELT TYPE
        verdana_small.text('fur length: ' + the_cat.pelt.length, ('center', 435))  # PELT LENGTH

        # PARENTS
        if the_cat.parent1 is None:
            verdana_small.text('parents: unknown', ('center', 450))
        elif the_cat.parent2 is None:
            par1 = str(the_cat.all_cats[the_cat.parent1].name)
            verdana_small.text('parents: '+par1+', unknown', ('center', 450))
        else:
            if the_cat.parent1 in the_cat.all_cats and the_cat.parent2 in the_cat.all_cats:
                par1 = str(the_cat.all_cats[the_cat.parent1].name)
                par2 = str(the_cat.all_cats[the_cat.parent2].name)
            elif the_cat.parent1 in the_cat.all_cats:
                par2 = "Error: Cat#" + the_cat.parent2 + " not found"
                par1 = str(the_cat.all_cats[the_cat.parent1].name)
            elif the_cat.parent2 in the_cat.all_cats:
                par1 = "Error: Cat#" + the_cat.parent1 + " not found"
                par2 = str(the_cat.all_cats[the_cat.parent2].name)
            else: 
                par1 = "Error: Cat#" + the_cat.parent1 + " not found"
                par2 = "Error: Cat#" + the_cat.parent2 + " not found"

            
            verdana_small.text('parents: ' + par1 + ' and ' + par2, ('center', 450))

        # MOONS
        if the_cat.dead:
            verdana_small.text(str(the_cat.moons) + ' moons (in life)', ('center', 465))
            verdana_small.text(str(the_cat.dead_for) + ' moons (in death)', ('center', 480))
        else:
            verdana_small.text(str(the_cat.moons) + ' moons', ('center', 465))

        # MATE
        if the_cat.mate is not None and not the_cat.dead:
            if the_cat.mate in cat_class.all_cats:
                verdana_small.text('mate: ' + str(cat_class.all_cats[the_cat.mate].name), ('center', 480))
            else:
                verdana_small.text('Error: mate: ' + str(the_cat.mate) + " not found", ('center', 480))

        # buttons
        buttons.draw_button((300, -160), text='See Family ', cur_screen='see kits screen')
        if not the_cat.dead:
            buttons.draw_button((-300, -160), text='Kill Cat', kill_cat=the_cat)

        if the_cat.age in ['young adult', 'adult', 'senior adult', 'elder'] and not the_cat.dead:
            buttons.draw_button(('center', -130), text='Pick mate for '+str(the_cat.name),
                                cur_screen='choose mate screen')

        if game.switches['new_leader'] is not False and game.switches['new_leader'] is not None:
            game.clan.new_leader(game.switches['new_leader'])

        if the_cat.status in ['warrior'] and not the_cat.dead and game.clan.leader.dead:
             buttons.draw_button(('center', -70), text='Promote to Leader', new_leader=the_cat)

        if game.switches['apprentice_switch'] is not False and game.switches['apprentice_switch'] is not None and game.switches['apprentice_switch'].status=='apprentice':
            game.switches['apprentice_switch'].status_change('medicine cat apprentice')
            game.switches['apprentice_switch'] = False

        if game.switches['apprentice_switch'] is not False and game.switches['apprentice_switch'] is not None and game.switches['apprentice_switch'].status=='medicine cat apprentice':
            game.switches['apprentice_switch'].status_change('apprentice')
            game.switches['apprentice_switch'] = False

        if game.switches['kill_cat'] is not False and game.switches['kill_cat'] is not None:
            game.switches['kill_cat'].dies()
            game.switches['kill_cat'] = False


        if the_cat.status in ['apprentice'] and not the_cat.dead:
             buttons.draw_button(('center', -70), text='Switch to medicine cat apprentice', apprentice_switch=the_cat)

        if the_cat.status in ['medicine cat apprentice'] and not the_cat.dead:
             buttons.draw_button(('center', -70), text='Switch to warrior apprentice', apprentice_switch=the_cat)

        buttons.draw_button(('center', -100), text='Back', cur_screen=game.switches['last_screen'])


class SingleEventScreen(Screens):
    def on_use(self):
        # LAYOUT
        if game.switches['event'] is not None:
            events_class.all_events[game.switches['event']].page()

        # buttons
        buttons.draw_button(('center', -150), text='Continue', cur_screen='events screen')

    def screen_switches(self):
        pass

class ViewChildrenScreen(Screens):
    def on_use(self):
        the_cat = cat_class.all_cats[game.switches['cat']]

        verdana_big.text('Family of ' + str(the_cat.name), ('center', 50))
        
        verdana.text('Parents:', ('center', 85))
        #the_cat.all_cats[the_cat.parent1].name
        if the_cat.parent1 is None:
            verdana_small.text('Unknown', (342, 165))
        elif the_cat.parent1 in cat_class.all_cats:
            buttons.draw_button((350, 120), image=cat_class.all_cats[the_cat.parent1].sprite, cat=the_cat.parent1,
                                    cur_screen='profile screen')
            name_len = verdana.text(str(cat_class.all_cats[the_cat.parent1].name))
            verdana_small.text(str(cat_class.all_cats[the_cat.parent1].name), (375 - name_len/2, 185))
        else:
            verdana_small.text('Error: cat ' + str(the_cat.parent1) + ' not found', (342, 165))

        if the_cat.parent2 is None:
            verdana_small.text('Unknown', (422, 165))
        elif the_cat.parent2 in cat_class.all_cats:
            buttons.draw_button((430, 120), image=cat_class.all_cats[the_cat.parent2].sprite, cat=the_cat.parent2,
                                    cur_screen='profile screen')                           
            name_len = verdana.text(str(cat_class.all_cats[the_cat.parent2].name))
            verdana_small.text(str(cat_class.all_cats[the_cat.parent2].name), (455 - name_len/2, 185))
        else:
            verdana_small.text('Error: cat ' + str(the_cat.parent2) + ' not found', (342, 165))

        
        pos_x = 0
        pos_y = 20

        siblings = False
        for x in game.clan.clan_cats:
            if the_cat.parent1 == cat_class.all_cats[x].parent1 and the_cat.parent2 == cat_class.all_cats[x].parent2 and the_cat.ID != cat_class.all_cats[x].ID and the_cat.parent1 is not None:
                buttons.draw_button((40 + pos_x, 220 + pos_y), image=cat_class.all_cats[x].sprite, cat=cat_class.all_cats[x].ID,
                                cur_screen='profile screen')
                name_len = verdana.text(str(cat_class.all_cats[x].name))
                verdana_small.text(str(cat_class.all_cats[x].name), (65 + pos_x - name_len/2, 280 + pos_y))
                siblings = True
                pos_x += 80
                if pos_x > 640:
                    pos_y += 70
                    pos_x = 0
        if siblings:
            verdana.text('Siblings:', ('center', 210))
        else:
            verdana.text('This cat has no siblings.', ('center', 210))

        buttons.draw_button(('center', -100), text='Back', cur_screen='profile screen')

        pos_x = 0
        pos_y = 60

        kittens = False
        for x in game.clan.clan_cats:
            if the_cat.ID in [cat_class.all_cats[x].parent1, cat_class.all_cats[x].parent2]:
                buttons.draw_button((40 + pos_x, 370 + pos_y), image=cat_class.all_cats[x].sprite, cat=cat_class.all_cats[x].ID,
                                cur_screen='profile screen')
                name_len = verdana.text(str(cat_class.all_cats[x].name))
                verdana_small.text(str(cat_class.all_cats[x].name), (65 + pos_x - name_len/2, 430 + pos_y))
                kittens = True
                pos_x += 80
                if pos_x > 640:
                    pos_y += 70
                    pos_x = 0
        if kittens:
            verdana.text('Offspring:', ('center', 400))
        else:
            verdana.text('This cat has never had offspring.', ('center', 400))

        buttons.draw_button(('center', -100), text='Back', cur_screen='profile screen')


class ChooseMateScreen(Screens):
    def on_use(self):
        # use this variable to point to the cat object in question
        the_cat = cat_class.all_cats[game.switches['cat']]

        # LAYOUT
        # cat's info
        verdana_big.text('Choose mate for ' + str(the_cat.name), ('center', 50))
        verdana_small.text('If the cat has chosen a mate, they will stay loyal and not have kittens with anyone else,',
                           ('center', 80))
        verdana_small.text('even if having kittens in said relationship is impossible.', ('center', 95))
        verdana_small.text('Chances of having kittens when possible is heightened though.', ('center', 110))
        the_cat.draw_large((200, 130))
        verdana_small.text(the_cat.age, (70, 200))
        verdana_small.text(the_cat.gender, (70, 215))
        verdana_small.text(the_cat.trait, (70, 230))

        # mate's/potential mate's info
        mate = None
        if game.switches['mate'] is not None and the_cat.mate is None:
            mate = cat_class.all_cats[game.switches['mate']]
        elif the_cat.mate is not None:
            if the_cat.mate in cat_class.all_cats:
                mate = cat_class.all_cats[the_cat.mate]
            else:
                the_cat.mate = None

        if mate is not None:
            mate.draw_large((450, 130))
            verdana.text(str(mate.name), ('center', 300))
            verdana_small.text(mate.age, (-100, 200))
            verdana_small.text(mate.gender, (-100, 215))
            verdana_small.text(mate.trait, (-100, 230))

            if the_cat.gender == mate.gender or 'elder' in [the_cat.age, mate.age]:
                verdana_small.text('(this pair will not be able to have kittens)', ('center', 320))

        valid_mates=[]
        pos_x = 0
        pos_y = 20 
        if the_cat.mate is None:  # if the cat doesn't already have a mate
            
            for x in game.clan.clan_cats:
                # possible mate as a Cat object
                pos_mate = cat_class.all_cats[x]
                


                # makign sure the pairing is possible and appropriate
                if not pos_mate.dead and pos_mate.age in ['young adult', 'adult', 'senior adult', 'elder'] and\
                        the_cat != pos_mate and the_cat.ID not in [pos_mate.parent1, pos_mate.parent2] and\
                        pos_mate.ID not in [the_cat.parent1, the_cat.parent2] and pos_mate.mate is None and\
                        (pos_mate.parent1 is None or pos_mate.parent1 not in [the_cat.parent1, the_cat.parent2]) and\
                        (pos_mate.parent2 is None or pos_mate.parent2 not in [the_cat.parent1, the_cat.parent2]):

                    # Making sure the ages are appropriate
                    if the_cat.age in ['senior adult', 'elder'] and cat_class.all_cats[x].age in ['senior adult',
                                                                                                  'elder']:
                        valid_mates.append(cat_class.all_cats[x])
                    elif cat_class.all_cats[x].age != 'elder' and the_cat.age != 'elder':
                        valid_mates.append(cat_class.all_cats[x])

                         
            all_pages = 1  # amount of pages
            if len(valid_mates) > 27:
                all_pages = int(ceil(len(valid_mates)/27.0))

                # dead cats
            
            cats_on_page = 0  # how many are on page already
            for x in range(len(valid_mates)):
                if (x + (game.switches['list_page']-1)*27)>len(valid_mates):
                    game.switches['list_page']=1
                pot_mate = valid_mates[x + (game.switches['list_page']-1)*27]
                ## draw mates
                buttons.draw_button((100 + pos_x, 320 + pos_y), image=pot_mate.sprite, mate=pot_mate.ID)
                pos_x += 50
                cats_on_page +=1
                if pos_x > 400:
                    pos_y += 50
                    pos_x = 0
                if cats_on_page >= 27 or x + (game.switches['list_page']-1)*27 == len(valid_mates)-1:
                    break

            # page buttons
            verdana.text('page ' + str(game.switches['list_page']) + ' / ' + str(all_pages), ('center', 600))
            if game.switches['list_page'] > 1:
                buttons.draw_button((300, 600), text='<', list_page=game.switches['list_page'] - 1)
            if game.switches['list_page'] < all_pages:
                buttons.draw_button((-300, 600), text='>', list_page=game.switches['list_page'] + 1)



                

        else:
            verdana.text('Already in a relationship.', ('center', 340))
            # draw kittens, if any
            kittens = False
            for x in game.clan.clan_cats:
                if the_cat.ID in [cat_class.all_cats[x].parent1, cat_class.all_cats[x].parent2] and\
                        mate.ID in [cat_class.all_cats[x].parent1, cat_class.all_cats[x].parent2]:
                    buttons.draw_button((200 + pos_x, 370 + pos_y), image=cat_class.all_cats[x].sprite, cat=cat_class.all_cats[x].ID,
                                    cur_screen='profile screen')
                    kittens = True
                    pos_x += 50
                    if pos_x > 400:
                        pos_y += 50
                        pos_x = 0
            if kittens:
                verdana.text('Their offspring:', ('center', 360))
            else:
                verdana.text('This pair has never had offspring.', ('center', 360))

        # buttons
        if mate is not None and the_cat.mate is None:
            buttons.draw_button(('center', -130), text="It\'s official!", cat_value=the_cat, mate=mate)
        elif the_cat.mate is not None:
            buttons.draw_button(('center', -130), text="Break it up...", cat_value=the_cat, mate=None)
        buttons.draw_button(('center', -100), text='Back', cur_screen='profile screen')

    def screen_switches(self):
        game.switches['mate'] = None


class ListScreen(Screens):
    # page can be found in game.switches['list_page']
    # the amount of cats a page can hold is 20, so the amount of pages is cats/20

    def on_use(self):
        # layout
        verdana_big.text(game.clan.name + 'Clan', ('center', 30))
        verdana.text('ALL CATS LIST', ('center', 100))

        #make a list of just living cats
        living_cats = []
        for x in range(len(cat_class.all_cats.values())):
            the_cat = list(cat_class.all_cats.values())[x]
            if not the_cat.dead:
                living_cats.append(the_cat)

        # pages
        all_pages = 1  # amount of pages
        if len(living_cats) > 24:
            all_pages = int(ceil(len(living_cats)/24.0))

        # dead cats
        pos_x = 0
        pos_y = 0
        cats_on_page = 0  # how many are on page already
        for x in range(len(living_cats)):
            if (x + (game.switches['list_page']-1)*24)>len(living_cats):
                game.switches['list_page']=1
            
            the_cat = living_cats[x + (game.switches['list_page']-1)*24]
            if not the_cat.dead:
                buttons.draw_button((130 + pos_x, 180 + pos_y), image=the_cat.sprite, cat=the_cat.ID,
                                    cur_screen='profile screen')
                # name length
                name_len = verdana.text(str(the_cat.name))
                verdana.text(str(the_cat.name), (155 + pos_x - name_len/2, 240 + pos_y))
                cats_on_page += 1
                pos_x += 100
                if pos_x >= 600:
                    pos_x = 0
                    pos_y += 100

                if cats_on_page >= 24 or x + (game.switches['list_page']-1)*24 == len(living_cats)-1:
                    break

        # page buttons
        verdana.text('page ' + str(game.switches['list_page']) + ' / ' + str(all_pages), ('center', 600))
        if game.switches['list_page'] > 1:
            buttons.draw_button((300, 600), text='<', list_page=game.switches['list_page'] - 1)
        if game.switches['list_page'] < all_pages:
            buttons.draw_button((-300, 600), text='>', list_page=game.switches['list_page'] + 1)

        # buttons
        buttons.draw_button((290, 70), text='EVENTS', cur_screen='events screen')
        buttons.draw_button((370, 70), text='CLAN', cur_screen='clan screen')
        buttons.draw_button((430, 70), text='STARCLAN', cur_screen='starclan screen')
        buttons.draw_button((50, 50), text='< Back to Main Menu', cur_screen='start screen')
        buttons.draw_button((-70, 50), text='List Cats', available=False)


# SCREENS
screens = Screens()

start_screen = StartScreen('start screen')
settings_screen = SettingsScreen('settings screen')
info_screen = InfoScreen('info screen')
clan_screen = ClanScreen('clan screen')

starclan_screen = StarClanScreen('starclan screen')
make_clan_screen = MakeClanScreen('make clan screen')
clan_created_screen = ClanCreatedScreen('clan created screen')
events_screen = EventsScreen('events screen')
profile_screen = ProfileScreen('profile screen')
single_event_screen = SingleEventScreen('single event screen')
choose_mate_screen = ChooseMateScreen('choose mate screen')
choose_mate_screen = ViewChildrenScreen('see kits screen')
list_screen = ListScreen('list screen')
switch_clan_screen = SwitchClanScreen('switch clan screen')


# CAT PROFILES
def cat_profiles():
    game.choose_cats.clear()
    game.cat_buttons.clear()
    for x in game.clan.clan_cats:
        game.choose_cats[x] = cat_class.all_cats[x]
        game.choose_cats[x].update_sprite()
