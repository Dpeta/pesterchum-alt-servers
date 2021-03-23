{"main":
 {"style": "background-color:rgba(0,0,0,0); background-repeat: no-repeat;",
  "background-image": "$path/scratchbg.png",
  "size": [650, 650],
  "icon": "$path/trayicon.png",
  "newmsgicon": "$path/trayicon2.png",
  "windowtitle": "Scratch",
  "close": { "image": "$path/x.png",
             "loc": [466, 54]},
  "minimize": { "image": "$path/m.png",
                "loc": [450, 60]},
  "menubar": { "style": "font-family: 'Arial'; font-size: 11px; font: bold; color: white;" },
  "menu" : { "style": "font-family: 'Arial'; font-size: 11px; font: bold; color: white; background-color: black; border:3px solid white;",
             "selected": "background-color: #545454",
             "menuitem": "margin-right:10px;",
             "loc": [175,53]
           },
  "sounds": { "alertsound": "$path/scratch.wav",
              "ceasesound": "$path/scratch2.wav" },
 "menus": {"client": {"_name": "Album",
                       "options": "Remix",
                       "memos": "Memos",
                       "logviewer": "Pesterlogs",
                       "randen": "Random Encounter",
                       "userlist": "Cronies",
                       "addgroup": "New Crew",
                       "import": "Import",
                       "reconnect": "Reconnect",
                       "idle": "Idle",
                       "exit": "Exit"},
            "profile": {"_name": "Track",
                        "switch": "Rap Name",
                        "theme": "Theme",
                        "color": "Color",
                        "block": "Haters",
                        "quirks": "Lingo" },
            "help": { "_name": "Info",
                      "help": "Info",
                      "calsprite": "Calsprite",
                      "nickserv": "NickServ",
                      "about": "The Deal" },
            "rclickchumlist": {"pester": "Patronize",
                               "removechum": "Forget",
                               "report": "Tell a Coppa",
                               "blockchum": "Slam",
                               "addchum": "Add to Crew",
                               "viewlog": "View Pesterlog",
                               "notes": "Edit Rhymes...",
                               "unblockchum": "Rectify",
                               "removegroup": "Forget Crew",
                               "renamegroup": "Rename Crew",
                               "movechum": "Change Crew",
                               "banuser": "Banish",
                               "opuser": "Hype",
                               "voiceuser": "Let Rap",
                               "quirkkill": "Kill Quirk",
                               "quirksoff": "Lingo Off",
                               "invitechum": "Invite Crew",
                               "memosetting": "Memo Settings",
                               "memonoquirk": "Disable Quirks",
                               "memohidden": "Hidden",
                               "memoinvite": "Invite-Only",
                               "memomute": "Mute" }
           },
  "chums": { "style": "font-size: 16px; background: black; border: 3px solid white; font-family: 'Arial';selection-background-color:rgb(100,100,100); color: white;",
             "loc": [175, 70],
             "size": [302, 500],
             "userlistcolor": "white",
             "moods": {

                 "chummy": { "icon": "$path/chummy.png", "color": "white" },

                 "rancorous": { "icon": "$path/rancorous.png", "color": "white" },

                 "offline": { "icon": "$path/offline.png", "color": "grey"},


                 "pleasant": { "icon": "$path/pleasant.png", "color": "white" },

                 "distraught": { "icon": "$path/distraught.png", "color": "white" },

                 "pranky": { "icon": "$path/pranky.png", "color": "white" },

                 "smooth": { "icon": "$path/smooth.png", "color": "white" },


                 "mystified": { "icon": "$path/mystified.png", "color": "white" },

                 "amazed": { "icon": "$path/amazed.png", "color": "white" },

                 "insolent": { "icon": "$path/insolent.png", "color": "white" },

                 "bemused": { "icon": "$path/bemused.png", "color": "white" },


                 "ecstatic": { "icon": "$path/ecstatic.png", "color": "red" },

                 "relaxed": { "icon": "$path/relaxed.png", "color": "red" },

                 "discontent": { "icon": "$path/discontent.png", "color": "red" },

                 "devious": { "icon": "$path/devious.png", "color": "red" },

                 "sleek": { "icon": "$path/sleek.png", "color": "red" },

                 "detestful": { "icon": "$path/detestful.png", "color": "red" },

                 "mirthful": { "icon": "$path/mirthful.png", "color": "red" },

                 "manipulative": { "icon": "$path/manipulative.png", "color": "red" },

                 "vigorous": { "icon": "$path/vigorous.png", "color": "red" },

                 "perky": { "icon": "$path/perky.png", "color": "red" },

                 "acceptant": { "icon": "$path/acceptant.png", "color": "red" },

                 "protective": { "icon": "$path/protective.png", "color": "lime" },

                 "blocked": { "icon": "$path/blocked.png", "color": "red" }

             }
           },
  "trollslum": {
      "style": "background: black; font-family: 'Arial'; color: white;",
      "size": [200, 450],
      "label": { "text": "Trollslum",
                 "style": "color: white ; font: bold; font-family: 'Arial'; border: 0px;" },
      "chumroll": {"style": "border: 3px solid white; background-color: black; color: white; padding: 5px; font: bold; font-family: 'Arial'; selection-background-color: rgb(100,100,100);" }
  },
  "mychumhandle": { "label": { "text": "",
                               "loc": [0,0],
                               "style": "color: rgba(0,0,0,0);" },
                    "handle": { "style": "background: black; padding: 3px; padding-left: 26px; color: white; font-family:'Arial'; font: bold; text-align:left; font-size: 12px; border: 3px solid white;",
                                "loc": [0,0],
                                "size": [0, 0] },
                    "colorswatch": { "loc": [0,0],
                                     "size": [0,0],
                                     "text": "" },
                    "currentMood": [0, 0]
                  },
  "defaultwindow": { "style": "color: black; background: rgb(210,0,0); font-family: 'Arial'; font: bold; selection-background-color: rgb(100,100,100);"
                   },
  "addchum":
      { "style": "background-image:url($path/a.png); border:0px;",
        "loc": [434, 55],
        "size": [8, 8],
               "text": ""
             },
  "pester":
      { "style": "background: rgba(0,0,0,0); border:0px;",
        "loc": [0, 0],
        "size": [0, 0],
              "text": ""
            },
  "block": { "style": "background: rgba(0,0,0,0); border:0px; color: rgba(0,0,0,0);",
             "loc": [0, 0],
             "size": [0, 0],
             "text": ""
           },
  "defaultmood": 6,
  "moodlabel": { "style": "",
                 "loc": [0, 0],
                 "text": ""
               },
  "moods": [
          { "style": "background-image:url($path/shades1.png); border:0px;",
        "selected": "background-image:url($path/shades2.png); border:0px;",
        "loc": [268, 580],
        "size": [104, 37],
        "text": "",
        "icon": "",
        "mood": 6
      },
      { "style": "background-image:url($path/offline1.png); border:0px;",
        "selected": "background-image:url($path/offline1.png); border:0px;",
        "loc": [382, 580],
        "size": [50, 50],
        "text": "",
        "icon": "",
        "mood": 2
      }
  ]
 },
 "convo":
 {"style": "background: black; font-family: 'Arial';",
  "scrollbar": { "style" : "", "handle": "" },
  "margins": {"top": 10, "bottom": 10, "left": 10, "right": 10 },
  "size": [400, 250],
  "size": [400, 250],
  "chumlabel": { "style": "background-image:url($path/chumlabelbg.png);background-color:rgb(180,0,0); background-repeat: no-repeat; color: white; padding: 2px; border:1px solid #c2c2c2; margin-bottom: 4px;",
                 "align": { "h": "left", "v": "center" },
                 "minheight": 22,
                 "maxheight": 36,
                 "text" : "Pestering: $handle"
               },
  "textarea": {
      "style": "background: white; border:2px solid #c2c2c2; font-size: 14px;"
  },
  "input": {
      "style": "background: white;margin-top:5px; border:1px solid #c2c2c2; font-size: 12px;"
  },
  "tabwindow" : {
    "style": "background: black; font-family: 'Arial'"
  },
  "tabs": {
      "style": "border: 2px solid white; background: black; color: white;",
      "selectedstyle": "border: 3px solid white; background: white; color: black;",
      "newmsgcolor": "red",
      "tabstyle": 0
  },
  "text": {
      "beganpester": "began pestering",
      "ceasepester": "ceased pestering",
      "blocked": "blocked",
      "unblocked": "unblocked",
      "openmemo": "opened memo on board",
      "joinmemo": "responded to memo",
      "closememo": "ceased responding to memo",
      "kickedmemo": "You have been banned from this memo!"
  },
  "systemMsgColor": "#646464"
 },
 "memos":
 {"memoicon": "$path/memo.png",
  "style": "background: black; font-family: 'Arial';",
  "size": [450,300],
  "tabs": {
      "style": "border: 2px solid white; background: black; color: white;",
      "selectedstyle": "border: 3px solid white; background: white; color: black;",
      "newmsgcolor": "red",
      "tabstyle": 0
  },
  "label": { "text": "Bulletin Board: $channel",
             "style": "background-image:url($path/chumlabelbg.png);background-color:rgb(180,0,0); background-repeat: no-repeat; color: white; padding: 2px; border:1px solid #c2c2c2; margin-bottom: 4px;",
             "align": { "h": "left", "v": "center" },
             "minheight": 18,
             "maxheight": 18
           },
  "textarea": {
      "style": "background: white; border:2px solid #c2c2c2; font-size: 12px;"
  },
  "input": {
      "style": "background: white;margin-top:5px; border:1px solid #c2c2c2; font-size: 12px; margin-bottom: 5px; "
  },
  "margins": {"top": 10, "bottom": 10, "left": 9, "right": 4 },
  "userlist": { "width": 125,
                "style": "font-size: 12px; background: white; margin-bottom: 5px; border:2px solid #c2c2c2; padding: 5px; font-family: 'Arial';selection-background-color:rgb(200,200,200);"
              },
  "time": { "text": { "width": 75,
                      "style": "color: black; font:bold;  border:1px solid #c2c2c2; background: white; height: 19px;"
                    },
            "slider": { "style": " border:1px solid #c2c2c2;",
                        "groove": "border-image:url($path/timeslider.png);",
                        "handle": "image:url($path/timeicon.png);"
                      },
            "buttons": { "style": "border:1px solid rgb(166,166,166); height: 17px; width: 50px; color: white; font-family: 'Arial'; background: black; margin-left: 2px;" },
            "arrows": { "left": "$path/leftarrow.png",
                        "right": "$path/rightarrow.png",
                        "style": "width: 19px; height: 19px; border:0px; margin-left: 2px;"
                      }
          },
  "systemMsgColor": "#646464",
  "op": { "icon": "$path/smooth.png" }
 }
}
