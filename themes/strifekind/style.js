{"inherits": "pesterchum2.5",
 "main":
 {"background-image": "$path/strife.png",
  "size": [300,620],
  "icon": "$path/trayicon.png",
  "newmsgicon": "$path/trayicon2.png",
  "windowtitle": "CHUMKIND",
  "menu" : { "style": "font-family: 'Courier'; font: bold; font-size: 14px; background-color: #00C661;border:2px solid #00E371" },
  "menubar": { "style": "font-family: 'Courier'; font:bold; font-size: 14px; color:#FFFFFF; text-align:center;" },
  "close": { "image": "$path/x.png",
             "loc": [10, 30]},
  "minimize": { "image": "$path/m.png",
                "loc": [20, 33]},
  "sounds": { "alertsound": "$path/alarm.wav",
			  "ceasesound": "$path/cease.wav" },
  "defaultwindow": { "style": "background: #FFFFFF; font-family:'Courier';font:bold;selection-background-color:black; " },
  "chums": { "style": "border:2px solid #FFFFFF; background-color: #FFFFFF;color: #000000;font: bold;font-size:14px;font-family: 'Courier';selection-background-color:black; ",
             "userlistcolor": "00C661", 
             "moods": { 

                 "chummy": { "icon": "$path/chummy.png", "color": "#000000" },

                 "rancorous": { "icon": "$path/rancorous.png", "color": "#7E7E7E" },

                 "offline": { "icon": "$path/offline.png", "color": "#00E371"},

			     
                 "pleasant": { "icon": "$path/pleasant.png", "color": "#000000" },

                 "distraught": { "icon": "$path/distraught.png", "color": "#000000" },

                 "pranky": { "icon": "$path/pranky.png", "color": "#000000" },


                 "smooth": { "icon": "$path/smooth.png", "color": "#000000" },

                 "mystified": { "icon": "$path/mystified.png", "color": "#000000" },

                 "amazed": { "icon": "$path/amazed.png", "color": "#000000" },

                 "insolent": { "icon": "$path/insolent.png", "color": "#000000" },

                 "bemused": { "icon": "$path/bemused.png", "color": "#000000" },


                 "ecstatic": { "icon": "$path/ecstatic.png", "color": "#7E7E7E" },

                 "relaxed": { "icon": "$path/relaxed.png", "color": "#7E7E7E" },

                 "discontent": { "icon": "$path/discontent.png", "color": "#7E7E7E" },

                 "devious": { "icon": "$path/devious.png", "color": "#7E7E7E" },

                 "sleek": { "icon": "$path/sleek.png", "color": "#7E7E7E" },
			     
                 "detestful": { "icon": "$path/detestful.png", "color": "#7E7E7E" },

                 "mirthful": { "icon": "$path/mirthful.png", "color": "#7E7E7E" },

                 "manipulative": { "icon": "$path/manipulative.png", "color": "#7E7E7E" },

                 "vigorous": { "icon": "$path/vigorous.png", "color": "#7E7E7E" },

                 "perky": { "icon": "$path/perky.png", "color": "#7E7E7E" },

                 "acceptant": { "icon": "$path/acceptant.png", "color": "#7E7E7E" },

                 "protective": { "icon": "$path/protective.png", "color": "#00C661" },

                 "blocked": { "icon": "$path/blocked.png", "color": "black" }
			 }
		   },
  "mychumhandle": { "label": 
                    { "text": "Kind:",
                      "style": "color: black ;font:bold; font-family: 'Courier';" 
                    },
					"handle": { "style": "background-color: #00C661; padding: 3px; padding-left: 25px; color:#FFFFFF; font-family:'Courier'; font:bold; text-align:left; border:2px solid #FFFFFF;" }
                  },
  "addchum":  { "style": "background: #00E371; border:2px solid #0E6037; font: bold; color: #000000; font-family:'Courier';"
              },
  "pester": { "style": "background: #00E371; border:2px solid #0E6037; font: bold; color: #000000; font-family:'Courier';"
            },
  "block": { "style": "background: #00E371; border:2px solid #0E6037; font: bold; color: #000000; font-family:'Courier';"
           },
  "moodlabel": { "style": "font:bold;font-family:'Courier';color:#008C45;"
			   },
  "defaultmood": 18,
  "moods": [
      { "style": "text-align:left; background:#FFFFFF;border:2px solid black;color: black; font-family:'Courier'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#008C45; border:2px solid #000000; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
		"loc": [15, 485],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/chummy.png",
		"mood": 0
	  },
      { "style": "text-align:left; background:#FFFFFF;border:2px solid black;color: black; font-family:'Courier'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#008C45; border:2px solid #000000; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
		"loc": [45, 485],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/rancorous.png",
		"mood": 1
	  },
      { "style": "text-align:left; background:#FFFFFF;border:2px solid black;color: black; font-family:'Courier'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#008C45; border:2px solid #000000; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
		"loc": [75, 485],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/bemused.png",
		"mood": 22
	  },
      { "style": "text-align:left; background:#FFFFFF;border:2px solid black;color: black; font-family:'Courier'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#008C45; border:2px solid #000000; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
		"loc": [105, 485],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/pleasant.png",
		"mood": 3
	  },
      { "style": "text-align:left; background:#FFFFFF;border:2px solid black;color: black; font-family:'Courier'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#008C45; border:2px solid #000000; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
		"loc": [135, 485],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/distraught.png",
		"mood": 4
	  },
      { "style": "text-align:left; background:#FFFFFF;border:2px solid black;color: black; font-family:'Courier'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#008C45; border:2px solid #000000; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
		"loc": [165, 485],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/pranky.png",
		"mood": 5
	  },
      { "style": "text-align:left; background:#FFFFFF;border:2px solid black;color: black; font-family:'Courier'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#008C45; border:2px solid #000000; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
		"loc": [195, 485],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/smooth.png",
		"mood": 6
	  },
      { "style": "text-align:left; background:#FFFFFF;border:2px solid black;color: black; font-family:'Courier'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#008C45; border:2px solid #000000; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
		"loc": [15, 545],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/estatic.png",
		"mood": 7
	  },

      { "style": "text-align:left; background:#FFFFFF;border:2px solid black;color: black; font-family:'Courier'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#008C45; border:2px solid #000000; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
		"loc": [75, 545],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/relaxed.png",
		"mood": 8
	  },

      { "style": "text-align:left; background:#FFFFFF;border:2px solid black;color: black; font-family:'Courier'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#008C45; border:2px solid #000000; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
		"loc": [45, 545],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/discontent.png",
		"mood": 9
	  },

      { "style": "text-align:left; background:#FFFFFF;border:2px solid black;color: black; font-family:'Courier'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#008C45; border:2px solid #000000; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
		"loc": [45, 515],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/devious.png",
		"mood": 10
	  },

      { "style": "text-align:left; background:#FFFFFF;border:2px solid black;color: black; font-family:'Courier'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#008C45; border:2px solid #000000; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
		"loc": [75, 515],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/sleek.png",
		"mood": 11
	  },

      { "style": "text-align:left; background:#FFFFFF;border:2px solid black;color: black; font-family:'Courier'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#008C45; border:2px solid #000000; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
		"loc": [105, 515],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/detestful.png",
		"mood": 12
	  },

      { "style": "text-align:left; background:#FFFFFF;border:2px solid black;color: black; font-family:'Courier'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#008C45; border:2px solid #000000; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
		"loc": [135, 515],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/mirthful.png",
		"mood": 13
	  },
      { "style": "text-align:left; background:#FFFFFF;border:2px solid black;color: black; font-family:'Courier'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#008C45; border:2px solid #000000; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
		"loc": [165, 515],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/manipulative.png",
		"mood": 14
	  },
      { "style": "text-align:left; background:#FFFFFF;border:2px solid black;color: black; font-family:'Courier'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#008C45; border:2px solid #000000; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
		"loc": [195, 515],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/vigorous.png",
		"mood": 15
	  },
      { "style": "text-align:left; background:#FFFFFF;border:2px solid black;color: black; font-family:'Courier'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#008C45; border:2px solid #000000; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
		"loc": [225, 515],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/perky.png",
		"mood": 16
	  },
      { "style": "text-align:left; background:#FFFFFF;border:2px solid black;color: black; font-family:'Courier'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#008C45; border:2px solid #000000; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
		"loc": [255, 515],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/acceptant.png",
		"mood": 17
	  },
      { "style": "text-align:left; background:#FFFFFF;border:2px solid black;color: black; font-family:'Courier'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#008C45; border:2px solid #000000; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
		"loc": [15, 515],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/mystified.png",
		"mood": 19
	  },
      { "style": "text-align:left; background:#FFFFFF;border:2px solid black;color: black; font-family:'Courier'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#008C45; border:2px solid #000000; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
		"loc": [255, 485],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/amazed.png",
		"mood": 20
	  },
      { "style": "text-align:left; background:#FFFFFF;border:2px solid black;color: black; font-family:'Courier'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#008C45; border:2px solid #000000; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
		"loc": [225, 485],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/insolent.png",
		"mood": 21
	  },
      { "style": "text-align:left; background:#FFFFFF;border:2px solid black;color: black; font-family:'Courier'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#008C45; border:2px solid #000000; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
		"loc": [105, 545],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/protective.png",
		"mood": 18
	  },
      { "style": "text-align:center; background:#0E6037;border:2px solid black;color: black; font-family:'Courier'; font:bold; padding-left:3px;", 
		"selected": "text-align:center; background:#008C45; border:2px solid #000000; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
		"loc": [135, 545],
		"size": [150, 30],
		"text": "HIDING/RUNNING",
		"icon": "$path/offline.png",
		"mood": 2
	  }
  ]
},
 "convo": {
     "style": "background-color: #008C45;border:2px solid black; font-family: 'Courier';",
     "chumlabel": { "style": "margin-bottom: 21px;background: #FFFFFF; color: black; border:0px; font-size: 14px;",
					"text" : ":: contacting: $handle ::" },
	 "textarea": {
		 "style": "background: #7FFFBF;  font-size: 14px;font:bold; border:2px solid #00E371;text-align:center; margin-right:10px; margin-left:10px;font-family: 'Courier'"
 	 },
  "input": { "style": "background: #00E371; border:2px solid #FFFFFF;margin-top:5px; margin-right:10px; margin-left:10px; font-size: 12px;" },
	 "tabwindow" : {
		 "style": ""
	 },
	 "tabs": {
		 "style": "",
		 "selectedstyle": "",
		 "newmsgcolor": "#00E371"
	 },
	 "scrollbar": null
 },
 "memos":
 { "size": [600,425],
   "style": "background-color: #A6A65D;border:2px solid black; font-family: 'Courier';",
   "label": { "style": "margin-bottom: 21px;background: #008C45; color: #2E2E2E; border:0px; font-size: 14px;"
			},
   "textarea": {
	   "style": "background: #7FFFBF;  font-size: 14px;font:bold; border:2px solid #00E371;text-align:center; margin-right:10px; margin-left:10px;font-family: 'Courier'"
   },
   "userlist": { "style": "border:2px solid #4B4B4B; background: #00C661;font: bold;font-family: 'Courier';selection-background-color:#0D1032; font-size: 12px;  margin-left:0px; margin-right:10px;"
               },
   "input": { "style": "background: #00C661; border:2px solid #00E371;margin-top:5px; margin-right:10px; margin-left:10px; font-size: 12px;" },
   "time": { "text": { "style": " border: 2px solid #00E371; background: #00C661; font-size: 12px; margin-top: 5px; margin-right: 5px; margin-left: 5px; font-family:'Courier';font:bold;" 
                    },
             "buttons": { "style": "color: white; font: bold; border: 2px solid #00E371; font: bold; font-size: 12px; background: #00E371; margin-top: 5px; margin-right: 5px; margin-left: 5px; padding: 2px; width: 50px;" }
          },

   "tabs": {
       "style": "",
       "selectedstyle": "#00E371",
       "newmsgcolor": "#00E371",
       "tabstyle": 0
   },
   "scrollbar": null
 }
}
