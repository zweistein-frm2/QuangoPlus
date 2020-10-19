
#this works from a local xterm
[ -z "$SSH_CLIENT" ] && docker run -it -e DISPLAY=$DISPLAY  -v /tmp/X11-unix:/tmp/.X11-unix -u qtuser quangoplus
#this works from  a remote xterm (via ssh)
[ "$SSH_CLIENT" ] && docker run --net=host  --volume="$HOME/.Xauthority:/root/.Xauthority:rw"  --env="DISPLAY" quangoplus