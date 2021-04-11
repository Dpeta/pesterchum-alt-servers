{"inherits": "pesterchum2.5",
 "main":
 {"background-image": "$path/srs.png",
  "size": [300,620],
  "icon": "$path/trayicon.png",
  "newmsgicon": "$path/trayicon2.png",
  "windowtitle": "Serious Business",
  "menu" : { "style": "font-family: 'Courier'; font: bold; font-size: 14px; background-color: #BABABA;border:2px solid #B3B3B3",
             "loc": [52,5]},
  "menubar": { "style": "font-family: 'Courier'; font:bold; font-size: 14px; color:#000000; text-align:center;" },
  "close": { "image": "$path/x.png",
             "loc": [236, 15]},
  "minimize": { "image": "$path/m.png",
                "loc": [222, 21]},
  "sounds": { "alertsound": "$path/alarm.wav",
              "ceasesound": "$path/cease.wav" },
  "defaultwindow": { "style": "background: #BABABA; font-family:'Courier';font:bold;selection-background-color:black; " },
  "chums": { "style": "border:2px solid #B3B3B3; background-color: #BABABA;color: #000000;font: bold;font-size:14px;font-family: 'Courier';selection-background-color:black; ",
             "moods": { 

                 "chummy": { "icon": "$path/chummy.png", "color": "#000000" },

                 "rancorous": { "icon": "$path/rancorous.png", "color": "#7E7E7E" },

                 "offline": { "icon": "$path/offline.png", "color": "#4E4949"},

                 
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

                 "protective": { "icon": "$path/protective.png", "color": "#cdcdcd" },

                 "blocked": { "icon": "$path/blocked.png", "color": "black" }
             }
           },
  "mychumhandle": { "label": 
                    { "text": "Alias:",
                      "style": "color: black ;font:bold; font-family: 'Courier';" 
                    },
                    "handle": { "style": "background-color: #C6C6C6; padding: 3px; padding-left: 25px; color:#7E7E7E; font-family:'Courier'; font:bold; text-align:left; border:2px solid #BABABA;" }
                  },
  "addchum":  { "style": "background: black; border:2px solid #B3B3B3; font: bold; color: #BABABA; font-family:'Courier';"
              },
  "pester": { "style": "background: black; border:2px solid #B3B3B3; font: bold; color: #BABABA; font-family:'Courier';"
            },
  "block": { "style": "background: black; border:2px solid #B3B3B3; font: bold; color: #BABABA; font-family:'Courier';"
           },
  "moodlabel": { "style": "font:bold;font-family:'Courier';color:#C6C6C6;"
               },
  "defaultmood": 18,
  "moods": [
      { "style": "text-align:left; background:#BABABA;border:2px solid black;color: black; font-family:'Courier'; font:bold; padding-left:3px;", 
        "selected": "text-align:left; background:#C6C6C6; border:2px solid #222222; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
        "loc": [15, 485],
        "size": [30, 30],
        "text": "",
        "icon": "$path/chummy.png",
        "mood": 0
      },
      { "style": "text-align:left; background:#BABABA;border:2px solid black;color: black; font-family:'Courier'; font:bold; padding-left:3px;", 
        "selected": "text-align:left; background:#C6C6C6; border:2px solid #222222; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
        "loc": [45, 485],
        "size": [30, 30],
        "text": "",
        "icon": "$path/rancorous.png",
        "mood": 1
      },
      { "style": "text-align:left; background:#BABABA;border:2px solid black;color: black; font-family:'Courier'; font:bold; padding-left:3px;", 
        "selected": "text-align:left; background:#C6C6C6; border:2px solid #222222; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
        "loc": [75, 485],
        "size": [30, 30],
        "text": "",
        "icon": "$path/bemused.png",
        "mood": 22
      },
      { "style": "text-align:left; background:#BABABA;border:2px solid black;color: black; font-family:'Courier'; font:bold; padding-left:3px;", 
        "selected": "text-align:left; background:#C6C6C6; border:2px solid #222222; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
        "loc": [105, 485],
        "size": [30, 30],
        "text": "",
        "icon": "$path/pleasant.png",
        "mood": 3
      },
      { "style": "text-align:left; background:#BABABA;border:2px solid black;color: black; font-family:'Courier'; font:bold; padding-left:3px;", 
        "selected": "text-align:left; background:#C6C6C6; border:2px solid #222222; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
        "loc": [135, 485],
        "size": [30, 30],
        "text": "",
        "icon": "$path/distraught.png",
        "mood": 4
      },
      { "style": "text-align:left; background:#BABABA;border:2px solid black;color: black; font-family:'Courier'; font:bold; padding-left:3px;", 
        "selected": "text-align:left; background:#C6C6C6; border:2px solid #222222; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
        "loc": [165, 485],
        "size": [30, 30],
        "text": "",
        "icon": "$path/pranky.png",
        "mood": 5
      },
      { "style": "text-align:left; background:#BABABA;border:2px solid black;color: black; font-family:'Courier'; font:bold; padding-left:3px;", 
        "selected": "text-align:left; background:#C6C6C6; border:2px solid #222222; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
        "loc": [195, 485],
        "size": [30, 30],
        "text": "",
        "icon": "$path/smooth.png",
        "mood": 6
      },
      { "style": "text-align:left; background:#BABABA;border:2px solid black;color: black; font-family:'Courier'; font:bold; padding-left:3px;", 
        "selected": "text-align:left; background:#C6C6C6; border:2px solid #222222; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
        "loc": [15, 545],
        "size": [30, 30],
        "text": "",
        "icon": "$path/estatic.png",
        "mood": 7
      },

      { "style": "text-align:left; background:#BABABA;border:2px solid black;color: black; font-family:'Courier'; font:bold; padding-left:3px;", 
        "selected": "text-align:left; background:#C6C6C6; border:2px solid #222222; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
        "loc": [75, 545],
        "size": [30, 30],
        "text": "",
        "icon": "$path/relaxed.png",
        "mood": 8
      },

      { "style": "text-align:left; background:#BABABA;border:2px solid black;color: black; font-family:'Courier'; font:bold; padding-left:3px;", 
        "selected": "text-align:left; background:#C6C6C6; border:2px solid #222222; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
        "loc": [45, 545],
        "size": [30, 30],
        "text": "",
        "icon": "$path/discontent.png",
        "mood": 9
      },

      { "style": "text-align:left; background:#BABABA;border:2px solid black;color: black; font-family:'Courier'; font:bold; padding-left:3px;", 
        "selected": "text-align:left; background:#C6C6C6; border:2px solid #222222; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
        "loc": [45, 515],
        "size": [30, 30],
        "text": "",
        "icon": "$path/devious.png",
        "mood": 10
      },

      { "style": "text-align:left; background:#BABABA;border:2px solid black;color: black; font-family:'Courier'; font:bold; padding-left:3px;", 
        "selected": "text-align:left; background:#C6C6C6; border:2px solid #222222; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
        "loc": [75, 515],
        "size": [30, 30],
        "text": "",
        "icon": "$path/sleek.png",
        "mood": 11
      },

      { "style": "text-align:left; background:#BABABA;border:2px solid black;color: black; font-family:'Courier'; font:bold; padding-left:3px;", 
        "selected": "text-align:left; background:#C6C6C6; border:2px solid #222222; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
        "loc": [105, 515],
        "size": [30, 30],
        "text": "",
        "icon": "$path/detestful.png",
        "mood": 12
      },

      { "style": "text-align:left; background:#BABABA;border:2px solid black;color: black; font-family:'Courier'; font:bold; padding-left:3px;", 
        "selected": "text-align:left; background:#C6C6C6; border:2px solid #222222; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
        "loc": [135, 515],
        "size": [30, 30],
        "text": "",
        "icon": "$path/mirthful.png",
        "mood": 13
      },
      { "style": "text-align:left; background:#BABABA;border:2px solid black;color: black; font-family:'Courier'; font:bold; padding-left:3px;", 
        "selected": "text-align:left; background:#C6C6C6; border:2px solid #222222; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
        "loc": [165, 515],
        "size": [30, 30],
        "text": "",
        "icon": "$path/manipulative.png",
        "mood": 14
      },
      { "style": "text-align:left; background:#BABABA;border:2px solid black;color: black; font-family:'Courier'; font:bold; padding-left:3px;", 
        "selected": "text-align:left; background:#C6C6C6; border:2px solid #222222; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
        "loc": [195, 515],
        "size": [30, 30],
        "text": "",
        "icon": "$path/vigorous.png",
        "mood": 15
      },
      { "style": "text-align:left; background:#BABABA;border:2px solid black;color: black; font-family:'Courier'; font:bold; padding-left:3px;", 
        "selected": "text-align:left; background:#C6C6C6; border:2px solid #222222; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
        "loc": [225, 515],
        "size": [30, 30],
        "text": "",
        "icon": "$path/perky.png",
        "mood": 16
      },
      { "style": "text-align:left; background:#BABABA;border:2px solid black;color: black; font-family:'Courier'; font:bold; padding-left:3px;", 
        "selected": "text-align:left; background:#C6C6C6; border:2px solid #222222; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
        "loc": [255, 515],
        "size": [30, 30],
        "text": "",
        "icon": "$path/acceptant.png",
        "mood": 17
      },
      { "style": "text-align:left; background:#BABABA;border:2px solid black;color: black; font-family:'Courier'; font:bold; padding-left:3px;", 
        "selected": "text-align:left; background:#C6C6C6; border:2px solid #222222; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
        "loc": [15, 515],
        "size": [30, 30],
        "text": "",
        "icon": "$path/mystified.png",
        "mood": 19
      },
      { "style": "text-align:left; background:#BABABA;border:2px solid black;color: black; font-family:'Courier'; font:bold; padding-left:3px;", 
        "selected": "text-align:left; background:#C6C6C6; border:2px solid #222222; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
        "loc": [255, 485],
        "size": [30, 30],
        "text": "",
        "icon": "$path/amazed.png",
        "mood": 20
      },
      { "style": "text-align:left; background:#BABABA;border:2px solid black;color: black; font-family:'Courier'; font:bold; padding-left:3px;", 
        "selected": "text-align:left; background:#C6C6C6; border:2px solid #222222; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
        "loc": [225, 485],
        "size": [30, 30],
        "text": "",
        "icon": "$path/insolent.png",
        "mood": 21
      },
      { "style": "text-align:left; background:#BABABA;border:2px solid black;color: black; font-family:'Courier'; font:bold; padding-left:3px;", 
        "selected": "text-align:left; background:#C6C6C6; border:2px solid #222222; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
        "loc": [105, 545],
        "size": [30, 30],
        "text": "",
        "icon": "$path/protective.png",
        "mood": 18
      },
      { "style": "text-align:center; background:#7F7F7F;border:2px solid black;color: black; font-family:'Courier'; font:bold; padding-left:3px;", 
        "selected": "text-align:center; background:#C6C6C6; border:2px solid #222222; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
        "loc": [135, 545],
        "size": [150, 30],
        "text": "UNAVAILABLE",
        "icon": "$path/offline.png",
        "mood": 2
      }
  ]
},
 "convo": {
     "style": "background-color: #9B9B9B;border:2px solid black; font-family: 'Courier';",
     "chumlabel": { "style": "margin-bottom: 21px;background: #BABABA; color: black; border:0px; font-size: 14px;",
                    "text" : ":: contacting: $handle ::" },
     "textarea": {
         "style": "background: #DCDCDC;  font-size: 14px;font:bold; border:2px solid #B3B3B3;text-align:center; margin-right:10px; margin-left:10px;font-family: 'Courier'"
     },
  "input": { "style": "background: #919191; border:2px solid #BABABA;margin-top:5px; margin-right:10px; margin-left:10px; font-size: 12px;" },
     "tabwindow" : {
         "style": ""
     },
     "tabs": {
         "style": "",
         "selectedstyle": "",
         "newmsgcolor": "#414141"
     },
     "scrollbar": null
 },
 "memos":
 { "size": [600,425],
   "style": "background-color: #A6A65D;border:2px solid black; font-family: 'Courier';",
   "label": { "style": "margin-bottom: 21px;background: #C4C4C4; color: #2E2E2E; border:0px; font-size: 14px;"
            },
   "textarea": {
       "style": "background: #DCDCDC;  font-size: 14px;font:bold; border:2px solid #B3B3B3;text-align:center; margin-right:10px; margin-left:10px;font-family: 'Courier'"
   },
   "userlist": { "style": "border:2px solid #4B4B4B; background: #A9A9A9;font: bold;font-family: 'Courier';selection-background-color:#0D1032; font-size: 12px;  margin-left:0px; margin-right:10px;"
               },
   "input": { "style": "background: #A9A9A9; border:2px solid #B3B3B3;margin-top:5px; margin-right:10px; margin-left:10px; font-size: 12px;" },
   "time": { "text": { "style": " border: 2px solid #B3B3B3; background: #A9A9A9; font-size: 12px; margin-top: 5px; margin-right: 5px; margin-left: 5px; font-family:'Courier';font:bold;" 
                    },
             "buttons": { "style": "color: white; font: bold; border: 2px solid #B3B3B3; font: bold; font-size: 12px; background: #B3B3B3; margin-top: 5px; margin-right: 5px; margin-left: 5px; padding: 2px; width: 50px;" }
          },

   "tabs": {
       "style": "",
       "selectedstyle": "#B3B3B3",
       "newmsgcolor": "#414141",
       "tabstyle": 0
   },
   "scrollbar": null
 }
}
