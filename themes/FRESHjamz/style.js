{"main":
 {"style": "background-color:rgba(0,0,0,0); background-repeat: no-repeat;",
  "background-image": "$path/fjbg.png",
  "size": [613, 401],
  "icon": "$path/trayicon.png",
  "newmsgicon": "$path/trayicon2.png",
  "windowtitle": "FRESHjamz",
  "close": { "image": "$path/x.png",
         "size": [13, 13],
             "loc": [101, 362]},
  "minimize": { "image": "$path/m.png",
          "size": [13, 13],
                "loc": [116, 362]},
  "menubar": { "style": "font-family: 'Arial'; font-size: 11px; font: bold; color: white;" },
  "menu" : { "style": "font-family: 'Arial'; font-size: 11px; font: bold; color: white; background-color: #393939; border:3px solid #797979;",
             "selected": "background-color: #545454",
             "menuitem": "margin-right:10px;",
             "loc": [198,141]
           },
  "sounds": { "alertsound": "$path/alarm.wav",
        "ceasesound": "$path/ohgodwhat.wav" },
  "menus": {"client": {"_name": "Album",
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
            "profile": {"_name": "Track",
                        "switch": "Switch",
                        "theme": "Theme",
                        "color": "Color",
                        "block": "Trollslum",
                        "quirks": "Quirks" },
            "help": { "_name": "Info",
                      "help": "Info",
                      "calsprite": "Calsprite",
                      "nickserv": "NickServ",
                      "about": "About" },
            "rclickchumlist": {"pester": "Pester",
                               "removechum": "Remove Chum",
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
                               "opuser": "Make OP",
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
  "chums": { "style": "font-size: 16px; background-image:url($path/chumbg.png); background-color: #414141; background-repeat: no-repeat; font-family: 'Arial'; border: 0px; selection-background-color: #222222; color: #ff168f;",
             "loc": [189, 162],
             "size": [272, 170],
             "userlistcolor": "#ff168f",
             "moods": {

                 "chummy": { "icon": "$path/chummy.png", "color": "white" },

                 "rancorous": { "icon": "$path/rancorous.png", "color": "#ff168f" },

                 "offline": { "icon": "$path/offline.png", "color": "grey"},


                 "pleasant": { "icon": "$path/pleasant.png", "color": "white" },

                 "distraught": { "icon": "$path/distraught.png", "color": "white" },

                 "pranky": { "icon": "$path/pranky.png", "color": "white" },

                 "smooth": { "icon": "$path/smooth.png", "color": "white" },


                 "mystified": { "icon": "$path/mystified.png", "color": "white" },

                 "amazed": { "icon": "$path/amazed.png", "color": "white" },

                 "insolent": { "icon": "$path/insolent.png", "color": "white" },

         "bemused": { "icon": "$path/bemused.png", "color": "white" },


                 "ecstatic": { "icon": "$path/ecstatic.png", "color": "#ff168f" },

                 "relaxed": { "icon": "$path/relaxed.png", "color": "#ff168f" },

                 "discontent": { "icon": "$path/discontent.png", "color": "#ff168f" },

                 "devious": { "icon": "$path/devious.png", "color": "#ff168f" },

                 "sleek": { "icon": "$path/sleek.png", "color": "#ff168f" },

                 "detestful": { "icon": "$path/detestful.png", "color": "#ff168f" },

                 "mirthful": { "icon": "$path/mirthful.png", "color": "#ff168f" },

                 "manipulative": { "icon": "$path/manipulative.png", "color": "#ff168f" },

                 "vigorous": { "icon": "$path/vigorous.png", "color": "#ff168f" },

                 "perky": { "icon": "$path/perky.png", "color": "#ff168f" },

                 "acceptant": { "icon": "$path/acceptant.png", "color": "#ff168f" },

                 "protective": { "icon": "$path/protective.png", "color": "lime" },

                 "blocked": { "icon": "$path/blocked.png", "color": "#ff168f" }

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
  "defaultwindow": { "style": "color: black; background: #797979; font-family: 'Arial'; font: bold; selection-background-color: rgb(100,100,100);"
                   },
  "addchum":
      { "style": "background-image:url($path/pause1.png); border:0px;",
      "pressed": "background-image:url($path/pause2.png); border:0px;",
        "loc": [239, 73],
        "size": [55, 58],
               "text": ""
             },
  "pester":
      { "style": "background-image:url($path/play1.png); border:0px;",
      "pressed": "background-image:url($path/play2.png); border:0px;",
        "loc": [180, 73],
        "size": [55, 58],
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
          { "style": "background-image:url($path/rewind1.png); border:0px;",
        "selected": "background-image:url($path/rewind2.png); border:0px;",
        "loc": [298, 73],
        "size": [55, 58],
        "text": "",
        "icon": "",
        "mood": 2
      },
      { "style": "background-image:url($path/fastforward1.png); border:0px;",
        "selected": "background-image:url($path/fastforward2.png); border:0px;",
        "loc": [357, 73],
        "size": [55, 58],
        "text": "",
        "icon": "",
        "mood": 0
      }
  ]
 },
 "convo":
 {"style": "background: #797979; font-family: 'Arial';",
  "scrollbar": { "style" : "", "handle": "" },
  "margins": {"top": 10, "bottom": 10, "left": 10, "right": 10 },
  "size": [400, 250],
  "chumlabel": { "style": "background-image:url($path/chumlabelbg.png);background-color:#393939; background-repeat: no-repeat; color: #ff168f; padding: 2px; border:1px solid #c2c2c2; margin-bottom: 4px;",
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
  "style": "background: #797979; font-family: 'Arial';",
  "size": [450,300],
  "tabs": {
      "style": "border: 2px solid white; background: black; color: white;",
      "selectedstyle": "border: 3px solid white; background: white; color: black;",
      "newmsgcolor": "red",
      "tabstyle": 0
  },
  "label": { "text": "Bulletin Board: $channel",
             "style": "background-image:url($path/chumlabelbg.png);background-color:#393939; background-repeat: no-repeat; color: #ff168f; padding: 2px; border:1px solid #c2c2c2; margin-bottom: 4px;",
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
            "buttons": { "style": "border:1px solid #ff9dcf; height: 17px; width: 50px; color: white; font-family: 'Arial'; background: #ff168f; margin-left: 2px;" },
            "arrows": { "left": "$path/leftarrow.png",
                        "right": "$path/rightarrow.png",
                        "style": "width: 19px; height: 19px; border:0px; margin-left: 2px;"
                      }
          },
  "systemMsgColor": "#646464",
  "op": { "icon": "$path/smooth.png" }
 }
}
