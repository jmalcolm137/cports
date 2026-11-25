# Interactive shells do not read /etc/profile, so give them the same PATH
# fixup (including the /usr/gnubin uutils overlay) that login shells get.

if [ -r /etc/profile.path ]; then
    . /etc/profile.path
elif [ -r /usr/share/base-files/profile.path ]; then
    . /usr/share/base-files/profile.path
fi
