/* rtemsQemuTestMain.cpp */
/* Author:  Marty Kraimer Date:    17MAR2000 */

#include <stddef.h>
#include <stdlib.h>
#include <stddef.h>
#include <string.h>
#include <stdio.h>
#include <errno.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <limits.h>

#include "epicsExit.h"
#include "epicsThread.h"
#include "envDefs.h"
#include "iocsh.h"

#define STARTUP_SCRIPT "/app/iocBoot/iocRTEMSTest/st.cmd"

/* Defaults for RTEMS IOCs. Override in the makefile with -DST_CMD=... and such, or do it here! */
#ifdef __rtems__
#   ifndef ST_CMD
#       define ST_CMD "st.cmd"
#   endif
#   ifndef IOC_DIR
#       define IOC_DIR "/app/iocBoot/iocRTEMSTest"
#   endif
#   ifndef IOC_TOP
#       define IOC_TOP "/app"
#   endif
    /* Typically, QEMU allocates an address on the subnet 10.0.2.X, so set the gateway to 10.0.2.255 by default */
    /* Override if you need to, but it should work in everyone's QEMU */
#   ifndef QEMU_EPICS_GATEWAY
#       define QEMU_EPICS_GATEWAY "10.0.2.255"
#   endif
#endif

int main(int argc,char *argv[])
{
#ifdef __rtems__
    if (chdir(IOC_DIR) < 0) {
        perror("chdir failed");
        abort();
    }
    epicsEnvSet("TOP", IOC_TOP);
    epicsEnvSet("EPICS_CA_ADDR_LIST", QEMU_EPICS_GATEWAY);

    iocsh("st.cmd");
    iocsh(NULL);
    epicsExit(0);
    return 0;
#else
    if(argc>=2) {
        iocsh(argv[1]);
        epicsThreadSleep(.2);
    }
    iocsh(NULL);
#endif
    epicsExit(0);
    return(0);
}
