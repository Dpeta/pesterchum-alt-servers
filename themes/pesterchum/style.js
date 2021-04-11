{"main":
 {"style": "background-repeat: no-repeat;",
  "background-image": "$path/pcbg.png",
  "size": [232, 380],
  "icon": "$path/trayicon.png",
  "newmsgicon": "$path/trayicon2.png",
  "windowtitle": "PESTERCHUM 6.0",
  "close": { "image": "$path/x.png",
             "loc": [214, 4]},
  "minimize": { "image": "$path/m.png",
                "loc": [198, 10]},
  "menubar": { "style": "font-family: 'Courier'; font:bold; font-size: 12px; color: black;" },
  "menu" : { "style": "font-family: 'Courier'; font: bold; font-size: 12px; color: black; background-color: #fdb302;border:2px solid #ffff00",
             "menuitem": "margin-right:10px;",
             "selected": "background-color: #ffff00",
             "disabled": "color: grey",
             "loc": [10,0]
           },
  "sounds": { "alertsound": "$path/alarm.wav",
                          "memosound": "$path/alarm2.wav",
                          "ceasesound": "$path/cease.wav" },
  "menus": {"client": {"_name": "CLIENT",
                       "options": "OPTIONS",
                       "memos": "MEMOS",
                       "logviewer": "PESTERLOGS",
                       "randen": "RANDOM ENCOUNTER",
                       "userlist": "USERLIST",
                       "addgroup": "ADD GROUP",
                       "talk": "PESTER",
                       "import": "IMPORT",
                       "reconnect": "RECONNECT",
                       "idle": "IDLE",
                       "exit": "EXIT",
                       "console": "CONSOLE"},
            "profile": {"_name": "PROFILE",
                        "switch": "SWITCH",
                        "color": "COLOR",
                        "theme": "THEME",
                        "block": "TROLLSLUM",
                        "quirks": "QUIRKS"},
            "help": { "_name": "HELP",
                      "about": "ABOUT",
                      "help": "HELP",
                      "calsprite": "CALSPRITE",
                      "chanserv": "CHANSERV",
                      "nickserv": "NICKSERV" },
            "rclickchumlist": {"pester": "PESTER",
                               "removechum": "REMOVE CHUM",
                               "report": "REPORT",
                               "blockchum": "BLOCK",
                               "addchum": "ADD CHUM",
                               "viewlog": "VIEW PESTERLOG",
                               "notes": "EDIT NOTES...",
                               "unblockchum": "UNBLOCK",
                               "removegroup": "REMOVE GROUP",
                               "renamegroup": "RENAME GROUP",
                               "movechum": "MOVE TO",
                               "banuser": "BAN USER",
                               "opuser": "MAKE OP",
                               "voiceuser": "GIVE VOICE",
                               "quirkkill": "KILL QUIRK",
                               "quirksoff": "QUIRKS OFF",
                               "ooc": "OOC",
                               "invitechum": "INVITE CHUM",
                               "memosetting": "MEMO SETTINGS",
                               "memonoquirk": "DISABLE QUIRKS",
                               "memohidden": "HIDDEN",
                               "memoinvite": "INVITE-ONLY",
                               "memomute": "MUTE",
                               "beeponmessage": "BEEP ON MESSAGE",
                               "flashonmessage": "FLASH ON MESSAGE",
                               "mutenotifications": "MUTE NOTIFICATIONS"
                              }
           },
  "chums": { "style": "border:2px solid yellow; background-color: black;color: white;font: bold;font-family: 'Courier';selection-background-color:#646464; ",
             "loc": [12, 117],
             "size": [209, 82],
             "userlistcolor": "white",
             "moods": {

                 "chummy": { "icon": "$path/chummy.png", "color": "white" },

                 "rancorous": { "icon": "$path/rancorous.png", "color": "red" },

                 "offline": { "icon": "$path/offline.png", "color": "#646464"},


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
      "style": "background: #fdb302; border:2px solid yellow; font-family: 'Courier'",
      "size": [195, 200],
      "label": { "text": "TROLLSLUM",
                 "style": "color: rgba(0, 0, 0, 100%) ;font:bold; font-family: 'Courier';border:0px;" },
      "chumroll": {"style": "border:2px solid yellow; background-color: black;color: white;font: bold;font-family: 'Courier';selection-background-color:#646464; " }
  },
  "mychumhandle": { "label": { "text": "CHUMHANDLE:",
                               "loc": [19,232],
                               "style": "color: rgba(255, 255, 0, 0%) ;font:bold; font-family: 'Courier';" },
                    "handle": { "style": "background: rgba(0,0,0,0); padding: 3px; color:white; font-family:'Courier'; font:bold; text-align:left;",
                                "loc": [36,246],
                                "size": [180, 21] },
                    "colorswatch": { "loc": [196,246],
                                     "size": [23,21],
                                     "text": "" },
                    "currentMood": [18, 249]
                  },
  "defaultwindow": { "style": "background: #fdb302; font-family:'Courier';font:bold;selection-background-color:#919191; "
                   },
  "addchum":  { "style": "background: rgba(255, 255, 0, 0%); border:2px solid #c48a00; font: bold; color: rgba(0, 0, 0, 0%); font-family:'Courier';",
                "pressed" : "background: rgb(255, 255, 255, 30%);",
                "loc": [12,202],
                "size": [71, 22],
                "text": ""
              },
  "pester": { "style": "background:  rgba(255, 255, 0, 0%); border:2px solid #c48a00; font: bold; color:  rgba(255, 255, 0, 0%); font-family:'Courier';",
              "pressed" : "background: rgb(255, 255, 255, 30%);",
              "loc": [150,202],
              "size": [71, 22],
              "text": ""
            },
  "block": { "style": "background:  rgba(255, 255, 0, 0%); border:2px solid #c48a00; font: bold; color:  rgba(255, 255, 0, 0%); font-family:'Courier';",
             "pressed" : "background: rgb(255, 255, 255, 30%);",
             "loc": [81,202],
             "size": [71, 22],
             "text": ""
           },
  "defaultmood": 0,
  "moodlabel": { "style": "",
                                 "loc": [20, 430],
                                 "text": "MOODS"
                           },
  "moods": [
      { "style": "text-align:left; border:2px solid #c48a00; padding: 5px;color: rgba(0, 0, 0, 0%); font-family:'Courier'",
                "selected": "text-align:left; background-image:url($path/moodcheck1.png); border:2px solid #c48a00; padding: 5px;color: rgba(0, 0, 0, 0%); font-family:'Courier';",
                "loc": [12, 288],
                "size": [104, 22],
            "text": "CHUMMY",
                "icon": "$path/chummy.png",
                "mood": 0
          },
      { "style": "text-align:left; border:2px solid #c48a00; padding: 5px;color: rgba(0, 0, 0, 0%); font-family:'Courier'",
                "selected": "text-align:left; background-image:url($path/moodcheck2.png); border:2px solid #c48a00; padding: 5px;color: rgba(0, 0, 0, 0%); font-family:'Courier';",
                "loc": [12, 308],
                "size": [104, 22],
                "text": "PALSY",
                "icon": "$path/chummy.png",
                "mood": 3
          },
      { "style": "text-align:left; border:2px solid #c48a00; padding: 5px;color: rgba(0, 0, 0, 0%); font-family:'Courier'",
                "selected": "text-align:left; background-image:url($path/moodcheck3.png); border:2px solid #c48a00; padding: 5px;color: rgba(0, 0, 0, 0%); font-family:'Courier';",
                "loc": [12, 328],
                "size": [104, 22],
                "text": "CHIPPER",
                "icon": "$path/chummy.png",
                "mood": 4
          },
      { "style": "text-align:left; border:2px solid #c48a00; padding: 5px;color: rgba(0, 0, 0, 0%); font-family:'Courier'",
                "selected": "text-align:left; background-image:url($path/moodcheck2.png); border:2px solid #c48a00; padding: 5px;color: rgba(0, 0, 0, 0%); font-family:'Courier';",
                "loc": [117, 288],
                "size": [104, 22],
                "text": "BULLY",
                "icon": "$path/chummy.png",
                "mood": 5
          },
      { "style": "text-align:left; border:2px solid #c48a00; padding: 5px;color: rgba(0, 0, 0, 0%); font-family:'Courier'",
                "selected": "text-align:left; background-image:url($path/moodcheck2.png); border:2px solid #c48a00; padding: 5px;color: rgba(0, 0, 0, 0%); font-family:'Courier';",
                "loc": [117, 308],
                "size": [104, 22],
                "text": "PEPPY",
                "icon": "$path/chummy.png",
                "mood": 6
          },
      { "style": "text-align:left; border:2px solid #c48a00; padding: 5px;color: rgba(0, 0, 0, 0%); font-family:'Courier'",
                "selected": "text-align:left; background-image:url($path/moodcheck4.png); border:2px solid #c48a00; padding: 5px;color: rgba(0, 0, 0, 0%); font-family:'Courier';",
                "loc": [117, 328],
                "size": [104, 22],
                "text": "RANCOROUS",
                "icon": "$path/rancorous.png",
                "mood": 1
          },
      { "style": "text-align:left; border:2px solid #c48a00; padding: 5px;color: rgba(0, 0, 0, 0%); font-family:'Courier'",
                "selected": "text-align:left; background-image:url($path/moodcheck5.png); border:2px solid #c48a00; padding: 5px;color: rgba(0, 0, 0, 0%); font-family:'Courier';",
                "loc": [12, 348],
                "size": [209, 22],
                "text": "ABSCOND",
                "icon": "",
                "mood": 2
          }
  ]
 },
 "convo":
 {"style": "background-color: #fdb302;background-image:url($path/convobg.png);background-repeat: no-repeat; border:2px solid yellow; font-family: 'Courier'",
  "scrollbar": { "style" : "padding-top:17px; padding-bottom:17px;width: 18px; background: white; border:2px solid #c48a00;",
                 "handle": "background-color:#c48a00;min-height:20px;",
                 "downarrow": "height:17px;border:0px solid #c48a00;",
                 "darrowstyle": "image:url($path/downarrow.png);",
                 "uparrow": "height:17px;border:0px solid #c48a00;",
                 "uarrowstyle": "image:url($path/uparrow.png);"
               },
  "margins": {"top": 0, "bottom": 6, "left": 0, "right": 0 },
  "size": [500, 325],
  "chumlabel": { "style": "margin-bottom: 21px;background: rgb(196, 138, 0); color: white; border:0px; font-size: 14px;font-family: 'Courier'",
                 "align": { "h": "center", "v": "center" },
                 "minheight": 47,
                 "maxheight": 47,
                 "text" : ":: $handle ::"
               },
  "textarea": {
      "style": "background: white;  font-size: 14px;font:bold; border:2px solid #c48a00;text-align:center; margin-right:10px; margin-left:10px;font-family: 'Courier'"
  },
  "input": {
      "style": "background: white; border:2px solid #c48a00;margin-top:5px; margin-right:10px; margin-left:10px; font-size: 12px;font-family: 'Courier'"
  },
  "tabwindow" : {
          "style": "background-color:#fdb302;border:0px"
  },
  "tabs": {
      "style": "background-color: #7f7f7f; font-family: 'Courier';font:bold;font-size:12px;min-height:25px;",
      "selectedstyle": "border:0px;background-color:#fdb302;border-top:2px solid yellow; border-left:2px solid yellow;border-right:2px solid yellow; border-top-left-radius: 4px; border-top-right-radius: 4px;",
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
  "style": "background-color: #fdb302; background-image:url($path/convobg.png); background-repeat: no-repeat; border:2px solid yellow; font-family: 'Courier'; font: bold; selection-background-color:#919191; ",
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
             "style": "margin-bottom: 21px;background: rgb(196, 138, 0); color: white; border:0px; font-size: 14px;",
             "align": { "h": "center", "v": "center" },
             "minheight": 47,
             "maxheight": 47
           },
  "input": { "style": "background: white; border:2px solid #c48a00;margin-top:5px; margin-right:10px; margin-left:10px; font-size: 12px;" },
  "textarea": { "style": "background: white;  font-size: 14px;font:bold; border:2px solid #c48a00;text-align:center; margin-right:10px; margin-left:10px;" },
  "margins": {"top": 0, "bottom": 6, "left": 0, "right": 0 },
  "userlist": { "width": 150,
                "style": "border:2px solid #c48a00; background: white;font: bold;font-family: 'Courier';selection-background-color:#646464; font-size: 12px;  margin-left:0px; margin-right:10px;"
              },
  "time": { "text": { "width": 75,
                      "style": " border: 2px solid yellow; background: white; font-size: 12px; margin-top: 5px; margin-right: 5px; margin-left: 5px; font-family:'Courier';font:bold;"
                    },
            "slider": { "style": "border: 0px;",
                        "groove": "",
                        "handle": ""
                      },
            "buttons": { "style": "color: black; font: bold; border: 2px solid #c48a00; font: bold; font-size: 12px; background: yellow; margin-top: 5px; margin-right: 5px; margin-left: 5px; padding: 2px; width: 50px;" },
            "arrows": { "left": "$path/leftarrow.png",
                        "right": "$path/rightarrow.png",
                        "style": " border:0px; margin-top: 5px; margin-right:10px;"
                      }
          },
  "systemMsgColor": "#646464",
  "op": { "icon": "$path/op.png" },
  "halfop": { "icon": "$path/halfop.png" },
  "voice": { "icon": "$path/voice.png" },
  "founder": { "icon": "$path/founder.png" },
  "admin": { "icon": "$path/admin.png" }
 },
 "toasts":
 {
   "width": 210,
   "height": 100,
   "style": "background: white;",
   "icon": { "signin": "$path/../enamel/chummy2.gif",
             "signout": "$path/../enamel/distraught2.gif",
             "style": "border: 2px solid black; border-width: 2px 0px 0px 2px;" },
   "title": { "minimumheight": 50,
              "style": "border: 2px solid black; border-width: 2px 2px 0px 0px; padding: 5px; font-weight:bold;"
            },
   "content": { "style": "background: black; color: white; padding: 5px;" }
 }
}
