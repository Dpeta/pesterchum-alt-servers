"""Functions for Applying a seccomp filter on Linux.

This prevents the process from using certain system calls, which has some security benefits.
Since Python and Qt use many calls and are pretty high-level, things are prone to breaking though.
Certain features like opening links almost always break.

Uses libseccomp's Python bindings, which sadly aren't available on PyPi (yet).
Check your distro's package manager for python-libseccomp (Arch) or python3-seccomp (Debian).

For info on system calls referencing software that uses seccomp like firejail/flatpak is useful.
Bindings documentation: https://github.com/seccomp/libseccomp/blob/main/src/python/seccomp.pyx
"""
import os
import logging
import threading

try:
    import seccomp
except ImportError:
    seccomp = None

pesterchum_log = logging.getLogger("pchumLogger")


def load_seccomp_blacklist():
    """Applies a selective seccomp filter only disallows certain risky calls.

    Should be less likely to cause issues than a full-on whitelist."""
    if seccomp is None:
        pesterchum_log.warning(
            "Failed to import seccomp, verify you have"
            " python-libseccomp (Arch) or python3-seccomp (Debian) installed."
            " If this is a pyinstaller/cx_freeze build, it may also be a linking issue."
        )
        return
    # Allows all calls by default.
    sec_filter = seccomp.SyscallFilter(defaction=seccomp.ALLOW)

    # Deny all socket domains other than AF_UNIX and and AF_INET.
    sec_filter.add_rule(seccomp.ERRNO(1), "socket", seccomp.Arg(0, seccomp.LT, 1))
    sec_filter.add_rule(seccomp.ERRNO(1), "socket", seccomp.Arg(0, seccomp.GT, 2))

    # Fully deny these calls.
    for call in CALL_BLACKLIST:
        try:
            sec_filter.add_rule(seccomp.ERRNO(1), call)
        except RuntimeError:
            pesterchum_log.warning("Failed to load deny '%s' call seccomp rule.", call)

    sec_filter.load()


def load_seccomp_whitelist():
    """Applies a restrictive seccomp filter that disallows most calls by default."""
    if seccomp is None:
        pesterchum_log.error(
            "Failed to import seccomp, verify you have"
            " python-libseccomp (Arch) or python3-seccomp (Debian) installed."
            " If this is a pyinstaller/cx_freeze build, it may also be a linking issue."
        )
        return
    # Violation gives "Operation not permitted".
    sec_filter = seccomp.SyscallFilter(defaction=seccomp.ERRNO(1))
    # Full access calls
    for call in CALL_WHITELIST:
        try:
            sec_filter.add_rule(seccomp.ALLOW, call)
        except RuntimeError:
            pesterchum_log.warning("Failed to load allow '%s' call seccomp rule.", call)

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

    # Allow openat as long as it's not in R+W mode.
    # We can't really lock down open/openat further without breaking everything,
    # even though it's one of the most important calls to lock down.
    # Could probably allow breaking out of the sandbox in the case of full-on RCE/ACE.
    sec_filter.add_rule(seccomp.ALLOW, "openat", seccomp.Arg(2, seccomp.NE, 2))

    sec_filter.load()


# Required for Pesterchum to function normally.
# We don't call most of these directly, there's a lot of abstraction with Python and Qt.
CALL_WHITELIST = [
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
    "getdents",  # Files? Required.
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

# Blacklists of calls we should be able to safely deny.
# Setuid might be useful to drop privileges.
SETUID = [
    "setgid",
    "setgroups",
    "setregid",
    "setresgid",
    "setresuid",
    "setreuid",
    "setuid",
]
SYSTEM = [
    "acct",
    "bpf",
    "capset",
    "chown",
    "chroot",
    "fanotify_init",
    "fsconfig",
    "fsmount",
    "fsopen",
    "fspick",
    "kexec_file_load",
    "kexec_load",
    "lookup_dcookie",
    "mount",
    "move_mount",
    "nfsservctl",
    "open_by_handle_at",
    "open_tree",
    "perf_event_open",
    "personality",
    "pidfd_getfd",
    "pivot_root",
    "pivot_root",
    "process_vm_readv",
    "process_vm_writev",
    "ptrace",  # <-- Important
    "quotactl",
    "reboot",
    "rtas",
    "s390_runtime_instr",
    "setdomainname",
    "setfsuid",
    "sethostname",
    "swapoff",
    "swapon",
    "sys_debug_setcontext",
    "umount",
    "umount2",
    "vhangup",
]
CALL_BLACKLIST = SYSTEM  # + SETUID

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
