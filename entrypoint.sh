#!/bin/sh
set -eu

usage() {
	echo "USAGE:"
	echo "  r53-private-zone-update [ARGS]"
	echo "  ec2-wait-instance-state [ARGS]"
	exit 1
}

case "${1:-}" in 
	"r53-private-zone-update" )
		shift
		cd /home/app
		su-exec app bin/r53-private-zone-update.py $@
		;;
	"ec2-wait-instance-state" )
		shift
		cd /home/app
		su-exec app bin/ec2-wait-instance-state.py $@
		;;
	"shell" )
		exec bash
		;;
	* )
		usage
		;;
esac

