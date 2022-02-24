app: terminator
-
# Set tags
tag(): terminal
tag(): user.tabs
tag(): user.generic_unix_shell
tag(): user.git
tag(): user.kubectl

vim editor: "vim "
jee editor: "gedit "
file copy: "cp "
file copy recursive: "cp -r "
file remove: "rm "
file remove recursive: "rm -r "
file move: "mv "
lisa all human: "ls -lah\n"
make dir: "mkdir "
secure shell: "ssh "
secure shell recursive: "ssh -r "
grep inside <user.text>: "grep -rwn . -e '{text}'"
exit terminal: "exit"
