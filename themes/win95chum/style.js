{"main":
 {"style": "",
  "background-image": "$path/win95bg.png",
  "size": [300,620],
  "icon": "$path/trayicon.png",
  "newmsgicon": "$path/trayicon2.png",
  "windowtitle": "PESTERCHUM 95",
  "menu" : { "style": "font-family: 'Courier'; font-size: 12px; color: #000000; background-color: #c3c3c3;border:1px solid #000000",
             "menuitem": "margin-right:1px;",
             "selected": "background-color: #ffffff",
             "disabled": "color: grey",
             "loc": [3,21]
           },
	"menubar": { "style": "font-family: 'arial';  font-size: 14px; color: #000000;" },
  "sounds": { "alertsound": "$path/alarm2.wav",
                          "memosound": "$path/alarm2.wav",
                          "ceasesound": "$path/cease.wav" },
   "menus": {"client": {"_name": "            ",
                       "options": "Options",
                       "memos": "Group Messaging",
                       "logviewer": "Message Logs",
                       "randen": "Random Messaging",
                       "userlist": "Users Online",
                       "console": "Console",
	    "talk": "Send Message",
                       "addgroup": "Add Group",
                       "import": "Import",
                       "reconnect": "Reconnect",
                       "idle": "Idle",
                       "exit": "Shutdown"},
            "profile": {"_name": "           ",
                        "switch": "Log Out",
                        "color": "Color",
                        "theme": "Theme",
                        "block": "Block List",
                        "quirks": "Quirks"},
            "help": { "_name": "            ",
                      "about": "About",
                      "help": "Help",
                      "calsprite": "Lil' Cal Buddy",
                      "rules": "Rules",
                      "reportbug": "Report Bug",
	   "chanserv": "Group Moderation",
                      "nickserv": "Nickserv" },
            "rclickchumlist": {"pester": "Message",
                               "removechum": "Unfriend",
                               "report": "Report User",
                               "blockchum": "Block",
                               "addchum": "Add Friend",
                               "viewlog": "View Message Logs",
                               "notes": "Edit Notes",
                               "unblockchum": "Unblock",
                               "removegroup": "Remove Group",
                               "renamegroup": "Rename Group",
                               "movechum": "Move Friend",
                               "banuser": "Ban User",
                               "opuser": "Give Operator",
                               "voiceuser": "Give Voice",
                               "quirkkill": "Kill Quirk",
                               "quirksoff": "Quirks Off",
	            "ooc": "OOC",
                               "invitechum": "Invite",
                               "memosetting": "Group Message Settings",
                               "memonoquirk": "Disable Quirks",
                               "memohidden": "Hidden Group",
                               "memoinvite": "Invite Only Group",
                               "memomute": "Mute Group Message"
                              }
           },
  "close": { "image": "$path/close.png",
             "loc": [279, 5]},
  "minimize": { "image": "$path/minimize.png",
                "loc": [262, 5]},
  "chums": { "style": "background: #c3c3c3 url($path/chumbg.png) repeat-x top left; background-attachment: fixed;border:0px solid dicks;font-size:14px;font-family: 'arial'; color: #000000;",
             "userlistcolor": "black",
				
				
				"loc": [12, 110],
				"size": [278, 339],
				
				

				"moods": {

                 "chummy": { "icon": "$path/chummy.png", "color": "#4AC925" },

                 "rancorous": { "icon": "$path/rancorous.png", "color": "#626262" },

                 "offline": { "icon": "$path/offline.png", "color": "#0000"},


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
      "style": "background: #c3c3c3; border:1px solid #000000; font-family: 'Arial'",
      "size": [195, 200],
      "label": { "text": "Block List",
                 "style": "color: #000000; font-family: 'Arial';border:0px;" },
      "chumroll": {"style": "border:1px solid #000000; background-color: #FFFFFF;color: #000000; font-family: 'Arial';selection-background-color:#FFFFFF; " }
  },
		   
	"mychumhandle": { 
            "handle": { "loc": [40,507],
                    "size": [233, 18],
                    "style": "background: transparent; color: #000000; font-family:'arial'; text-align:left;"
                                                        },
                    "colorswatch": { "loc": [260,504],
                                     "size": [29,25],
                                     "text": " " },
                    "currentMood": [21, 508]
                  },
	"defaultwindow": { "style": "background: #c3c3c3; color:#000000; font-family:arial;selection-background-color:#FFFFFF; "
                   },
				  
  "addchum":  { "style": "background: transparent;",
                "loc": [18,454],
                "size": [90, 44]
              },
  "pester": { "style": "background: transparent;",
              "loc": [108,454],
              "size": [90, 44]
            },
  "block": { "style": "background: transparent;",
             "loc": [198,454],
             "size": [90, 44]
           },
  "defaultmood": 1,
  "moodlabel": { "style": "",
                                 "loc": [20, 430],
                                 "text": ""
                           },   
  "moods": [
      { "style": "text-align:left; background:#c3c3c3; color: #000000; font-family:'arial';  padding-left:3px;",
                "selected": "text-align:left; background: #314159; color: #000000; font-family:'arial';  padding-left:2px;",
                "loc": [18, 535],
                "size": [90, 22],
            "text": "Chummy",
                "icon": "$path/chummy.png",
                "mood": 0
          },

      { "style": "text-align:left; background:#c3c3c3; color: #000000; font-family:'arial';  padding-left:3px;",
                "selected": "text-align:left; background: #314159; color: #000000; font-family:'arial';  padding-left:3px;",
                "loc": [18, 557],
                "size": [90, 22],
            "text": "Pleasant",
                "icon": "$path/pleasant.png",
                "mood": 3
          },

      { "style": "text-align:left; background:#c3c3c3; color: #000000; font-family:'arial';  padding-left:3px;",
                "selected": "text-align:left; background: #314159; color: #000000; font-family:'arial';  padding-left:3px;",
                "loc": [18, 579],
                "size": [90, 22],
            "text": "Rancorous",
                "icon": "$path/rancorous.png",
                "mood": 1
          },

      { "style": "text-align:left; background:#c3c3c3; color: #000000; font-family:'arial';  padding-left:3px;",
                "selected": "text-align:left; background: #314159; color: #000000; font-family:'arial';  padding-left:3px;",
                "loc": [108, 535],
                "size": [90, 22],
            "text": "Pranky",
                "icon": "$path/pranky.png",
                "mood": 5
          },

      { "style": "text-align:left; background:#c3c3c3; color: #000000; font-family:'arial';  padding-left:3px;",
                "selected": "text-align:left; background: #314159; color: #000000; font-family:'arial';  padding-left:3px;",
                "loc": [108, 557],
                "size": [90, 22],
            "text": "Smooth",
                "icon": "$path/smooth.png",
                "mood": 6
          },
		  
      { "style": "text-align:left; background:#c3c3c3; color: #000000; font-family:'arial';  padding-left:3px;",
                "selected": "text-align:left; background: #314159; color: #000000; font-family:'arial';  padding-left:3px;",
                "loc": [108, 579],
                "size": [90, 22],
            "text": "Relaxed",
                "icon": "$path/relaxed.png",
                "mood": 8
          },		  

      { "style": "text-align:left; background:#c3c3c3; color: #000000; font-family:'arial';  padding-left:3px;",
                "selected": "text-align:left; background: #314159; color: #000000; font-family:'arial';  padding-left:3px;",
                "loc": [198, 535],
                "size": [90, 22],
				"text": "Insolent",
                "icon": "$path/insolent.png",
                "mood": 21
          },
		  

      { "style": "text-align:left; background:#c3c3c3; color: #000000; font-family:'arial';  padding-left:3px;",
                "selected": "text-align:left; background: #314159; color: #000000; font-family:'arial';  padding-left:3px;",
                "loc": [198, 557],
                "size": [90, 22],
            "text": "Devious",
                "icon": "$path/devious.png",
                "mood": 10
          },		  
		  
      { "style": "text-align:left; background:#c3c3c3;color: #000000; font-family:'arial'; padding-left:3px;",
                "selected": "text-align:left; background: #314159; color: #000000; font-family:'arial';  padding-left:3px;",
                "loc": [198, 579],
                "size": [90, 22],
                "text": "Abscond",
                "icon": "$path/offline.png",
                "mood": 2
          }
  ]
 },
  "convo":
 {"style": "background: #c3c3c3; font-family: 'Arial'; font-size: 14px; ",
  "scrollbar": { "style" : "background: #c3c3c3", "handle": "" },
  "margins": {"top": 5, "bottom": 9, "left": 10, "right": 10 },
  "size": [500,425],
  "chumlabel": { "style": "font-size: 12px;background-color: #000000; color: #000000; padding-left: 3px;",
                 "align": { "h": "left", "v": "center" },
                 "minheight": 0,
                 "maxheight": 0,
                 "text" : ""
               },
  
  "tabwindow" : {
      "style": "background: #c3c3c3 repeat-x top left; font-family: Courier;"
  },
  "textarea": {
      "style": "background: #FFFFFF repeat-x top left; background-attachment: fixed; border:1px solid #000000; font-size: 14px; color: #000000; margin-top: 10px;"
  },
  "input": {
      "style": "background: #FFFFFF; margin-top:5px; border:1px solid #4d4b48; font-size: 12px; color: #000000; "
  },
  
  "tabs": {
      "style": "background: #4a4846; color: #a6a4a1; height: 21px; margin: 3px 1px 0px 1px; padding-left: 3px; padding-bottom: 3px;",
      "selectedstyle": "background: #a0a0a0 url($path/tabbg.png) repeat-x top left; color: #000000; padding-bottom: 10px",
       "newmsgcolor": "#FFFF00",
       "tabstyle": 0
	   
  },
  "text": {
      "beganpester": "began messaging",
      "ceasepester": "stopped messaging",
      "blocked": "blocked user",
      "unblocked": "unblocked user",
      "openmemo": "connected to group message",
      "joinmemo": "connected to group message",
      "closememo": "disconnected from group message",
      "kickedmemo": "You have been banned from this group message!"
  },
  "systemMsgColor": "#000000"
 },
 "memos":
 {"size": [500,325],
 "memoicon": "$path/trayicon.png",
  "style": "background: #c3c3c3; border:1px solid #000000; color: #000000; font-family: 'Courier';",
  "tabs": {
      "style": "",
      "selectedstyle": "",
       "newmsgcolor": "#42c8f5",
       "tabstyle": 0
	   
  },
    "tabwindow" : {
      "style": "background: #0088ff; color:#000000; font-family: Courier;"
  },

  "scrollbar": { "style" : "background:#000000 transparent; padding-top:17px; padding-bottom:17px;width: 13px; border:0px;",
                 "handle": "background:#c3c3c3 url($path/scrollhandle.png) no-repeat center;min-height:24px;padding-top:1px;padding-bottom:1px;",
                 "downarrow": "background: #c3c3c3;height:17px;",
                 "darrowstyle": "image:url($path/downarrow.png);",
                 "uparrow": "background: #c3c3c3;height:17px;",
                 "uarrowstyle": "image:url($path/uparrow.png);"
               },
  "label": { "text": "Welcome to $channel!",
             "style": "margin-bottom: 21px;background: #000082; color: #FFFFFF; border:0px; font-size: 14px;",
             "align": { "h": "center", "v": "center" },
             "minheight": 47,
             "maxheight": 47
           },
  "input": { "style": "background: #FFFFFF; color: #000000; border:1px solid #4d4b48;margin-top:5px; margin-right:10px; margin-left:10px; font-size: 12px;" },
  "textarea": { "style": "background: #FFFFFF; font-size: 14px; border:1px solid #000000;text-align:center; margin-right:10px; margin-left:10px;" },
  "margins": {"top": 0, "bottom": 6, "left": 0, "right": 0 },
  "userlist": { "width": 150,
                "style": "background: #FFFFFF; border:1px solid #4d4b48; font-size: 14px; color: #000000; selection-background-color:#FFFFFF; margin-left:0px; margin-right:10px;"
              },
  "time": { "text": { "width": 75,
                      "style": "color: #000000; border: 1px solid #000000; background: #FFFFFF; font-size: 12px; margin-top: 5px; margin-right: 11px; margin-left:10px; font-family:'Courier';"
                    },
            "slider": { "style": " border:0px solid #c2c2c2;margin-top:5px;margin-left:6px;",
                        "groove": "border-image:url($path/timeslider.png);",
                        "handle": "image:url($path/handle.png);"
                      },
            "buttons": { "style": "color: #000000;  border: 1px solid #4d4b48;  font-size: 12px; background: #FFFFFF; margin-top: 5px; margin-right: 5px; margin-left: 0px; width: 50px;" },
            "arrows": { "left": "$path/leftarrow.png",
                        "right": "$path/rightarrow.png",
                        "style": " border:0px; margin-top: 5px; margin-right:10px;background: #c3c3c3;"
                      }
          },
  "systemMsgColor": "#000000",
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
   "content": { "style": "background: #c3c3c3; color: black; padding: 5px;" }
 }
}
