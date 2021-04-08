{"inherits": "pesterchum",
 "main":
 {"style": "",
  "background-image": "$path/pcbg.png",
  "size": [300,620],
  "icon": "$path/trayicon.png",
  "newmsgicon": "$path/trayicon2.png",
  "windowtitle": "PESTERCHUM",
  "menu" : { "style": "font-family: 'Courier'; font: bold; font-size: 14px; color: #000000; background-color: #fdb302;border:2px solid #ffff00",
                         "menuitem": "font-size:14px;" },
  "menubar": { "style": "font-family: 'Courier'; font:bold; font-size: 14px; color: #000000;" },
  "close": { "image": "$path/x.png",
             "loc": [286, 6]},
  "minimize": { "image": "$path/m.png",
                "loc": [268, 12]},
  "chums": { "style": "border:2px solid yellow; background-color: black;color: white;font: bold;font-size:14px;font-family: 'Courier';selection-background-color:#646464; ",
                         "loc": [15, 70],
                         "size": [270, 300]
           },
  "mychumhandle": { "label":
                    { "text": "CHUMHANDLE:",
                      "loc": [12,415],
                      "style": "color: black; font:bold; font-family: 'Courier';"
                    },
                    "handle": { "loc": [15,435],
                                "size": [240, 25],
                                                                "style": "background-color: black; padding: 3px; padding-left: 25px; color:white; font-family:'Courier'; font:bold; text-align:left; border:2px solid #ffff00;"
                                                          },
                    "colorswatch": { "loc": [255,435],
                                     "size": [30,25],
                                     "text": "C" },
                    "currentMood": [20, 440]
                  },
  "addchum":  { "style": "background: rgba(255, 255, 0, 100%); border:2px solid #c48a00; font: bold; color: black; font-family:'Courier';",
                "loc": [15,380],
                "size": [90, 30],
                "text": "ADD CHUM"
              },
  "pester": { "style": "background:  rgba(255, 255, 0, 100%); border:2px solid #c48a00; font: bold; color: black; font-family:'Courier';",
              "loc": [193,380],
              "size": [89, 30],
              "text": "PESTER!"
            },
  "block": { "style": "background: #F00000; border:2px solid #c48a00; font: bold; color: black; font-family:'Courier';",
             "loc": [104,380],
             "size": [90, 30],
             "text": "BLOCK"
           },
  "moodlabel": { "style": "font:bold;font-family:'Courier';color:black;",
                                 "loc": [12, 466],
                                 "text": "MOOD:"
                           },
  "moods": [
      { "style": "text-align:left; background:#ffff00;border:2px solid #c48a00;color: black; font-family:'Courier'; font:bold; padding-left:3px;",
                "selected": "text-align:left; background:white; border:2px solid #c48a00; color: black; font-family:'Courier'; font:bold; padding-left:3px;",
                "loc": [15, 485],
                "size": [135, 30],
            "text": "CHUMMY",
                "icon": "$path/chummy.png",
                "mood": 0
          },

      { "style": "text-align:left; background:#ffff00;border:2px solid #c48a00;color: black; font-family:'Courier'; font:bold;padding-left:3px;",
                "selected": "text-align:left; background:white; border:2px solid #c48a00; color: black; font-family:'Courier'; font:bold;padding-left:3px;",
                "loc": [15, 513],
                "size": [135, 30],
            "text": "PLEASANT",
                "icon": "$path/pleasant.png",
                "mood": 3
          },

      { "style": "text-align:left; background:#ffff00;border:2px solid #c48a00;color: black; font-family:'Courier'; font:bold;padding-left:3px;",
                "selected": "text-align:left; background:white; border:2px solid #c48a00; color: black; font-family:'Courier'; font:bold;padding-left:3px;",
                "loc": [15, 541],
                "size": [135, 30],
            "text": "DISTRAUGHT",
                "icon": "$path/distraught.png",
                "mood": 4
          },

      { "style": "text-align:left; background:#ffff00;border:2px solid #c48a00;color: black; font-family:'Courier'; font:bold;padding-left:3px;",
                "selected": "text-align:left; background:white; border:2px solid #c48a00; color: black; font-family:'Courier'; font:bold;padding-left:3px;",
                "loc": [148, 485],
                "size": [135, 30],
            "text": "PRANKY",
                "icon": "$path/pranky.png",
                "mood": 5
          },

      { "style": "text-align:left; background:#ffff00;border:2px solid #c48a00;color: black; font-family:'Courier'; font:bold;padding-left:3px;",
                "selected": "text-align:left; background:white; border:2px solid #c48a00; color: black; font-family:'Courier'; font:bold;padding-left:3px;",
                "loc": [148, 513],
                "size": [135, 30],
            "text": "SMOOTH",
                "icon": "$path/smooth.png",
                "mood": 6
          },

      { "style": "text-align:left; background:#f00000;border:2px solid #c48a00;color: black; font-family:'Courier'; font:bold;padding-left:3px;",
                "selected": "text-align:left; background:white; border:2px solid #c48a00; color: red; font-family:'Courier'; font:bold;padding-left:3px;",
                "loc": [148, 541],
                "size": [135, 30],
            "text": "RANCOROUS",
                "icon": "$path/rancorous.png",
                "mood": 1
          },

      { "style": "text-align:center; border:2px solid #c48a00; background:black;color: white; font-family:'Courier'; font:bold;padding-left:3px;",
                "selected": "text-align:left; background:white; border:2px solid #c48a00; padding: 5px;color: black; font-family:'Courier'; font:bold;padding-left:3px;",
                "loc": [15, 569],
                "size": [270, 30],
                "text": "ABSCOND",
                "icon": "$path/offline.png",
                "mood": 2
          }
  ]
 },
 "convo": {
     "style": "background-color: #fdb302;border:2px solid yellow; font-family: 'Courier';",
     "tabstyle": "background-color: #fdb302; font-family: 'Courier'",
     "size": [487, 466],
     "chumlabel": { "style": "margin-bottom: 21px;background: rgb(196, 138, 0); color: white; border:0px; font-size: 14px;",
                    "align": { "h": "center", "v": "center" },
                    "minheight": 47,
                    "maxheight": 65
                  }
 },
 "memos":
 { "size": [600,425] }
}
