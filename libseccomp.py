"""
Applies a seccomp filter on Linux via libseccomp's Python bindings.
Has some security benefits, but since Python and Qt use many calls
and are pretty high-level, things are prone to breaking.

Certain features like opening links almost always break.

Libseccomp's Python bindings aren't available on the pypi, check your distro's
package manager for python-libseccomp (Arch) or python3-seccomp (Debian).
"""
import os
import logging
import threading

try:
    import seccomp
except ImportError:
    seccomp = None

pesterchum_log = logging.getLogger("pchumLogger")


def activate_seccomp():
    """Sets the process into seccomp filter mode."""
    if seccomp is None:
        pesterchum_log.error(
            "Failed to import seccomp, verify you have"
            " python-libseccomp (Arch) or python3-seccomp (Debian) installed"
            " and aren't running a pyinstaller build."
        )
        return
    # Violation gives "Operation not permitted".
    sec_filter = seccomp.SyscallFilter(defaction=seccomp.ERRNO(1))
    # Full access calls
    for call in PCHUM_SYSTEM_CALLS:
        sec_filter.add_rule(seccomp.ALLOW, call)

    # Allow only UNIX and INET sockets, see the linux manual and source on socket for reference.
    # Arg(0, seccomp.EQ, 1) means argument 0 must be equal to 1, 1 being the value of AF_UNIX.
    # Allow AF_UNIX
    sec_filter.add_rule(seccomp.ALLOW, "socket", seccomp.Arg(0, seccomp.EQ, 1))
    # Allow AF_INET
    sec_filter.add_rule(seccomp.ALLOW, "socket", seccomp.Arg(0, seccomp.EQ, 2))

    # Python/Qt might close itself via kill call in case of error.
    sec_filter.add_rule(seccomp.ALLOW, "kill", seccomp.Arg(0, seccomp.EQ, os.getpid()))
    sec_filter.add_rule(
        seccomp.ALLOW, "tgkill", seccomp.Arg(1, seccomp.EQ, threading.get_native_id())
    )

    # Allow openat as along as it's not in R+W mode.
    # We can't really lock down open/openat further without breaking everything,
    # even though it's one of the most important calls to lock down.
    # Could probably allow breaking out of the sandbox in the case of full-on RCE/ACE.
    sec_filter.add_rule(seccomp.ALLOW, "openat", seccomp.Arg(2, seccomp.NE, 2))

    sec_filter.load()


# Required for Pesterchum to function normally.
# Pesterchum doesn't call most of these directly, there's a lot of abstraction with Python and Qt.
PCHUM_SYSTEM_CALLS = [
    "access",  # Files
    "brk",  # Required
    "clone3",  # Required
    "close",  # Sockets (Audio + Network)
    "connect",  # Sockets (Audio + Network)
    "exit",  # Exiting
    "exit_group",  # Exiting
    "fallocate",  # Qt
    "fcntl",  # Required (+ Audio)
    "fsync",  # Fsync log files
    "ftruncate",  # Required
    "futex",  # Required
    "getcwd",  # Get working directory
    "getdents64",  # Files? Required.
    "getgid",  # Audio
    "getpeername",  # Connect
    "getpid",  # Audio
    "getrandom",  # Malloc
    "getsockname",  # Required for sockets
    "getsockopt",  # Required for sockets
    "getuid",  # Audio
    "ioctl",  # Socket/Network
    "lseek",  # Files
    "memfd_create",  # Required (For Qt?)
    "mkdir",  # Gotta make folderz sometimez
    "mmap",  # Audio
    "mprotect",  # QThread::start
    "munmap",  # Required (segfault)
    "newfstatat",  # Required (Audio + Path?)
    "pipe2",  # Audio
    "poll",  # Required for literally everything
    "pselect6",  # Sockets/Network
    "read",  # It's read :3
    "readlink",  # Files
    "recv",  # Network
    "recvfrom",  # Network + DNS
    "recvmsg",  # Sockets (incl. Audio + Network)
    "rseq",  # Required
    "rt_sigprocmask",  # Required (segfault)
    "select",  # Useful for sockets
    "sendmmsg",  # Network
    "sendmsg",  # Sockets
    "sendto",  # Eternal eepy!! Sockets + required for waking up mainloop.
    "setsockopt",  # Audio
    "statx",  # File info
    "uname",  # Required
    "write",  # Required
]

"""
# Optional
EXTRA_CALLS = [
    "mlock",
    "munlock",
    "socketcall",
    "socketpair",
    "readlink",
    "getsockname",
    "getpeername",
    "writev",
    "open",
    "time",
    "listen",
]
# Required on launch
LAUNCH_CALLS = [
    "prctl",
    "faccessat",
    "faccessat2",
    "pwrite64",
]
# Required before full initialize
PRE_INITIALIZE_CALLS = [
    "bind",
    "eventfd2",
    "getegid",
    "geteuid",
    "getresgid",
    "getresuid",
    "gettid",
    "recvmmsg",
    "restart_syscall",
    "rt_sigaction",
    "rt_sigreturn",
    "sched_getaffinity",
    "sched_getattr",
    "sched_setattr",
    "shutdown",
    "umask",
]
# Required for opening links, but opening links still doesn't work anyway.
LINK_CALLS = [
    "wait4",  # for links?
    "clone",  # for links?
]
"""
