#!/usr/bin/env bash

TARGET_ARCH=RTEMS-pc686-qemu
QEMU_ARCH=

function usage() {
    echo "$0 [-t target] [-q qemu-arch]"
    echo " ex: $0 -t RTEMS-pc686-qemu -q i386"
}

for arg in $@; do
    case $arg in
        -t|--target)
            TARGET_ARCH=$2
            shift 2
            ;;
        -q|--qemu-arch)
            QEMU_ARCH=$2
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            shift
            ;;
    esac
done

if [ -z $QEMU_ARCH ]; then
    case $TARGET_ARCH in
        *x86_64*)
            QEMU_ARCH=x86_64
            ;;
        *386*|*486*|*686*|*i586*|*x86*|*pentium*)
            QEMU_ARCH=i386
            ;;
        *beatnik*|*mvme3100*|*mvme2700*|*ppc*|*mpc854*)
            QEMU_ARCH=ppc
            ;;
        *uC5282*|680*0)
            QEMU_ARCH=m68k
            ;;
        *sparc64*)
            QEMU_ARCH=sparc64
            ;;
        *sparc*)
            QEMU_ARCH=sparc
            ;;
        *arm64*|*aarch64*|*zynq*)
            QEMU_ARCH=aarch64
            ;;
        *arm*|*aarch32*)
            QEMU_ARCH=arm
            ;;
        *)
            echo "Unable to determine QEMU architecture, please pass -q <arch> or --qemu-arch <arch>"
            exit 1
            ;;
    esac
fi

# Some detail for what's going on here:
#  Bridge both UDP/TCP 5064/5065 from host to guest, for channel access. 
#  We then set EPICS_CA_ADDR_LIST to 10.0.2.255 in rtemsQemuTestApp right before starting the IOC. QEMU always allocates on the 10.0.2.X subnet,
#  so this is portable.
#  -nic user,hostfwd=udp::5064-:5064,hostfwd=tcp::5064-:5064
#  -nic user,hostfwd=udp::5065-:5065,hostfwd=tcp::5065-:5065
qemu-system-$QEMU_ARCH \
    -m 64 \
    -no-reboot \
    -serial stdio \
    -display none \
    -net nic,model=e1000 \
    -net user,restrict=yes \
    -append "--video=off --console=/dev/com1" \
    -kernel "./bin/$TARGET_ARCH/rtemsQemuTest" \
    -nic user,hostfwd=udp::5064-:5064,hostfwd=tcp::5064-:5064 \
    -nic user,hostfwd=udp::5065-:5065,hostfwd=tcp::5065-:5065
