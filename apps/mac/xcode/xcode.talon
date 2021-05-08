os: mac
and app.bundle: com.apple.dt.Xcode
-
tag(): user.find_and_replace
tag(): user.line_commands
tag(): user.tabs

file:
	key(cmd-shift-o)

file name <user.text>:
	key(cmd-shift-o)
	insert(user.text)

action(code.toggle_comment): key(cmd-/)

action(edit.indent_less): key(cmd-[)
action(edit.indent_more): key(cmd-])

# user.find_and_replace
action(user.find_next): key(cmd-g)
action(user.find_previous): key(cmd-shift-g)

# user.line_commands
action(user.delete_camel_left): key(ctrl-backspace)
action(user.delete_camel_right): key(ctrl-delete)
action(user.extend_camel_left): key(ctrl-shift-left)
action(user.extend_camel_right): key(ctrl-shift-right)
action(user.camel_left): key(ctrl-left)
action(user.camel_right): key(ctrl-right)

# user.tabs
action(app.tab_previous): key(cmd-shift-[)
action(app.tab_next): key(cmd-shift-])