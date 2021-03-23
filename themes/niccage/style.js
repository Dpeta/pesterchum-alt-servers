{"main":
 {"style": "background-repeat: no-repeat; font-family: 'Arial'; font-size: 14px;",
  "background-image": "$path/ebg.png",
  "size": [801, 555],
  "icon": "$path/trayicon.png",
  "newmsgicon": "$path/trayicon2.png",
  "windowtitle": "Cagechum",
  "close": { "image": "$path/x.gif",
             "loc": [315, 26]},
  "minimize": { "image": "$path/m.gif",
                "loc": [300, 32]},
  "menubar": { "style": "font-family: 'Arial'; font-size: 14px; color:#7c6dbc" },
  "menu" : { "style": "font-family: 'Arial'; font-size: 14px; color: #000000; background-color: #F7E430;border:2px solid #F7B53D",
             "menuitem": "margin-right:25px;",
             "selected": "background-color: #F7B53D",
             "loc": [480,30]
           },
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
                               "unblockchum": "Unblock",
                               "removegroup": "Remove Group",
                               "renamegroup": "Rename Group",
                               "movechum": "Move To",
                               "banuser": "Ban User",
                               "opuser": "Make OP",
                               "voiceuser": "Give Voice",
                               "quirksoff": "Quirks Off",
                               "invitechum": "Invite Chum"
                              }
           },
  "chums": { "style": "font-size: 16px; background-image:url($path/chumbg.png); background-color: #C2C4EB; background-repeat: no-repeat; font-family: 'Arial'; border: 0px; selection-background-color: #222222; color: black;",
             "loc": [440, 211],
             "size": [289, 275],
              "text": "",
             "userlistcolor": "black",
             "loc": [440, 211],
             "size": [289, 275],
             "moods": {

                 "chummy": { "icon": "$path/chummy.gif", "color": "black" },

                 "rancorous": { "icon": "$path/rancorous.gif", "color": "#9697C3" },

                 "offline": { "icon": "$path/offline.gif", "color": "#7c6dbc"},


                 "pleasant": { "icon": "$path/pleasant.gif", "color": "black" },

                 "distraught": { "icon": "$path/distraught.gif", "color": "black" },

                 "pranky": { "icon": "$path/pranky.gif", "color": "black" },


                 "smooth": { "icon": "$path/smooth.gif", "color": "black" },

                 "mystified": { "icon": "$path/mystified.gif", "color": "black" },

                 "amazed": { "icon": "$path/amazed.gif", "color": "black" },

                 "insolent": { "icon": "$path/insolent.gif", "color": "black" },

                 "bemused": { "icon": "$path/bemused.gif", "color": "black" },


                 "ecstatic": { "icon": "$path/ecstatic.gif", "color": "#9697C3" },

                 "relaxed": { "icon": "$path/relaxed.gif", "color": "#9697C3" },

                 "discontent": { "icon": "$path/discontent.gif", "color": "#9697C3" },

                 "devious": { "icon": "$path/devious.gif", "color": "#9697C3" },

                 "sleek": { "icon": "$path/sleek.gif", "color": "#9697C3" },

                 "detestful": { "icon": "$path/detestful.gif", "color": "#9697C3" },

                 "mirthful": { "icon": "$path/mirthful.gif", "color": "#9697C3" },

                 "manipulative": { "icon": "$path/manipulative.gif", "color": "#9697C3" },

                 "vigorous": { "icon": "$path/vigorous.gif", "color": "#9697C3" },

                 "perky": { "icon": "$path/perky.gif", "color": "#9697C3" },

                 "acceptant": { "icon": "$path/acceptant.gif", "color": "#9697C3" },

                 "protective": { "icon": "$path/protective.png", "color": "#00ff00" },

                 "blocked": { "icon": "$path/blocked.gif", "color": "#9697C3" }

             }
           },
  "trollslum": {
      "style": "background: #F7E430; border:2px solid #FFD47C; font-family: 'Arial'",
      "size": [195, 200],
      "label": { "text": "TROLLSLUM",
                 "style": "color: rgba(0, 0, 0, 100%) ;font:bold; font-family: 'Arial';border:0px;" },
      "chumroll": {"style": "border:2px solid #FFD47C; background-color: black;color: #FFFCBD;font: bold;font-family: 'Ariall';selection-background-color:#646464; " }
  },
  "mychumhandle": { "label": { "text": "",
                               "loc": [0,0],
                               "style": "color: rgba(255, 255, 0, 0%) ;font:bold; font-family: 'Arial';" },
                    "handle": { "style": "background: rgba(255, 255, 0, 0%); color:#FFFCBD; font-family:'Arial'; font-size:14px; text-align:left;",
                                "loc": [0,0],
                                "size": [0, 0] },
                    "colorswatch": { "loc": [0,0],
                                     "size": [0,0],
                                     "text": "" },
                    "currentMood": [1500, 1500]
                  },
  "defaultwindow": { "style": "background: #F7E430; font-family:'Arial';font:bold;selection-background-color:#919191; "
                   },
  "addchum":  { "style": "background: rgba(255, 255, 0, 0%); border:0px; color: rgba(0, 0, 0, 0%);",
              "loc": [443,144],
              "size": [284, 60],
                "text": ""
              },
  "pester": { "style": "background:  rgba(255, 255, 0, 0%); border:0px; font: bold; color:  rgba(255, 255, 0, 0%); font-family:'Arial';",
              "pressed" : "background-image:url($path/pesterhold.png);",
                "loc": [0,0],
                "size": [0, 0],
              "text": ""
            },
  "block": { "style": "background:  rgba(255, 255, 0, 0%); border:2px solid #F7B53D; font: bold; color:  rgba(255, 255, 0, 0%); font-family:'Arial';",
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
                "size": [100,125],
                 "text": "",
                "icon": "",
                "mood": 0
          },
      { "style": "background-image:url($path/mood2.png); border:0px;",
                "selected": "background-image:url($path/mood2c.png); border:0px;",
                "loc": [106, 258],
                "size": [100, 125],
                 "text": "",
                "icon": "",
                "mood": 19
          },
      { "style": "background-image:url($path/mood3.png); border:0px;",
                "selected": "background-image:url($path/mood3c.png); border:0px;",
                "loc": [212, 258],
                "size": [100, 125],
                 "text": "",
                "icon": "",
                "mood": 22
          },
      { "style": "background-image:url($path/mood4.png); border:0px;",
                "selected": "background-image:url($path/mood4c.png); border:0px;",
                "loc": [318, 258],
                "size": [100, 125],
                 "text": "",
                "icon": "",
                "mood": 4
          },
      { "style": "background-image:url($path/mood5.png); border:0px;",
                "selected": "background-image:url($path/mood5c.png); border:0px;",
                "loc": [0, 382],
                "size": [100, 125],
                 "text": "",
                "icon": "",
                "mood": 3
          },
      { "style": "background-image:url($path/mood6.png); border:0px;",
                "selected": "background-image:url($path/mood6c.png); border:0px;",
                "loc": [106, 382],
                "size": [100, 125],
                 "text": "",
                "icon": "",
                "mood": 20
          },
      { "style": "background-image:url($path/mood7.png); border:0px;",
                "selected": "background-image:url($path/mood7c.png); border:0px;",
                "loc": [212, 382],
                "size": [100, 125],
                 "text": "",
                "icon": "",
                "mood": 5
          },
      { "style": "background-image:url($path/mood8.png); border:0px;",
                "selected": "background-image:url($path/mood8c.png); border:0px;",
                "loc": [318, 382],
                "size": [100, 125],
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
 {"style": "background-color: rgba(0, 0, 0, 0%);border-width: 5px; border-image:url($path/convobg.png) 5px; font-family: 'Arial'",
  "tabstyle": "background-color: #F7E430; font-family: 'Arial'",
  "scrollbar": { "style" : "padding-top:17px; padding-bottom:17px;width: 18px; background:  rgba(255, 255, 0, 0%); border:0px;",
                 "handle": "border-width: 5px; border-image:url($path/scrollbg.png) 5px; min-height:60px;",
                 "downarrow": "height:17px;border:0px solid #F7B53D;",
                 "darrowstyle": "image:url($path/downarrow.png);",
                 "uparrow": "height:17px;border:0px solid #F7B53D;",
                 "uarrowstyle": "image:url($path/uparrow.png);"
               },
  "margins": {"top": 35, "bottom": 35, "left": 32, "right": 20 },
  "size": [480, 348],
  "chumlabel": { "style": " background:  rgba(255, 255, 0, 0%); color: #FFFCBD; border:0px; font-size: 0px;",
                 "align": { "h": "center", "v": "center" },
                 "minheight": 0,
                 "maxheight": 0,
                 "text" : ""
               },
  "textarea": {
      "style": "background-color: #D0CEE5;  background-image: url(); font: bold; font-size: 14px; font-family: 'Arial'; border:2px solid #6769A8;text-align:center;"
  },
  "input": { "style": "background: #D0CEE5; border:2px solid #6769A8;margin-top:10px; font: bold; font-size: 14px; font-family: 'Arial'" },
  "tabs": {
      "style": "",
      "selectedstyle": "",
      "newmsgcolor": "#F7E430",
      "tabstyle": 0
  },
  "tabwindow" : {
	  "style": "background: #6769A8; font-family: 'Arial'"
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
 {"style": "background-color: rgba(0,0,0,0); border-width: 5px; border-image:url($path/convobg.png) 5px; font-family: 'Arial'; selection-background-color:#919191; ",
  "size": [500,325],
  "tabs": {
      "style": "",
      "selectedstyle": "",
      "newmsgcolor": "#F7E430",
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
             "style": "margin-bottom: 7px; margin-top: 10px; background-color: rgba (0,0,0,0) ; background-image:url($path/nothing.png); color: #FFFCBD; border:0px; font-size: 16px;",
             "align": { "h": "center", "v": "center" },
             "minheight": 47,
             "maxheight": 47
           },
  "input": { "style": "background: #FFFCBD; border:2px solid #F7B53D;margin-top:5px; margin-right:10px; margin-left:10px; font: bold; font-size: 14px; font-family: 'Arial'" },
  "textarea": { "style": " background-color: #FFFCBD; background-image:url();  font: bold; font-size: 14px; font-family: 'Arial'; border:2px solid #F7B53D;text-align:center; margin-right:10px; margin-left:10px;" },
  "margins": {"top": 0, "bottom": 6, "left": 0, "right": 0 },
  "userlist": { "width": 150,
                "style": "border:2px solid #F7B53D; background: #FFFCBD; font-family: 'Arial';selection-background-color:#646464; font-size: 14px;  margin-left:0px; margin-right:10px;"
              },
  "time": { "text": { "width": 75,
                      "style": " border: 2px solid #FFD47C; background: #FFFCBD; font-size: 12px; margin-top: 5px; margin-right: 5px; margin-left: 5px; font-family:'Arial';font:bold;"
                    },
            "slider": { "style": "border: 0px;",
                        "groove": "",
                        "handle": ""
                      },
            "buttons": { "style": "color: black; font: bold; border: 2px solid #F7B53D; font-size: 12px; background: #FFD47C; margin-top: 5px; margin-right: 5px; margin-left: 5px; padding: 2px; width: 50px;" },
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
