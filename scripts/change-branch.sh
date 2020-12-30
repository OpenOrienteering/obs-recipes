#!/bin/sh

# Synopsis:
#  ./scripts/$0 mapper
#  ./scripts/$0 mapper-master
#  ./scripts/$0 mapper-unstable

set -e

if [ -f openorienteering-mapper.spec ] ; then
	FROM=mapper
elif [ -f openorienteering-mapper-master.spec ] ; then
	FROM=mapper-master
elif [ -f openorienteering-mapper-unstable.spec ] ; then
	FROM=mapper-unstable
else
	echo "Cannot identify source branch"
	exit 1
fi

TO="$1"
case "${TO}" in
mapper|mapper-master|mapper-unstable)
	echo -n "Switching from openorienteering-${FROM}'"
	echo " to 'openorienteering-${TO}'"
	break
	;;
*)
	echo "${TO}: Target not supported"
	exit 1
	;;
esac

git mv arch.openorienteering-${FROM}.install arch.openorienteering-${TO}.install
for I in openorienteering-${FROM}?*
do
	git mv $I openorienteering-${TO}${I#openorienteering-${FROM}}
done

for I in debian.* openorienteering-${TO}?* PKGBUILD
do
	sed -e "/BRANCH_SUFFIX\|nativename/,$ b;/[[]openorienteering/ b;s/-${FROM}/-${TO}/" -i -- ${I}
done
SPEC=openorienteering-${TO}.spec
case "${TO}" in
mapper)
	sed -e "s/.*%global branch.*/#%%global branch master/" -i -- ${SPEC}
	;;
*)
	sed -e "s/.*%global branch.*/%global branch ${TO#mapper-}/" -i -- ${SPEC}
	;;
esac

git add -u
git commit -m "Switch to openorienteering-${TO}"

