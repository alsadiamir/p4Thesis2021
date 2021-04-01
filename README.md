# p4Thesis2021

**Some examples to kick off the repo:**

|   [**Simple network with ingress 2 egress cloning**](./clone_examples/basic/) |                         Description                          |  
| :----------------------------------------------------------: | :----------------------------------------------------------: |
| <img src="/misc/img/P4img-basic.png" alt="basic-i2e.png" style="zoom:30%;"/> | A 3 hosts, 1 switch network that clones every packet exchanged between h1 and h2 to h3. The clone happens between the ingress and egress queue.|
|   [**Simple network with egress 2 egress cloning**](./clone_examples/basic_e2e/) |                **Description**                                 |  
|   <img src="/misc/img/P4img-basic.png" alt="basic-e2e.png" style="zoom:30%;"/> |A 3 hosts, 1 switch network that clones every packet exchanged between h1 and h2 to h3.The clone happens between the egress and egress queue.|
|   [**Ingress 2 egress cloning and packet tunneling**](./clone_examples/clone_with_tunnel/) |   **Description**                            |  
|   <img src="/misc/img/P4img-basic_with_tunnel.png" alt="tunnel.png" style="zoom:50%;"/> |A 4 hosts, 2 switch network that clones every packet exchanged between h1 and h2 to h3 with the help of a tunneling rule. Packets exchanged between h3 and h4 are tunneled to h3 as well.|
|   [**Multiple cloning based on the source address**](./clone_examples/clone_multiple_mirroring/) |   **Description**                            |  
|   <img src="/misc/img/P4img-multiple_cloning.png" alt="multiple_cloning.png" style="zoom:50%;"/> |A 6 hosts, 1 switch network that clones every packet exchanged coming from h1 to h4, from h2 to h5 and from h3 to h6.|
|   [**Programmable cloning**](./clone_examples/dynamic_fw) |   **Description**                            |  
|   <img src="/misc/img/P4img-dynamic_fw.png" alt="programmable.png" style="zoom:50%;"/> |A 5 hosts, 1 switch network in which host1 sets which cloning channel is enabled at the moment.|

**Algorithms to calculate One Way Delay(OWD) of a link**
|   [**Controller in the loop**](./test_algorithms/Controller_in_the_loop/) |                         Description                          |  
| :----------------------------------------------------------: | :----------------------------------------------------------: |
| <img src="/misc/img/P4img-test_CLL.png" alt="cll.png" style="zoom:30%;"/> | A 4 hosts, 2 switch network that calculates OWD using a Controller-in-the-Loop method.|
|   [**Many data loops**](./test_algorithms/Many_Data_Loops/) |                **Description**                                 | 
| <img src="/misc/img/P4img-test_MDL.png" alt="mdl.png" style="zoom:30%;"/> | A 2 hosts, 2 switch network that calculates OWD using a Many-data-loops method.|
|   [**TTL based looping**](./test_algorithms/TTL_Based_Looping/) |                **Description**                                 | 
| <img src="/misc/img/P4img-test_TTL.png" alt="mdl.png" style="zoom:30%;"/> | A 2 hosts, 2 switch network that calculates OWD using a TTL-based-looping method.|
