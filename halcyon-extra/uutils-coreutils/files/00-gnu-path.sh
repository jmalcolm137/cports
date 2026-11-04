# Prefer the uutils/GNU userland overlay for regular (non-system) users,
# right after /usr/local/bin so locally installed tools keep precedence.
# System accounts (UID below 1000) keep the default Chimera userland.
_gnu_uid="$(/usr/bin/id -u 2>/dev/null)"
[ -n "$_gnu_uid" ] || _gnu_uid=0

if [ "$_gnu_uid" -ge 1000 ]; then
    _gnu_old="$PATH"
    _gnu_new=
    _gnu_added=
    _gnu_ifs="$IFS"
    IFS=:
    for _gnu_dir in $_gnu_old; do
        # drop an existing overlay entry, it is re-inserted below
        [ "$_gnu_dir" = /usr/bin/gnu ] && continue
        _gnu_new="${_gnu_new:+$_gnu_new:}$_gnu_dir"
        if [ -z "$_gnu_added" ] && [ "$_gnu_dir" = /usr/local/bin ]; then
            _gnu_new="$_gnu_new:/usr/bin/gnu"
            _gnu_added=1
        fi
    done
    IFS="$_gnu_ifs"

    # no /usr/local/bin in PATH: keep the overlay in front
    if [ -z "$_gnu_added" ]; then
        _gnu_new="/usr/bin/gnu${_gnu_new:+:$_gnu_new}"
    fi

    PATH="$_gnu_new"
    export PATH
    unset _gnu_old _gnu_new _gnu_added _gnu_ifs _gnu_dir
fi

unset _gnu_uid
