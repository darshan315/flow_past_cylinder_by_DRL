#!/usr/bin/bash

# [case] [args : which file where to]

case $1 in 
	cluster ) 
		read -p "Phrase : " phrase
		scp -r $2 y009$phrase@phoenix.hlr.rz.tu-bs.de:./$DIR/$3
		;;
	pc )
		read -p "Phrase : " phrase
		scp -r y009$phrase@phoenix.hlr.rz.tu-bs.de:./$DIR/$2 $3
		;;
esac

