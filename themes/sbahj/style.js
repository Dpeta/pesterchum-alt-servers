{"inherits": "pesterchum2.5",
 "main":
 {"background-image": "$path/hbasj.png",
  "size": [300,620],
  "icon": "$path/trayicon.png",
  "newmsgicon": "$path/trayicon2.png",
  "windowtitle": "Sweet Bro",
  "menu" : { "style": "font-family: 'Comic Sans'; font: bold; font-size: 14px; background-color: #06E8FF;border:2px solid #F84107" },
  "menubar": { "style": "font-family: 'Comic Sans'; font:bold; font-size: 14px; color:#000000; text-align:center;" },
  "close": { "image": "$path/x.png",
             "loc": [282, 4]},
  "minimize": { "image": "$path/m.png",
                "loc": [264, 10]},
  "sounds": { "alertsound": "$path/alarm.wav",
			  "ceasesound": "$path/cease.wav" },
  "defaultwindow": { "style": "background: #06E8FF; font-family:'Comic Sans';font:bold;selection-background-color:black; " },
  "chums": { "style": "border:2px solid #F84107; background-color: #06E8FF;color: #000000;font: bold;font-size:14px;font-family: 'Comic Sans';selection-background-color:black; ",
             "moods": { 

                 "chummy": { "icon": "$path/chummy.png", "color": "#FA9716" },

                 "rancorous": { "icon": "$path/rancorous.png", "color": "#F84107" },

                 "offline": { "icon": "$path/offline.png", "color": "#D510A5"},

			     
                 "pleasant": { "icon": "$path/pleasant.png", "color": "#FA9716" },

                 "distraught": { "icon": "$path/distraught.png", "color": "#FA9716" },

                 "pranky": { "icon": "$path/pranky.png", "color": "#FA9716" },


                 "smooth": { "icon": "$path/smooth.png", "color": "#FA9716" },

                 "mystified": { "icon": "$path/mystified.png", "color": "#FA9716" },

                 "amazed": { "icon": "$path/amazed.png", "color": "#FA9716" },

                 "insolent": { "icon": "$path/insolent.png", "color": "#FA9716" },

                 "bemused": { "icon": "$path/bemused.png", "color": "#FA9716" },


                 "ecstatic": { "icon": "$path/ecstatic.png", "color": "#F84107" },

                 "relaxed": { "icon": "$path/relaxed.png", "color": "#F84107" },

                 "discontent": { "icon": "$path/discontent.png", "color": "#F84107" },

                 "devious": { "icon": "$path/devious.png", "color": "#F84107" },

                 "sleek": { "icon": "$path/sleek.png", "color": "#F84107" },
			     
                 "detestful": { "icon": "$path/detestful.png", "color": "#F84107" },

                 "mirthful": { "icon": "$path/mirthful.png", "color": "#F84107" },

                 "manipulative": { "icon": "$path/manipulative.png", "color": "#F84107" },

                 "vigorous": { "icon": "$path/vigorous.png", "color": "#F84107" },

                 "perky": { "icon": "$path/perky.png", "color": "#F84107" },

                 "acceptant": { "icon": "$path/acceptant.png", "color": "#F84107" },

                 "protective": { "icon": "$path/protective.png", "color": "#0707F7" },

                 "blocked": { "icon": "$path/blocked.png", "color": "black" }
			 }
		   },
  "mychumhandle": { "label": 
                    { "text": "NAYM:",
                      "style": "color: #F60805 ;font:bold; font-family: 'Comic Sans';" 
                    },
					"handle": { "style": "background-color: #F8F242; padding: 3px; padding-left: 25px; color:#F84107; font-family:'Comic Sans'; font:bold; text-align:left; border:2px solid #06E8FF;" }
                  },
  "addchum":  { "style": "background: #F8F242; border:2px solid #F84107; font: bold; color: #19A937; font-family:'Comic Sans';"
              },
  "pester": { "style": "background: #F8F242; border:2px solid #F84107; font: bold; color: #19A937; font-family:'Comic Sans';"
            },
  "block": { "style": "background: #F8F242; border:2px solid #F84107; font: bold; color: #19A937; font-family:'Comic Sans';"
           },
  "moodlabel": { "style": "font:bold;font-family:'Comic Sans';color:#FA9716;"
			   },
  "defaultmood": 18,
  "moods": [
      { "style": "text-align:left; background:#06E8FF;border:2px solid black;color: black; font-family:'Comic Sans'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#F84107; border:2px solid #F4D80C; color: black; font-family:'Comic Sans'; font:bold; padding-left:3px;",
		"loc": [15, 485],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/chummy.png",
		"mood": 0
	  },
      { "style": "text-align:left; background:#06E8FF;border:2px solid black;color: black; font-family:'Comic Sans'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#F84107; border:2px solid #F4D80C; color: black; font-family:'Comic Sans'; font:bold; padding-left:3px;",
		"loc": [45, 485],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/rancorous.png",
		"mood": 1
	  },
      { "style": "text-align:left; background:#06E8FF;border:2px solid black;color: black; font-family:'Comic Sans'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#F84107; border:2px solid #F4D80C; color: black; font-family:'Comic Sans'; font:bold; padding-left:3px;",
		"loc": [75, 485],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/bemused.png",
		"mood": 22
	  },
      { "style": "text-align:left; background:#06E8FF;border:2px solid black;color: black; font-family:'Comic Sans'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#F84107; border:2px solid #F4D80C; color: black; font-family:'Comic Sans'; font:bold; padding-left:3px;",
		"loc": [105, 485],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/pleasant.png",
		"mood": 3
	  },
      { "style": "text-align:left; background:#06E8FF;border:2px solid black;color: black; font-family:'Comic Sans'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#F84107; border:2px solid #F4D80C; color: black; font-family:'Comic Sans'; font:bold; padding-left:3px;",
		"loc": [135, 485],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/distraught.png",
		"mood": 4
	  },
      { "style": "text-align:left; background:#06E8FF;border:2px solid black;color: black; font-family:'Comic Sans'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#F84107; border:2px solid #F4D80C; color: black; font-family:'Comic Sans'; font:bold; padding-left:3px;",
		"loc": [165, 485],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/pranky.png",
		"mood": 5
	  },
      { "style": "text-align:left; background:#06E8FF;border:2px solid black;color: black; font-family:'Comic Sans'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#F84107; border:2px solid #F4D80C; color: black; font-family:'Comic Sans'; font:bold; padding-left:3px;",
		"loc": [195, 485],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/smooth.png",
		"mood": 6
	  },
      { "style": "text-align:left; background:#06E8FF;border:2px solid black;color: black; font-family:'Comic Sans'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#F84107; border:2px solid #F4D80C; color: black; font-family:'Comic Sans'; font:bold; padding-left:3px;",
		"loc": [15, 545],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/estatic.png",
		"mood": 7
	  },

      { "style": "text-align:left; background:#06E8FF;border:2px solid black;color: black; font-family:'Comic Sans'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#F84107; border:2px solid #F4D80C; color: black; font-family:'Comic Sans'; font:bold; padding-left:3px;",
		"loc": [75, 545],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/relaxed.png",
		"mood": 8
	  },

      { "style": "text-align:left; background:#06E8FF;border:2px solid black;color: black; font-family:'Comic Sans'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#F84107; border:2px solid #F4D80C; color: black; font-family:'Comic Sans'; font:bold; padding-left:3px;",
		"loc": [45, 545],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/discontent.png",
		"mood": 9
	  },

      { "style": "text-align:left; background:#06E8FF;border:2px solid black;color: black; font-family:'Comic Sans'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#F84107; border:2px solid #F4D80C; color: black; font-family:'Comic Sans'; font:bold; padding-left:3px;",
		"loc": [45, 515],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/devious.png",
		"mood": 10
	  },

      { "style": "text-align:left; background:#06E8FF;border:2px solid black;color: black; font-family:'Comic Sans'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#F84107; border:2px solid #F4D80C; color: black; font-family:'Comic Sans'; font:bold; padding-left:3px;",
		"loc": [75, 515],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/sleek.png",
		"mood": 11
	  },

      { "style": "text-align:left; background:#06E8FF;border:2px solid black;color: black; font-family:'Comic Sans'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#F84107; border:2px solid #F4D80C; color: black; font-family:'Comic Sans'; font:bold; padding-left:3px;",
		"loc": [105, 515],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/detestful.png",
		"mood": 12
	  },

      { "style": "text-align:left; background:#06E8FF;border:2px solid black;color: black; font-family:'Comic Sans'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#F84107; border:2px solid #F4D80C; color: black; font-family:'Comic Sans'; font:bold; padding-left:3px;",
		"loc": [135, 515],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/mirthful.png",
		"mood": 13
	  },
      { "style": "text-align:left; background:#06E8FF;border:2px solid black;color: black; font-family:'Comic Sans'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#F84107; border:2px solid #F4D80C; color: black; font-family:'Comic Sans'; font:bold; padding-left:3px;",
		"loc": [165, 515],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/manipulative.png",
		"mood": 14
	  },
      { "style": "text-align:left; background:#06E8FF;border:2px solid black;color: black; font-family:'Comic Sans'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#F84107; border:2px solid #F4D80C; color: black; font-family:'Comic Sans'; font:bold; padding-left:3px;",
		"loc": [195, 515],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/vigorous.png",
		"mood": 15
	  },
      { "style": "text-align:left; background:#06E8FF;border:2px solid black;color: black; font-family:'Comic Sans'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#F84107; border:2px solid #F4D80C; color: black; font-family:'Comic Sans'; font:bold; padding-left:3px;",
		"loc": [225, 515],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/perky.png",
		"mood": 16
	  },
      { "style": "text-align:left; background:#06E8FF;border:2px solid black;color: black; font-family:'Comic Sans'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#F84107; border:2px solid #F4D80C; color: black; font-family:'Comic Sans'; font:bold; padding-left:3px;",
		"loc": [255, 515],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/acceptant.png",
		"mood": 17
	  },
      { "style": "text-align:left; background:#06E8FF;border:2px solid black;color: black; font-family:'Comic Sans'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#F84107; border:2px solid #F4D80C; color: black; font-family:'Comic Sans'; font:bold; padding-left:3px;",
		"loc": [15, 515],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/mystified.png",
		"mood": 19
	  },
      { "style": "text-align:left; background:#06E8FF;border:2px solid black;color: black; font-family:'Comic Sans'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#F84107; border:2px solid #F4D80C; color: black; font-family:'Comic Sans'; font:bold; padding-left:3px;",
		"loc": [255, 485],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/amazed.png",
		"mood": 20
	  },
      { "style": "text-align:left; background:#06E8FF;border:2px solid black;color: black; font-family:'Comic Sans'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#F84107; border:2px solid #F4D80C; color: black; font-family:'Comic Sans'; font:bold; padding-left:3px;",
		"loc": [225, 485],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/insolent.png",
		"mood": 21
	  },
      { "style": "text-align:left; background:#06E8FF;border:2px solid black;color: black; font-family:'Comic Sans'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#F84107; border:2px solid #F4D80C; color: black; font-family:'Comic Sans'; font:bold; padding-left:3px;",
		"loc": [105, 545],
		"size": [30, 30],
	    "text": "",
		"icon": "$path/protective.png",
		"mood": 18
	  },
      { "style": "text-align:left; background:#E90A0A;border:2px solid black;color: black; font-family:'Comic Sans'; font:bold; padding-left:3px;", 
		"selected": "text-align:left; background:#FA9716; border:2px solid #F4D80C; color: black; font-family:'Comic Sans'; font:bold; padding-left:3px;",
		"loc": [135, 545],
		"size": [150, 30],
		"text": "AWAYAWAYAWAYS",
		"icon": "$path/offline.png",
		"mood": 2
	  }
  ]
},
 "convo": {
     "style": "background-color: #A700FE;border:2px solid black; font-family: 'Comic Sans';",
     "chumlabel": { "style": "margin-bottom: 21px;background: #06E8FF; color: black; border:0px; font-size: 14px;",
					"text" : ":: contacting: $handle ::" },
	 "textarea": {
		 "style": "background: #D2FFFF;  font-size: 14px;font:bold; border:2px solid #F84107;text-align:center; margin-right:10px; margin-left:10px;font-family: 'Comic Sans'"
 	 },
  "input": { "style": "background: #FA9716; border:2px solid #06E8FF;margin-top:5px; margin-right:10px; margin-left:10px; font-size: 12px;" },
	 "tabwindow" : {
		 "style": ""
	 },
	 "tabs": {
		 "style": "",
		 "selectedstyle": "",
		 "newmsgcolor": "#A4AE1A"
	 },
	 "scrollbar": null
 },
 "memos":
 { "size": [600,425],
   "style": "background-color: #A6A65D;border:2px solid black; font-family: 'Comic Sans';",
   "label": { "style": "margin-bottom: 21px;background: #05FF17; color: #FA9716; border:0px; font-size: 14px;"
			},
   "textarea": {
	   "style": "background: #EAF729;  font-size: 14px;font:bold; border:2px solid #F84107;text-align:center; margin-right:10px; margin-left:10px;font-family: 'Comic Sans'"
   },
   "userlist": { "style": "border:2px solid #82873E; background: #FA9716;font: bold;font-family: 'Comic Sans';selection-background-color:#D510A5; font-size: 12px;  margin-left:0px; margin-right:10px;"
               },
   "input": { "style": "background: #FA9716; border:2px solid #F84107;margin-top:5px; margin-right:10px; margin-left:10px; font-size: 12px;" },
   "time": { "text": { "style": " border: 2px solid #F84107; background: #FA9716; font-size: 12px; margin-top: 5px; margin-right: 5px; margin-left: 5px; font-family:'Comic Sans';font:bold;" 
                    },
             "buttons": { "style": "color: black; font: bold; border: 2px solid #F84107; font: bold; font-size: 12px; background: #F84107; margin-top: 5px; margin-right: 5px; margin-left: 5px; padding: 2px; width: 50px;" }
          },

   "tabs": {
       "style": "",
       "selectedstyle": "#F84107",
       "newmsgcolor": "#A4AE1A",
       "tabstyle": 0
   },
   "scrollbar": null
 }
}
