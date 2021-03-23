{"main":
 {"style": "background-repeat: no-repeat; font-family: Arial; font-size: 14px;",
  "background-image": "$path/gbg2.png",
  "size": [333, 290],
  "icon": "$path/trayicon.png",
  "newmsgicon": "$path/trayicon2.png",
  "windowtitle": "PESTERCHUM 7.0",
  "close": { "image": "$path/x.png",
             "loc": [319, 28]},
  "minimize": { "image": "$path/m.png",
                "loc": [304, 34]},
  "menubar": { "style": "font-family: 'Arial'; font:bold; font-size: 12px; color: #000000;" },
  "menu" : { "style": "font-family: 'Arial'; font: bold; font-size: 12px; color: #000000; background-color: #fdb302;border:2px solid #ffff00",
             "menuitem": "margin-right:15px;",
             "selected": "background-color: #ffff00",
             "loc": [150,22]
           },
  "sounds": { "alertsound": "$path/alarm.wav",
                          "memosound": "$path/alarm2.wav",
                          "ceasesound": "$path/cease.wav" },
  "menus": {"client": {"_name": "Client",
                       "options": "Options",
                       "memos": "Memos",
                       "logviewer": "Pesterlogs",
                       "randen": "Random Encounter",
                       "userlist": "Userlist",
                       "addgroup": "Add Group",
                       "talk": "Pester",
                       "import": "Import",
                       "reconnect": "Reconnect",
                       "idle": "Idle",
                       "exit": "Exit"},
            "profile": {"_name": "Profile",
                        "switch": "Switch",
                        "color": "Color",
                        "theme": "Theme",
                        "block": "Trollslum",
                        "quirks": "Quirks"},
            "help": { "_name": "Help",
                      "about": "About",
                      "help": "Help",
                      "calsprite": "CalSprite",
                      "nickserv": "NickServ" },
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
                               "banuser": "Ban User",
                               "opuser": "Make OP",
                               "voiceuser": "Give Voice",
                               "quirkkill": "Kill Quirk",
                               "quirksoff": "Quirks Off",
                               "invitechum": "Invite Chum",
                               "memosetting": "Memo Settings",
                               "memonoquirk": "Disable Quirks",
                               "memohidden": "Hidden",
                               "memoinvite": "Invite-Only",
                               "memomute": "Mute"
                              }
           },
  "chums": { "style": "border:0px; background-image:url($path/chumbg.png); background-color: rgb(110,110,110); background-repeat: no-repeat; color: white; font-family: 'Arial';selection-background-color:#646464; font-size:14px; ",
             "loc": [123, 88],
             "size": [190, 65],
             "userlistcolor": "white",
             "moods": {

                 "chummy": { "icon": "$path/chummy.png", "color": "white" },

                 "rancorous": { "icon": "$path/rancorous.png", "color": "red" },

                 "offline": { "icon": "$path/offline.png", "color": "#bebebe"},


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

                 "protective": { "icon": "$path/protective.png", "color": "#00ff00" },

                 "blocked": { "icon": "$path/blocked.png", "color": "black" }

             }
           },
  "trollslum": {
      "style": "background: #fdb302; border:2px solid yellow; font-family: 'Arial'",
      "size": [195, 200],
      "label": { "text": "TROLLSLUM",
                 "style": "color: rgba(0, 0, 0, 100%) ;font:bold; font-family: 'Arial';border:0px;" },
      "chumroll": {"style": "border:2px solid yellow; background-color: black;color: white;font: bold;font-family: 'Arial';selection-background-color:#646464; " }
  },
  "mychumhandle": { "label": { "text": "CHUMHANDLE:",
                               "loc": [0,0],
                               "style": "color: rgba(255, 255, 0, 0%) ;font:bold; font-family: 'Arial';" },
                    "handle": { "style": "background: rgba(255, 255, 0, 0%); color:white; font-family:'Arial'; font-size:14px; text-align:left;",
                                "loc": [157,170],
                                "size": [191, 26] },
                    "colorswatch": { "loc": [0,0],
                                     "size": [0,0],
                                     "text": "" },
                    "currentMood": [129, 176]
                  },
  "defaultwindow": { "style": "background: #fdb302; font-family:'Arial';font:bold;selection-background-color:#919191; "
                   },
  "addchum":  { "style": "background: rgba(255, 255, 0, 0%); border:0px; color: rgba(0, 0, 0, 0%);",
              "loc": [25,0],
              "size": [69, 70],
                "text": ""
              },
  "pester": { "style": "background:  rgba(255, 255, 0, 0%); border:0px; font: bold; color:  rgba(255, 255, 0, 0%); font-family:'Arial';",
              "pressed" : "background-image:url($path/pesterhold.png);",
                "loc": [15,83],
                "size": [95, 75],
              "text": ""
            },
  "block": { "style": "background:  rgba(255, 255, 0, 0%); border:2px solid #c48a00; font: bold; color:  rgba(255, 255, 0, 0%); font-family:'Arial';",
             "loc": [0,0],
             "size": [0, 0],
             "text": ""
           },
  "defaultmood": 0,
  "moodlabel": { "style": "",
                                 "loc": [20, 430],
                                 "text": "MOODS"
                           },
  "moods": [
      { "style": "border:0px;",
                "selected": "background-image:url($path/moodcheck1.png); border:0px;",
                "loc": [13, 204],
                "size": [101, 27],
                 "text": "",
                "icon": "",
                "mood": 0
          },
      { "style": "border:0px;",
                "selected": "background-image:url($path/moodcheck2.png); border:0px;",
                "loc": [13, 231],
                "size": [101, 27],
                 "text": "",
                "icon": "",
                "mood": 19
          },
      { "style": "border:0px;",
                "selected": "background-image:url($path/moodcheck3.png); border:0px;",
                "loc": [13, 258],
                "size": [101, 27],
                 "text": "",
                "icon": "",
                "mood": 20
          },
      { "style": "border:0px;",
                "selected": "background-image:url($path/moodcheck4.png); border:0px;",
                "loc": [116, 204],
                "size": [101, 27],
                 "text": "",
                "icon": "",
                "mood": 21
          },
      { "style": "border:0px;",
                "selected": "background-image:url($path/moodcheck5.png); border:0px;",
                "loc": [116, 231],
                "size": [101, 27],
                 "text": "",
                "icon": "",
                "mood": 22
          },
      { "style": "border:0px;",
                "selected": "background-image:url($path/moodcheck6.png); border:0px;",
                "loc": [116, 258],
                "size": [101, 27],
                 "text": "",
                "icon": "",
                "mood": 5
          },
      { "style": "border:0px;",
                "selected": "background-image:url($path/moodcheck7.png); border:0px;",
                "loc": [219, 204],
                "size": [101, 27],
                 "text": "",
                "icon": "",
                "mood": 6
          },
      { "style": "border:0px;",
                "selected": "background-image:url($path/moodcheck8.png); border:0px;",
                "loc": [219, 231],
                "size": [101, 27],
                 "text": "",
                "icon": "",
                "mood": 3
          },
      { "style": "border:0px;",
                "selected": "background-image:url($path/moodcheck9.png); border:0px;",
                "loc": [219, 258],
                "size": [101, 27],
                 "text": "",
                "icon": "",
                "mood": 1
          },
      { "style": "border:0px;",
                "selected": "border:0px;",
                "loc": [13, 175],
                "size": [101, 27],
                 "text": "",
                "icon": "",
                "mood": 2
          }
  ]
 },
 "convo":
 {"style": "background-color: rgba(0, 0, 0, 0%);border-width: 5px; border-image:url($path/convobg.png) 5px; font-family: 'Arial'",
  "tabstyle": "background-color: #fdb302; font-family: 'Arial'",
  "scrollbar": { "style" : "padding-top:17px; padding-bottom:17px;width: 18px; background:  rgba(255, 255, 0, 0%); border:0px;",
                 "handle": "background-color:#c48a00;min-height:20px;",
                 "downarrow": "height:17px;border:0px solid #c48a00;",
                 "darrowstyle": "image:url($path/downarrow.png);",
                 "uparrow": "height:17px;border:0px solid #c48a00;",
                 "uarrowstyle": "image:url($path/uparrow.png);"
               },
  "margins": {"top": 0, "bottom": 6, "left": 0, "right": 0 },
  "size": [500, 325],
  "chumlabel": { "style": "margin-bottom: 7px; margin-top: 10px; background:  rgba(255, 255, 0, 0%); color: white; border:0px; font-size: 16px;",
                 "align": { "h": "center", "v": "center" },
                 "minheight": 47,
                 "maxheight": 47,
                 "text" : ":: $handle ::"
               },
  "textarea": {
      "style": "background: white;  font-size: 14px; border:2px solid #c48a00;text-align:center; margin-right:10px; margin-left:10px; margin-bottom:5px;"
  },
  "input": {
      "style": "background: white; border:2px solid #c48a00; margin-right:10px; margin-left:10px; font-size: 14px;"
  },
  "tabs": {
      "style": "",
      "selectedstyle": "",
      "newmsgcolor": "#fdb302",
      "tabstyle": 0
  },
  "text": {
      "beganpester": "began pestering",
      "ceasepester": "ceased pestering",
      "blocked": "blocked",
      "unblocked": "unblocked",
          "blockedmsg": "did not receive message from",
      "openmemo": "opened memo on board",
      "joinmemo": "responded to memo",
      "closememo": "ceased responding to memo",
      "kickedmemo": "You have been banned from this memo!",
          "idle": "is now an idle chum!"
  },
  "systemMsgColor": "#646464"
 },
 "memos":
 {"memoicon": "$path/memo.png",
  "style": "background-color: rgba(0,0,0,0); background-image:url($path/convobg.png); background-repeat: no-repeat; border:0px; font-family: 'Arial'; selection-background-color:#919191; ",
  "size": [500,325],
  "tabs": {
      "style": "",
      "selectedstyle": "",
      "newmsgcolor": "#fdb302",
      "tabstyle": 0
  },
  "scrollbar": { "style" : "padding-top:17px; padding-bottom:17px;width: 18px; background:  rgba(255, 255, 0, 0%); border:0px;",
                 "handle": "background-color:#c48a00;min-height:20px;",
                 "downarrow": "height:17px;border:0px solid #c48a00;",
                 "darrowstyle": "image:url($path/downarrow.png);",
                 "uparrow": "height:17px;border:0px solid #c48a00;",
                 "uarrowstyle": "image:url($path/uparrow.png);"
               },
  "label": { "text": "Bulletin Board: $channel",
             "style": "margin-bottom: 7px; margin-top: 10px; background:  rgba(255, 255, 0, 0%); color: white; border:0px; font-size: 16px;",
             "align": { "h": "center", "v": "center" },
             "minheight": 47,
             "maxheight": 47
           },
  "input": { "style": "background: white; border:2px solid #c48a00;margin-top:5px; margin-right:10px; margin-left:10px; font-size: 14px;" },
  "textarea": { "style": "background: white;  font-size: 14px; border:2px solid #c48a00;text-align:center; margin-right:10px; margin-left:10px;" },
  "margins": {"top": 0, "bottom": 6, "left": 0, "right": 0 },
  "userlist": { "width": 150,
                "style": "border:2px solid #c48a00; background: white; font-family: 'Arial';selection-background-color:#646464; font-size: 14px;  margin-left:0px; margin-right:10px;"
              },
  "time": { "text": { "width": 75,
                      "style": " border: 2px solid yellow; background: white; font-size: 12px; margin-top: 5px; margin-right: 5px; margin-left: 5px; font-family:'Arial';font:bold;"
                    },
            "slider": { "style": "border: 0px;",
                        "groove": "",
                        "handle": ""
                      },
            "buttons": { "style": "color: black; font: bold; border: 2px solid #c48a00; font-size: 12px; background: yellow; margin-top: 5px; margin-right: 5px; margin-left: 5px; padding: 2px; width: 50px;" },
            "arrows": { "left": "$path/leftarrow.png",
                        "right": "$path/rightarrow.png",
                        "style": " border:0px; margin-top: 5px; margin-right:10px;"
                      }
          },
  "systemMsgColor": "#646464",
  "op": { "icon": "$path/smooth.png" },
  "voice": { "icon": "$path/voice.png" }
 }
}
