{"main":
 {"style": "background-repeat: no-repeat;",
  "background-image": "$path/twbg.png",
  "size": [300, 345],
  "icon": "$path/trayicon.png",
  "newmsgicon": "$path/trayicon2.png",
  "windowtitle": "Typewriter",
  "close": { "image": "$path/x.png",
             "loc": [266, 164]},
  "minimize": { "image": "$path/m.png",
                "loc": [240, 169]},
  "menubar": { "style": "font-family: 'Courier'; font:bold; font-size: 12px; color: rgba(0,0,0,0);" },
  "menu" : { "style": "font-family: 'Courier'; font: bold; font-size: 12px; color: #000000; background-color: white;border:2px solid black;",
             "menuitem": "margin-right:30px;",
             "selected": "background-color: black",
             "loc": [43,220]
           },
  "sounds": { "alertsound": "$path/alarm.wav",
        "memosound": "$path/alarm2.wav",
        "ceasesound": "$path/cease.wav" },
  "menus": {"client": {"_name": "Typewriter",
                       "options": "Preferences",
                       "memos": "Bulletin Boards",
                       "logviewer": "Pesterlogs",
                       "randen": "Random Encounter",
                       "userlist": "Userlist",
                       "addgroup": "Add Group",
                       "talk": "Converse",
                       "import": "Import",
                       "idle": "Idle",
                       "reconnect": "Reconnect",
                       "exit": "Cease",
                       "console": "Console"},
            "profile": {"_name": "Ink",
                        "switch": "Alias",
                        "color": "Ink Color",
                        "theme": "Theme",
                        "block": "Ruffians",
                        "quirks": "Quirks"},
            "help": { "_name": "Assistance",
                      "about": "About",
                      "help": "Assistance",
                      "calsprite": "CalSprite",
                      "chanserv": "ChanServ",
                      "nickserv": "NickServ",
                      "reportbug": "Report Bug",
                      "rules": "Rules" },
            "rclickchumlist": {"pester": "Converse",
                               "removechum": "Erase User",
                               "report": "Report User",
                               "blockchum": "Condemn",
                               "addchum": "Add User",
                               "viewlog": "View Pesterlog",
                               "notes": "Edit Notes...",
                               "unblockchum": "Forgive",
                               "removegroup": "Remove Group",
                               "renamegroup": "Rename Group",
                               "movechum": "Move To",
                               "banuser": "Expel User",
                               "opuser": "Promote",
                               "voiceuser": "Let Speak",
                               "quirkkill": "Kill Quirk",
                               "quirksoff": "Quirks Off",
                               "invitechum": "Invite User",
                               "memosetting": "Memo Settings",
                               "memonoquirk": "Disable Quirks",
                               "memohidden": "Hidden",
                               "memoinvite": "Invite-Only",
                               "memomute": "Mute",
                               "beeponmessage": "Beep on Message",
                               "flashonmessage": "Flash on Message",
                               "mutenotifications": "Mute Notifications" 
                              }
           },
  "chums": { "style": "border:0px; background-color: white; font: bold;font-family: 'Courier';selection-background-color: black; ",
             "loc": [70, 20],
             "size": [175,100],
             "userlistcolor": "black",
             "moods": {

                 "chummy": { "icon": "$path/chummy.png", "color": "black" },

                 "rancorous": { "icon": "$path/rancorous.png", "color": "red" },

                 "offline": { "icon": "$path/offline.png", "color": "#646464"},


                 "pleasant": { "icon": "$path/pleasant.png", "color": "black" },

                 "distraught": { "icon": "$path/distraught.png", "color": "black" },

                 "pranky": { "icon": "$path/pranky.png", "color": "black" },


                 "smooth": { "icon": "$path/smooth.png", "color": "black" },

                 "mystified": { "icon": "$path/mystified.png", "color": "black" },

                 "amazed": { "icon": "$path/amazed.png", "color": "black" },

                 "insolent": { "icon": "$path/insolent.png", "color": "black" },

                 "bemused": { "icon": "$path/bemused.png", "color": "black" },


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
      "style": "background: #bebebe; border:2px solid black; font-family: 'Courier'",
      "size": [195, 200],
      "label": { "text": "Ruffians",
                 "style": "color: rgba(0, 0, 0, 100%) ;font:bold; font-family: 'Courier';border:0px;" },
      "chumroll": {"style": "border:2px solid black; background-color: white;color: black;font: bold;font-family: 'Courier';selection-background-color:black; " }
  },
  "mychumhandle": { "label": { "text": "",
                               "loc": [0,0],
                               "style": "color: rgba(255, 255, 0, 0%) ;font:bold; font-family: 'Courier';" },
                    "handle": { "style": "background: rgba(0,0,0,0); padding: 3px; color:white; font-family:'Courier'; font:bold; text-align:left;",
                                "loc": [0,0],
                                "size": [0, 0] },
                    "colorswatch": { "loc": [0,0],
                                     "size": [0,0],
                                     "text": "" },
                    "currentMood": [0, 0]
                  },
  "defaultwindow": { "style": "background: #bebebe; font-family:'Courier';font:bold;selection-background-color: black; "
                   },
  "addchum":  { "style": "background: rgba(255, 255, 0, 0%); border:0px solid #c48a00; font: bold; color: rgba(0, 0, 0, 0%); font-family:'Courier';",
                "pressed" : "background: rgb(255, 255, 255, 30%);",
                "loc": [30,197],
                "size": [70, 15],
                "text": ""
              },
  "pester": { "style": "background:  rgba(255, 255, 0, 0%); border:0px solid #c48a00; font: bold; color:  rgba(255, 255, 0, 0%); font-family:'Courier';",
              "pressed" : "background: rgb(255, 255, 255, 30%);",
              "loc": [220,197],
              "size": [70, 15],
              "text": ""
            },
  "block": { "style": "background:  rgba(255, 255, 0, 0%); border:2px solid #c48a00; font: bold; color:  rgba(255, 255, 0, 0%); font-family:'Courier';",
             "pressed" : "background: rgb(255, 255, 255, 30%);",
             "loc": [0,0],
             "size": [0, 0],
             "text": ""
           },
  "defaultmood": 18,
  "moodlabel": { "style": "",
         "loc": [20, 430],
         "text": "MOODS"
         },
  "moods": [
      { "style": "text-align:left; border:0px solid #c48a00; padding: 0px;color: rgba(0, 0, 0, 0%); font-family:'Courier'",
    "selected": "text-align:left; background-image:url($path/moodcheck1.png); border:0px solid #c48a00; padding: 0px;color: rgba(0, 0, 0, 0%); font-family:'Courier';",
    "loc": [95, 323],
    "size": [62, 9],
      "text": "",
    "icon": "",
    "mood": 18
    },
      { "style": "text-align:left; border:0px solid #c48a00; padding: 0px;color: rgba(0, 0, 0, 0%); font-family:'Courier'",
    "selected": "text-align:left; background-image:url($path/moodcheck2.png); border:0px solid #c48a00; padding: 0px;color: rgba(0, 0, 0, 0%); font-family:'Courier';",
    "loc": [165, 323],
    "size": [70, 9],
    "text": "",
    "icon": "",
    "mood": 2
    }
  ]
 },
 "convo":
 {"style": "background-color: grey; border:2px solid black; font-family: 'Courier'; background-image:url($path/convobg.png); background-repeat: no-repeat;",
  "tabwindow": {"style": "background-color: grey; font-family: 'Courier';" },
  "margins": {"top": 0, "bottom": 6, "left": 0, "right": 0 },
  "size": [500, 325],
  "chumlabel": { "style": "margin-bottom: 21px;background: #bebebe; color: white; border:0px; font-size: 14px;",
                 "align": { "h": "center", "v": "center" },
                 "minheight": 47,
                 "maxheight": 47,
                 "text" : ":: $handle ::"
               },
  "textarea": {
      "style": "background: white;  font-size: 14px;font:bold; border:2px solid black;text-align:center; margin-right:10px; margin-left:10px;"
  },
  "input": {
      "style": "background: white; border:2px solid black;margin-top:5px; margin-right:10px; margin-left:10px; font-size: 12px;"
  },
  "tabs": {
      "style": "background-color: #7f7f7f; font-family: 'Courier';font:bold;font-size:12px;min-height:25px;",
      "selectedstyle": "border:0px;background-color:#bebebe;border-top:2px solid black; border-left:2px solid black;border-right:2px solid black; border-top-left-radius: 4px; border-top-right-radius: 4px;",
      "newmsgcolor": "white",
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
  "style": "background-image:url($path/convobg.png); background-repeat: no-repeat; background-color: grey; border:2px solid black; font-family: 'Courier'; font: bold; selection-background-color:black; ",
  "size": [500,325],
  "tabs": {
      "style": "",
      "selectedstyle": "",
      "newmsgcolor": "#fdb302",
      "tabstyle": 0
  },
  "scrollbar": { "style" : "padding-top:17px; padding-bottom:17px;width: 18px; background:  rgba(255, 255, 0, 0%); border:0px;",
                 "handle": "background-color:black;min-height:20px;",
                 "downarrow": "height:17px;border:0px;",
                 "darrowstyle": "image:url($path/downarrow.png);",
                 "uparrow": "height:17px;border:0px;",
                 "uarrowstyle": "image:url($path/uparrow.png);"
               },
  "label": { "text": "Bulletin Board: $channel",
             "style": "margin-bottom: 21px; background:  #bebebe; color: white; border:0px; font-size: 14px;",
             "align": { "h": "center", "v": "center" },
             "minheight": 47,
             "maxheight": 47
           },
  "input": { "style": "background: white; border:2px solid black;margin-top:5px; margin-right:10px; margin-left:10px; font-size: 12px;" },
  "textarea": { "style": "background: white;  font-size: 14px;font:bold; border:2px solid black;text-align:center; margin-right:10px; margin-left:10px;" },
  "margins": {"top": 0, "bottom": 6, "left": 0, "right": 0 },
  "userlist": { "width": 150,
                "style": "border:2px solid black; background: white;font: bold;font-family: 'Courier';selection-background-color:black; font-size: 12px;  margin-left:0px; margin-right:10px;"
              },
  "time": { "text": { "width": 75,
                      "style": " border: 2px solid black; background: white; font-size: 12px; margin-top: 5px; margin-right: 5px; margin-left: 5px; font-family:'Courier';font:bold;"
                    },
            "slider": { "style": "border: 0px;",
                        "groove": "",
                        "handle": ""
                      },
            "buttons": { "style": "color: black; font: bold; border: 2px solid black; font: bold; font-size: 12px; background: white; margin-top: 5px; margin-right: 5px; margin-left: 5px; padding: 2px; width: 50px;" },
            "arrows": { "left": "$path/leftarrow.png",
                        "right": "$path/rightarrow.png",
                        "style": " border:0px; margin-top: 5px; margin-right:10px;"
                      }
          },
  "systemMsgColor": "#646464",
  "op": { "icon": "$path/protective.png" },
  "voice": { "icon": "$path/voice.png" }
 }
}
