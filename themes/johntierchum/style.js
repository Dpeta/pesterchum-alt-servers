{"inherits": "pesterchum2.5",
 "main":
 {"background-image": "$path/johntier.png",
  "size": [619,832],
  "icon": "$path/trayicon.png",
  "newmsgicon": "$path/trayicon2.png",
  "windowtitle": "Godtier",
  "menu" : { "style": "font-family: 'Arial'; font:bold; font-size: 14px; color:#FFFFFF; background-color: #6277BC;border:2px solid #9BC4F2",
  "selected": "background-color: #6090C6", 
              "loc": [161,52]},
  "menubar": { "style": "font-family: 'Arial'; font:bold; font-size: 14px; color:#9AC3F0; text-align:center;", 
              "loc": [171,52]},
  "close": { "image": "$path/x.png",
             "loc": [351, 34]},
  "minimize": { "image": "$path/m.png",
                "loc": [370, 42]},
  "sounds": { "alertsound": "$path/alarm.wav",
			  "ceasesound": "$path/cease.wav" },
  "defaultwindow": { "style": "background: #9BC4F2; font-family:'Arial';font:bold;selection-background-color:#66A5EC; " },
  "chums": { "style": "border:2px solid rgba(0,0,0,0%); background-color: rgba(0,0,0,0%);color: black;font: bold;font-size:14px;font-family: 'Arial';selection-background-color:white; ",
             "size": [200, 180],
             "loc": [233,400],
             "moods": { 

                 "chummy": { "icon": "$path/chummy.png", "color": "#FFFFFF" },

                 "rancorous": { "icon": "$path/rancorous.png", "color": "#E5E5E5" },

                 "offline": { "icon": "$path/offline.png", "color": "#646464"},

			     
                 "pleasant": { "icon": "$path/pleasant.png", "color": "#FFFFFF" },

                 "distraught": { "icon": "$path/distraught.png", "color": "#FFFFFF" },

                 "pranky": { "icon": "$path/pranky.png", "color": "#FFFFFF" },


                 "smooth": { "icon": "$path/smooth.png", "color": "#FFFFFF" },

                 "mystified": { "icon": "$path/mystified.png", "color": "#FFFFFF" },

                 "amazed": { "icon": "$path/amazed.png", "color": "#FFFFFF" },

                 "insolent": { "icon": "$path/insolent.png", "color": "#FFFFFF" },

                 "bemused": { "icon": "$path/bemused.png", "color": "#FFFFFF" },


                 "ecstatic": { "icon": "$path/ecstatic.png", "color": "#E5E5E5" },

                 "relaxed": { "icon": "$path/relaxed.png", "color": "#E5E5E5" },

                 "discontent": { "icon": "$path/discontent.png", "color": "#E5E5E5" },

                 "devious": { "icon": "$path/devious.png", "color": "#E5E5E5" },

                 "sleek": { "icon": "$path/sleek.png", "color": "#E5E5E5" },
			     
                 "detestful": { "icon": "$path/detestful.png", "color": "#E5E5E5" },

                 "mirthful": { "icon": "$path/mirthful.png", "color": "#E5E5E5" },

                 "manipulative": { "icon": "$path/manipulative.png", "color": "#E5E5E5" },

                 "vigorous": { "icon": "$path/vigorous.png", "color": "#E5E5E5" },

                 "perky": { "icon": "$path/perky.png", "color": "#E5E5E5" },

                 "acceptant": { "icon": "$path/acceptant.png", "color": "#E5E5E5" },

                 "protective": { "icon": "$path/protective.png", "color": "#000000" },

                 "blocked": { "icon": "$path/blocked.png", "color": "#000000" }
			 }
		   },
  "mychumhandle": { "label": { "text": "",
                               "loc": [0,0],
                               "style": "color: rgba(0,0,0,0);" },
                    "handle": { "style": "background: rgba(0,0,0,0); padding: 3px; padding-left: 26px; color: white; font-family:'Verdana'; font: bold; text-align:left; font-size: 12px; border: 3px solid rgba(0,0,0,0);",
                                "loc": [235,590],
                                "size": [202, 27] },
                    "colorswatch": { "loc": [412,593],
                                     "size": [22,21],
                                     "text": "" },
                    "currentMood": [241, 595]
                  },
  "addchum":  { "style": "background: #6277BC; border:2px solid white; font: bold; color: white; font-family:'Verdana';",
                "pressed" : "background: #6090C6;",
                "loc": [260,620],
                "size": [71, 22],
                "text": "Greet"
              },
  "pester": { "style": "background: #6277BC; border:2px solid white; font: bold; color:  white; font-family:'Verdana';",
              "pressed" : "background: #6090C6;",
              "loc": [330,620],
              "size": [71, 22],
              "text": "Pester"
            },
  "block":  { "style": "background: rgba(0,0,0,0); border:0px; color: rgba(0,0,0,0);",
             "loc": [0, 0],
             "size": [0, 0],
             "text": ""
           },
  "moodlabel": { "text": "",
                 "style": "font:bold;font-family:'Arial';color:#000000;"
			   },
  "defaultmood": 5,
  "moods": [
      { "style": "text-align:left; background:rgba(0,0,0,0);border:2px solid rgba(0,0,0,0);color: #66A5EC; font-family:'Arial'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:rgba(0,0,0,0); border:2px solid rgba(0,0,0,0); color: #66A5EC; font-family:'Arial'; font:bold; padding-left:3px;",
		"loc": [302, 133],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/chummy.png",
		"mood": 0
	  },
      { "style": "text-align:left; background:rgba(0,0,0,0);border:2px solid rgba(0,0,0,0);color: #66A5EC; font-family:'Arial'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:rgba(0,0,0,0); border:2px solid rgba(0,0,0,0); color: #66A5EC; font-family:'Arial'; font:bold; padding-left:3px;",
		"loc": [460, 432],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/rancorous.png",
		"mood": 1
	  },
      { "style": "text-align:left; background:rgba(0,0,0,0);border:2px solid rgba(0,0,0,0);color: #66A5EC; font-family:'Arial'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:rgba(0,0,0,0); border:2px solid rgba(0,0,0,0); color: #66A5EC; font-family:'Arial'; font:bold; padding-left:3px;",
		"loc": [368, 162],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/bemused.png",
		"mood": 22
	  },
      { "style": "text-align:left; background:rgba(0,0,0,0);border:2px solid rgba(0,0,0,0);color: #66A5EC; font-family:'Arial'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:rgba(0,0,0,0); border:2px solid rgba(0,0,0,0); color: #66A5EC; font-family:'Arial'; font:bold; padding-left:3px;",
		"loc": [391, 192],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/pleasant.png",
		"mood": 3
	  },
      { "style": "text-align:left; background:rgba(0,0,0,0);border:2px solid rgba(0,0,0,0);color: #66A5EC; font-family:'Arial'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:rgba(0,0,0,0); border:2px solid rgba(0,0,0,0); color: #66A5EC; font-family:'Arial'; font:bold; padding-left:3px;",
		"loc": [409, 223],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/distraught.png",
		"mood": 4
	  },
      { "style": "text-align:left; background:rgba(0,0,0,0);border:2px solid rgba(0,0,0,0);color: #66A5EC; font-family:'Arial'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:rgba(0,0,0,0); border:2px solid rgba(0,0,0,0); color: #66A5EC; font-family:'Arial'; font:bold; padding-left:3px;",
		"loc": [416, 260],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/pranky.png",
		"mood": 5
	  },
      { "style": "text-align:left; background:rgba(0,0,0,0);border:2px solid rgba(0,0,0,0);color: #66A5EC; font-family:'Arial'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:rgba(0,0,0,0); border:2px solid rgba(0,0,0,0); color: #66A5EC; font-family:'Arial'; font:bold; padding-left:3px;",
		"loc": [412, 289],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/smooth.png",
		"mood": 6
	  },

      { "style": "text-align:left; background:rgba(0,0,0,0);border:2px solid rgba(0,0,0,0);color: #66A5EC; font-family:'Arial'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:rgba(0,0,0,0); border:2px solid rgba(0,0,0,0); color: #66A5EC; font-family:'Arial'; font:bold; padding-left:3px;",
		"loc": [335, 145],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/amazed.png",
		"mood": 20
	  },
      { "style": "text-align:left; background:rgba(0,0,0,0);border:2px solid rgba(0,0,0,0);color: #66A5EC; font-family:'Arial'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:rgba(0,0,0,0); border:2px solid rgba(0,0,0,0); color: #66A5EC; font-family:'Arial'; font:bold; padding-left:3px;",
		"loc": [265, 122],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/insolent.png",
		"mood": 21
	  },
      { "style": "text-align:left; background:rgba(0,0,0,0);border:2px solid rgba(0,0,0,0);color: #66A5EC; font-family:'Arial'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:rgba(0,0,0,0); border:2px solid rgba(0,0,0,0); color: #66A5EC; font-family:'Arial'; font:bold; padding-left:3px;",
		"loc": [387, 309],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/protective.png",
		"mood": 18
	  },
      { "style": "text-align:left; background:rgba(0,0,0,0);border:2px solid rgba(0,0,0,0);color: #66A5EC; font-family:'Arial'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:rgba(0,0,0,0); border:2px solid rgba(0,0,0,0); color: #66A5EC; font-family:'Arial'; font:bold; padding-left:3px;",
		"loc": [436, 404],
		"size": [30, 30],
		"text": "",
		"icon": "$path/offline.png",
		"mood": 2
	  }
  ]
},
 "convo": {
     "style": "background-color: #4473a8;border:2px solid #626262; font-family: 'Arial';",
     "chumlabel": { "style": "margin-bottom: 21px;background: #66A5EC; color: #000000; border:0px; font-size: 14px;",
					"text" : "~ Pranking $handle ~" },
	 "textarea": {
		 "style": "background: #BDDFFF;  font-size: 14px;font:bold; border:2px solid #5C5C5C;text-align:center; margin-right:10px; margin-left:10px;font-family: 'Arial'"
 	 },
  "input": { "style": "background: #99c2f0; border:2px solid #626262;margin-top:5px; margin-right:10px; margin-left:10px; font-size: 12px;" },
	 "tabwindow" : {
		 "style": "background: #6277bc; font-family: 'Arial'"
	 },
	 "tabs": {
		 "style": "border: 2px solid #D4DEFF; background: #6277bc; color: #FFFFFF;",
		 "selectedstyle": "border: 3px solid #D4DEFF; background: #7C9CD2; color: #76ADFF;",
		 "newmsgcolor": "#730F0F"
	 },
	 "scrollbar": null
 },
 "memos":
 { "size": [600,425],
   "style": "background-color: #0F731C;border:2px solid #626262; font-family: 'Arial';",
   "label": { "style": "margin-bottom: 21px;background: #AFBAEE; color: #5C5C5C; border:0px; font-size: 14px;"
			},
   "textarea": {
	   "style": "background: #DFEFFF;  font-size: 14px;font:bold; border:2px solid #5C5C5C;text-align:center; margin-right:10px; margin-left:10px;font-family: 'Arial'"
   },
   "userlist": { "style": "border:2px solid #000079; background: #AFBAEE;font: bold;font-family: 'Courier';selection-background-color:#646464; font-size: 12px;  margin-left:0px; margin-right:10px;"
               },
   "input": { "style": "background: #99c2f0; border:2px solid #5C5C5C;margin-top:5px; margin-right:10px; margin-left:10px; font-size: 12px;" },
   "time": { "text": { "style": "color:#003789; border: 2px solid #5C5C5C; background: #7188D5; font-size: 12px; margin-top: 5px; margin-right: 5px; margin-left: 5px; font-family:'Arial';font:bold;" 
                    },
             "buttons": { "style": "color: #003789; font: bold; border: 2px solid #5C5C5C; font: bold; font-size: 12px; background: #7188D5; margin-top: 5px; margin-right: 5px; margin-left: 5px; padding: 2px; width: 50px;" }
          },

   "tabs": {
       "style": "",
       "selectedstyle": "#5C5C5C",
       "newmsgcolor": "#FA0A0A",
       "tabstyle": 0
   },
   "scrollbar": null
 }
}
