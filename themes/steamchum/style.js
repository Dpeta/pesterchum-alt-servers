{"main":
 {"style": "",
  "background-image": "$path/steambg.png",
  "size": [300,620],
  "icon": "$path/trayicon.png",
  "newmsgicon": "$path/trayicon2.png",
  "windowtitle": "STEAMCHUM",
  "menu" : { "style": "font-family: 'arial'; font-size: 12px; color: #bebdb7; background-color: #3d3b3a;border:1px solid #4d4b48",
             "menuitem": "margin-right:10px;",
             "selected": "background-color: #314159",
             "disabled": "color: grey",
             "loc": [9,10]
           },
	"menubar": { "style": "font-family: 'arial';  font-size: 14px; color: #000000;" },
   "menus": {"client": {"_name": "            ",
                       "options": "Options",
                       "memos": "Community",
                       "logviewer": "Library",
                       "randen": "Random Encounter",
                       "userlist": "Userlist",
                       "addgroup": "Add Group",
                       "import": "Import",
                       "reconnect": "Reconnect",
                       "idle": "Idle",
                       "exit": "Log Off"},
            "profile": {"_name": "           ",
                        "switch": "Switch",
                        "color": "Color",
                        "theme": "Theme",
                        "block": "Block List",
                        "quirks": "Quirks"},
            "help": { "_name": "            ",
                      "about": "About",
                      "help": "Help",
                      "calsprite": "Calsprite",
                      "nickserv": "Nickserv" },
            "rclickchumlist": {"pester": "Message",
                               "removechum": "Remove",
                               "report": "Report",
                               "blockchum": "Block",
                               "addchum": "Add",
                               "viewlog": "View Pesterlogs",
                               "notes": "Edit Notes",
                               "unblockchum": "Unblock",
                               "removegroup": "Remove Group",
                               "renamegroup": "Rename Group",
                               "movechum": "Move",
                               "banuser": "Ban",
                               "opuser": "Give OP",
                               "voiceuser": "Give Voice",
                               "quirkkill": "Kill Quirk",
                               "quirksoff": "Quirks Off",
							   "ooc": "OOC",
                               "invitechum": "Invite",
                               "memosetting": "Memo Settings",
                               "memonoquirk": "Disable Quirks",
                               "memohidden": "Hidden",
                               "memoinvite": "Invite Only",
                               "memomute": "Mute Memo"
                              }
           },
  "close": { "image": "$path/m.png",
             "loc": [278, 9]},
  "minimize": { "image": "$path/m.png",
                "loc": [262, 9]},
  "chums": { "style": "background: #151515 url($path/chumbg.png) repeat-x top left; background-attachment: fixed;border:0px solid dicks;font-size:14px;font-family: 'arial'; color: #e5e2df",
				
				
				"loc": [12, 110],
				"size": [278, 339],
				
				

				"moods": {

                 "chummy": { "icon": "$path/chummy.png", "color": "#4AC925" },

                 "rancorous": { "icon": "$path/rancorous.png", "color": "#626262" },

                 "offline": { "icon": "$path/offline.png", "color": "#f3f3f3"},


                 "pleasant": { "icon": "$path/pleasant.png", "color": "#B536DA" },

                 "distraught": { "icon": "$path/distraught.png", "color": "#B536DA" },

                 "pranky": { "icon": "$path/pranky.png", "color": "#0715cd" },


                 "smooth": { "icon": "$path/smooth.png", "color": "#E00707" },

                 "mystified": { "icon": "$path/mystified.png", "color": "#B536DA" },

                 "amazed": { "icon": "$path/amazed.png", "color": "#4AC925" },

                 "insolent": { "icon": "$path/insolent.png", "color": "#4AC925" },

                 "bemused": { "icon": "$path/bemused.png", "color": "#4AC925" },


                 "ecstatic": { "icon": "$path/ecstatic.png", "color": "#77003C" },

                 "relaxed": { "icon": "$path/relaxed.png", "color": "#008141" },

                 "discontent": { "icon": "$path/discontent.png", "color": "#A15000" },

                 "devious": { "icon": "$path/devious.png", "color": "#008282" },

                 "sleek": { "icon": "$path/sleek.png", "color": "#A1A100" },

                 "detestful": { "icon": "$path/detestful.png", "color": "#6A006A" },

                 "mirthful": { "icon": "$path/mirthful.png", "color": "#2B0057" },

                 "manipulative": { "icon": "$path/manipulative.png", "color": "#005682" },

                 "vigorous": { "icon": "$path/vigorous.png", "color": "#000056" },

                 "perky": { "icon": "$path/perky.png", "color": "#436600" },

                 "acceptant": { "icon": "$path/acceptant.png", "color": "#A10000" },

                 "protective": { "icon": "$path/protective.png", "color": "#00ff00" },

                 "blocked": { "icon": "$path/blocked.png", "color": "red" }
                         }
						 
           },
		   
  "trollslum": {
      "style": "background: #363636; border:1px solid #4d4b48; font-family: 'Arial'",
      "size": [195, 200],
      "label": { "text": "Block List",
                 "style": "color: #bebdb7; font-family: 'Arial';border:0px;" },
      "chumroll": {"style": "border:1px solid #4d4b48; background-color: #363636;color: bebdb7; font-family: 'Arial';selection-background-color:#314159; " }
  },
		   
	"mychumhandle": { 
            "handle": { "loc": [40,507],
                    "size": [233, 18],
                    "style": "background: transparent; color: #a8a8a8; font-family:'arial'; text-align:left;"
                                                        },
                    "colorswatch": { "loc": [262,507],
                                     "size": [25,20],
                                     "text": "C" },
                    "currentMood": [21, 508]
                  },
	"defaultwindow": { "style": "background: #363636; color: #e5e2df; font-family:arial;selection-background-color:#314159; "
                   },
				  
  "addchum":  { "style": "background: transparent;",
                "loc": [19,462],
                "size": [102, 17]
              },
  "pester": { "style": "background:  transparent;",
              "loc": [0,0],
              "size": [0, 0]
            },
  "block": { "style": "background: transparent;",
             "loc": [172,462],
             "size": [105, 17]
           },
  "defaultmood": 1,
  "moodlabel": { "style": "",
                                 "loc": [20, 430],
                                 "text": ""
                           },   
  "moods": [
      { "style": "text-align:left; background:#363636; color: #d1cfcd; font-family:'arial';  padding-left:3px;",
                "selected": "text-align:left; background: #314159; color: #d1cfcd; font-family:'arial';  padding-left:3px;",
                "loc": [17, 537],
                "size": [80, 18],
            "text": "Chummy",
                "icon": "$path/chummy.png",
                "mood": 0
          },

      { "style": "text-align:left; background:#363636; color: #d1cfcd; font-family:'arial';  padding-left:3px;",
                "selected": "text-align:left; background: #314159; color: #d1cfcd; font-family:'arial';  padding-left:3px;",
                "loc": [17, 559],
                "size": [80, 18],
            "text": "Pleasant",
                "icon": "$path/pleasant.png",
                "mood": 3
          },

      { "style": "text-align:left; background:#363636; color: #d1cfcd; font-family:'arial';  padding-left:3px;",
                "selected": "text-align:left; background: #314159; color: #d1cfcd; font-family:'arial';  padding-left:3px;",
                "loc": [17, 581],
                "size": [80, 18],
            "text": "Rancorous",
                "icon": "$path/rancorous.png",
                "mood": 1
          },

      { "style": "text-align:left; background:#363636; color: #d1cfcd; font-family:'arial';  padding-left:3px;",
                "selected": "text-align:left; background: #314159; color: #d1cfcd; font-family:'arial';  padding-left:3px;",
                "loc": [110, 537],
                "size": [90, 18],
            "text": "Pranky",
                "icon": "$path/pranky.png",
                "mood": 5
          },

      { "style": "text-align:left; background:#363636; color: #d1cfcd; font-family:'arial';  padding-left:3px;",
                "selected": "text-align:left; background: #314159; color: #d1cfcd; font-family:'arial';  padding-left:3px;",
                "loc": [110, 559],
                "size": [90, 18],
            "text": "Smooth",
                "icon": "$path/smooth.png",
                "mood": 6
          },
		  
      { "style": "text-align:left; background:#363636; color: #d1cfcd; font-family:'arial';  padding-left:3px;",
                "selected": "text-align:left; background: #314159; color: #d1cfcd; font-family:'arial';  padding-left:3px;",
                "loc": [110, 581],
                "size": [90, 18],
            "text": "Relaxed",
                "icon": "$path/relaxed.png",
                "mood": 8
          },		  

      { "style": "text-align:left; background:#363636; color: #d1cfcd; font-family:'arial';  padding-left:3px;",
                "selected": "text-align:left; background: #314159; color: #d1cfcd; font-family:'arial';  padding-left:3px;",
                "loc": [190, 537],
                "size": [90, 18],
				"text": "Insolent",
                "icon": "$path/insolent.png",
                "mood": 21
          },
		  

      { "style": "text-align:left; background:#363636; color: #d1cfcd; font-family:'arial';  padding-left:3px;",
                "selected": "text-align:left; background: #314159; color: #d1cfcd; font-family:'arial';  padding-left:3px;",
                "loc": [190, 559],
                "size": [90, 18],
            "text": "Devious",
                "icon": "$path/devious.png",
                "mood": 10
          },		  
		  
      { "style": "text-align:left; background:black;color: #6c757c; font-family:'arial'; padding-left:3px;",
                "selected": "text-align:left; background: #314159; color: #d1cfcd; font-family:'arial';  padding-left:3px;",
                "loc": [190, 581],
                "size": [90, 18],
                "text": "Abscond",
                "icon": "$path/offline.png",
                "mood": 2
          }
  ]
 },
  "convo":
 {"style": "background: #383635; font-family: 'Arial'; font-size: 14px; ",
  "scrollbar": { "style" : "", "handle": "" },
  "margins": {"top": 5, "bottom": 9, "left": 10, "right": 10 },
  "size": [500,425],
  "chumlabel": { "style": "font-size: 12px;background-color: #383635; color: #86b5d9; padding-left: 3px;",
                 "align": { "h": "left", "v": "center" },
                 "minheight": 0,
                 "maxheight": 0,
                 "text" : ""
               },
  
  "tabwindow" : {
      "style": "background: #1b1a19 url($path/othertabbg.png) repeat-x top left; font-family: Arial;"
  },
  "textarea": {
      "style": "background: #171614 url($path/textbg.png) repeat-x top left; background-attachment: fixed; border:1px solid #4d4b48; font-size: 14px; color: #cdcdcd; margin-top: 10px;"
  },
  "input": {
      "style": "background: #383635; margin-top:5px; border:1px solid #4d4b48; font-size: 12px; color: #cdcdcd; "
  },
  
  "tabs": {
      "style": "background: #4a4846; color: #a6a4a1; height: 21px; margin: 3px 1px 0px 1px; padding-left: 3px; padding-bottom: 3px;",
      "selectedstyle": "background: #1b1a19 url($path/tabbg.png) repeat-x top left; color: #f7fffd; padding-bottom: 10px",
       "newmsgcolor": "#FF724C",
       "tabstyle": 0
	   
  },
  "text": {
      "beganpester": "began messaging",
      "ceasepester": "stopped messaging",
      "blocked": "blocked",
      "unblocked": "mercifully forgave",
      "openmemo": "opened memo on board",
      "joinmemo": "responded to memo",
      "closememo": "ceased responding to memo",
      "kickedmemo": "You have been banned from this memo!"
  },
  "systemMsgColor": "#d1cfcd"
 },
 "memos":
 {"size": [500,325],
 "memoicon": "$path/memo.png",
  "style": "background: #383635; border:1px solid #4d4b48; font-family: 'arial';",
  "tabs": {
      "style": "",
      "selectedstyle": "",
       "newmsgcolor": "#FF724C",
       "tabstyle": 0
	   
  },
    "tabwindow" : {
      "style": "background: #383635; font-family: Arial;"
  },

  "scrollbar": { "style" : "background: transparent; padding-top:17px; padding-bottom:17px;width: 13px; border:0px;",
                 "handle": "background:#5e5b58 url($path/scrollhandle.png) no-repeat center center;min-height:24px;padding-top:1px;padding-bottom:1px;",
                 "downarrow": "background: #1b1a19;height:17px;",
                 "darrowstyle": "image:url($path/downarrow.png);",
                 "uparrow": "background: #1b1a19;height:17px;",
                 "uarrowstyle": "image:url($path/uparrow.png);"
               },
  "label": { "text": "Bulletin Board: $channel",
             "style": "margin-bottom: 21px;background: #383635; color: #7db5d9; border:0px; font-size: 14px;",
             "align": { "h": "center", "v": "center" },
             "minheight": 47,
             "maxheight": 47
           },
  "input": { "style": "background: #1b1a19; color: #cdcdcd; border:1px solid #4d4b48;margin-top:5px; margin-right:10px; margin-left:10px; font-size: 12px;" },
  "textarea": { "style": "background: #383635; font-size: 14px; border:1px solid #4d4b48;text-align:center; margin-right:10px; margin-left:10px;" },
  "margins": {"top": 0, "bottom": 6, "left": 0, "right": 0 },
  "userlist": { "width": 150,
                "style": "background: #383635; border:1px solid #4d4b48; font-size: 14px; color: #cdcdcd; selection-background-color:#646464; margin-left:0px; margin-right:10px;"
              },
  "time": { "text": { "width": 75,
                      "style": "color: #818181; border: 1px solid #4d4b48; background: #1b1a19; font-size: 12px; margin-top: 5px; margin-right: 18px; font-family:'arial';"
                    },
            "slider": { "style": " border:0px solid #c2c2c2;margin-top:3px;",
                        "groove": "border-image:url($path/timeslider.png);",
                        "handle": "image:url($path/handle.png);"
                      },
            "buttons": { "style": "color: #818181;  border: 1px solid #4d4b48;  font-size: 12px; background: #1b1a19; margin-top: 5px; margin-right: 5px; margin-left: 0px; width: 50px;" },
            "arrows": { "left": "$path/leftarrow.png",
                        "right": "$path/rightarrow.png",
                        "style": " border:0px; margin-top: 5px; margin-right:10px;background: #1b1a19;"
                      }
          },
  "systemMsgColor": "#d1cfcd",
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