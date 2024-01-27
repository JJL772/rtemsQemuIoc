#- Example RTEMS startup script

#- You may have to change rtemsQemuTest to something else
#- everywhere it appears in this file

#< envPaths

cd "${TOP}"

## Register all support components
dbLoadDatabase("dbd/rtemsQemuTest.dbd")
rtemsQemuTest_registerRecordDeviceDriver(pdbbase)

## Load record instances
#dbLoadTemplate("db/rtemsQemuTest.substitutions")
#dbLoadRecords("db/rtemsQemuTest.db", "user=jeremy")
dbLoadRecords("db/test.db")

iocInit

## Start any sequence programs
#seq(sncxxx, "user=jeremy")
