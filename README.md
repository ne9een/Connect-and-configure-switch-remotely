# Connect-and-configure-switch-remotely
With this Python script we can connect to Distributed Main Switch Conroller (DMXC) and configure it accordingly.
We used 
- Paramiko module to be able to ssh to DMXC CLI
- Subprocess module to run the cli command and retreive the outcome
- threading module to show the progress during the configuraiton ( it does not show the actual progress but only a dynamic string 
running .../-|\
- pdb module for debugging

