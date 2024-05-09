from shell_wrapper import Shell

REMOTE_DEPENDENCIES = {
    "remote": [
        "python3",
        "tar",
        "make",
        ("gcc", "clang"),
        "yacc",
    ],
    "local": [
        "curl",
        "git",
        "tar",
    ]
}

LOCAL_DEPENDENCIES = [
    "tar",
    "make",
    ("gcc", "clang"),
    "yacc",
    "curl",
    "git",
]

def check_dependencies(shell: Shell, dependencies: list) -> bool:
    ret = True

    for d in dependencies:
        if isinstance(d, tuple):
            if not any(shell.check_dependency(dep) for dep in d):
                print(f"WARNING: {' or '.join(d)} not found")
                ret = False
        else:
            if not shell.check_dependency(d):
                print(f"WARNING: {d} not found")
                ret = False
    
    return ret