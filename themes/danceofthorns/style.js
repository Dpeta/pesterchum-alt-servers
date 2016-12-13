{"inherits": "pesterchum2.5",
 "main":
 {"background-image": "$path/lordthorn.png",
  "size": [513,749],
  "icon": "$path/trayicon.png",
  "newmsgicon": "$path/trayicon2.png",
  "windowtitle": "Terrorchum",
  "menu" : { "style": "font-family: 'Verdana'; font-size: 14px; font: bold; color: black; background-color: #A78DB3; border:2px solid #B969D7;",
             "selected": "background-color: #AE6BB9",
             "menuitem": "margin-right:14px;",
             "loc": [49,59]},
  "menubar": { "style": "font-family: 'Verdana'; font:bold; font-size: 14px; color:#FFFFFF; align:center;" },
  "menus": {"client": {"_name": "Client",
                       "options": "Options",
                       "memos": "Cults",
                       "logviewer": "Grimoires",
                       "userlist": "Followers",
                       "import": "Import",
                       "reconnect": "Return",
					   "idle": "Sleep",
                       "exit": "Exit"},
            "profile": {"_name": "Profile",
                        "switch": "Change",
                        "color": "Colour",
                        "theme": "Style",
                        "block": "Demons",
                        "quirks": "Quirks"},
            "help": { "_name": "Help",
                      "about": "About" },
            "rclickchumlist": {"pester": "Manifest",
                               "removechum": "Remove Chum",
                               "blockchum": "Block",
                               "report": "Accuse",
                               "addchum": "Add Buddy",
                               "viewlog": "Peruse Tome",
                               "unblockchum": "Unblock",
                               "banuser": "Ban User",
                               "opuser": "Make OP",
                               "quirksoff": "Unfog Speech"
                              }
           },
  "close": { "image": "$path/x.png",
             "loc": [303, 62]},
  "minimize": { "image": "$path/m.png",
                "loc": [290, 62]},
  "sounds": { "alertsound": "$path/alarm.wav",
			  "ceasesound": "$path/cease.wav" },
  "defaultwindow": { "style": "background: #A78DB3; font-family:'Verdana';font:bold;selection-background-color:black; " },
  "chums": { "style": "border:2px solid #000000; background-color: #B38DB2;color: #581883;font: bold;font-size:14px;font-family: 'Verdana';selection-background-color:black; ",
             "loc": [42, 101],
             "moods": { 

                 "chummy": { "icon": "$path/chummy.png", "color": "#DA79F7" },

                 "rancorous": { "icon": "$path/rancorous.png", "color": "#470045" },

                 "offline": { "icon": "$path/offline.png", "color": "#542A69"},

			     
                 "pleasant": { "icon": "$path/pleasant.png", "color": "#DA79F7" },

                 "distraught": { "icon": "$path/distraught.png", "color": "#DA79F7" },

                 "pranky": { "icon": "$path/pranky.png", "color": "#DA79F7" },


                 "smooth": { "icon": "$path/smooth.png", "color": "#DA79F7" },

                 "mystified": { "icon": "$path/mystified.png", "color": "#DA79F7" },

                 "amazed": { "icon": "$path/amazed.png", "color": "#DA79F7" },

                 "insolent": { "icon": "$path/insolent.png", "color": "#DA79F7" },

                 "bemused": { "icon": "$path/bemused.png", "color": "#DA79F7" },


                 "ecstatic": { "icon": "$path/ecstatic.png", "color": "#470045" },

                 "relaxed": { "icon": "$path/relaxed.png", "color": "#470045" },

                 "discontent": { "icon": "$path/discontent.png", "color": "#470045" },

                 "devious": { "icon": "$path/devious.png", "color": "#470045" },

                 "sleek": { "icon": "$path/sleek.png", "color": "#470045" },
			     
                 "detestful": { "icon": "$path/detestful.png", "color": "#470045" },

                 "mirthful": { "icon": "$path/mirthful.png", "color": "#470045" },

                 "manipulative": { "icon": "$path/manipulative.png", "color": "#470045" },

                 "vigorous": { "icon": "$path/vigorous.png", "color": "#470045" },

                 "perky": { "icon": "$path/perky.png", "color": "#470045" },

                 "acceptant": { "icon": "$path/acceptant.png", "color": "#470045" },

                 "protective": { "icon": "$path/protective.png", "color": "#672770" },

                 "blocked": { "icon": "$path/blocked.png", "color": "black" }
			 }
		   },

  "mychumhandle": { "label": { "text": "",
                               "loc": [42,440],
                               "style": "color: #DA79F7 ;font:bold; font-family: 'Verdana';" },
                    "handle": { "style": "background: black; padding: 3px; padding-left: 25px; color: #B969D7; font-family:'Verdana'; font: bold; text-align:left; font-size: 12px; border: 2px solid #A78DB3;",
                                "loc": [42,440],
                                "size": [202, 25]},
                    "colorswatch": { "loc": [252,442],
                                     "size": [22,21],
                                     "text": "" },
                    "currentMood": [46, 444]
                  },
  "addchum":  { "text": "SUMMON", "style": "background: black; border:2px solid #B969D7; font: bold; color: #A78DB3; font-family:'Verdana';",
        "loc": [42, 403]},
  "pester": { "text": "PEST'R", "style": "background: black; border:2px solid #B969D7; font: bold; color: #A78DB3; font-family:'Verdana';",
        "loc": [132, 403]},
  "block": { "text": "BANISH", "style": "background: black; border:2px solid #B969D7; font: bold; color: #A78DB3; font-family:'Verdana';",
        "loc": [221, 403]},
  "moodlabel": { "style": "",
                 "text": ""
			   },
  "defaultmood": 18,
  "moods": [
      { "style": "text-align:left; background:#A78DB3;border:2px solid black;color: black; font-family:'Verdana'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#8A6B94; border:2px solid #B969D7; color: black; font-family:'Verdana'; font:bold; padding-left:3px;",
		"loc": [45, 485],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/chummy.png",
		"mood": 0
	  },
      { "style": "text-align:left; background:#A78DB3;border:2px solid black;color: black; font-family:'Verdana'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#8A6B94; border:2px solid #B969D7; color: black; font-family:'Verdana'; font:bold; padding-left:3px;",
		"loc": [75, 485],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/rancorous.png",
		"mood": 1
	  },
      { "style": "text-align:left; background:#A78DB3;border:2px solid black;color: black; font-family:'Verdana'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#8A6B94; border:2px solid #B969D7; color: black; font-family:'Verdana'; font:bold; padding-left:3px;",
		"loc": [105, 485],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/bemused.png",
		"mood": 22
	  },
      { "style": "text-align:left; background:#A78DB3;border:2px solid black;color: black; font-family:'Verdana'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#8A6B94; border:2px solid #B969D7; color: black; font-family:'Verdana'; font:bold; padding-left:3px;",
		"loc": [135, 485],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/pleasant.png",
		"mood": 3
	  },
      { "style": "text-align:left; background:#A78DB3;border:2px solid black;color: black; font-family:'Verdana'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#8A6B94; border:2px solid #B969D7; color: black; font-family:'Verdana'; font:bold; padding-left:3px;",
		"loc": [165, 485],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/distraught.png",
		"mood": 4
	  },
      { "style": "text-align:left; background:#A78DB3;border:2px solid black;color: black; font-family:'Verdana'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#8A6B94; border:2px solid #B969D7; color: black; font-family:'Verdana'; font:bold; padding-left:3px;",
		"loc": [195, 485],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/pranky.png",
		"mood": 5
	  },
      { "style": "text-align:left; background:#A78DB3;border:2px solid black;color: black; font-family:'Verdana'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#8A6B94; border:2px solid #B969D7; color: black; font-family:'Verdana'; font:bold; padding-left:3px;",
		"loc": [45, 515],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/smooth.png",
		"mood": 6
	  },
      { "style": "text-align:left; background:#A78DB3;border:2px solid black;color: black; font-family:'Verdana'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#8A6B94; border:2px solid #B969D7; color: black; font-family:'Verdana'; font:bold; padding-left:3px;",
		"loc": [105, 545],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/estatic.png",
		"mood": 7
	  },

      { "style": "text-align:left; background:#A78DB3;border:2px solid black;color: black; font-family:'Verdana'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#8A6B94; border:2px solid #B969D7; color: black; font-family:'Verdana'; font:bold; padding-left:3px;",
		"loc": [75, 545],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/relaxed.png",
		"mood": 8
	  },

      { "style": "text-align:left; background:#A78DB3;border:2px solid black;color: black; font-family:'Verdana'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#8A6B94; border:2px solid #B969D7; color: black; font-family:'Verdana'; font:bold; padding-left:3px;",
		"loc": [45, 545],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/discontent.png",
		"mood": 9
	  },

      { "style": "text-align:left; background:#A78DB3;border:2px solid black;color: black; font-family:'Verdana'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#8A6B94; border:2px solid #B969D7; color: black; font-family:'Verdana'; font:bold; padding-left:3px;",
		"loc": [135, 545],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/devious.png",
		"mood": 10
	  },

      { "style": "text-align:left; background:#A78DB3;border:2px solid black;color: black; font-family:'Verdana'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#8A6B94; border:2px solid #B969D7; color: black; font-family:'Verdana'; font:bold; padding-left:3px;",
		"loc": [165, 545],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/sleek.png",
		"mood": 11
	  },

      { "style": "text-align:left; background:#A78DB3;border:2px solid black;color: black; font-family:'Verdana'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#8A6B94; border:2px solid #B969D7; color: black; font-family:'Verdana'; font:bold; padding-left:3px;",
		"loc": [105, 515],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/detestful.png",
		"mood": 12
	  },

      { "style": "text-align:left; background:#A78DB3;border:2px solid black;color: black; font-family:'Verdana'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#8A6B94; border:2px solid #B969D7; color: black; font-family:'Verdana'; font:bold; padding-left:3px;",
		"loc": [135, 515],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/mirthful.png",
		"mood": 13
	  },
      { "style": "text-align:left; background:#A78DB3;border:2px solid black;color: black; font-family:'Verdana'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#8A6B94; border:2px solid #B969D7; color: black; font-family:'Verdana'; font:bold; padding-left:3px;",
		"loc": [165, 515],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/manipulative.png",
		"mood": 14
	  },
      { "style": "text-align:left; background:#A78DB3;border:2px solid black;color: black; font-family:'Verdana'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#8A6B94; border:2px solid #B969D7; color: black; font-family:'Verdana'; font:bold; padding-left:3px;",
		"loc": [195, 515],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/vigorous.png",
		"mood": 15
	  },
      { "style": "text-align:left; background:#A78DB3;border:2px solid black;color: black; font-family:'Verdana'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#8A6B94; border:2px solid #B969D7; color: black; font-family:'Verdana'; font:bold; padding-left:3px;",
		"loc": [225, 515],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/perky.png",
		"mood": 16
	  },
      { "style": "text-align:left; background:#A78DB3;border:2px solid black;color: black; font-family:'Verdana'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#8A6B94; border:2px solid #B969D7; color: black; font-family:'Verdana'; font:bold; padding-left:3px;",
		"loc": [255, 515],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/acceptant.png",
		"mood": 17
	  },
      { "style": "text-align:left; background:#A78DB3;border:2px solid black;color: black; font-family:'Verdana'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#8A6B94; border:2px solid #B969D7; color: black; font-family:'Verdana'; font:bold; padding-left:3px;",
		"loc": [75, 515],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/mystified.png",
		"mood": 19
	  },
      { "style": "text-align:left; background:#A78DB3;border:2px solid black;color: black; font-family:'Verdana'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#8A6B94; border:2px solid #B969D7; color: black; font-family:'Verdana'; font:bold; padding-left:3px;",
		"loc": [255, 485],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/amazed.png",
		"mood": 20
	  },
      { "style": "text-align:left; background:#A78DB3;border:2px solid black;color: black; font-family:'Verdana'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#8A6B94; border:2px solid #B969D7; color: black; font-family:'Verdana'; font:bold; padding-left:3px;",
		"loc": [225, 485],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/insolent.png",
		"mood": 21
	  },
      { "style": "text-align:left; background:#A78DB3;border:2px solid black;color: black; font-family:'Verdana'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#8A6B94; border:2px solid #B969D7; color: black; font-family:'Verdana'; font:bold; padding-left:3px;",
		"loc": [195, 545],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/protective.png",
		"mood": 18
	  },
      { "style": "text-align:center; background:#B9C3E4;border:2px solid black;color: black; font-family:'Verdana'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#DA79F7; border:2px solid #B969D7; color: black; font-family:'Verdana'; font:bold; padding-left:3px;",
		"loc": [225, 545],
		"size": [60, 30],
		"text": "OFF",
		"icon": "$path/offline.png",
		"mood": 2
	  }
  ]
},
 "convo": {
     "style": "background-color: #7C5D90;border:2px solid black; font-family: 'Verdana';",
     "chumlabel": { "style": "margin-bottom: 21px;background: #A78DB3; color: black; border:0px; font-size: 14px;",
					"text" : ":: contacting: $handle ::" },
	 "textarea": {
		 "style": "background: #ECC3FF;  font-size: 14px;font:bold; border:2px solid #B969D7;text-align:center; margin-right:10px; margin-left:10px;font-family: 'Verdana'"
 	 },
  "input": { "style": "background: #DA79F7; border:2px solid #A78DB3;margin-top:5px; margin-right:10px; margin-left:10px; font-size: 12px;" },
	 "tabwindow" : {
		 "style": ""
	 },
	 "tabs": {
		 "style": "",
		 "selectedstyle": "",
		 "newmsgcolor": "#7C1AAE"
	 },
	 "scrollbar": null
 },
 "memos":
 { "size": [600,425],
   "style": "background-color: #A6A65D;border:2px solid black; font-family: 'Verdana';",
   "label": { "style": "margin-bottom: 21px;background: #C4C4C4; color: #3F1D50; border:0px; font-size: 14px;"
			},
   "textarea": {
	   "style": "background: #F9E7F8;  font-size: 14px;font:bold; border:2px solid #B969D7;text-align:center; margin-right:10px; margin-left:10px;font-family: 'Verdana'"
   },
   "userlist": { "style": "border:2px solid #3F1D50; background: #D6B6E6;font: bold;font-family: 'Verdana';selection-background-color:#542A69; font-size: 12px;  margin-left:0px; margin-right:10px;"
               },
   "input": { "style": "background: #D6B6E6; border:2px solid #B969D7;margin-top:5px; margin-right:10px; margin-left:10px; font-size: 12px;" },
   "time": { "text": { "style": " border: 2px solid #B969D7; background: #D6B6E6; font-size: 12px; margin-top: 5px; margin-right: 5px; margin-left: 5px; font-family:'Verdana';font:bold;" 
                    },
             "buttons": { "style": "color: black; font: bold; border: 2px solid #B969D7; font: bold; font-size: 12px; background: #B969D7; margin-top: 5px; margin-right: 5px; margin-left: 5px; padding: 2px; width: 50px;" }
          },

   "tabs": {
       "style": "",
       "selectedstyle": "#B969D7",
       "newmsgcolor": "#7C1AAE",
       "tabstyle": 0
   },
   "scrollbar": null
 }
}
