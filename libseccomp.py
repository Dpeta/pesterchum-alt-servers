"""
Applies a seccomp filter on Linux via libseccomp's Python bindings.
May have some security benefits, but since Python and Qt use many calls
and are pretty high-level, things are very prone to breaking.

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
        pesterchum_log.error("Failed to import seccomp.")
        return
    # Violation gives "Operation not permitted".
    sec_filter = seccomp.SyscallFilter(defaction=seccomp.ERRNO(1))
    # Full access calls
    for call in PCHUM_SYSTEM_CALLS:
        sec_filter.add_rule(seccomp.ALLOW, call)

    # Allow only UNIX and INET sockets, see the linux manual and source on socket for reference.
    # Arg(0, seccomp.EQ, 1) means argument 0 must be equal to 1, 1 being the value of AF_UNIX.
    sec_filter.add_rule(seccomp.ALLOW, "socket", seccomp.Arg(0, seccomp.EQ, 1))  # AF_UNIX
    sec_filter.add_rule(seccomp.ALLOW, "socket", seccomp.Arg(0, seccomp.EQ, 2))  # AF_INET

    # We can kill ourselves in case of skill issues but not others.
    sec_filter.add_rule(seccomp.ALLOW, "kill", seccomp.Arg(0, seccomp.EQ, os.getpid()))
    sec_filter.add_rule(seccomp.ALLOW, "tgkill", seccomp.Arg(1, seccomp.EQ, threading.get_native_id()))
    
    sec_filter.load()

def restrict_open():
    # Allow only opening for reading/writing
    sec_filter.add_rule(seccomp.ALLOW, "openat", seccomp.Arg(0, seccomp.EQ, os.getpid()))

# Required for Pesterchum to run.
PCHUM_SYSTEM_CALLS = [
    "access",
    "bind",
    "brk",
    "clone3",
    "close",
    "connect",
    "eventfd2",
    "exit",
    "exit_group",
    "faccessat",
    "faccessat2",
    "fallocate",
    "fcntl",
    "fsync",
    "ftruncate",
    "futex",
    "getcwd",
    "getdents64",
    "getegid",
    "geteuid",
    "getgid",
    "getpeername",
    "getpid",
    "getrandom",
    "getresgid",
    "getresuid",
    "getsockname",
    "getsockopt",
    "gettid",
    "getuid",
    "ioctl",
    "lseek",
    "memfd_create",
    "mkdir",
    "mmap",
    "mprotect",
    "munmap",
    "newfstatat",
    "openat",
    "pipe2",
    "poll",
    "prctl",
    "pselect6",
    "pwrite64",
    "read",
    "recv",
    "recvfrom",
    "recvfrom",
    "recvmmsg",
    "recvmsg",
    "restart_syscall",
    "rseq",
    "rt_sigaction",
    "rt_sigprocmask",
    "rt_sigreturn",
    "sched_getaffinity",
    "sched_getattr",
    "sched_setattr",
    "select",
    "sendmmsg",
    "sendmsg",
    "sendto",
    "setsockopt",
    "shutdown",
    "statx",
    "umask",
    "uname",
    "write",
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
    "wait4",  # for links?
    "clone",  # for links?
]
"""
