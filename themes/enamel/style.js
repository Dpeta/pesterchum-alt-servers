{"main":
 {"style": "background-repeat: no-repeat; font-family: 'Century Gothic'; font-size: 14px;",
  "background-image": "$path/ebg.png",
  "size": [801, 555],
  "icon": "$path/trayicon.png",
  "newmsgicon": "$path/trayicon2.png",
  "windowtitle": "Pesterchum Enamel",
  "close": { "image": "$path/x.gif",
             "loc": [315, 26]},
  "minimize": { "image": "$path/m.gif",
                "loc": [300, 32]},
  "menubar": { "style": "font-family: 'Century Gothic'; font-size: 14px; color:#9d9d9d" },
  "menu" : { "style": "font-family: 'Century Gothic'; font-size: 14px; color: #000000; background-color: #fdb302;border:2px solid #ffff00",
             "menuitem": "margin-right:25px;",
             "selected": "background-color: #ffff00",
             "loc": [480,30]
           },
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
                               "blockchum": "Block",
                               "report": "Report",
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
  "chums": { "style": "text-align: center; border:0px; background-image:url($path/chumbg.png); background-color: #ffe400; background-repeat: no-repeat; color: white; font-family: 'Century Gothic';selection-background-color:#646464; font-size:18px; ",
             "scrollbar": { "style" : "background-image:url($path/chumbg.png); background-color: #ffe400;",
                            "handle": "border-width: 5px; border-image:url($path/scrollbg.png) 5px; min-height:60px; max-height:60px;",
                            "downarrow": "",
                            "darrowstyle": "",
                            "uparrow": "",
                            "uarrowstyle": ""
                          },
             "loc": [440, 211],
             "size": [289, 275],
             "userlistcolor": "black",
             "moods": {

                 "chummy": { "icon": "$path/chummy.gif", "color": "black" },

                 "rancorous": { "icon": "$path/rancorous.gif", "color": "red" },

                 "offline": { "icon": "$path/offline.gif", "color": "#9d9d9d"},


                 "pleasant": { "icon": "$path/pleasant.gif", "color": "black" },

                 "distraught": { "icon": "$path/distraught.gif", "color": "black" },

                 "pranky": { "icon": "$path/pranky.gif", "color": "black" },


                 "smooth": { "icon": "$path/smooth.gif", "color": "black" },

                 "mystified": { "icon": "$path/mystified.gif", "color": "black" },

                 "amazed": { "icon": "$path/amazed.gif", "color": "black" },

                 "insolent": { "icon": "$path/insolent.gif", "color": "black" },

                 "bemused": { "icon": "$path/bemused.gif", "color": "black" },


                 "ecstatic": { "icon": "$path/ecstatic.gif", "color": "red" },

                 "relaxed": { "icon": "$path/relaxed.gif", "color": "red" },

                 "discontent": { "icon": "$path/discontent.gif", "color": "red" },

                 "devious": { "icon": "$path/devious.gif", "color": "red" },

                 "sleek": { "icon": "$path/sleek.gif", "color": "red" },

                 "detestful": { "icon": "$path/detestful.gif", "color": "red" },

                 "mirthful": { "icon": "$path/mirthful.gif", "color": "red" },

                 "manipulative": { "icon": "$path/manipulative.gif", "color": "red" },

                 "vigorous": { "icon": "$path/vigorous.gif", "color": "red" },

                 "perky": { "icon": "$path/perky.gif", "color": "red" },

                 "acceptant": { "icon": "$path/acceptant.gif", "color": "red" },

                 "protective": { "icon": "$path/protective.png", "color": "#00ff00" },

                 "blocked": { "icon": "$path/blocked.gif", "color": "red" }

             }
           },
  "trollslum": {
      "style": "background: #fdb302; border:2px solid yellow; font-family: 'Century Gothic'",
      "size": [195, 200],
      "label": { "text": "TROLLSLUM",
                 "style": "color: rgba(0, 0, 0, 100%) ;font:bold; font-family: 'Century Gothic';border:0px;" },
      "chumroll": {"style": "border:2px solid yellow; background-color: black;color: white;font: bold;font-family: 'Century Gothicl';selection-background-color:#646464; " }
  },
  "mychumhandle": { "label": { "text": "",
                               "loc": [0,0],
                               "style": "color: rgba(255, 255, 0, 0%) ;font:bold; font-family: 'Century Gothic';" },
                    "handle": { "style": "background: rgba(255, 255, 0, 0%); color:white; font-family:'Century Gothic'; font-size:14px; text-align:left;",
                                "loc": [0,0],
                                "size": [0, 0] },
                    "colorswatch": { "loc": [0,0],
                                     "size": [0,0],
                                     "text": "" },
                    "currentMood": [1500, 1500]
                  },
  "defaultwindow": { "style": "background: #fdb302; font-family:'Century Gothic';font:bold;selection-background-color:#919191; "
                   },
  "addchum":  { "style": "background: rgba(255, 255, 0, 0%); border:0px; color: rgba(0, 0, 0, 0%);",
              "loc": [443,144],
              "size": [284, 60],
                "text": ""
              },
  "pester": { "style": "background:  rgba(255, 255, 0, 0%); border:0px; font: bold; color:  rgba(255, 255, 0, 0%); font-family:'Century Gothic';",
              "pressed" : "background-image:url($path/pesterhold.png);",
                "loc": [0,0],
                "size": [0, 0],
              "text": ""
            },
  "block": { "style": "background:  rgba(255, 255, 0, 0%); border:2px solid #c48a00; font: bold; color:  rgba(255, 255, 0, 0%); font-family:'Century Gothic';",
             "loc": [0,0],
             "size": [0, 0],
             "text": ""
           },
  "defaultmood": 0,
  "moodlabel": { "style": "",
                                 "loc": [20, 430],
                                 "text": ""
                           },
  "moods": [
      { "style": "background-image:url($path/mood1.png); border:0px;",
                "selected": "background-image:url($path/mood1c.png); border:0px;",
                "loc": [0, 258],
                "size": [100,110],
                 "text": "",
                "icon": "",
                "mood": 0
          },
      { "style": "background-image:url($path/mood2.png); border:0px;",
                "selected": "background-image:url($path/mood2c.png); border:0px;",
                "loc": [106, 258],
                "size": [100, 110],
                 "text": "",
                "icon": "",
                "mood": 19
          },
      { "style": "background-image:url($path/mood3.png); border:0px;",
                "selected": "background-image:url($path/mood3c.png); border:0px;",
                "loc": [212, 258],
                "size": [100, 110],
                 "text": "",
                "icon": "",
                "mood": 22
          },
      { "style": "background-image:url($path/mood4.png); border:0px;",
                "selected": "background-image:url($path/mood4c.png); border:0px;",
                "loc": [318, 258],
                "size": [100, 110],
                 "text": "",
                "icon": "",
                "mood": 4
          },
      { "style": "background-image:url($path/mood5.png); border:0px;",
                "selected": "background-image:url($path/mood5c.png); border:0px;",
                "loc": [0, 382],
                "size": [100, 110],
                 "text": "",
                "icon": "",
                "mood": 3
          },
      { "style": "background-image:url($path/mood6.png); border:0px;",
                "selected": "background-image:url($path/mood6c.png); border:0px;",
                "loc": [106, 382],
                "size": [100, 110],
                 "text": "",
                "icon": "",
                "mood": 20
          },
      { "style": "background-image:url($path/mood7.png); border:0px;",
                "selected": "background-image:url($path/mood7c.png); border:0px;",
                "loc": [212, 382],
                "size": [100, 110],
                 "text": "",
                "icon": "",
                "mood": 5
          },
      { "style": "background-image:url($path/mood8.png); border:0px;",
                "selected": "background-image:url($path/mood8c.png); border:0px;",
                "loc": [318, 382],
                "size": [100, 110],
                 "text": "",
                "icon": "",
                "mood": 1
          },
      { "style": "border:0px;",
                "selected": "border:0px;",
                "loc": [0, 0],
                "size": [100, 100],
                 "text": "",
                "icon": "",
                "mood": 2
          }
  ]
 },
 "convo":
 {"style": "background-color: rgba(0, 0, 0, 0%);border-width: 5px; border-image:url($path/convobg.png) 5px; font-family: 'Century Gothic'",
  "tabstyle": "background-color: #fdb302; font-family: 'Century Gothic'",
  "scrollbar": { "style" : "padding-top:17px; padding-bottom:17px;width: 18px; background:  rgba(255, 255, 0, 0%); border:0px;",
                 "handle": "border-width: 5px; border-image:url($path/scrollbg.png) 5px; min-height:60px;",
                 "downarrow": "height:17px;border:0px solid #c48a00;",
                 "darrowstyle": "image:url($path/downarrow.png);",
                 "uparrow": "height:17px;border:0px solid #c48a00;",
                 "uarrowstyle": "image:url($path/uparrow.png);"
               },
  "margins": {"top": 35, "bottom": 35, "left": 32, "right": 20 },
  "size": [480, 348],
  "chumlabel": { "style": " background:  rgba(255, 255, 0, 0%); color: white; border:0px; font-size: 0px;",
                 "align": { "h": "center", "v": "center" },
                 "minheight": 0,
                 "maxheight": 0,
                 "text" : ""
               },
  "textarea": {
      "style": "background-color: white;  background-image: url(); font: bold; font-size: 14px; font-family: 'Century Gothic'; border:2px solid yellow;text-align:center;"
  },
  "input": { "style": "background: white; border:2px solid yellow;margin-top:10px; font: bold; font-size: 14px; font-family: 'Century Gothic'" },
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
 {"style": "background-color: rgba(0,0,0,0); border-width: 5px; border-image:url($path/convobg.png) 5px; font-family: 'Century Gothic'; selection-background-color:#919191; ",
  "size": [500,325],
  "tabs": {
      "style": "",
      "selectedstyle": "",
      "newmsgcolor": "#fdb302",
      "tabstyle": 0
  },
  "scrollbar": { "style" : "padding-top:17px; padding-bottom:17px;width: 18px; background:  rgba(255, 255, 0, 0%); border:0px;",
                 "handle": "border-width: 5px; border-image:url($path/scrollbg.png) 5px; min-height:60px;",
                 "downarrow": "height:17px;border:0px;",
                 "darrowstyle": "image:url();",
                 "uparrow": "height:17px;border:0px;",
                 "uarrowstyle": "image:url();"
               },
  "label": { "text": "Bulletin Board: $channel",
             "style": "margin-bottom: 7px; margin-top: 10px; background-color: rgba (0,0,0,0) ; background-image:url($path/nothing.png); color: white; border:0px; font-size: 16px;",
             "align": { "h": "center", "v": "center" },
             "minheight": 47,
             "maxheight": 47
           },
  "input": { "style": "background: white; border:2px solid #c48a00;margin-top:5px; margin-right:10px; margin-left:10px; font: bold; font-size: 14px; font-family: 'Century Gothic'" },
  "textarea": { "style": " background-color: white; background-image:url();  font: bold; font-size: 14px; font-family: 'Century Gothic'; border:2px solid #c48a00;text-align:center; margin-right:10px; margin-left:10px;" },
  "margins": {"top": 0, "bottom": 6, "left": 0, "right": 0 },
  "userlist": { "width": 150,
                "style": "border:2px solid #c48a00; background: white; font-family: 'Century Gothic';selection-background-color:#646464; font-size: 14px;  margin-left:0px; margin-right:10px;"
              },
  "time": { "text": { "width": 75,
                      "style": " border: 2px solid yellow; background: white; font-size: 12px; margin-top: 5px; margin-right: 5px; margin-left: 5px; font-family:'Century Gothic';font:bold;"
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
  "op": { "icon": "$path/smooth.gif" },
  "voice": { "icon": "$path/voice.png" }
 }
}
