{"main":
 {"style": "background-repeat: no-repeat; font-family: 'Courier'; font-size: 14px;",
  "background-image": "$path/ebg.png",
  "size": [810, 555],
  "icon": "$path/trayicon.png",
  "newmsgicon": "$path/trayicon2.png",
  "windowtitle": "Slayerchum",
  "close": { "image": "$path/x.png",
             "loc": [430, 36]},
  "minimize": { "image": "$path/m.png",
                "loc": [440, 40]},
  "menubar": { "style": "font-family: 'Courier'; font: bold; font-size: 14px; color:#000000" },
  "menu" : { "style": "font-family: 'Courier'; font-size: 14px; background-color: #BC000D;border:2px solid #AB6B6B",
             "menuitem": "margin-right:25px;",
             "selected": "background-color: #AB6B6B",
             "loc": [480,30]
           },
  "menus": {"client": {"_name": "Heists",
                       "options": "Options",
                       "memos": "Memos",
                       "logviewer": "Memories",
                       "userlist": "Users",
                       "import": "Import",
                       "reconnect": "Reconnect",
					   "idle": "Idle",
                       "exit": "Exit"},
            "profile": {"_name": "Alias",
                        "switch": "Change",
                        "color": "Colour",
                        "theme": "Theme",
                        "block": "Rivals",
                        "quirks": "Quirks"},
            "help": { "_name": "Assistance",
                      "about": "About!" },
            "rclickchumlist": {"pester": "Meet Up With",
                               "removechum": "Remove Chum",
                               "blockchum": "Stab",
                               "report": "Report",
                               "addchum": "Add Chum",
                               "viewlog": "View Chitty",
                               "unblockchum": "Unblock",
                               "banuser": "Slay User",
                               "opuser": "Make Sidekick",
                               "quirksoff": "No Frills"
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

                 "chummy": { "icon": "$path/chummy.gif", "color": "white" },

                 "rancorous": { "icon": "$path/rancorous.gif", "color": "#007200" },

                 "offline": { "icon": "$path/offline.gif", "color": "#4a4a4a"},

			     
                 "pleasant": { "icon": "$path/pleasant.gif", "color": "white" },

                 "distraught": { "icon": "$path/distraught.gif", "color": "white" },

                 "pranky": { "icon": "$path/pranky.gif", "color": "white" },


                 "smooth": { "icon": "$path/smooth.gif", "color": "white" },

                 "mystified": { "icon": "$path/mystified.gif", "color": "white" },

                 "amazed": { "icon": "$path/amazed.gif", "color": "white" },

                 "insolent": { "icon": "$path/insolent.gif", "color": "white" },

                 "bemused": { "icon": "$path/bemused.gif", "color": "white" },


                 "ecstatic": { "icon": "$path/ecstatic.gif", "color": "#007200" },

                 "relaxed": { "icon": "$path/relaxed.gif", "color": "#007200" },

                 "discontent": { "icon": "$path/discontent.gif", "color": "#007200" },

                 "devious": { "icon": "$path/devious.gif", "color": "#007200" },

                 "sleek": { "icon": "$path/sleek.gif", "color": "#007200" },
			     
                 "detestful": { "icon": "$path/detestful.gif", "color": "#007200" },

                 "mirthful": { "icon": "$path/mirthful.gif", "color": "#007200" },

                 "manipulative": { "icon": "$path/manipulative.gif", "color": "#007200" },

                 "vigorous": { "icon": "$path/vigorous.gif", "color": "#007200" },

                 "perky": { "icon": "$path/perky.gif", "color": "#007200" },

                 "acceptant": { "icon": "$path/acceptant.gif", "color": "#007200" },

                 "protective": { "icon": "$path/protective.png", "color": "#000000" },

                 "blocked": { "icon": "$path/blocked.gif", "color": "#007200" }

             }
           },
  "trollslum": { 
      "style": "background: #BC000D; border:2px solid green; font-family: 'Courier'",
      "size": [195, 200],
      "label": { "text": "MEANIES",
                 "style": "color: rgba(0, 0, 0, 100%) ;font:bold; font-family: 'Courier';border:0px;" },
      "chumroll": {"style": "border:2px solid green; background-color: black;color: #C6FFA9;font: bold;font-family: 'Courier';selection-background-color:#393939; " }
  },
  "mychumhandle": { "label": { "text": "",
                               "loc": [0,0],
                               "style": "color: rgba(130, 230, 80, 0%) ;font:bold; font-family: 'Courier';" },
                    "handle": { "style": "background: rgba(130, 230, 80, 0%); color:#C6FFA9; font-family:'Courier'; font-size:14px; text-align:left;",
                                "loc": [0,0],
                                "size": [0, 0] },
                    "colorswatch": { "loc": [0,0],
                                     "size": [0,0],
                                     "text": "" },
                    "currentMood": [1500, 1500]
                  },
  "defaultwindow": { "style": "background: #BC000D; font-family:'Courier';font:bold;selection-background-color:#919191; " 
                   },
  "addchum":  { "style": "background: rgba(130, 230, 80, 0%); border:0px; color: rgba(0, 0, 0, 0%);",
              "loc": [443,144],
              "size": [284, 60],
                "text": ""
              },
  "pester": { "style": "background:  rgba(130, 230, 80, 0%); border:0px; font: bold; color:  rgba(130, 230, 80, 0%); font-family:'Courier';",
              "pressed" : "background-image:url($path/pesterhold.png);",
                "loc": [0,0],
                "size": [0, 0],
              "text": ""
            },
  "block": { "style": "background:  rgba(130, 230, 80, 0%); border:2px solid #2EC600; font: bold; color:  rgba(130, 230, 80, 0%); font-family:'Courier';",
             "loc": [0,0],
             "size": [0, 0],
             "text": ""
           },
  "defaultmood": 6,
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
 {"style": "background-color: rgba(0, 0, 0, 0%);border-width: 5px; border-image:url($path/convobg.png) 5px; font-family: 'Courier'",
  "tabstyle": "background-color: #BC000D; font-family: 'Courier'",
  "scrollbar": { "style" : "padding-top:17px; padding-bottom:17px;width: 18px; background:  #000000; border:0px;",
                 "handle": "border-width: 5px; border-image:url($path/scrollbg.png) 5px; min-height:60px;",
                 "downarrow": "height:17px;border:0px solid #2EC600;", 
                 "darrowstyle": "image:url($path/downarrow.png);",
                 "uparrow": "height:17px;border:0px solid #2EC600;",
                 "uarrowstyle": "image:url($path/uparrow.png);"
               },
  "margins": {"top": 35, "bottom": 35, "left": 32, "right": 20 },
  "size": [480, 348],
  "chumlabel": { "style": " background:  rgba(199, 0, 0, 0%); color: #000000; border:0px; font-size: 20px;",
                 "align": { "h": "center", "v": "center" },
                 "text" : "$handle"
               },
  "textarea": {
      "style": "background-color: #C6FFA9;  background-image: url(); font: bold; font-size: 14px; font-family: 'Courier'; border:2px solid green;text-align:center;"
  },
  "input": { "style": "background: #CC040B; border:2px solid green;margin-top:10px; font: bold; font-size: 14px; font-family: 'Courier'" },
  "tabs": {
      "style": "border: 2px solid green; background: black; color: white;",
      "selectedstyle": "border: 3px solid green; background: #CC040B; color: black;",
      "newmsgcolor": "#BC000D",
      "tabstyle": 0
  },
  "tabwindow" : {
	  "style": "background: black; font-family: 'Courier'"
  },
  "text": {
      "beganpester": "began pestering",
      "ceasepester": "ceased pestering",
      "blocked": "blocked",
      "unblocked": "unblocked",
	  "blockedmsg": "did not receive message from",
      "openmemo": "looked at",
      "joinmemo": "answered the memo",
      "closememo": "went away from the memo",
      "kickedmemo": "You have been banned from this memo",
	  "idle": "is now an idle chum"
  },
  "systemMsgColor": "#393939"
 },
 "memos":
 {"memoicon": "$path/memo.png",
  "style": "background-color: rgba(0,0,0,0); border-width: 5px; border-image:url($path/convobg.png) 5px; font-family: 'Courier'; selection-background-color:#919191; ",
  "size": [500,325],
  "tabs": {
      "style": "border: 2px solid green; background: black; color: white;",
      "selectedstyle": "border: 3px solid green; background: #CC040B; color: black;",
      "newmsgcolor": "#BC000D",
      "tabstyle": 0
  },
  "scrollbar": { "style" : "padding-top:17px; padding-bottom:17px;width: 18px; background:  #000000; border:0px;",
                 "handle": "border-width: 5px; border-image:url($path/scrollbg.png) 5px; min-height:60px;",
                 "downarrow": "height:17px;border:0px;", 
                 "darrowstyle": "image:url();",
                 "uparrow": "height:17px;border:0px;",
                 "uarrowstyle": "image:url();"
               },
  "label": { "text": "Bulletin Board: $channel",
             "style": "margin-bottom: 7px; margin-top: 10px; background-color: #C70000 ; background-image:url($path/nothing.png); color: #000000; border:0px; font-size: 16px;",
             "align": { "h": "center", "v": "center" },
             "minheight": 47,
             "maxheight": 47
           },
  "input": { "style": "background: #CC040B; border:2px solid #2EC600;margin-top:5px; margin-right:10px; margin-left:10px; font: bold; font-size: 14px; font-family: 'Courier'" },
  "textarea": { "style": " background-color: #C6FFA9; background-image:url();  font: bold; font-size: 14px; font-family: 'Courier'; border:2px solid #2EC600;text-align:center; margin-right:10px; margin-left:10px;" },
  "margins": {"top": 0, "bottom": 6, "left": 0, "right": 0 },
  "userlist": { "width": 150,
                "style": "border:2px solid #B73A3E; background: #CC040B; font-family: 'Courier';selection-background-color:#393939; font-size: 14px;  margin-left:0px; margin-right:10px;"
              },
  "time": { "text": { "width": 75, 
                      "style": " border: 2px solid green; background: #CC040B; font-size: 12px; margin-top: 5px; margin-right: 5px; margin-left: 5px; font-family:'Courier';font:bold;" 
                    },
            "slider": { "style": "border: 0px;",
                        "groove": "",
                        "handle": ""
                      },
            "buttons": { "style": "color: black; font: bold; border: 2px solid green; font-size: 12px; background: #CC040B; margin-top: 5px; margin-right: 5px; margin-left: 5px; padding: 2px; width: 50px;" }, 
            "arrows": { "left": "$path/leftarrow.png", 
                        "right": "$path/rightarrow.png",
                        "style": " border:0px; margin-top: 5px; margin-right:10px;" 
                      }
          },
  "systemMsgColor": "#393939",
  "op": { "icon": "$path/smooth.png" }
 }
}