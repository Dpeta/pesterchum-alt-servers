{"main":
 {"style": "background-repeat: no-repeat;",
  "background-image": "$path/bbbg2.png",
  "size": [665, 506],
  "icon": "$path/bettybother.png",
  "newmsgicon": "$path/tbettybother2.png",
  "windowtitle": "BettyBother",
  "close": { "image": "$path/x.png",
             "loc": [214, 100]},
  "minimize": { "image": "$path/m.png",
                "loc": [198, 100]},
  "menubar": { "style": "font-family: 'Arial'; font:bold; font-size: 12px; color: white;" },
  "menu" : { "style": "font-family: 'Arial'; font: bold; font-size: 12px; color: white; background-color: #f21515;border:2px solid #bb0019",
             "menuitem": "margin-right:20px;",
             "selected": "background-color: #bb0019",
             "loc": [346,100]
           },
  "sounds": { "alertsound": "$path/harlarm.wav",
                          "memosound": "$path/alarm.wav",
                          "ceasesound": "$path/nannacease.wav" },
  "menus": {"client": {"_name": "CLIENT",
                       "options": "OPTIONS",
                       "memos": "MEMOS",
                       "logviewer": "PESTERLOGS",
                       "randen": "RANDOM ENCOUNTER",
                       "userlist": "USERLIST",
                       "addgroup": "ADD GROUP",
                       "import": "IMPORT",
                       "reconnect": "RECONNECT",
                                           "idle": "IDLE",
                       "exit": "EXIT"},
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
                      "nickserv": "NICKSERV" },
            "rclickchumlist": {"pester": "PESTER",
                               "removechum": "REMOVE CHUM",
                               "report": "REPORT",
                               "blockchum": "BLOCK",
                               "addchum": "ADD CHUM",
                               "viewlog": "VIEW PESTERLOG",
                               "unblockchum": "UNBLOCK",
                               "removegroup": "REMOVE GROUP",
                               "renamegroup": "RENAME GROUP",
                               "movechum": "MOVE TO",
                               "banuser": "BAN USER",
                               "opuser": "MAKE OP",
                               "voiceuser": "GIVE VOICE",
                               "quirksoff": "QUIRKS OFF",
                               "invitechum": "INVITE CHUM"
                              }
           },
  "chums": { "style": "border:0px; background-image:url($path/chumbg.png); background-color: rgb(102,102,102); background-repeat: no-repeat; color: white;font: bold;font-family: 'Arial';selection-background-color:#646464; ",
             "loc": [367, 270],
             "size": [261, 90],
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

                 "destructive": { "icon": "$path/destructive.png", "color": "#009900" },

                 "blocked": { "icon": "$path/blocked.png", "color": "black" }

             }
           },

  "trollslum": {
      "style": "background: #f21515; border:2px solid #bb0019; font-family: 'Arial'",
      "size": [195, 200],
      "label": { "text": "TROLLSLUM",
                 "style": "color: rgba(0, 0, 0, 100%) ;font:bold; font-family: 'Arial';border:0px;" },

      "chumroll": {"style": "border:0px; background-image:url($path/chumbg.png); background-color: rgb(102,102,102); background-repeat: no-repeat; color: white;font: bold;font-family: 'Arial';selection-background-color:#646464; " }
  },
  "mychumhandle": { "label": { "text": "",
                               "loc": [0,0],
                               "style": "color: rgba(0,0,0,0);font:bold; font-family: 'Arial';" },
                    "handle": { "style": "background: rgba(0,0,0,0); padding: 3px; color:rgba(0,0,0,0); font-family:'Arial'; font:bold; text-align:center;",
                                "loc": [239,0],
                                "size": [426, 94] },
                    "colorswatch": { "loc": [0,0],
                                     "size": [0,0],
                                     "text": "" },
                    "currentMood": [1000, 0]
                  },
  "defaultwindow": { "style": "background: #f21515; font-family:'Arial';font:bold;selection-background-color:#919191; "
                  },
  "addchum":  { "style": "background-image:url($path/gushers1.png); border:0px;",
                "pressed" : "background-image:url($path/gushers2.png);",
                "loc": [358,182],
                "size": [278, 70],
                "text": ""
              },
  "pester": { "style": "background-image:url($path/first1.png); border:0px;",
              "pressed" : "background-image:url($path/first2.png);",
                "loc": [0,97],
                "size": [328,189],
              "text": ""
            },
  "block": { "style": "background-image:url($path/douche1.png); border:0px;",
             "pressed" : "background-image:url($path/douche2.png);",
             "loc": [156,289],
             "size": [171, 169],
             "text": ""
           },
  "defaultmood": 20,
  "moodlabel": { "style": "",
                                 "loc": [0,0],
                                 "text": ""
                           },
  "moods": [
      { "style": "background: rgba(0,0,0,0%); border:0px; color: rgba(0,0,0,0%);",
                "selected": "background-image:url($path/moodcheck.png); border:0px; color: rgba(0,0,0,0%);",
                "loc": [361, 381],
                "size": [35, 33],
            "text": "",
                "icon": "$path/chummy.png",
                "mood": 0
          },
      { "style": "background: rgba(0,0,0,0%); border:0px; color: rgba(0,0,0,0%);",
                "selected": "background-image:url($path/moodcheck.png); border:0px; color: rgba(0,0,0,0%);",
                "loc": [395, 381],
                "size": [35, 33],
                "text": "",
                "icon": "$path/pleasant.png",
                "mood": 3
          },
      { "style": "background: rgba(0,0,0,0%); border:0px; color: rgba(0,0,0,0%);",
                "selected": "background-image:url($path/moodcheck.png); border:0px; color: rgba(0,0,0,0%);",
                "loc": [429, 381],
                "size": [35, 33],
                "text": "",
                "icon": "$path/distraught.png",
                "mood": 4
          },
      { "style": "background: rgba(0,0,0,0%); border:0px; color: rgba(0,0,0,0%);",
                "selected": "background-image:url($path/moodcheck.png); border:0px; color: rgba(0,0,0,0%);",
                "loc": [463, 381],
                "size": [35, 33],
                "text": "",
                "icon": "$path/pranky.png",
                "mood": 5
          },
      { "style": "background: rgba(0,0,0,0%); border:0px; color: rgba(0,0,0,0%);",
                "selected": "background-image:url($path/moodcheck.png); border:0px; color: rgba(0,0,0,0%);",
                "loc": [497, 381],
                "size": [35, 33],
                "text": "",
                "icon": "$path/smooth.png",
                "mood": 6
          },
      { "style": "background: rgba(0,0,0,0%); border:0px; color: rgba(0,0,0,0%);",
                "selected": "background-image:url($path/moodcheck.png); border:0px; color: rgba(0,0,0,0%);",
                "loc": [531, 381],
                "size": [35, 33],
                "text": "",
                "icon": "$path/amazed.png",
                "mood": 20
          },
      { "style": "background: rgba(0,0,0,0%); border:0px; color: rgba(0,0,0,0%);",
                "selected": "background-image:url($path/moodcheck.png); border:0px; color: rgba(0,0,0,0%);",
                "loc": [565, 381],
                "size": [35, 33],
                "text": "",
                "icon": "$path/mystified.png",
                "mood": 19
          },
      { "style": "background: rgba(0,0,0,0%); border:0px; color: rgba(0,0,0,0%);",
                "selected": "background-image:url($path/moodcheck.png); border:0px; color: rgba(0,0,0,0%);",
                "loc": [599, 381],
                "size": [35, 33],
                "text": "",
                "icon": "$path/insolent.png",
                "mood": 21
          },
      { "style": "background: rgba(0,0,0,0%); border:0px; color: rgba(0,0,0,0%);",
                "selected": "background-image:url($path/moodcheck.png); border:0px; color: rgba(0,0,0,0%);",
                "loc": [361, 413],
                "size": [35, 33],
                "text": "",
                "icon": "$path/bemused.png",
                "mood": 22
          },
      { "style": "background: rgba(0,0,0,0%); border:0px; color: rgba(0,0,0,0%);",
                "selected": "background-image:url($path/moodcheck.png); border:0px; color: rgba(0,0,0,0%);",
                "loc": [395, 413],
                "size": [35, 33],
                "text": "",
                "icon": "$path/rancorous.png",
                "mood": 1
          },
      { "style": "background: rgba(0,0,0,0%); border:0px; color: rgba(0,0,0,0%);",
                "selected": "background-image:url($path/moodcheck.png); border:0px; color: rgba(0,0,0,0%);",
                "loc": [429, 413],
                "size": [35, 33],
                "text": "",
                "icon": "$path/acceptant.png",
                "mood": 17
          },
      { "style": "background: rgba(0,0,0,0%); border:0px; color: rgba(0,0,0,0%);",
                "selected": "background-image:url($path/moodcheck.png); border:0px; color: rgba(0,0,0,0%);",
                "loc": [463, 413],
                "size": [35, 33],
                "text": "",
                "icon": "$path/discontent.png",
                "mood": 9
          },
      { "style": "background: rgba(0,0,0,0%); border:0px; color: rgba(0,0,0,0%);",
                "selected": "background-image:url($path/moodcheck.png); border:0px; color: rgba(0,0,0,0%);",
                "loc": [497, 413],
                "size": [35, 33],
                "text": "",
                "icon": "$path/sleek.png",
                "mood": 11
          },
      { "style": "background: rgba(0,0,0,0%); border:0px; color: rgba(0,0,0,0%);",
                "selected": "background-image:url($path/moodcheck.png); border:0px; color: rgba(0,0,0,0%);",
                "loc": [531, 413],
                "size": [35, 33],
                "text": "",
                "icon": "$path/perky.png",
                "mood": 16
          },
      { "style": "background: rgba(0,0,0,0%); border:0px; color: rgba(0,0,0,0%);",
                "selected": "background-image:url($path/moodcheck.png); border:0px; color: rgba(0,0,0,0%);",
                "loc": [565, 413],
                "size": [35, 33],
                "text": "",
                "icon": "$path/relaxed.png",
                "mood": 8
          },
      { "style": "background: rgba(0,0,0,0%); border:0px; color: rgba(0,0,0,0%);",
                "selected": "background-image:url($path/moodcheck.png); border:0px; color: rgba(0,0,0,0%);",
                "loc": [599, 413],
                "size": [35, 33],
                "text": "",
                "icon": "$path/devious.png",
                "mood": 10
          },
      { "style": "background: rgba(0,0,0,0%); border:0px; color: rgba(0,0,0,0%);",
                "selected": "background-image:url($path/moodcheck.png); border:0px; color: rgba(0,0,0,0%);",
                "loc": [361, 447],
                "size": [35, 33],
                "text": "",
                "icon": "$path/manipulative.png",
                "mood": 14
          },
      { "style": "background: rgba(0,0,0,0%); border:0px; color: rgba(0,0,0,0%);",
                "selected": "background-image:url($path/moodcheck.png); border:0px; color: rgba(0,0,0,0%);",
                "loc": [395, 447],
                "size": [35, 33],
                "text": "",
                "icon": "$path/vigorous.png",
                "mood": 15
          },
      { "style": "background: rgba(0,0,0,0%); border:0px; color: rgba(0,0,0,0%);",
                "selected": "background-image:url($path/moodcheck.png); border:0px; color: rgba(0,0,0,0%);",
                "loc": [429, 447],
                "size": [35, 33],
                "text": "",
                "icon": "$path/mirthful.png",
                "mood": 13
          },
      { "style": "background: rgba(0,0,0,0%); border:0px; color: rgba(0,0,0,0%);",
                "selected": "background-image:url($path/moodcheck.png); border:0px; color: rgba(0,0,0,0%);",
                "loc": [463, 447],
                "size": [35, 33],
                "text": "",
                "icon": "$path/detestful.png",
                "mood": 12
          },
      { "style": "background: rgba(0,0,0,0%); border:0px; color: rgba(0,0,0,0%);",
                "selected": "background-image:url($path/moodcheck.png); border:0px; color: rgba(0,0,0,0%);",
                "loc": [497, 447],
                "size": [35, 33],
                "text": "",
                "icon": "$path/ecstatic.png",
                "mood": 7
          },
      { "style": "background: rgba(0,0,0,0%); border:0px; color: rgba(0,0,0,0%);",
                "selected": "background-image:url($path/moodcheck.png); border:0px; color: rgba(0,0,0,0%);",
                "loc": [531, 447],
                "size": [35, 33],
                "text": "",
                "icon": "$path/protective.png",
                "mood": 18
          },
      { "style": "background: rgba(0,0,0,0%); border:0px; color: rgba(0,0,0,0%);",
                "selected": "background-image:url($path/moodcheck.png); border:0px; color: rgba(0,0,0,0%);",
                "loc": [565, 447],
                "size": [35, 33],
                "text": "",
                "icon": "$path/destructive.png",
                "mood": 23
          },
      { "style": "background: rgba(0,0,0,0%); border:0px; color: rgba(0,0,0,0%);",
                "selected": "background-image:url($path/moodcheck.png); border:0px; color: rgba(0,0,0,0%);",
                "loc": [599, 447],
                "size": [35, 33],
                "text": "",
                "icon": "$path/offline.png",
                "mood": 2
          }
  ]
 },
 "convo":
 {"style": "background-color: rgba(0,0,0,0);border-width: 5px; border-image:url($path/convobg.png) 5px; font-family: 'Arial'",
  "tabstyle": "background-color: #f21515; font-family: 'Arial'",
  "scrollbar": { "style" : "padding-top:17px; padding-bottom:17px;width: 18px; background:  rgba(0,0,0,0); border:0px;",
                 "handle": "background-color:#bb0019;min-height:20px;",
                 "downarrow": "height:17px;border:0px solid #bb0019;",
                 "darrowstyle": "image:url($path/downarrow.png);",
                 "uparrow": "height:17px;border:0px solid #bb0019;",
                 "uarrowstyle": "image:url($path/uparrow.png);"
               },
  "margins": {"top": 0, "bottom": 6, "left": 0, "right": 0 },
  "size": [500, 325],
  "chumlabel": { "style": "margin-bottom: 7px; margin-top: 10px; background:  rgba(0,0,0,0); color: white; border:0px; font-size: 16px;",
                 "align": { "h": "center", "v": "center" },
                 "minheight": 47,
                 "maxheight": 47,
                 "text" : ":: $handle ::"
               },
  "textarea": {
      "style": "background: white;  font-size: 14px; border:2px solid #bb0019;text-align:center; margin-right:10px; margin-left:10px; margin-bottom:5px;"
  },
  "input": {
      "style": "background: white; border:2px solid #bb0019; margin-right:10px; margin-left:10px; font-size: 14px;"
  },
  "tabs": {
      "style": "background-color: #ff7e7e; font-family: 'Arial';font:bold;font-size:12px;min-height:25px;",
      "selectedstyle": "border:0px;background-color:#f21515;border-top:2px solid #bb0019; border-left:2px solid #bb0019;border-right:2px solid #bb0019; border-top-left-radius: 4px; border-top-right-radius: 4px;",
      "newmsgcolor": "white",
      "tabstyle": 0
  },
  "text": {
      "beganpester": "began bothering",
      "ceasepester": "ceased bothering",
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
      "style": "background-color: #ff7e7e; font-family: 'Arial';font:bold;font-size:12px;min-height:25px;",
      "selectedstyle": "border:0px;background-color:#f21515;border-top:2px solid #bb0019; border-left:2px solid #bb0019;border-right:2px solid #bb0019; border-top-left-radius: 4px; border-top-right-radius: 4px;",
      "newmsgcolor": "white",
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
  "input": { "style": "background: white; border:2px solid #bb0019;margin-top:5px; margin-right:10px; margin-left:10px; font-size: 14px;" },
  "textarea": { "style": "background: white;  font-size: 14px; border:2px solid #bb0019;text-align:center; margin-right:10px; margin-left:10px;" },
  "margins": {"top": 0, "bottom": 6, "left": 0, "right": 0 },
  "userlist": { "width": 150,
                "style": "border:2px solid #bb0019; background: white; font-family: 'Arial';selection-background-color:#646464; font-size: 14px;  margin-left:0px; margin-right:10px;"
              },
  "time": { "text": { "width": 75,
                      "style": " border: 2px solid #bb0019; background: white; font-size: 12px; margin-top: 5px; margin-right: 5px; margin-left: 5px; font-family:'Arial';font:bold;"
                    },
            "slider": { "style": "border: 0px;",
                        "groove": "",
                        "handle": ""
                      },
            "buttons": { "style": "color: black; font: bold; border: 2px solid #bb0019; font-size: 12px; background: #ff7e7e; margin-top: 5px; margin-right: 5px; margin-left: 5px; padding: 2px; width: 50px;" },
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
