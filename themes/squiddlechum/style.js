{"main":
 {"style": "background-repeat: no-repeat; font-family: Arial; font-size: 14px;",
  "background-image": "$path/gbg2.png",
  "size": [333, 290],
  "icon": "$path/trayicon.png",
  "newmsgicon": "$path/trayicon2.png",
  "windowtitle": "Tanglechum",
  "close": { "image": "$path/x.png",
             "loc": [315, 26]},
  "minimize": { "image": "$path/m.png",
                "loc": [300, 28]},
  "menubar": { "style": "font-family: 'Arial'; font:bold; font-size: 12px;" },
  "menu" : { "style": "font-family: 'Arial'; font: bold; font-size: 12px; background-color: #E8B8E5;border:2px solid #B9D7FF",
             "menuitem": "margin-right:15px;",
             "selected": "background-color: #B9D7FF",
             "loc": [150,22]
           },
  "sounds": { "alertsound": "$path/alarm.wav",
			  "ceasesound": "$path/cease.wav" },
  "menus": {"client": {"_name": "Client",
                       "options": "Options",
                       "memos": "Memos",
                       "logviewer": "Pesterlogs",
                       "userlist": "Userlist",
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
                      "about": "About" },
            "rclickchumlist": {"pester": "Pester",
                               "removechum": "Remove Chum",
                               "report": "Report",
                               "blockchum": "Block",
                               "addchum": "Add Chum",
                               "viewlog": "View Pesterlog",
                               "unblockchum": "Unblock",
                               "banuser": "Ban User",
                               "opuser": "Make OP",
                               "quirksoff": "Quirks Off"
                              }
           },
  "chums": { "style": "border:0px; background-color: rgb(184,136,232); background-repeat: no-repeat; color: #FFD0FA; font-family: 'Arial';selection-background-color:#646464; font-size:14px; ",
             "loc": [123, 88],
             "size": [190, 65],
             "userlistcolor": "#FFD0FA",
             "moods": { 

                 "chummy": { "icon": "$path/chummy.png", "color": "#FFD0FA" },

                 "rancorous": { "icon": "$path/rancorous.png", "color": "#CE5D5D" },

                 "offline": { "icon": "$path/offline.png", "color": "#bebebe"},

			     
                 "pleasant": { "icon": "$path/pleasant.png", "color": "#FFD0FA" },

                 "distraught": { "icon": "$path/distraught.png", "color": "#FFD0FA" },

                 "pranky": { "icon": "$path/pranky.png", "color": "#FFD0FA" },


                 "smooth": { "icon": "$path/smooth.png", "color": "#FFD0FA" },

                 "mystified": { "icon": "$path/mystified.png", "color": "#FFD0FA" },

                 "amazed": { "icon": "$path/amazed.png", "color": "#FFD0FA" },

                 "insolent": { "icon": "$path/insolent.png", "color": "#FFD0FA" },

                 "bemused": { "icon": "$path/bemused.png", "color": "#FFD0FA" },


                 "ecstatic": { "icon": "$path/ecstatic.png", "color": "#CE5D5D" },

                 "relaxed": { "icon": "$path/relaxed.png", "color": "#CE5D5D" },

                 "discontent": { "icon": "$path/discontent.png", "color": "#CE5D5D" },

                 "devious": { "icon": "$path/devious.png", "color": "#CE5D5D" },

                 "sleek": { "icon": "$path/sleek.png", "color": "#CE5D5D" },
			     
                 "detestful": { "icon": "$path/detestful.png", "color": "#CE5D5D" },

                 "mirthful": { "icon": "$path/mirthful.png", "color": "#CE5D5D" },

                 "manipulative": { "icon": "$path/manipulative.png", "color": "#CE5D5D" },

                 "vigorous": { "icon": "$path/vigorous.png", "color": "#CE5D5D" },

                 "perky": { "icon": "$path/perky.png", "color": "#CE5D5D" },

                 "acceptant": { "icon": "$path/acceptant.png", "color": "#CE5D5D" },

                 "protective": { "icon": "$path/protective.png", "color": "#00ff00" },

                 "blocked": { "icon": "$path/blocked.png", "color": "black" }

             }
           },
  "trollslum": { 
      "style": "background: #E8B8E5; border:2px solid #DFFACC; font-family: 'Arial'",
      "size": [195, 200],
      "label": { "text": "TROLLSLUM",
                 "style": "color: rgba(0, 0, 0, 100%) ;font:bold; font-family: 'Arial';border:0px;" },
      "chumroll": {"style": "border:2px solid #DFFACC; background-color: black;color: #FFD0FA;font: bold;font-family: 'Arial';selection-background-color:#646464; " }
  },
  "mychumhandle": { "label": { "text": "CHUMHANDLE:",
                               "loc": [0,0],
                               "style": "color: rgba(255, 255, 202, 0%) ;font:bold; font-family: 'Arial';" },
                    "handle": { "style": "background: rgba(255, 255, 202, 0%); color:#FFD0FA; font-family:'Arial'; font-size:14px; text-align:left;",
                                "loc": [157,170],
                                "size": [191, 26] },
                    "colorswatch": { "loc": [0,0],
                                     "size": [0,0],
                                     "text": "" },
                    "currentMood": [129, 176]
                  },
  "defaultwindow": { "style": "background: #E8B8E5; font-family:'Arial';font:bold;selection-background-color:#919191; " 
                   },
  "addchum":  { "style": "background: rgba(255, 255, 202, 0%); border:0px; color: rgba(0, 0, 0, 0%);",
              "loc": [25,0],
              "size": [69, 70],
                "text": ""
              },
  "pester": { "style": "background:  rgba(255, 255, 202, 0%); border:0px; font: bold; color:  rgba(255, 255, 202, 0%); font-family:'Arial';",
              "pressed" : "background-image:url($path/pesterhold.png);",
                "loc": [15,83],
                "size": [95, 75],
              "text": ""
            },
  "block": { "style": "background:  rgba(255, 255, 202, 0%); border:2px solid #00B2C6; font: bold; color:  rgba(255, 255, 202, 0%); font-family:'Arial';",
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
 {"style": "background-color: rgba(0, 0, 0, 0%);border-width: 5px; border-image:url($path/convobg2.png) 5px; font-family: 'Arial'",
  "tabstyle": "background-color: #E8B8E5; font-family: 'Arial'",
  "scrollbar": { "style" : "padding-top:17px; padding-bottom:17px;width: 18px; background:  rgba(255, 255, 202, 0%); border:0px;",
                 "handle": "background-color:#00B2C6;min-height:20px;",
                 "downarrow": "height:17px;border:0px solid #00B2C6;", 
                 "darrowstyle": "image:url($path/downarrow.png);",
                 "uparrow": "height:17px;border:0px solid #00B2C6;",
                 "uarrowstyle": "image:url($path/uparrow.png);"
               },
  "margins": {"top": 0, "bottom": 6, "left": 0, "right": 0 },
  "size": [500, 325],
  "chumlabel": { "style": "margin-bottom: 7px; margin-top: 10px; background:  rgba(255, 255, 202, 0%); color: #7FAACB; border:0px; font-size: 16px;",
                 "align": { "h": "center", "v": "center" },
                 "minheight": 47,
                 "maxheight": 47,
                 "text" : ":: $handle ::"
               },
  "textarea": {
      "style": "background: #FFD0FA;  font-size: 14px; border:2px solid #00B2C6;text-align:center; margin-right:10px; margin-left:10px; margin-bottom:5px;"
  },
  "input": {
      "style": "background: #FFD0FA; border:2px solid #00B2C6; margin-right:10px; margin-left:10px; font-size: 14px; height: 20px"
  },
  "tabwindow" : {
	  "style": "background: #B8C2E9; font-family: 'Arial'"
  },
  "tabs": {
      "style": "",
      "selectedstyle": "",
      "newmsgcolor": "#E8B8E5",
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
  "style": "background-color: rgba(0,0,0,0); background-image:url($path/convobg2.png); background-repeat: no-repeat; border:0px; font-family: 'Arial'; selection-background-color:#919191; ",
  "size": [500,325],
  "tabs": {
      "style": "",
      "selectedstyle": "",
      "newmsgcolor": "#E8B8E5",
      "tabstyle": 0
  },
  "scrollbar": { "style" : "padding-top:17px; padding-bottom:17px;width: 18px; background:  rgba(255, 255, 202, 0%); border:0px;",
                 "handle": "background-color:#00B2C6;min-height:20px;",
                 "downarrow": "height:17px;border:0px solid #00B2C6;", 
                 "darrowstyle": "image:url($path/downarrow.png);",
                 "uparrow": "height:17px;border:0px solid #00B2C6;",
                 "uarrowstyle": "image:url($path/uparrow.png);"
               },
  "label": { "text": "Bulletin Board: $channel",
             "style": "margin-bottom: 7px; margin-top: 10px; background:  rgba(255, 255, 202, 0%); color: #81CD97; border:0px; font-size: 16px;",
             "align": { "h": "center", "v": "center" },
             "minheight": 47,
             "maxheight": 47
           },
  "input": { "style": "background: #FFD0FA; border:2px solid #00B2C6;margin-top:5px; margin-right:10px; margin-left:10px; font-size: 14px;" },
  "textarea": { "style": "background: #FFD0FA;  font-size: 14px; border:2px solid #00B2C6;text-align:center; margin-right:10px; margin-left:10px;" },
  "margins": {"top": 0, "bottom": 6, "left": 0, "right": 0 },
  "userlist": { "width": 150,
                "style": "border:2px solid #00B2C6; background: #FFD0FA; font-family: 'Arial';selection-background-color:#646464; font-size: 14px;  margin-left:0px; margin-right:10px;"
              },
  "time": { "text": { "width": 75, 
                      "style": " border: 2px solid #DFFACC; background: #FFD0FA; font-size: 12px; margin-top: 5px; margin-right: 5px; margin-left: 5px; font-family:'Arial';font:bold;" 
                    },
            "slider": { "style": "border: 0px;",
                        "groove": "",
                        "handle": ""
                      },
            "buttons": { "style": "color: black; font: bold; border: 2px solid #00B2C6; font-size: 12px; background: #DFFACC; margin-top: 5px; margin-right: 5px; margin-left: 5px; padding: 2px; width: 50px;" }, 
            "arrows": { "left": "$path/leftarrow.png", 
                        "right": "$path/rightarrow.png",
                        "style": " border:0px; margin-top: 5px; margin-right:10px;" 
                      }
          },
  "systemMsgColor": "#646464",
  "op": { "icon": "$path/smooth.png" }
 }
}