# Prefer the uutils/GNU userland overlay for regular (non-system) users.
# System accounts (UID below 1000) keep the default Chimera userland.
_gnu_uid="$(id -u 2>/dev/null)"
[ -n "$_gnu_uid" ] || _gnu_uid=0

if [ "$_gnu_uid" -ge 1000 ]; then
    case ":${PATH}:" in
        *:/usr/bin/gnu:*) ;;
        *) PATH="/usr/bin/gnu:${PATH}" ;;
    esac
    export PATH
fi

unset _gnu_uid
