{"inherits": "trollian",
 "main":
 {"style": "background-color:rgba(0,0,0,0); background-repeat: no-repeat;",
  "background-image": "$path/tnbg2.png",
  "size": [650, 450],
  "icon": "$path/trayicon.png",
  "newmsgicon": "$path/trayicon2.png",
  "windowtitle": "TROLLIAN",
  "close": { "image": "$path/x.png",
             "loc": [639, 4]},
  "minimize": { "image": "$path/m.png",
                "loc": [625, 10]},
  "sounds": { "alertsound": "$path/alarm.wav",
              "memosound": "$path/alarm2.wav"},
  "chums": { "scrollbar": { "handle": "background-color:#13cae0;height:20px;border:2px solid #12c4ff;" }
           },
  "defaultmood": 10
 },
 "convo":
 {"style": "background: #04a6be; font-family: 'Arial';",
  "scrollbar": { "style" : "", "handle": "" },
  "margins": {"top": 22, "bottom": 9, "left": 10, "right": 4 },
  "size": [400, 250],
  "size": [400, 250],
  "chumlabel": { "style": "background-image:url($path/chumlabelbg.png);background-color:#12e6ff; background-repeat: no-repeat; color: white; padding: 2px; border:1px solid #c2c2c2; margin-bottom: 4px;"
               },
  "tabwindow" : {
    "style": "background: #04a6be; font-family: 'Arial'"
  },
  "tabs": {
      "style": "",
      "selectedstyle": "",
      "newmsgcolor": "#04a6be",
      "tabstyle": 0
  }
 },
 "memos":
 {"style": "background-color: #04a6be; font-family: 'Arial';",
  "size": [450,300],
  "tabs": {
      "style": "",
      "selectedstyle": "",
      "newmsgcolor": "#04a6be",
      "tabstyle": 0
  },
  "label": { "text": "Bulletin Board: $channel",
             "style": "background-image:url($path/chumlabelbg.png);background-color:#12e6ff; background-repeat: no-repeat; color: white; padding: 2px; border:1px solid #c2c2c2; margin-bottom: 4px;"
           },
  "time": { "text": { "width": 75,
                      "style": "color: black; font:bold;  border:1px solid #c2c2c2; background: white; height: 19px;"
                    },
            "slider": { "style": " border:1px solid #c2c2c2;",
                        "groove": "border-image:url($path/timeslider.png);",
                        "handle": "image:url($path/aquaicon.png);"
                      },
            "buttons": { "style": "border:1px solid #68a1a6; height: 17px; width: 50px; color: #8fc6cd; font-family: 'Arial'; background: #04a6be; margin-left: 2px;" },
            "arrows": { "left": "$path/leftarrow.png",
                        "right": "$path/rightarrow.png",
                        "style": "width: 19px; height: 19px; border:0px; margin-left: 2px;"
                      }
          }
 }
}
