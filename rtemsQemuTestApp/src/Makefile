TOP=../..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

#=============================
# Build the IOC application

PROD_IOC = rtemsQemuTest
# rtemsQemuTest.dbd will be created and installed
DBD += rtemsQemuTest.dbd

# rtemsQemuTest.dbd will be made up from these files:
rtemsQemuTest_DBD += base.dbd

# Include dbd files from all support applications:
#rtemsQemuTest_DBD += xxx.dbd

# Add all the support libraries needed by this IOC
#rtemsQemuTest_LIBS += xxx

# rtemsQemuTest_registerRecordDeviceDriver.cpp derives from rtemsQemuTest.dbd
rtemsQemuTest_SRCS += rtemsQemuTest_registerRecordDeviceDriver.cpp
rtemsQemuTest_SRCS += rtemsQemuTest_FS.cpp

# Build the main IOC entry point on workstation OSs.
rtemsQemuTest_SRCS_DEFAULT += rtemsQemuTestMain.cpp
rtemsQemuTest_SRCS_vxWorks += -nil-

# Add support from base/src/vxWorks if needed
#rtemsQemuTest_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

# Finally link to the EPICS Base libraries
rtemsQemuTest_LIBS += $(EPICS_BASE_IOC_LIBS)

#===========================

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

rtemsQemuTest_FS.cpp:
	python3 $(TOP)/createMemFs.py -o $@ $(TOP)
