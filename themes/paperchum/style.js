{"main":
 {"style": "",
  "background-image": "$path/paperbg.png",
  "size": [300,620],
  "icon": "$path/trayicon.png",
  "newmsgicon": "$path/trayicon2.png",
  "windowtitle": "PAPERCHUM",
  "menu" : { "style": "font-family: 'arial'; font-size: 12px; color: #3e240d; background-color: #9b896c;border:1px solid #3f3a32",
             "menuitem": "margin-right:10px;",
             "selected": "background-color: #594731",
             "disabled": "color: tan",
             "loc": [9,10]
           },
	"menubar": { "style": "font-family: 'arial';  font-size: 14px; color: #000000;" },
   "menus": {"client": {"_name": "            ",
                       "options": "Options",
                       "memos": "Memos",
                       "logviewer": "Library",
                       "randen": "Random Encounter",
                       "userlist": "Userlist",
                       "addgroup": "Add Group",
                       "import": "Import",
                       "reconnect": "Reconnect",
                       "idle": "Idle",
                       "exit": "Log Off"},
            "profile": {"_name": "           ",
                        "switch": "Switch",
                        "color": "Color",
                        "theme": "Theme",
                        "block": "Block List",
                        "quirks": "Quirks"},
            "help": { "_name": "            ",
                      "about": "About",
                      "help": "Help",
                      "calsprite": "Calsprite",
                      "nickserv": "Nickserv" },
            "rclickchumlist": {"pester": "Message",
                               "removechum": "Remove",
                               "report": "Report",
                               "blockchum": "Block",
                               "addchum": "Add",
                               "viewlog": "View Pesterlogs",
                               "notes": "Edit Notes",
                               "unblockchum": "Unblock",
                               "removegroup": "Remove Group",
                               "renamegroup": "Rename Group",
                               "movechum": "Move",
                               "banuser": "Ban",
                               "opuser": "Give OP",
                               "voiceuser": "Give Voice",
                               "quirkkill": "Kill Quirk",
                               "quirksoff": "Quirks Off",
							   "ooc": "OOC",
                               "invitechum": "Invite",
                               "memosetting": "Memo Settings",
                               "memonoquirk": "Disable Quirks",
                               "memohidden": "Hidden",
                               "memoinvite": "Invite Only",
                               "memomute": "Mute Memo"
                              }
           },
  "close": { "image": "$path/m.png",
             "loc": [278, 9]},
  "minimize": { "image": "$path/m.png",
                "loc": [262, 9]},
  "chums": { "style": "background:  url($path/chumbg.png) repeat-x top left; background-attachment: fixed;border:0px solid dicks;font-size:14px;font-family: 'arial'; color: #3e240d",
				
				
				"loc": [12, 110],
				"size": [278, 339],
				
				

				"moods": {

                 "chummy": { "icon": "$path/chummy.png", "color": "#3e240d" },

                 "rancorous": { "icon": "$path/rancorous.png", "color": "#3e240d" },

                 "offline": { "icon": "$path/offline.png", "color": "#1f1308"},


                 "pleasant": { "icon": "$path/pleasant.png", "color": "#3e240d" },

                 "distraught": { "icon": "$path/distraught.png", "color": "#3e240d" },

                 "pranky": { "icon": "$path/pranky.png", "color": "#3e240d" },


                 "smooth": { "icon": "$path/smooth.png", "color": "#3e240d" },

                 "mystified": { "icon": "$path/mystified.png", "color": "#3e240d" },

                 "amazed": { "icon": "$path/amazed.png", "color": "#3e240d" },

                 "insolent": { "icon": "$path/insolent.png", "color": "#3e240d" },

                 "bemused": { "icon": "$path/bemused.png", "color": "#3e240d" },


                 "ecstatic": { "icon": "$path/ecstatic.png", "color": "#3e240d" },

                 "relaxed": { "icon": "$path/relaxed.png", "color": "#3e240d" },

                 "discontent": { "icon": "$path/discontent.png", "color": "#3e240d" },

                 "devious": { "icon": "$path/devious.png", "color": "#3e240d" },

                 "sleek": { "icon": "$path/sleek.png", "color": "#3e240d" },

                 "detestful": { "icon": "$path/detestful.png", "color": "#3e240d" },

                 "mirthful": { "icon": "$path/mirthful.png", "color": "#3e240d" },

                 "manipulative": { "icon": "$path/manipulative.png", "color": "#3e240d" },

                 "vigorous": { "icon": "$path/vigorous.png", "color": "#3e240d" },

                 "perky": { "icon": "$path/perky.png", "color": "#3e240d" },

                 "acceptant": { "icon": "$path/acceptant.png", "color": "#3e240d" },

                 "protective": { "icon": "$path/protective.png", "color": "#3e240d" },

                 "blocked": { "icon": "$path/blocked.png", "color": "red" }
                         }
						 
           },
		   
  "trollslum": {
      "style": "background: #9b896c; border:1px solid #4d4b48; font-family: 'Arial'",
      "size": [195, 200],
      "label": { "text": "Block List",
                 "style": "color: #3e240d; font-family: 'Arial';border:0px;" },
      "chumroll": {"style": "border:1px solid #4d4b48; background-color: #9b896c;color: 3e240d; font-family: 'Arial';selection-background-color:#314159; " }
  },
		   
	"mychumhandle": { 
            "handle": { "loc": [40,507],
                    "size": [233, 18],
                    "style": "background: transparent; color: #614023; font-family:'arial'; text-align:left;"
                                                        },
                    "colorswatch": { "loc": [262,507],
                                     "size": [25,20],
                                     "text": "C" },
                    "currentMood": [21, 508]
                  },
	"defaultwindow": { "style": "background: #9b896c; color: #3e240d; font-family:arial;selection-background-color:#314159; "
                   },
				  
  "addchum":  { "style": "background: transparent;",
                "loc": [19,462],
                "size": [102, 17]
              },
  "pester": { "style": "background:  transparent;",
              "loc": [0,0],
              "size": [0, 0]
            },
  "block": { "style": "background: transparent;",
             "loc": [172,462],
             "size": [105, 17]
           },
  "defaultmood": 1,
  "moodlabel": { "style": "",
                                 "loc": [20, 430],
                                 "text": ""
                           },   
  "moods": [
      { "style": "text-align:left; background:#9b896c; color: #4c2f13; font-family:'arial';  padding-left:3px;",
                "selected": "text-align:left; background: #314159; color: #4c2f13; font-family:'arial';  padding-left:3px;",
                "loc": [17, 537],
                "size": [80, 18],
            "text": "Chummy",
                "icon": "$path/chummy.png",
                "mood": 0
          },

      { "style": "text-align:left; background:#9b896c; color: #4c2f13; font-family:'arial';  padding-left:3px;",
                "selected": "text-align:left; background: #314159; color: #4c2f13; font-family:'arial';  padding-left:3px;",
                "loc": [17, 559],
                "size": [80, 18],
            "text": "Pleasant",
                "icon": "$path/pleasant.png",
                "mood": 3
          },

      { "style": "text-align:left; background:#9b896c; color: #4c2f13; font-family:'arial';  padding-left:3px;",
                "selected": "text-align:left; background: #314159; color: #4c2f13; font-family:'arial';  padding-left:3px;",
                "loc": [17, 581],
                "size": [80, 18],
            "text": "Rancorous",
                "icon": "$path/rancorous.png",
                "mood": 1
          },

      { "style": "text-align:left; background:#9b896c; color: #4c2f13; font-family:'arial';  padding-left:3px;",
                "selected": "text-align:left; background: #314159; color: #4c2f13; font-family:'arial';  padding-left:3px;",
                "loc": [110, 537],
                "size": [90, 18],
            "text": "Pranky",
                "icon": "$path/pranky.png",
                "mood": 5
          },

      { "style": "text-align:left; background:#9b896c; color: #4c2f13; font-family:'arial';  padding-left:3px;",
                "selected": "text-align:left; background: #314159; color: #4c2f13; font-family:'arial';  padding-left:3px;",
                "loc": [110, 559],
                "size": [90, 18],
            "text": "Smooth",
                "icon": "$path/smooth.png",
                "mood": 6
          },
		  
      { "style": "text-align:left; background:#9b896c; color: #4c2f13; font-family:'arial';  padding-left:3px;",
                "selected": "text-align:left; background: #314159; color: #4c2f13; font-family:'arial';  padding-left:3px;",
                "loc": [110, 581],
                "size": [90, 18],
            "text": "Relaxed",
                "icon": "$path/relaxed.png",
                "mood": 8
          },		  

      { "style": "text-align:left; background:#9b896c; color: #4c2f13; font-family:'arial';  padding-left:3px;",
                "selected": "text-align:left; background: #314159; color: #4c2f13; font-family:'arial';  padding-left:3px;",
                "loc": [190, 537],
                "size": [90, 18],
				"text": "Insolent",
                "icon": "$path/insolent.png",
                "mood": 21
          },
		  

      { "style": "text-align:left; background:#9b896c; color: #4c2f13; font-family:'arial';  padding-left:3px;",
                "selected": "text-align:left; background: #314159; color: #4c2f13; font-family:'arial';  padding-left:3px;",
                "loc": [190, 559],
                "size": [90, 18],
            "text": "Devious",
                "icon": "$path/devious.png",
                "mood": 10
          },		  
		  
      { "style": "text-align:left; background:black;color: #1f1308; font-family:'arial'; padding-left:3px;",
                "selected": "text-align:left; background: #314159; color: #1f1308; font-family:'arial';  padding-left:3px;",
                "loc": [190, 581],
                "size": [90, 18],
                "text": "Abscond",
                "icon": "$path/offline.png",
                "mood": 2
          }
  ]
 },
  "convo":
 {"style": "background: #9b896c; font-family: 'Arial'; font-size: 14px; ",
  "scrollbar": { "style" : "", "handle": "" },
  "margins": {"top": 5, "bottom": 9, "left": 10, "right": 10 },
  "size": [500,425],
  "chumlabel": { "style": "font-size: 12px;background-color: #9b896c; color: #86b5d9; padding-left: 3px;",
                 "align": { "h": "left", "v": "center" },
                 "minheight": 0,
                 "maxheight": 0,
                 "text" : ""
               },
  
  "tabwindow" : {
      "style": "background: #eeeae2 url($path/othertabbg.png) repeat-x top left; font-family: Arial;"
  },
  "textarea": {
      "style": "background: #eeeae2 url($path/textbg.png) repeat-x top left; background-attachment: fixed; border:1px solid #4d4b48; font-size: 14px; color: #5d5044; margin-top: 10px;"
  },
  "input": {
      "style": "background: #baac96; margin-top:5px; border:1px solid #4d4b48; font-size: 12px; color: #3c3228; "
  },
  
  "tabs": {
      "style": "background: #504031; color: #a6a4a1; height: 21px; margin: 3px 1px 0px 1px; padding-left: 3px; padding-bottom: 3px;",
      "selectedstyle": "background: #eeeae2 url($path/tabbg.png) repeat-x top left; color: #f7fffd; padding-bottom: 10px",
       "newmsgcolor": "#FF724C",
       "tabstyle": 0
	   
  },
  "text": {
      "beganpester": "began messaging",
      "ceasepester": "stopped messaging",
      "blocked": "blocked",
      "unblocked": "mercifully forgave",
      "openmemo": "opened memo on board",
      "joinmemo": "responded to memo",
      "closememo": "ceased responding to memo",
      "kickedmemo": "You have been banned from this memo!"
  },
  "systemMsgColor": "#4c2f13"
 },
 "memos":
 {"size": [500,325],
 "memoicon": "$path/memo.png",
  "style": "background: #ffffff url($path/textbg.png); border:1px solid #4d4b48; font-family: 'arial';",
  "tabs": {
      "style": "",
      "selectedstyle": "",
       "newmsgcolor": "#FF724C",
       "tabstyle": 0
	   
  },
    "tabwindow" : {
      "style": "background: #9b896c; font-family: Arial;"
  },

  "scrollbar": { "style" : "background: transparent; padding-top:17px; padding-bottom:17px;width: 13px; border:0px;",
                 "handle": "background:#9b896c url($path/scrollhandle.png) no-repeat center center;min-height:24px;padding-top:1px;padding-bottom:1px;",
                 "downarrow": "background: #eeeae2;height:17px;",
                 "darrowstyle": "image:url($path/downarrow.png);",
                 "uparrow": "background: #eeeae2;height:17px;",
                 "uarrowstyle": "image:url($path/uparrow.png);"
               },
  "label": { "text": "Bulletin Board: $channel",
             "style": "margin-bottom: 21px;background: #9b896c; color: #59432a; border:0px; font-size: 14px;",
             "align": { "h": "center", "v": "center" },
             "minheight": 47,
             "maxheight": 47
           },
  "input": { "style": "background: #eeeae2; color: #5d5044; border:1px solid #4d4b48;margin-top:5px; margin-right:10px; margin-left:10px; font-size: 12px;" },
  "textarea": { "style": "background: #eeeae2; font-size: 14px; border:1px solid #4d4b48;text-align:center; margin-right:10px; margin-left:10px;" },
  "margins": {"top": 0, "bottom": 6, "left": 0, "right": 0 },
  "userlist": { "width": 150,
                "style": "background: #eeeae2; border:1px solid #4d4b48; font-size: 14px; color: #5d5044; selection-background-color:#646464; margin-left:0px; margin-right:10px;"
              },
  "time": { "text": { "width": 75,
                      "style": "color: #818181; border: 1px solid #4d4b48; background: #eeeae2; font-size: 12px; margin-top: 5px; margin-right: 18px; font-family:'arial';"
                    },
            "slider": { "style": " border:0px solid #c2c2c2;margin-top:3px;",
                        "groove": "border-image:url($path/timeslider.png);",
                        "handle": "image:url($path/handle.png);"
                      },
            "buttons": { "style": "color: #818181;  border: 1px solid #4d4b48;  font-size: 12px; background: #eeeae2; margin-top: 5px; margin-right: 5px; margin-left: 0px; width: 50px;" },
            "arrows": { "left": "$path/leftarrow.png",
                        "right": "$path/rightarrow.png",
                        "style": " border:0px; margin-top: 5px; margin-right:10px;background: #eeeae2;"
                      }
          },
  "systemMsgColor": "#4c2f13",
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
   "content": { "style": "background: black; color: white; padding: 5px;" }
 }
}