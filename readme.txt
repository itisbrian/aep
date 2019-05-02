Green Fireball AEP Tester
V 1.0

by: brianchen@supermicro.com
    patrickg@gsupermicro.com

1/25/2019
---------------------------------------------------------------------------------------------------
*All resources and packages can be found on http://westworld.bnet
*Be careful when you update the FW on these systems. 


Usage Instructions:

1. Install Fedora, http://westworld.bnet/repo/fedora/Fedora-Server-dvd-x86_64-29-1.2.iso , default fedora packages are fine.
2. run 'yum update -y' , wait for update to finish and reboot.
3. Confirm Kernel version is 4.18 or higher.
4. run 'wget http://westworld.bnet/aep/gfb.sh' , chmod +x
5. Verify script executed properly, and returned no exit errors.
6. Verify '/root/green_fireball' folder exists under the root directory.
7. Before starting the tests, it is best to clear existing namespaces / configurations on the memory to 100% MM mode.

8. GFB will execute on Alt + F7, system will reboot many times, do not panic.

Start: ./root/green_fireball/bin/gfb_start
Stop : ./root/green_fireball/bin/gfb_stop
Reset: ./root/green_fireball/bin/gfb_reset


'Tests completed successfully.' will be displayed on Alt F7 when all tests are finished.


Notes: 

1. Run on Cascade Lake b0 stepping with 3.0a bios.
2. Make sure the processor supports the maximum ammount of memory.
3. Make sure the total AEP vs total DDR4 dimm size ratio is within limits.
4. Make sure to test the valid configurations according to the intel document.
5. ipmctl and ndctl are the primary 2 commands used for this operation.
6. Make sure bios is able to pick up incorrect dimm population errors.
