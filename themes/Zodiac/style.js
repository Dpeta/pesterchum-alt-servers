{"main":
 {"style": "background-color:rgba(0,0,0,0); background-repeat: no-repeat;",
  "background-image": "$path/zodiacalternia.png",
  "size": [650, 650],
  "icon": "$path/pester1.png",
  "newmsgicon": "$path/pester2.png",
  "windowtitle": "Zodiac",
  "close": { "image": "$path/x.png",
             "loc": [416, 134]},
  "minimize": { "image": "$path/m.png",
                "loc": [400, 140]},
  "menubar": { "style": "font-family: 'Arial'; font-size: 11px; font: bold; color: white;" },
  "menu" : { "style": "font-family: 'Arial'; font-size: 11px; font: bold; color: white; background-color: black; border:3px solid white;",
             "selected": "background-color: #545454",
             "menuitem": "margin-right:14px;",
             "loc": [225,133]
           },
  "sounds": { "alertsound": "$path/alarm.wav",
              "ceasesound": "$path/cease.wav" },
  "menus": {"client": {"_name": "Client",
                       "options": "Options",
                       "memos": "Memos",
                       "logviewer": "Pesterlogs",
                       "randen": "Random Encounter",
                       "userlist": "Userlist",
                       "addgroup": "Add Group",
                       "import": "Import",
                       "reconnect": "Reconnect",
                       "idle": "Idle",
                       "exit": "Exit"},
            "profile": {"_name": "Profile",
                        "switch": "Chumhandle",
                        "theme": "Theme",
                        "color": "Color",
                        "block": "Trollslum",
                        "quirks": "Quirks" },
            "help": { "_name": "Help",
                      "help": "Help",
                      "calsprite": "Calsprite",
                      "nickserv": "NickServ",
                      "about": "About" },
            "rclickchumlist": {"pester": "Pester",
                               "removechum": "Remove",
                               "report": "Report",
                               "blockchum": "Block",
                               "addchum": "Add Chum",
                               "viewlog": "View Pesterlog",
                               "notes": "Edit Notes...",
                               "unblockchum": "Unblock",
                               "removegroup": "Remove Group",
                               "renamegroup": "Rename Group",
                               "movechum": "Move To",
                               "banuser": "Ban",
                               "opuser": "Promote",
                               "voiceuser": "Give Voice",
                               "quirkkill": "Kill Quirk",
                               "quirksoff": "Quirks Off",
                               "invitechum": "Invite Chump",
                               "memosetting": "Memo Settings",
                               "memonoquirk": "Disable Quirks",
                               "memohidden": "Hidden",
                               "memoinvite": "Invite-Only",
                               "memomute": "Mute" }
           },
  "chums": { "style": "font-size: 12px; background: black; border: 3px solid white; font:bold; font-family: 'Arial';selection-background-color:rgb(100,100,100); color: white;",
             "loc": [225, 150],
             "size": [202, 294],
             "userlistcolor": "white",
             "moods": {

                 "chummy": { "icon": "$path/chummy.png", "color": "#63ea00" },

                 "rancorous": { "icon": "$path/rancorous.png", "color": "#7f7f7f" },

                 "offline": { "icon": "$path/offline.png", "color": "white"},


                 "pleasant": { "icon": "$path/pleasant.png", "color": "#d69df8" },

                 "distraught": { "icon": "$path/distraught.png", "color": "#706eba" },

                 "pranky": { "icon": "$path/pranky.png", "color": "blue" },

                 "smooth": { "icon": "$path/smooth.png", "color": "red" },


                 "mystified": { "icon": "$path/mystified.png", "color": "red" },

                 "amazed": { "icon": "$path/amazed.png", "color": "red" },

                 "insolent": { "icon": "$path/insolent.png", "color": "white" },

         "bemused": { "icon": "$path/bemused.png", "color": "white" },


                 "ecstatic": { "icon": "$path/ecstatic.png", "color": "#99004d" },

                 "relaxed": { "icon": "$path/relaxed.png", "color": "#078446" },

                 "discontent": { "icon": "$path/discontent.png", "color": "#a75403" },

                 "devious": { "icon": "$path/devious.png", "color": "#008282" },

                 "sleek": { "icon": "$path/sleek.png", "color": "#a1a100" },

                 "detestful": { "icon": "$path/detestful.png", "color": "#6a006a" },

                 "mirthful": { "icon": "$path/mirthful.png", "color": "#450077" },

                 "manipulative": { "icon": "$path/manipulative.png", "color": "#004182" },

                 "vigorous": { "icon": "$path/vigorous.png", "color": "#0021cb" },

                 "perky": { "icon": "$path/perky.png", "color": "#406600" },

                 "acceptant": { "icon": "$path/acceptant.png", "color": "#a10000" },

                 "protective": { "icon": "$path/protective.png", "color": "white" },

                 "blocked": { "icon": "$path/blocked.png", "color": "white" }

             }
           },
  "trollslum": {
      "style": "background: black; font-family: 'Arial'; color: white;",
      "size": [200, 450],
      "label": { "text": "Chumpdump",
                 "style": "color: white ; font: bold; font-family: 'Arial'; border: 0px;" },
      "chumroll": {"style": "border: 3px solid white; background-color: black; color: white; padding: 5px; font: bold; font-family: 'Arial'; selection-background-color: rgb(100,100,100);" }
  },
  "mychumhandle": { "label": { "text": "",
                               "loc": [0,0],
                               "style": "color: rgba(0,0,0,0);" },
                    "handle": { "style": "background: black; padding: 3px; padding-left: 26px; color: white; font-family:'Arial'; font: bold; text-align:left; font-size: 12px; border: 3px solid white;",
                                "loc": [225,450],
                                "size": [202, 27] },
                    "colorswatch": { "loc": [402,453],
                                     "size": [22,21],
                                     "text": "" },
                    "currentMood": [231, 455]
                  },
  "defaultwindow": { "style": "color: black; background: rgb(210,0,0); font-family: 'Arial'; font: bold; selection-background-color: rgb(100,100,100);"
                   },
  "addchum":
      { "style": "background-image:url($path/addchum1.png); border:0px;",
        "pressed": "background-image:url($path/addchum2.png); border:0px;",
        "loc": [225, 564],
        "size": [50, 50],
               "text": ""
             },
  "pester":
      { "style": "background-image:url($path/pester1.png); border:0px;",
        "pressed": "background-image:url($path/pester2.png); border:0px;",
        "loc": [367, 564],
        "size": [50, 50],
              "text": ""
            },
  "block": { "style": "background: rgba(0,0,0,0); border:0px; color: rgba(0,0,0,0);",
             "loc": [0, 0],
             "size": [0, 0],
             "text": ""
           },
  "defaultmood": 0,
  "moodlabel": { "style": "",
                 "loc": [0, 0],
                 "text": ""
               },
  "moods": [
      { "style": "background-image:url($path/aries1.png); border:0px;",
        "selected": "background-image:url($path/aries2.png); border:0px;",
        "loc": [56, 433],
        "size": [50, 50],
        "text": "",
        "icon": "",
        "mood": 17
      },
      { "style": "background-image:url($path/tauros1.png); border:0px;",
        "selected": "background-image:url($path/tauros2.png); border:0px;",
        "loc": [157, 534],
        "size": [50, 50],
        "text": "",
        "icon": "",
        "mood": 9
      },
      { "style": "background-image:url($path/gemini1.png); border:0px;",
        "selected": "background-image:url($path/gemini2.png); border:0px;",
        "loc": [295, 574],
        "size": [50, 50],
        "text": "",
        "icon": "",
        "mood": 11
      },
      { "style": "background-image:url($path/cancer1.png); border:0px;",
        "selected": "background-image:url($path/cancer2.png); border:0px;",
        "loc": [432, 534],
        "size": [50, 50],
        "text": "",
        "icon": "",
        "mood": 1
      },
      { "style": "background-image:url($path/leo1.png); border:0px;",
        "selected": "background-image:url($path/leo2.png); border:0px;",
        "loc": [533, 433],
        "size": [50, 50],
        "text": "",
        "icon": "",
        "mood": 16
      },
      { "style": "background-image:url($path/virgo1.png); border:0px;",
        "selected": "background-image:url($path/virgo2.png); border:0px;",
        "loc": [574, 295],
        "size": [50, 50],
        "text": "",
        "icon": "",
        "mood": 8
      },
      { "style": "background-image:url($path/libra1.png); border:0px;",
        "selected": "background-image:url($path/libra2.png); border:0px;",
        "loc": [533, 157],
        "size": [50, 50],
        "text": "",
        "icon": "",
        "mood": 10
      },
      { "style": "background-image:url($path/scorpio1.png); border:0px;",
        "selected": "background-image:url($path/scorpio2.png); border:0px;",
        "loc": [432, 56],
        "size": [50, 50],
        "text": "",
        "icon": "",
        "mood": 14
      },
      { "style": "background-image:url($path/sagittarius1.png); border:0px;",
        "selected": "background-image:url($path/sagittarius2.png); border:0px;",
        "loc": [295, 16],
        "size": [50, 50],
        "text": "",
        "icon": "",
        "mood": 15
      },
      { "style": "background-image:url($path/capricorn1.png); border:0px;",
        "selected": "background-image:url($path/capricorn2.png); border:0px;",
        "loc": [157, 56],
        "size": [50, 50],
        "text": "",
        "icon": "",
        "mood": 13
      },
      { "style": "background-image:url($path/aquarius1.png); border:0px;",
        "selected": "background-image:url($path/aquarius2.png); border:0px;",
        "loc": [56, 157],
        "size": [50, 50],
        "text": "",
        "icon": "",
        "mood": 12
      },
      { "style": "background-image:url($path/pisces1.png); border:0px;",
        "selected": "background-image:url($path/pisces2.png); border:0px;",
        "loc": [16, 295],
        "size": [50, 50],
        "text": "",
        "icon": "",
        "mood": 7
      },

          { "style": "background-image:url($path/john1.png); border:0px;",
        "selected": "background-image:url($path/john2.png); border:0px;",
        "loc": [367, 27],
        "size": [50, 50],
        "text": "",
        "icon": "",
        "mood": 5
      },
          { "style": "background-image:url($path/rose1.png); border:0px;",
        "selected": "background-image:url($path/rose2.png); border:0px;",
        "loc": [30, 369],
        "size": [50, 50],
        "text": "",
        "icon": "",
        "mood": 3
      },
          { "style": "background-image:url($path/dave1.png); border:0px;",
        "selected": "background-image:url($path/dave2.png); border:0px;",
        "loc": [99, 494],
        "size": [50, 50],
        "text": "",
        "icon": "",
        "mood": 6
      },
          { "style": "background-image:url($path/jade1.png); border:0px;",
        "selected": "background-image:url($path/jade2.png); border:0px;",
        "loc": [566, 369],
        "size": [50, 50],
        "text": "",
        "icon": "",
        "mood": 0
      },
              { "style": "background-image:url($path/bec1.png); border:0px;",
        "selected": "background-image:url($path/bec2.png); border:0px;",
        "loc": [492, 494],
        "size": [50, 50],
        "text": "",
        "icon": "",
        "mood": 18
      },

              { "style": "background-image:url($path/hearts1.png); border:0px;",
        "selected": "background-image:url($path/hearts2.png); border:0px;",
        "loc": [492, 101],
        "size": [50, 50],
        "text": "",
        "icon": "",
        "mood": 20
      },
          { "style": "background-image:url($path/spades1.png); border:0px;",
        "selected": "background-image:url($path/spades2.png); border:0px;",
        "loc": [99, 101],
        "size": [50, 50],
        "text": "",
        "icon": "",
        "mood": 21
      },
          { "style": "background-image:url($path/diamonds1.png); border:0px;",
        "selected": "background-image:url($path/diamonds2.png); border:0px;",
        "loc": [30, 225],
        "size": [50, 50],
        "text": "",
        "icon": "",
        "mood": 19
      },
              { "style": "background-image:url($path/clubs1.png); border:0px;",
        "selected": "background-image:url($path/clubs2.png); border:0px;",
        "loc": [566, 225],
        "size": [50, 50],
        "text": "",
        "icon": "",
        "mood": 22
      },

      { "style": "background-image:url($path/offline1.png); border:0px;",
        "selected": "background-image:url($path/offline2.png); border:0px;",
        "loc": [223, 27],
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
  "chumlabel": { "style": "background-image:url($path/chumlabelbg.png);background-color:rgb(108,108,108); background-repeat: no-repeat; color: white; padding: 2px; border:1px solid #c2c2c2; margin-bottom: 4px;",
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
             "style": "background-image:url($path/chumlabelbg.png);background-color:rgb(108,108,108); background-repeat: no-repeat; color: white; padding: 2px; border:1px solid #c2c2c2; margin-bottom: 4px;",
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
