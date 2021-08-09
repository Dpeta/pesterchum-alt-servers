{"main":
 {"style": "background-color:rgba(0,0,0,0); background-repeat: no-repeat;",
  "background-image": "$path/tnbg2.png",
  "size": [650, 450],
  "icon": "$path/trayicon.png",
  "newmsgicon": "$path/trayicon2.png",
  "windowtitle": "TROLLIAN",
  "close": { "image": "$path/x.png",
             "loc": [639, 4]},
  "minimize": { "image": "$path/m.png",
                "loc": [625, 10]},
  "menubar": { "style": "font-family: 'Arial'; font-size: 11px; color: rgba(0,0,0,0);" },
  "menu" : { "style": "font-family: 'Arial'; font-size: 11px; color: #000000; background-color: #c2c2c2; border:1px solid #545454;",
             "selected": "background-color: #545454",
             "menuitem": "margin-right:14px;",
             "loc": [14,90]
           },
  "sounds": { "alertsound": "$path/alarm.wav",
              "memosound": "$path/alarm2.wav"},
  "menus": {"client": {"_name": "Trollian",
                       "options": "Options",
                       "memos": "Memos",
                       "logviewer": "Pesterlogs",
                       "randen": "Random Encounter",
                       "userlist": "Fresh Targets",
                       "addgroup": "Add Group",
                       "talk": "Troll",
                       "import": "import U2;",
                       "reconnect": "Reconnect",
                       "idle": "Idle",
                       "exit": "Abscond",
                       "console": "Console"},
            "profile": {"_name": "View",
                        "switch": "Trolltag",
                        "theme": "Theme",
                        "color": "Hemospectrum",
                        "block": "Chumpdump",
                        "quirks": "Annoying" },
            "help": { "_name": "Help",
                      "rules": "Rules",
                      "about": "About",
                      "help": "Help",
                      "calsprite": "CalSprite",
                      "chanserv": "ChanServ",
                      "nickserv": "NickServ",
                      "reportbug": "Report Bug" },
            "rclickchumlist": {"pester": "Troll",
                               "removechum": "Trash",
                               "report": "Tattle",
                               "blockchum": "Block",
                               "addchum": "Add Chump",
                               "viewlog": "View Pesterlog",
                               "notes": "Edit Notes...",
                               "unblockchum": "Mercy",
                               "removegroup": "Remove Group",
                               "renamegroup": "Rename Group",
                               "movechum": "Move To",
                               "banuser": "Ban",
                               "opuser": "Promote",
                               "voiceuser": "Let Speak",
                               "quirkkill": "Kill Quirk",
                               "quirksoff": "Quirks Off",
                               "invitechum": "Invite Chump",
                               "memosetting": "Memo Settings",
                               "memonoquirk": "Disable Quirks",
                               "memohidden": "Hidden",
                               "memoinvite": "Invite-Only",
                               "memomute": "Mute",
                               "beeponmessage": "Beep on Message",
                               "flashonmessage": "Flash on Message",
                               "mutenotifications": "Mute Notifications" }
           },
  "chums": { "style": "font-size: 12px; background: white; border:0px; font-family: 'Arial';selection-background-color:rgb(200,200,200); ",
             "scrollbar": { "style" : "background-color:#c2c2c2;",
                            "handle": "background-color:#e02413;height:20px;border:2px solid #ff2612;",
                            "downarrow": "",
                            "darrowstyle": "",
                            "uparrow": "",
                            "uarrowstyle": ""
                          },
             "loc": [477, 91],
             "size": [171, 357],
             "userlistcolor": "black",
             "moods": {

                 "chummy": { "icon": "$path/chummy.png", "color": "#63ea00" },

                 "rancorous": { "icon": "$path/rancorous.png", "color": "#7f7f7f" },

                 "offline": { "icon": "$path/offline.png", "color": "black"},


                 "pleasant": { "icon": "$path/pleasant.png", "color": "#d69df8" },

                 "distraught": { "icon": "$path/distraught.png", "color": "#706eba" },

                 "pranky": { "icon": "$path/pranky.png", "color": "blue" },


                 "smooth": { "icon": "$path/smooth.png", "color": "red" },


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

                 "blocked": { "icon": "$path/blocked.png", "color": "black" }

             }
           },
  "trollslum": {
      "style": "background:  rgb(190, 19, 4); font-family: 'Arial'",
      "size": [175, 461],
      "label": { "text": "Chumpdump",
                 "style": "color: rgba(0, 0, 0, 100%) ;font:bold; font-family: 'Arial';border: 0px;" },
      "chumroll": {"style": "border: 0px; background-color: white; padding: 5px; font-family: 'Arial';selection-background-color:rgb(200,200,200); " }
  },
  "mychumhandle": { "label": { "text": "",
                               "loc": [0,0],
                               "style": "color:rgba(0,0,0,0);" },
                    "handle": { "style": "background: rgba(0,0,0,0); color:rgba(0,0,0,0);",
                                "loc": [0,0],
                                "size": [0,0] },
                    "colorswatch": { "loc": [0,0],
                                     "size": [0,0],
                                     "text": "" },
                    "currentMood": []
                  },
  "defaultwindow": { "style": "background: #c2c2c2; font-family:'Arial';font:bold;selection-background-color:#545454; "
                   },
  "addchum": { "style": "background: rgba(0,0,0,0); border:0px; color: rgba(0,0,0,0);",
               "loc": [475, 67],
               "size": [175, 18],
               "text": ""
             },
  "pester": { "style": "background: rgba(0,0,0,0); border:0px; color: rgba(0,0,0,0);",
              "loc": [0,0],
              "size": [0, 0],
              "text": ""
            },
  "block": { "style": "background: rgba(0,0,0,0); border:0px; color: rgba(0,0,0,0);",
             "loc": [1500,202],
             "size": [71, 22],
             "text": ""
           },
  "defaultmood": 7,
  "moodlabel": { "style": "",
                 "loc": [0, 0],
                 "text": ""
               },
  "moods": [
      { "style": "border:0px;",
        "selected": "background-image:url($path/moodcheck1.png); border:0px;",
        "loc": [16, 141],
        "size": [38, 270],
        "text": "",
        "icon": "",
        "mood": 17
      },
      { "style": "border:0px;",
        "selected": "background-image:url($path/moodcheck2.png); border:0px;",
        "loc": [51, 141],
        "size": [38, 270],
        "text": "",
        "icon": "",
        "mood": 9
      },
      { "style": "border:0px;",
        "selected": "background-image:url($path/moodcheck3.png); border:0px;",
        "loc": [86, 141],
        "size": [38, 270],
        "text": "",
        "icon": "",
        "mood": 11
      },
      { "style": "border:0px;",
        "selected": "background-image:url($path/moodcheck4.png); border:0px;",
        "loc": [121, 141],
        "size": [38, 270],
        "text": "",
        "icon": "",
        "mood": 1
      },
      { "style": "border:0px;",
        "selected": "background-image:url($path/moodcheck5.png); border:0px;",
        "loc": [156, 141],
        "size": [38, 270],
        "text": "",
        "icon": "",
        "mood": 16
      },
      { "style": "border:0px;",
        "selected": "background-image:url($path/moodcheck6.png); border:0px;",
        "loc": [191, 141],
        "size": [38, 270],
        "text": "",
        "icon": "",
        "mood": 8
      },
      { "style": "border:0px;",
        "selected": "background-image:url($path/moodcheck7.png); border:0px;",
        "loc": [226, 141],
        "size": [38, 270],
        "text": "",
        "icon": "",
        "mood": 10
      },
      { "style": "border:0px;",
        "selected": "background-image:url($path/moodcheck8.png); border:0px;",
        "loc": [261, 141],
        "size": [38, 270],
        "text": "",
        "icon": "",
        "mood": 14
      },
      { "style": "border:0px;",
        "selected": "background-image:url($path/moodcheck9.png); border:0px;",
        "loc": [296, 141],
        "size": [38, 270],
        "text": "",
        "icon": "",
        "mood": 15
      },
      { "style": "border:0px;",
        "selected": "background-image:url($path/moodcheck10.png); border:0px;",
        "loc": [331, 141],
        "size": [38, 270],
        "text": "",
        "icon": "",
        "mood": 13
      },
      { "style": "border:0px;",
        "selected": "background-image:url($path/moodcheck11.png); border:0px;",
        "loc": [366, 141],
        "size": [38, 270],
        "text": "",
        "icon": "",
        "mood": 12
      },
      { "style": "border:0px;",
        "selected": "background-image:url($path/moodcheck12.png); border:0px;",
        "loc": [401, 141],
        "size": [38, 270],
        "text": "",
        "icon": "",
        "mood": 7
      },

      { "style": "border:0px;color: rgba(0, 0, 0, 0%);",
        "selected": "border:0px; color: rgba(0, 0, 0, 0%);",
        "loc": [12, 117],
        "size": [435, 18],
        "text": "",
        "icon": "",
        "mood": 2
      }
  ]
 },
 "convo":
 {"style": "background:  rgb(190, 19, 4); font-family: 'Arial';",
  "scrollbar": { "style" : "", "handle": "" },
  "margins": {"top": 22, "bottom": 9, "left": 10, "right": 4 },
  "size": [400, 250],
  "size": [400, 250],
  "chumlabel": { "style": "background-image:url($path/chumlabelbg.png);background-color:rgb(255,38,18); background-repeat: no-repeat; color: white; padding: 2px; border:1px solid #c2c2c2; margin-bottom: 4px;",
                 "align": { "h": "left", "v": "center" },
                 "minheight": 22,
                 "maxheight": 36,
                 "text" : "trolling: $handle"
               },
  "textarea": {
      "style": "background: white; border:2px solid #c2c2c2; font-size: 14px;"
  },
  "input": {
      "style": "background: white;margin-top:5px; border:1px solid #c2c2c2; margin-right: 54px; font-size: 12px;"
  },
  "tabwindow" : {
    "style": "background: rgb(190, 19, 4); font-family: 'Arial'"
  },
  "tabs": {
      "style": "",
      "selectedstyle": "",
      "newmsgcolor": "red",
      "tabstyle": 0
  },
  "text": {
      "beganpester": "began trolling",
      "ceasepester": "gave up trolling",
      "blocked": "blocked",
      "unblocked": "mercifully forgave",
      "openmemo": "opened memo on board",
      "joinmemo": "responded to memo",
      "closememo": "ceased responding to memo",
      "kickedmemo": "You have been banned from this memo!"
  },
  "systemMsgColor": "#646464"
 },
 "memos":
 {"memoicon": "$path/memo.png",
  "style": "background:  rgb(190, 19, 4); font-family: 'Arial';",
  "size": [450,300],
  "tabs": {
      "style": "",
      "selectedstyle": "",
      "newmsgcolor": "red",
      "tabstyle": 0
  },
  "label": { "text": "Bulletin Board: $channel",
             "style": "background-image:url($path/chumlabelbg.png);background-color:rgb(255,38,18); background-repeat: no-repeat; color: white; padding: 2px; border:1px solid #c2c2c2; margin-bottom: 4px;",
             "align": { "h": "left", "v": "center" },
             "minheight": 18,
             "maxheight": 36
           },
  "textarea": {
      "style": "background: white; border:2px solid #c2c2c2; font-size: 12px;"
  },
  "input": {
      "style": "background: white;margin-top:5px; border:1px solid #c2c2c2; font-size: 12px; margin-bottom: 5px; "
  },
  "margins": {"top": 22, "bottom": 10, "left": 9, "right": 4 },
  "userlist": { "width": 125,
                "style": "font-size: 12px; background: white; margin-bottom: 5px; border:2px solid #c2c2c2; padding: 5px; font-family: 'Arial';selection-background-color:rgb(200,200,200);"
              },
  "time": { "text": { "width": 75,
                      "style": "color: black; font:bold;  border:1px solid #c2c2c2; background: white; height: 19px;"
                    },
            "slider": { "style": " border:1px solid #c2c2c2;",
                        "groove": "border-image:url($path/timeslider.png);",
                        "handle": "image:url($path/acceptant.png);"
                      },
            "buttons": { "style": "border:1px solid #a68168; height: 17px; width: 50px; color: #cd8f9d; font-family: 'Arial'; background: rgb(190, 19, 4); margin-left: 2px;" },
            "arrows": { "left": "$path/leftarrow.png",
                        "right": "$path/rightarrow.png",
                        "style": "width: 19px; height: 19px; border:0px; margin-left: 2px;"
                      }
          },
  "systemMsgColor": "#646464",
  "op": { "icon": "$path/op.png" },
  "halfop": { "icon": "$path/halfop.png" },
  "voice": { "icon": "$path/voice.png" },
  "founder": { "icon": "$path/founder.png" }
 },
 "toasts":
 {
   "width": 210,
   "height": 100,
   "style": "background: rgb(255,38,18);",
   "icon": { "signin": "$path/../enamel/ecstatic2.gif",
             "signout": "$path/../enamel/discontent2.gif",
             "style": "border: 0px;" },
   "title": { "minimumheight": 50,
              "style": "border: 0px; padding: 5px; font-weight: bold; color: white;"
            },
   "content": { "style": "background: rgb(190, 19, 4); color: black; padding: 5px;" }
 }
}
