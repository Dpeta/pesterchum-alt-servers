import json, logging, re, time, urllib, zipfile
try:
    import tarfile
except:
    tarfile = None
import os, sys, shutil
from pnc.dep.attrdict import AttrDict

logger = logging.getLogger(__name__)

USER_TYPE = "user"
                  # user - for normal people
                  # beta - for the original beta testers
                  # dev  - used to be for git users, now it's anyone with the 3.41 beta
                  # edge - new git stuff. bleeding edge, do not try at home (kiooeht version)

INSTALL_TYPE = "installer"
                  # installer - Windows/Mac installer     (exe/dmg)
                  # zip       - Windows zip               (zip)
                  # source    - Win/Linux/Mac source code (zip/tar)

OS_TYPE = sys.platform # win32, linux, darwin
if OS_TYPE.startswith("linux"):
    OS_TYPE = "linux"
elif OS_TYPE == "darwin":
    OS_TYPE = "mac"

# These will eventually be phased out
_pcMajor = "3.41"
_pcMinor = "4"
_pcStatus = "A" # A  = alpha
                # B  = beta
                # RC = release candidate
                # None = public release
_pcRevision = "13"
_pcVersion = ""

_updateCheckURL = "https://github.com/karxi/pesterchum/raw/master/VERSION.js"
_downloadURL = "https://github.com/karxi/pesterchum/archive/master.zip"

jsodeco = json.JSONDecoder()

# Whether or not we've completed an update (requires a restart).
has_updated = False

# Not 100% finished - certain output formats seem odd
def get_pchum_ver(raw=0, pretty=False, file=None, use_hard_coded=None):
    # If use_hard_coded is None, we don't care. If it's False, we won't use it.
    getrawlines = lambda fobj: [ x.strip() for x in fobj.readlines() ]
    if file:
        # Don't fall back onto defaults if we were given a file.
        use_hard_coded = False

    try:
        if use_hard_coded:
            # This is messy code, but we just want it to work for now.
            raise ValueError

        if file:
            # Leave closing this to the caller.
            raw_ver = getrawlines(file)
        else:
            # Open our default file ourselves.
            with open("VERSION.js", 'r') as fo:
                raw_ver = getrawlines(fo)
        raw_ver = ' '.join(raw_ver)
        # Now that we have the actual version, we can just set everything up
        # neatly.
        ver = jsodeco.decode(raw_ver)
        ver = AttrDict( (k.encode('ascii'), v) for k, v in ver.items() )
        # Do a bit of compensation for the unicode part of JSON.
        ver.status, ver.utype = str(ver.status), str(ver.utype)
    except:
        if use_hard_coded == False:
            # We refuse to use the hard-coded values, period.
            raise

        global _pcMajor, _pcMinor, _pcStatus, _pcRevision, USER_TYPE
        ver = AttrDict({
            "major": _pcMajor, "minor": _pcMinor,
            "status": _pcStatus, "rev": _pcRevision,
            "utype": USER_TYPE
            })

    ver.major = float(ver.major)
    ver.minor = int(ver.minor)
    if not ver.status:
        ver.status = None
    ver.rev = int(ver.rev)
    if raw:
        if raw > 1:
            # Give the AttrDict.
            return ver
        else:
            # Give a tuple.
            return (ver.major, ver.minor, ver.status, ver.rev, ver.utype)
    # Compose the version information into a string.
    # We usually specify the format for this pretty strictly.
    # We wnat it to look like "3.14.01-A07", for example.
    elif pretty:
        if pretty > True:
            # True == 1; we get here if pretty is greater than 1
            if ver.utype == "edge":
                # If this is an edge build, the other types don't really
                # matter.
                ver.status = "Bleeding Edge"
            else:
                statuses = {
                        # These are slightly unnecessary, but....
                        "A":    "Alpha",
                        "B":    "Beta",
                        "RC":   "Release Candidate"
                        }
                # Pick a status or don't give one.
                ver.status = statuses.get(ver.status, "")
            if ver.status:
                ver.status = " " + ver.status
            # Not the same as the original output, but it seems nicer.
            retval = "{major:.2f}.{minor:02d}{status!s} {rev:02d}"
        else:
            retval = "{major:.2f}.{minor:02d}-r{rev:02d}{status!s} ({utype!s})"
    elif ver.status:
        retval = "{major:.2f}.{minor:02d}-{status!s}{rev:02d}"
    else:
        retval = "{major:.2f}.{minor:02d}.{rev:02d}"
    return retval.format(**ver)

def pcVerCalc():
    global _pcVersion

    # The logic for this has been moved for the sake of ease of use.
    _pcVersion = get_pchum_ver(raw=False)


def lexVersion(short=False):
    if not _pcStatus:
        return "%s.%s" % (_pcMajor, _pcMinor)

    utype = ""
    if USER_TYPE == "edge":
        utype = "E"

    if short:
        return "%s.%s%s%s%s" % (_pcMajor, _pcMinor, _pcStatus, _pcRevision, utype);

    stype = ""
    if _pcStatus == "A":
        stype = "Alpha"
    elif _pcStatus == "B":
        stype = "Beta"
    elif _pcStatus == "RC":
        stype = "Release Candidate"

    if utype == "E":
        utype = " Bleeding Edge"

    return "%s.%s %s %s%s" % (_pcMajor, _pcMinor, stype, _pcRevision, utype);

# Naughty I know, but it lets me grab it from the bash script.
if __name__ == "__main__":
    print lexVersion()

def verStrToNum(ver):
    w = re.match("(\d+\.?\d+)\.(\d+)-?([A-Za-z]{0,2})\.?(\d*):(\S+)", ver)
    if not w:
        print "Update check Failure: 3"; return
    full = ver[:ver.find(":")]
    return full,w.group(1),w.group(2),w.group(3),w.group(4),w.group(5)

def is_outdated(url=None):
    if not url:
        global _updateCheckURL
        url = _updateCheckURL

    # karxi: Do we really need to sleep here? Why?
    time.sleep(3)
    try:
        jsfile = urllib.urlopen(_updateCheckURL)
        gitver = get_pchum_ver(raw=2, file=jsfile)
    except:
        # No error handling yet....
        raise
    finally:
        jsfile.close()
    ourver = get_pchum_ver(raw=2)

    # Now we can compare.
    outdated = False
    # What, if anything, tipped us off
    trigger = None
    keys = ("major", "minor", "rev", "status")
    for k in keys:
        if gitver[k] > ourver[k]:
            # We don't test for 'bleeding edge' just yet.
            trigger = k
            outdated = True
    if outdated:
        logger.info(
            "Out of date (newer is {0!r} {1} to our {2})".format(
                trigger, gitver[trigger], ourver[trigger]))
    return outdated
# So now all that's left to do is to set up the actual downloading of
# updates...or at least a notifier, until it can be automated.

def updatePesterchum(url=None):
    # TODO: This is still WIP; the actual copying needs to be adjusted.
    if url is None:
        global _downloadURL
        url = _downloadURL

    try:
        # Try to fetch the update.
        fn, fninfo = urllib.urlretrieve(url)
    except urllib.ContentTooShortError:
        # Our download was interrupted; there's not really anything we can do
        # here.
        raise

    ext = osp.splitext(fn)

    if ext == ".zip":
        import zipfile
        is_updatefile = zipfile.is_zipfile
        openupdate = zipfile.ZipFile
    elif tarfile and ext.startswith(".tar"):
        import tarfile
        is_updatefile = tarfile.is_tarfile
        openupdate = tarfile.open
    else:
        logger.info("No handler available for update {0!r}".format(fn))
        return
    logger.info("Opening update {0!s} {1!r} ...".format(ext, fn))

    if is_updatefile(fn):
        update = openupdate(fn, 'r')
        tmpfldr, updfldr = "tmp", "update"

        # Set up the folder structure.
        if osp.exists(updfldr):
            # We'll need this later.
            shutil.rmtree(updfldr)
        if osp.exists(tmpfldr):
            shutil.rmtree(tmpfldr)
        os.mkdir(tmpfldr)
        update.extractall(tmpfldr)
        contents = os.listdir(tmpfldr)

        # Is there only one folder here? Git likes to do this with repos.
        # If there is, move it to our update folder.
        # If there isn't, move the temp directory to our update folder.
        if len(tmpcts) == 1:
            arcresult = osp.join(tmpfldr, contents[0])
            if osp.isdir(arcresult):
                shutil.move(arcresult, updfldr)
        else:
            shutil.move(tmpfldr, updfldr)
        # Remove the temporary folder.
        os.rmdir(tmpfldr)
        # Remove the update file.
        os.remove(fn)
        # ... What does this even do? It recurses....
        removeCopies(updfldr)
        # Why do these both skip the first seven characters?!
        copyUpdate(updfldr)

        # Finally, remove the update folder.
        shutil.rmtree(updfldr)

def updateCheck(q):
    # karxi: Disabled for now; causing issues.
    # There should be an alternative system in place soon.
    return q.put((False,0))

    time.sleep(3)
    data = urllib.urlencode({"type" : USER_TYPE, "os" : OS_TYPE, "install" : INSTALL_TYPE})
    try:
        f = urllib.urlopen("http://distantsphere.com/pesterchum.php?" + data)
    except:
        print "Update check Failure: 1"; return q.put((False,1))
    newest = f.read()
    f.close()
    if not newest or newest[0] == "<":
        print "Update check Failure: 2"; return q.put((False,2))
    try:
        (full, major, minor, status, revision, url) = verStrToNum(newest)
    except TypeError:
        return q.put((False,3))
    print full
    print repr(verStrToNum(newest))

    if major <= _pcMajor:
        if minor <= _pcMinor:
            if status:
                if status <= _pcStatus:
                    if revision <= _pcRevision:
                        return q.put((False,0))
            else:
                if not _pcStatus:
                    if revision <= _pcRevision:
                        return q.put((False,0))
    print "A new version of Pesterchum is avaliable!"
    q.put((full,url))


def removeCopies(path):
    for f in os.listdir(path):
        filePath = osp.join(path, f)
        trunc, rem = filePath[:7], filePath[7:]
        if not osp.isdir(filePath):
            if osp.exists(rem):
                logger.debug(
                    "{0: <4}Deleting copy: {1!r} >{2!r}<".format(
                        '', trunc, rem)
                )
                os.remove(rem)
        else:
            # Recurse
            removeCopies(filePath)

def copyUpdate(path):
    for f in os.listdir(path):
        filePath = osp.join(path, f)
        trunc, rem = filePath[:7], filePath[7:]
        if not osp.isdir(filePath):
            logger.debug(
                "{0: <4}Making copy: {1!r} ==> {2!r}".format(
                    '', filePath, rem)
            )
            shutil.copy2(filePath, rem)
        else:
            if not osp.exists(rem):
                os.mkdir(rem)
            # Recurse
            copyUpdate(filePath)

def updateExtract(url, extension):
    if extension:
        fn = "update" + extension
        urllib.urlretrieve(url, fn)
    else:
        fn = urllib.urlretrieve(url)[0]
        if tarfile and tarfile.is_tarfile(fn):
            extension = ".tar.gz"
        elif zipfile.is_zipfile(fn):
            extension = ".zip"
        else:
            try:
                from libs import magic # :O I'M IMPORTING /MAGIC/!! HOLY SHIT!
                mime = magic.from_file(fn, mime=True)
                if mime == 'application/octet-stream':
                    extension = ".exe"
            except:
                pass

    print url, fn, extension

    if extension == ".exe":
        pass
    elif extension == ".zip" or extension.startswith(".tar"):
        if extension == ".zip":
            from zipfile import is_zipfile as is_updatefile, ZipFile as openupdate
            print "Opening .zip"
        elif tarfile and extension.startswith(".tar"):
            from tarfile import is_tarfile as is_updatefile, open as openupdate
            print "Opening .tar"
        else:
            return

        if is_updatefile(fn):
            update = openupdate(fn, 'r')
            if os.path.exists("tmp"):
                shutil.rmtree("tmp")
            os.mkdir("tmp")
            update.extractall("tmp")
            tmp = os.listdir("tmp")
            if os.path.exists("update"):
                shutil.rmtree("update")
            if len(tmp) == 1 and \
               os.path.isdir("tmp/"+tmp[0]):
                shutil.move("tmp/"+tmp[0], "update")
            else:
                shutil.move("tmp", "update")
            os.rmdir("tmp")
            os.remove(fn)
            removeCopies("update")
            copyUpdate("update")
            shutil.rmtree("update")

def updateDownload(url):
    extensions = [".exe", ".zip", ".tar.gz", ".tar.bz2"]
    found = False
    for e in extensions:
        if url.endswith(e):
            found = True
            updateExtract(url, e)
    if not found:
        if url.startswith("https://github.com/") and url.count('/') == 4:
            updateExtract(url+"/tarball/master", None)
        else:
            updateExtract(url, None)
