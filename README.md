# Simulated RTEMS IOC

This is a simple proof of concept RTEMS IOC running in QEMU, for testing purposes. Ideally, a setup like this will allow for automated testing of EPICS software being ported to RTEMS 6 and later. 

Usefulness is still limited due to the nature of hard IOCs running on RTEMS (usually these are running in PPC VME systems with specialized hardware).

## TODO LIST

- [ ] Add proper dependency detection with createMemFs.py, so we don't need to make clean + make all to reassemble the memfs with new content (Or we could ditch the memfs entirely and use userspace NFS or TFTP to serve files to the IOC)
- [ ] Fixup envPaths post build, so we can actually point the RTEMS IOC at the right TOP directory. For now I have TOP hardcoded via a define and we do not load envPaths in st.cmd
- [ ] Fix iocBoot directory dependency hack
- [ ] Make everything less ugly
