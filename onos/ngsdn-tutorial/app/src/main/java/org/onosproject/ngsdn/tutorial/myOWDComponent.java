/*
 * Copyright 2015 Open Networking Foundation
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.onosproject.ngsdn.tutorial;

import org.onosproject.net.packet.OutboundPacket;
import com.google.common.collect.HashMultimap;
import org.osgi.service.component.annotations.Activate;
import org.osgi.service.component.annotations.Component;
import org.osgi.service.component.annotations.Deactivate;
import org.osgi.service.component.annotations.Reference;
import org.osgi.service.component.annotations.ReferenceCardinality;
import org.onlab.packet.DeserializationException;
import org.onlab.packet.Ethernet;
import org.onlab.packet.IPv4;
import org.onlab.packet.MacAddress;
import org.onosproject.core.ApplicationId;
import org.onosproject.core.CoreService;
import org.onosproject.net.DeviceId;
import org.onosproject.net.flow.DefaultTrafficSelector;
import org.onosproject.net.flow.DefaultTrafficTreatment;
import org.onosproject.net.flow.FlowRule;
import org.onosproject.net.flow.FlowRuleEvent;
import org.onosproject.net.flow.FlowRuleListener;
import org.onosproject.net.flow.FlowRuleService;
import org.onosproject.net.flow.TrafficSelector;
import org.onosproject.net.flow.TrafficTreatment;
import org.onosproject.net.flow.criteria.Criterion;
import org.onosproject.net.flow.criteria.EthCriterion;
import org.onosproject.net.flowobjective.DefaultForwardingObjective;
import org.onosproject.net.flowobjective.FlowObjectiveService;
import org.onosproject.net.flowobjective.ForwardingObjective;
import org.onosproject.net.packet.PacketContext;
import org.onosproject.net.packet.PacketPriority;
import org.onosproject.net.packet.PacketProcessor;
import org.onosproject.net.packet.PacketService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.onosproject.ngsdn.tutorial.packet.myTunnel;
import java.util.Objects;
import java.util.Optional;
import java.util.Timer;
import java.util.TimerTask;
import org.onosproject.net.PortNumber;
import org.onosproject.net.packet.DefaultOutboundPacket;
import java.nio.ByteBuffer;
import java.lang.InterruptedException;
import java.io.FileWriter;   // Import the FileWriter class
import java.io.IOException;  // Import the IOException class to handle errors
import java.io.File;  // Import the File class
import java.io.IOException;  // Import the IOException class to handle errors
import java.nio.file.Files;
import java.nio.file.StandardOpenOption;
import java.nio.file.Paths;

import static org.onosproject.net.flow.FlowRuleEvent.Type.RULE_REMOVED;
import static org.onosproject.net.flow.criteria.Criterion.Type.ETH_SRC;

/**
 * Sample application that permits only one ICMP ping per minute for a unique
 * src/dst MAC pair per switch.
 */
@Component(immediate = true, enabled = true)
public class myOWDComponent {

    private static Logger log = LoggerFactory.getLogger(myOWDComponent.class);

    private static final int PRIORITY = 128;
    private static final int DROP_PRIORITY = 129;
    private static final int TIMEOUT_SEC = 60; // seconds
    private static final short TYPE_MYTUNNEL = 0x1212;

    @Reference(cardinality = ReferenceCardinality.MANDATORY)
    protected CoreService coreService;

    @Reference(cardinality = ReferenceCardinality.MANDATORY)
    protected FlowObjectiveService flowObjectiveService;

    @Reference(cardinality = ReferenceCardinality.MANDATORY)
    protected FlowRuleService flowRuleService;

    @Reference(cardinality = ReferenceCardinality.MANDATORY)
    protected PacketService packetService;

    @Reference(cardinality = ReferenceCardinality.MANDATORY)
    private MainComponent mainComponent;

    private ApplicationId appId;
    private final PacketProcessor packetProcessor = new myTunnelProcessor();
    private final FlowRuleListener flowListener = new InternalFlowListener();

    // Selector for mytunnel traffic that is to be intercepted
    private final TrafficSelector intercept = DefaultTrafficSelector.builder()
            .matchEthType(TYPE_MYTUNNEL).build();

    private void sendPackets() throws InterruptedException{
//        while(true) {
            Thread.sleep(20);
            TrafficTreatment treatment = DefaultTrafficTreatment.builder().setOutput(PortNumber.portNumber(255)).build();
            OutboundPacket outboundPacket;
            myTunnel myTun = new myTunnel();
            myTun.setDestinationMACAddress("00:00:00:00:00:10");
            myTun.setSourceMACAddress("00:00:00:00:00:40");
            myTun.setDst_id((short)2);
            outboundPacket = new DefaultOutboundPacket(DeviceId.deviceId("device:leaf1"), treatment, ByteBuffer.wrap(myTun.serialize()));
            packetService.emit(outboundPacket);
//        }
    }

    @Activate
    public void activate() throws InterruptedException{
        appId = mainComponent.getAppId();
        packetService.addProcessor(packetProcessor, PRIORITY);
        flowRuleService.addListener(flowListener);
        packetService.requestPackets(intercept, PacketPriority.CONTROL, appId,
                Optional.empty());
        log.info("Started");
        sendPackets();
    }

    @Deactivate
    public void deactivate() {
        packetService.removeProcessor(packetProcessor);
        flowRuleService.removeFlowRulesById(appId);
        flowRuleService.removeListener(flowListener);
        log.info("Stopped");
    }

    // Processes the specified IPV4 ping packet.
    private void processmyTunnel(PacketContext context) {
        DeviceId deviceId = context.inPacket().receivedFrom().deviceId();
        byte[] payloadBytes = context.inPacket().unparsed().array();
        myTunnel myTun = new myTunnel();
            try {
                myTun = myTunnel.deserializer().deserialize(
                        payloadBytes, 0, payloadBytes.length);
            } catch (DeserializationException dex) {
                log.error(dex.getMessage());
            }
        //log.info("PACKET = "+myTun);
        long I1 = byteArrayToLong(myTun.getTs_ing1());
        float I1f = I1;
        log.info("I1" + I1f);
        long E1 = byteArrayToLong(myTun.getTs_eg1());
        long IS2 = byteArrayToLong(myTun.getTs_is2());
        long ES2 = byteArrayToLong(myTun.getTs_es2());
        long I2 = byteArrayToLong(myTun.getTs_ing2());
        long E2 = byteArrayToLong(myTun.getTs_eg2());
        long rs1_1 = E1 - I1;
        long rs1_2 = E2 - I2;
        long rs2 = ES2 - IS2;
        long rtt = E2 - I1 - rs1_2;
        long owd = (rtt - rs2 - rs1_2) / 2;
        owd = owd*10;
        log.info("OWD = "+ owd + "e-7 secs");
        writeToFile(owd);
    }

    // Intercepts packets
    private class myTunnelProcessor implements PacketProcessor {
        @Override
        public void process(PacketContext context) {
            Ethernet eth = context.inPacket().parsed();
            //log.info("PACKETOUT = "+ context.outPacket().sendThrough());
            if (eth.getEtherType() == TYPE_MYTUNNEL) {
                processmyTunnel(context);
            }
        }
    }

    // Listens for our removed flows.
    private class InternalFlowListener implements FlowRuleListener {
        @Override
        public void event(FlowRuleEvent event) {
            FlowRule flowRule = event.subject();
            //log.info("FLOWRULE = "+flowRule);
        }
    }

    private static long byteArrayToLong(byte[] bytes) {
        long l = 0;
        for (int i=0; i<6; i++) {
            l <<= 8;
            l ^= (long) bytes[i] & 0xff;
        }
        return l;
    }



    private void writeToFile(long owd) {
        try {
            File myObj = new File("owd.txt");
            if (myObj.createNewFile()) {
                log.info("File created: " + myObj.getName());
            }
            Files.write(Paths.get("owd.txt"), (""+owd+"\n").getBytes(), StandardOpenOption.APPEND);
        } catch (IOException e) {
            log.info("An error occurred in opening owd.txt.");
            e.printStackTrace();
        }
    }
}