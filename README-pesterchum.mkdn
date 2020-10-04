Welcome to Pesterchum 3.41!
=============================

WHAT'S NEW?
-----------
* Check out the CHANGELOG file to see what's changed!

What do I do now?
-----------------

Most questions can be answered by visiting the forums! Go to HELP->HELP
and you'll be transported to the proper thread!

Here's some tips to help you get started:
-----------------------------------------

- Some themes can be confusing if you haven't used the program
already! Some hints:
    * Trollian: Moods are set by clicking the timelines, and you
can add chums by clicking "Chumproll." Moods correspond to the troll
that would most likely exhibit them. You can go offline by hitting the
"Timelines" menu bar.

    * Gold: Add chums by hitting the two chumpeoples in the upper left
corner. Go offline by clicking the "CHUMHANDLE:" label.

    * Enamel: Add chums by hitting the "CHUMROLL" label. Go offline by
clicking the upper left hand corner.

- Right-click is your friend! There are useful right click
options on the chumroll, by clicking the chumhandle in a conversation,
online userlist, or the list of memo browsers.

Cool features:
--------------

- Profile switching. Instantly switch profiles, loading your color and
quirks with it.
- Theme switching and creation. So far this comes with a few official
themes! But you can also make your own: just make a new directory in
the themes folder with the proper images and style.js file. The
style.js file will be documented soon, but feel free to poke at it.
- Memos. Memos that are a lot more like the ones in the comic and
allow you to appear at multiple times in one chat.
- Quirks: Prefix, suffix, simple replace, regexp replace (like in
2.5), random replacement, and an auto-mispeller :P
- Chum groups. Organize your chums into collapsible groups for easy
management.
- Block/user list
- Add/block chums directly from a conversation, the userlist, or memo
userlist.
- Timestamps saved in logs and shown in conversations if wanted.
- Logging. Logs are output in bbcode (for easy forum posting), html,
and plain text.
- Logviewer for easy log reading inside Pesterchum
- Idling. You can set yourself idle manually, and the computer will
set it for you after a configurable amount of time.
- Improved /me. Any letters immediately following /me will be
processed correctly. e.g. /me'd rather be fishing -> `-- ghostDunk'd
[GD'D] rather be fishing --`
- Hyperlinks! Now if someone types http://whatever it will turn into a
link you can just click and follow. No more copy/paste.
- Memo links. Link your friends to your memos.
- Smilies. We've added about 30-40 smilies from the forums. There is a
list later on in this readme.
- Submit quotes directly to the Pesterchum QDB!

FA%
---
__Q:__ Norton says it has a virus and then deletes it!  
__A:__ Read this helpful Norton FAQ:

Alright, here's a guide to by-passing Norton:

* First, to download Pesterchum:
    1. Make sure you're on a Moderator account. Moreso for the Norton steps than these ones.
    2. Download the .zip file, not the .exe file.
    3. Unzip the .zip file onto memory. Pesterchum should now be installed.

* Now, to by-pass Norton:
    1. Make sure you're still on a moderator account.
    2. Open up Norton.
    3. Click on 'Settings' up in the upperright hand corner.
    4. Click on 'Anitivirus', off to the upper left. It has a small image of a needle or something similar off to it's side.
    5. There's a word that reads 'SONAR protection' halfway to the bottomleft. Off to it's right, there's a bar that's half green. Click on the bar.
    6. It will warn you about turning off SONAR. Have it set to turn back on when the system restarts.
    7. If done properly, the background for the main page of Norton(what you saw on steps 2-3) has turned an apocaliptic red. Feel free to close Norton now. Keep in mind to stay off suspicious online sites now.
    8. Open up Pesterchum, and let the chummy convos begin.

* When finished:
    1. Log off of Pesterchum. LOG OFF, NOT CLOSE IT.
    2. Then, you can either shut off your comp, and Norton will re-enable SONAR, or you can repeat steps 1-5, except turning the red bar green. If done right, Norton will be it's happy color again.
    3, Keep in mind that you must repeat all of this(other than the download) every time you want to get on Pesterchum.

* Hope this is helpful!

(This guide brought to you by the slightly combined efforts of empireomega and Xanaomin)

------------------------------------------------------------------------------------

__Q:__ I can't connect because my school/university/network/stolen wifi is blocking my connection! OR I can't seem to connect to the server at all and I'm not running any firewalls!  
__A:__ Edit your pesterchum.js file. Open it up in notepad or something, and then edit the beginning so it looks like this:

```
{"port": "1413", ....
```

where the .... is the rest of the gobbledygook there.

------------------------------------------------------------------------------------

__Q:__ The mood buttons on Pesterchum 6.0 don't match up to what it sets your mood to! What gives?  
__A:__ The mood names are just there to look canon. It is intentional.

------------------------------------------------------------------------------------

__Q:__ I'm appearing as offline to 2.5 users/other users appear the wrong
mood? What's happeninggggg  
__A:__ The 2.5 people decided to change the mood protocol. When I made
this program, I decided to go with Tinychat's original protocol (and
extend it). So some moods will appear wrong between 2.5
users. (\*COUGH\*tell them to switch to 3.14\*COUGH\*)

------------------------------------------------------------------------------------

__Q:__ Pesterchum 2.5 users don't get my /me messages correctly!  
__A:__ That's because they implemented the /me command differently.

------------------------------------------------------------------------------------

__Q:__ Can we resize the main window?  
__A:__ No. This is done so we can offer more flexible UI creation. It's a
lot easier to make themes that look canon this way.

------------------------------------------------------------------------------------

__Q:__ Can we have different chum rolls for different users?  
__A:__ No. Instead what we now have crum groups to organize people.

------------------------------------------------------------------------------------

__Q:__ Can we delete profiles?  
__A:__ Yes. Go to the profile switcher, choose a profile and press DELETE.

------------------------------------------------------------------------------------

__Q:__ You should make it so you can ban specific time frames in memos.  
__A:__ This was too complicated to implement, and I don't have the UI
quite figured out. This will probably go in a future update.


DOCUMENTATION
-------------

STARTING
--------

If this is your first time running Pesterchum 3.14, you need to create
a new profile. Just type in your chum handle in the box and click the
color swatch to pick your color. Check the "default" checkbox to make
this your default profile.

BASIC PESTERING
---------------

To begin pestering, first click the "ADD CHUM" button and type in
their pester handle. The handle must be all lower case except for one
capital letter. Once you've added that person, they will appear on
your chumroll. You can double click to begin pestering them, or
right-click to bring up a menu where you can pester them, block them,
or remove them from your chumroll. (Or you can select them and hit
"enter" OR hit the "PESTER" button.)

Once you begin pestering somebody (or they begin pestering you), it
will bring up the conversation window. Here you can type to your
chum. Also remember that if you right-click on the area just above the
Pesterlog, it will bring up a list of options: Quirks Off will turn
your quirks off, Add Chum will add this chum to your list, and Block
will block them. (Those last two options are useful if you are being
pestered by someone you don't have on your list yet!)

While pestering your chum, here are some useful features:

* Type /me to create a system message. "/me facepalms." will generate:
  
  ```
  -- ghostDunk [GD] facepalms. --
  ```

  You can also append 's after /me like so: "/me's computer exploded."

  ```
  -- ghostDunk's [GD'S] computer exploded. --
  ```

  In fact, any characters you type after a /me before the space will
  be added: "/meing is the Ghost Nation's official pastime."

  ```
  -- ghostDunking [GDING] is the Ghost Nation's official pastime. --
  ```

* Color tags! If you feel the need to talk about The Green Sun or add
  some appleberry blast to your conversation, just use color
  tags. These work like in TC 1.5: `<c=(color)>colored text</c>`. But in
  PC 3.14, you can type your color in a lot of different ways:
  
  - You can use the familiar r,g,b method:  
    `<c=0,255,0>The Green Sun</c>`
  - You can use HTML tags:  
    `<c=#7f7f7f>DURR I'M KARKAT AND I'M A HUGE IDIOT</c>`
  - You can even use [plain color names](http://en.wikipedia.org/wiki/Web_colors): 
    `<c=red>D4V3 TH1S 1S SO D3C4D3NT</c>`  
  - You don't even have to add the `</c>` if you are lazy. Just use a
    new color tag whenever you want to change colors and PC 3.14 will
    add the extra tags for you.

* URLs (anything with `http://` or `www.` in front of it) will automatically be
  detected and made into a link you can CLICK.

* You can also link people to memos by typing "#" and the name of the
  menu like so: #R41NBOW_RUMPUS_P4RTYTOWN  
  Clicking the link will open up the memo select menu.

* Smilies! There are a list of smilies at the end of this document;
  they are based on the MSPA Forum smilies.

* Don't worry about your quirks screwing up any of the above: PC will
  apply your quirks AFTER it figures out color codes, links, smilies, etc.

* Pressing the up arrow will cycle through a history of your comments,
  so if you want to retype something, you can pull it up.

* You can submit directly to the Pesterchum Quote Database! If you
  have a particualarly awesome conversation, you can submit it to the
  database by simply highlighting the good part of the conversation,
  right clicking it and choosing "Submit to Pesterchum QDB!"


MEMOS
-----

One of the most interesting features to make was the memos, and make
them as close to the comic as I could without actually inventing time
travel. So here is the TIME TUTORIAL:

* __Joining:__ When you go CLIENT->MEMOS, you'll see a list of memos pop up
-- those are memos people already have open. To join one, just
highlight one of them. If you want to make a new memo, just type it in
the input. If you'd like to make it secret, so that it doesn't appear
in the list, check "HIDDEN CHANNEL". Then, choose what timeframe you
want to appear to be in. So if you wanted to be in the future, you
could move the slider to the right. You can also enter the time
manually. Then hit JOIN.

* __Explaining time:__ Time in memos, unlike Homestuck, will not be relative
to your position. That is, if you choose 4:13 in the future, you will
not see someone who has set their time as "current" (or "0") in the
past: you will see them as "current" and yourself as "future." This is
because we do not have time travel! Memo time setting is basically an
RP mechanic: you are pretending to be from the future! It will also
help keep everyone straight: everyone will see the same thing!

* __The time slider:__ The slider shows your current position in the time
stream. If you want to change your time frame, simply move the slider
(or type a time in) and hit GO. This will open a new time frame, and
the next time you type a message, the memo will show that you've
responded to it in that time frame. You can now switch between your
time frames simply by clicking the arrows in the right hand
corner. (THIS COMES IN HANDY IF YOU WANT TO ARGUE WITH YOURSELF.) You
can have any number of open time frames, and the program will number
them in the order in which you open them (like in the comic). You can
have one of your time frames cease responding to the memo by hitting
"CLOSE." If you open that time frame again, the program will remember
the number it originally gave it. If you want to be mysteeeeeeeerious,
you can type in "?" and you will appear as ???.

* __The memo viewer list:__ To the right is a list of people currently
browsing the memo. A shade icon next to their name means they are the
"operator" of the memo: meaning they can kick ("ban") people from the
memo and make other people operators as well. A "ban" is not permanent
(like in the comic), and the program will ask if you want to reconnect
to the memo. You kick and op people by right clicking their name in
the window. You can also add them to your chumroll!

* __Inviting people to your memo:__ You can link to a memo by simply typing
"#nameofmemo" in any conversation or memo window. So you can say:

  ```
  CG: NOW YOU, ME, AND EGBERT NEED TO HAVE A CHAT.
  CG: CLICK IT.
  CG: #FRUITYRUMPUSASSHOLEFACTORY
  ```

  and it will appear as a link that you can click, which will open the
  memo chooser window.

CLIENT MENU
-----------

### OPTIONS: ###

* __Chum List__
    * __Hide Offline Chums:__ Turning this option on will hide all offline chums
    off your chumroll.

    * __Show Empty Groups:__ Turning this option on will show empty groups.

    * __Show Number of Online Chums:__ Show number of online chums in each group.

    * __Sort Chums:__ How would you like your chums sorted?

* __Conversations__
    * __Time Stamps:__ Turning this on will show timestamps in your chats.

    * __12/24 hour:__ Formatting for timestamps. Whether you want them in 12 or
    24 hour time.

    * __Show Seconds:__ Turning this on will show the seconds in your timestamps.

    * __Show OP and Voice Messages in Memos:__ Whether or not you would like
    to see messages when people gain/lose OP or Voice.

    * __Use animated smilies:__ To animate or not to animate.

* __Interface__
    * __Tabbed Conversations:__ Turns tabbed conversations on and off. Don't
    worry if you do this in the middle of a conversation, PC will save
    them for you.

    * __Minimize:__ What do you want the minimize button to do?

    * __Close:__ What do you want the close button to do?

* __Sound__
    * __Sounds On:__ Uncheck to shut it the fuck up.

    * __Pester Sounds:__ Uncheck to only turn off Pester sounds.

    * __Memo Sounds:__ Uncheck to only turn off Memo sounds.

    * __Memo Mentions:__ Check to have a separate noise when your initials
    get mentioned in a memo.

* __Logging__
    * __Log all Pesters:__ Log one-on-one chats.

    * __Log all Memos:__ Log everything said in memos.

    * __Log Time Stamps for Pesters__

    * __Log Time Stamps for Memos__

* __Idle/Updates__
    * __Minutes before Idle:__ How long before you should be considered idle.

    * __Check for Pesterchum Updates:__ How often to check for updates
    to Pesterchum.

    * __Check for MSPA Updates:__ Check the MSPA site for updates to comics.

* __Theme__
    * __Pick a Theme__

### MEMOS: ###

Opens the Memo list as above.

### USERLIST: ###

Shows a list of all the users that are currently logged onto
Pesterchum. Right-click their names and select "ADD CHUM" to add them
to your chum roll!

### IDLE: ###

Make yourself an idle chum. You will appear as idle until you
uncheck this box, or if you *actually* go idle (stop using the
computer) for 10 minutes and then come back.

### IMPORT: ###

Imports your old Pesterchum 2.0, 2.5 and Tinychum chum
rolls. This will also import your old quirks from Pesterchum 2.5.

### RECONNECT: ###

Forces PC to reconnect to the server.

### EXIT: ###

noooooooooooooooooooooooo


PROFILE MENU
------------

### QUIRKS: ###

Opens the quirks menu. More on that below!

### TROLLSLUM: ###

Opens up the window where you can view people you've
blocked. You can add and remove people to the list from here as well.

### COLOR: ####

Change your text color here!

### SWITCH: ###

Switch your profile! You can have any number of profiles, and
PC will save your color, quirks, and theme for that profile. Chumrolls
and block lists are the same for all profiles. Feel free to have
multiple instances of PC running on two or more handles!


HELP MENU
---------

### HELP: ###

Get taken to a handy dandy tutorial for Pesterchum!

### CALSPRITE: ###

Open a chat with calSprite (learn more about calSprite below).

### NICKSERV: ###

Open a chat with NickServ. If you don't know what NickServ is, you don't need to.

### ABOUT: ###

See which version of Pesterchum you have. Learn about all the awesome people
that helped bring Pesterchum 3.14 to you!

### REPORT BUG: ###

Report any bugs you come across so we can fix them and make Pesterchum
even better!


CALSPRITE
---------

calSprite is the bot that helps moderate canon handle usage! Simply pester
calSprite with the world "HELP" (turn your quirks off!) and you
will get instructions on how to use calSprite!


QUIRKS
------

There are six kinds of quirks! I'll teach you how to use them all!
(In this section, I will use quotes ("") around things so it's clearer
to see exactly what to type! Don't include these quotes when using
these examples!

Also, note that your quirks will not work until you save them by
hitting "OK" on the Quirk window.

* __Prefix/Suffix:__
  This will put text before or after everything you
  say. So for example, we can use prefixes to emulate part of Nepeta or
  Equius' quirks:

    ```
    PREFIX: ":33 < "
    You type: "*ac twitches her friendly whiskers at ct*"
    Result:
    AC: :33 < *ac twitches her friendly whiskers at ct*
    ```

    ```
    PREFIX: "D --> "
    You type: "Hi"
    Result:
    CT: D --> Hi
    ```

    Suffixes work the same way, but at the end of the message:

    ```
    SUFFIX: "!!!"
    You type: hey there
    Result:
    GD: hey there!!!
    ```

    Remember that it doesn't automatically add a space! You'll need to add
    it in (see CT and AC examples again!)

* __Simple Replace:__
This will simply take a set of characters and replace them with other
characters.
    * Let's add a quirk to our Nepeta:
    
    ```  
    Replace: "ee" With: "33"
    You type: "*ac saunters from her dark cave a little bit sleepy from
    the recent kill*"
    Result:
    AC: :33 < *ac saunters from her dark cave a little bit sl33py from the
    recent kill*
    ```

    * Let's add two to Equius:
    
    ```  
    Replace: "loo" With: "100"
    Replace: "x" With "%"
    You type: "look"
    Result:
    CT: D --> 100k
    ```

    ```
    You type: "What are you expecting to accomplish with this"
    Result:
    CT: D --> What are you e%pecting to accomplish with this
    ```

    * Aradia:
    
    ```  
    Replace: "o" With: "0"
    You type: "and the reward would be within our reach"
    Result:
    AA: and the reward w0uld be within 0ur reach
    ```

    Notice that it is CASE SENSITIVE. So in the above case, if you typed
    "ABSCOND", it would not replace the "O".

    * Sollux:
    
    ```  
    Replace: "i" With: "ii"
    Replace: "s" With: "2"
    ```

    * Eridan:
    
    ```  
    Replace: "v" With: "vv"
    Replace: "w" With: "ww"
    ```

    * Feferi:
    
    ```  
    Replace: "h" with: ")("
    Replace: "H" with: ")("
    Replace: "E" with: "-E"
    ```

* __Regexp Replace:__
This is a more complex kind of replacement. [Regexp](http://en.wikipedia.org/wiki/Regexp)
stands for "regular expression", a kind of programming language (yes, it is a language)
used to find and replace text. PC 3.14 also includes a few functions (`upper()`,
`lower()`, `scramble()`). If you want to learn it on your own,
I suggest you start with the [Python tutorial](http://docs.python.org/howto/regex.html)
since PC 3.14 uses Python's regexps. Check out V2.5's tutorial too, as that is a pretty
good start as well.

    * Let's start with Karkat. Regexps are just like your every day find and
    replace: they search for a string that matches what you want to
    replace, and replaces it with... the replacement.
    
    ```
    Regexp: "(.)" Replace with: "upper(\1)"
    ```

    Three concepts here. Let's look at the regexp. "(.)" has two things
    going on. The first is that ".". In regexp speak, "." is the wildcard:
    it will match *any* character -- and just one.

    The parentheses tell the regexp to *save* what's inside them so you
    can put it back when you replace. That's what the "\1" is for -- it
    means, "put the match inside parentheses #1 here". You can have any
    number of parentheses.

    * __"upper()"__ is a function special to PC 3.14 -- it will uppercase
    anything inside the parentheses. So in this case, upper will uppercase
    "\1" -- which, as you recall is what we found inside the
    parentheses. Which was *every* character. So to sum up, it replaces
    every character with an uppercase version of that character. WHICH
    MAKES YOU TALK LIKE THIS.

    * Let's look at Terezi next.
    
    ```
    Regexp: "[aA]" Replace with: "4"
    Regexp: "[iI]" Replace with: "1"
    Regexp: "[eE]" Replace with: "3"
    Regexp: "(.)" Replace with: "upper(\1)"
    ```

    We already know what the last line does. But what's up with those
    brackets? What's their deal? Basically, in regular expressions,
    brackets indicate a list of matching characters. So, basically any
    single character within the brackets will be matched. In this case,
    either "a" or "A" will be matched and replaced with "4," and likewise,
    "i" and "I" will be replaced with "1", and "e" and "E" will be
    replaced with "3."

    Just like there is an `upper()` function, there is also a `lower()`
    function. It acts just like `upper()` but instead makes everything
    inside the parentheses lowercase. This allows you to do things like:
    
    ```
    Regexp: "(.)" Replace with: "lower(\1)"
    You type: "I AM YELLING"
    Result:
    GD: i am yelling
    ```

    Along with the upper and lower functions is a `scramble()` function.
    The purpose of this function is to randomly scramble anything inside
    the parentheses.
    
    ```
    Regexp: "(\w)(\w*)(\w)" Replace with: "\1scramble(\2)\3"
    You type: "hello there"
    Result:
    GD: hlelo trhee
    ```

    This particular regular expression scrambles all of the letters in
    the middle of a word. Notice that the "h" and "o" at the beginning
    and end of hello remain in place while the other letters are scrambled.

    You should also know that "^" is a special character in brackets. If
    placed immediately after the opening bracket (like "[^"), then the
    brackets instead match every character *except* the ones in the
    brackets. So, for example, if you wanted to have a quirk where you
    capitalized all your letters *except* o, you'd do this:
    
    ```
    Regexp: "([^o])" Replace with: "upper(\1)"
    You type: "hello there"
    Result:
    GD: HELLo THERE
    ```

    You can also specify a *range* of characters inside the brackets, by
    using the "-" character. [a-z] will match any lowercase letter. You
    can combine them, too: [a-z0-9] will match any digit and lowercase letter.

    There are also different shortcuts for character types:
    
    ```
    \d matches any digit; same as [0-9]
    \D matches any non-digit; same as [^0-9]
    \s matches any spaces
    \S matches any non-space
    \w matches any alphanumeric character; same as [a-zA-Z0-9_]
    \W matches any non-alphanumeric character; same as [^a-zA-Z0-9_]

    Note \w and \W also match extended Latin or Unicode alphanumerics.
    ```

    You can include this inside brackets, too.

    There's also a special character, \\b. What \\b does is make sure that
    you are at the beginning or end of a word.
    * So with that knowledge, let's try Kanaya:
    
    ```
    Regexp: \b(\w) Replace with: upper(\1)
    You type: "i suggest you come to terms with it"
    Result:
    GA: I Suggest You Come To Terms With It
    ```

    Another feature of regular expressions is the ability to match
    *repeated* characters. There are three repeat characters: the "\*", the
    "+", "?", and "{m,n}". They work by playing them after the character,
    or character type you want to match. (So, you could say "\s+" or ".*")

    The "\*" character matches ZERO or more of that character. So, for
    example, "f\*" would match "", "f" and "ff" -- and any other character!
    That's right, every character counts as matching it zero times. Yeah,
    it's weird. I suggest you use...

    The "+" character matches ONE or more of that character. So, if we
    wanted to have a character that wanted to elongate their s's so that
    they used four 's's every time, like sssso, but didn't want to have
    eight s's when using words with double s's, like pass, we'd do this:
    
    ```
    Regexp: "s+" Replace with: "ssss"
    You type: "you shall not pass"
    Result:
    UU: you sssshall not passss
    ```

    As for the other two, I can't really think of any useful quirks to be
    made with them. But to let you know, "?" matches either 0 or 1 of that
    character, so "trolls?" would match "troll" and "trolls". "{m,n}"
    matches between m and n characters. (If you leave out 'n', any number
    of characters more than m will be matched: "s{3,}" will match 3 or more 's'.)
    So "s{2,4}" will match "ss", "sss", and "ssss" and that's it. 

    Also, "?" is equivalent to "{0,1}", "*" is equivalent to "{0,}", and
    "+" is equivalent to "{1,}".

    Now with repeating expressions, we can do something like make EVERY
    other WORD capitalized:
    
    ```
    Regexp: "(\w+) (\w+)" Replace with: "upper(\1) \2"
    You type: "this is pretty annoying i bet"
    Result:
    GD: THIS is PRETTY annoying I bet
    ```

    The \1 represents the first word -- which has been matched because the
    word is alphanumeric characters, repeated once or more -- and \2
    represents the second word.

    Another operator to use is the "|", which will match more than one set
    of characters. For example, "black|red" will match "black" or
    "red". If you want to match something in the middle of words, you have
    to use parentheses: "(black|red) romance" will match "black romance"
    and "red romance".

    Finally, there are the "^" and "$" characters. Yes, we already did the
    "^" character, but this is OUTSIDE of brackets, not INSIDE. "^"
    matches the beginning of a message, and "$" matches the end of it. You
    can use this to make more sophisticated prefix and suffix
    behaviors. For example, if we have a quirk that adds "..." to the end
    of all our messages, we can set it up so it doesn't do that if we put
    punctuation [?!.] at the end. So:
    
    ```
    Regexp: "([^?!.])$" Replace with: "\1..."
    ```

    This will match the end of any message as long as it doesn't have
    "?", "!", or "." at the end. Then it will replace it with whatever the
    last character of the sentence was (remember we're replacing it, so we
    have to put it back!) and add "..." at the end.

    Careful with the beginning and ending replaces -- if you use more than
    one, you may not get what you expect because they will ALL be applied,
    one after the other! This is a bug in my opinion, that I plan to fix!

* __Random replace:__
  Just like the regexp replace, except that instead of just one thing to
  replace it with, you give it a list. PC will then choose from that
  list randomly. So let's say I want to randomly end my sentences with
  either "bro" or "dog":
    
    ```
    Regexp: "$" Replace with: "bro" and "dog"
    ```

    * You can also imitate Araida's random "ribbits" in between words:
    
    ```
    Regexp: "\s" Replace with: " ribbit ", " ", " ", " ", " ", " ", etc....
    ```

      where " " is just a blank space added a bunch of times. (You can see
      how many blank spaces you've added by clicking on the list.) You have
      to add the spaces because each entry has the same chance of being
      selected. (Yes, I know this could be improved.) If you add " ribbit "
      and 9 spaces, " ribbit " will have a 1/10 chance of being picked.

    Also note that if you add more than one prefix or more than one
    suffix, it will pick randomly from them instead of adding them both!

* __Mispeller__:
Be careful with thsi one. The mispeller will randomly mispell x% of
the words you type -- where x is the percentage you set the slider
to. I have attempted to mimic SBaHJ mispelling style but whoof knows
what will happen oh god ive created a mosnter


SMILIES
-------
Here's a list of smilies:

* `:rancorous:`
* `:apple:`
* `:bathearst:`
* `:cathearst:`
* `:woeful:`
* `:pleasant:`
* `:blueghost:`
* `:slimer:`
* `:candycorn:`
* `:cheer:`
* `:duhjohn:`
* `:datrump:`
* `:facepalm:`
* `:bonk:`
* `:mspa:`
* `:gun:`
* `:cal:`
* `:amazedfirman:`
* `:amazed:`
* `:chummy:`
* `:cool:`
* `:smooth:`
* `:distraughtfirman:`
* `:distraught:`
* `:insolent:`
* `:bemused:`
* `:3:`
* `:mystified:`
* `:pranky:`
* `:tense:`
* `:record:`
* `:squiddle:`
* `:tab:`
* `:beetip:`
* `:flipout:`
* `:befuddled:`
* `:pumpkin:`
* `:trollcool:`
* `:jadecry:`
* `:ecstatic:`
* `:relaxed:`
* `:discontent:`
* `:devious:`
* `:sleek:`
* `:detestful:`
* `:mirthful:`
* `:manipulative:`
* `:vigorous:`
* `:perky:`
* `:acceptant:`
* `:olliesouty:`
* `:billiards:`
* `:billiardslarge:`
* `:whatdidyoudo:`
