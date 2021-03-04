# p4Thesis2021
This repo is designed to track every step of my P4 thesis.

Some example of clones to kick off the repo:

|   [**Simple network with ingress 2 egress cloning**](./clone_examples/basic/) |                         Description                          |  
| :----------------------------------------------------------: | :----------------------------------------------------------: |
| <img src="/misc/img/P4img-basic.png" alt="basic-i2e.png" style="zoom:30%;"/> | A 3 hosts, 1 switch network that clones every packet exchanged between h1 and h2 to h3. The clone happens between the ingress and egress queue.|
|   [**Simple network with egress 2 egress cloning**](./clone_examples/basic_e2e/) |                         Description                          |  
|   <img src="/misc/img/P4img-basic.png" alt="basic-e2e.png" style="zoom:30%;"/> |A 3 hosts, 1 switch network that clones every packet exchanged between h1 and h2 to h3.The clone happens between the egress and egress queue.|
|   [**Simple network with ingress 2 egress cloning and packet tunneling**](./clone_examples/clone_with_tunnel/) |                         Description                          |  
|   <img src="/misc/img/P4img-basic_with_tunnel.png" alt="tunnel.png" style="zoom:30%;"/> |A 4 hosts, 2 switch network that clones every packet exchanged between h1 and h2 to h3 with the help of a tunneling rule. Packets exchanged between h3 and h4 are tunneled to h3 as well.|

