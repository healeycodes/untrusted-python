import sys
import resource
import pyseccomp as seccomp


MEMORY_LIMIT = 64 * 1024 * 1024  # 64kb
CPU_TIME_LIMIT = 1  # 1sec
WRITE_LIMIT = 512  # 512bytes


def drop_perms():
    syscalls = [
        "write",  # write to open files (i.e. stdout)
    ]
    filter = seccomp.SyscallFilter(seccomp.ERRNO(seccomp.errno.EPERM))
    for c in syscalls:
        filter.add_rule(seccomp.ALLOW, c)
    filter.load()


def set_mem_limit():
    resource.setrlimit(resource.RLIMIT_AS, (MEMORY_LIMIT, MEMORY_LIMIT))
    resource.setrlimit(resource.RLIMIT_CPU, (CPU_TIME_LIMIT, CPU_TIME_LIMIT))
    resource.setrlimit(resource.RLIMIT_FSIZE, (WRITE_LIMIT, WRITE_LIMIT))


if __name__ == "__main__":
    code = sys.stdin.read()
    set_mem_limit()
    drop_perms()
    exec(code)
