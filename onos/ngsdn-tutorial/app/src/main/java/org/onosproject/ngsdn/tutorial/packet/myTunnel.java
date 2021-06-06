/*
 * Copyright 2014-present Open Networking Foundation
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

package org.onosproject.ngsdn.tutorial.packet;

import java.nio.ByteBuffer;
import java.util.Arrays;
import java.util.Collection;
import java.util.Map;
import org.onlab.packet.*;

import com.google.common.collect.ImmutableMap;
import org.onlab.packet.Deserializer;

import static com.google.common.base.MoreObjects.toStringHelper;
import static org.onlab.packet.PacketUtils.*;

/**
 * Implements IPv4 packet format.
 */
public class myTunnel extends BasePacket {
    public static final short TYPE_MYTUNNEL = 0x1212;
    public static final short DATALAYER_TIMESTAMP_LENGTH = 6; // bytes

    private static final short HEADER_LENGTH = 56;

    protected MacAddress destinationMACAddress;
    protected MacAddress sourceMACAddress;
    protected short etherType = TYPE_MYTUNNEL;
    protected short pid = 0;
    protected short dst_id = 0;
    protected short nhop = 0;
    protected byte[] ts_ing1 = new byte[DATALAYER_TIMESTAMP_LENGTH];
    protected byte[] ts_eg1 = new byte[DATALAYER_TIMESTAMP_LENGTH];
    protected byte[] ts_is2 = new byte[DATALAYER_TIMESTAMP_LENGTH];
    protected byte[] ts_es2 = new byte[DATALAYER_TIMESTAMP_LENGTH];
    protected byte[] ts_ing2 = new byte[DATALAYER_TIMESTAMP_LENGTH];
    protected byte[] ts_eg2 = new byte[DATALAYER_TIMESTAMP_LENGTH];


    public myTunnel() {
        super();
    }

    public short getPid() {
        return pid;
    }

    public void setPid(short pid) {
        this.pid = pid;
    }

    public short getDst_id() {
        return dst_id;
    }

    public void setDst_id(short dst_id) {
        this.dst_id = dst_id;
    }

    public short getNhop() {
        return nhop;
    }

    public void setNhop(short nhop) {
        this.nhop = nhop;
    }

    public byte[] getTs_ing1() {
        return ts_ing1;
    }

    public void setTs_ing1(byte[] ts_ing1) {
        this.ts_ing1 = ts_ing1;
    }

    public byte[] getTs_eg1() {
        return ts_eg1;
    }

    public void setTs_eg1(byte[] ts_eg1) {
        this.ts_eg1 = ts_eg1;
    }

    public byte[] getTs_is2() {
        return ts_is2;
    }

    public void setTs_is2(byte[] ts_is2) {
        this.ts_is2 = ts_is2;
    }

    public byte[] getTs_es2() {
        return ts_es2;
    }

    public void setTs_es2(byte[] ts_es2) {
        this.ts_es2 = ts_es2;
    }

    public byte[] getTs_ing2() {
        return ts_ing2;
    }

    public void setTs_ing2(byte[] ts_ing2) {
        this.ts_ing2 = ts_ing2;
    }

    public byte[] getTs_eg2() {
        return ts_eg2;
    }

    public void setTs_eg2(byte[] ts_eg2) {
        this.ts_eg2 = ts_eg2;
    }

    public MacAddress getDestinationMACAddress() {
        return destinationMACAddress;
    }

    public void setDestinationMACAddress(final byte[] destinationMac) {
        this.destinationMACAddress = MacAddress.valueOf(destinationMac);
    }

    public void setDestinationMACAddress(final String destinationMac) {
        this.destinationMACAddress = MacAddress.valueOf(destinationMac);
    }

    public MacAddress getSourceMACAddress() {
        return sourceMACAddress;
    }

    public void setSourceMACAddress(final byte[] sourceMac) {
        this.sourceMACAddress = MacAddress.valueOf(sourceMac);
    }

    public void setSourceMACAddress(final String sourceMac) {
        this.sourceMACAddress = MacAddress.valueOf(sourceMac);
    }

    public short getEtherType() {
        return etherType;
    }

    public void setEtherType(short etherType) {
        this.etherType = etherType;
    }

    /**
     * Serializes the packet. Will compute and set the following fields if they
     * are set to specific values at the time serialize is called: -checksum : 0
     * -headerLength : 0 -totalLength : 0
     */
    @Override
    public byte[] serialize() {
        byte[] payloadData = null;
        if (this.payload != null) {
            this.payload.setParent(this);
            payloadData = this.payload.serialize();
        }

        final byte[] data = new byte[HEADER_LENGTH];
        final ByteBuffer bb = ByteBuffer.wrap(data);
        bb.put(this.destinationMACAddress.toBytes());
        bb.put(this.sourceMACAddress.toBytes());
        bb.putShort(this.etherType);
        bb.putShort(this.pid);
        bb.putShort(this.dst_id);
        bb.putShort(this.nhop);
        bb.put(this.ts_ing1);
        bb.put(this.ts_eg1);
        bb.put(this.ts_is2);
        bb.put(this.ts_es2);
        bb.put(this.ts_ing2);
        bb.put(this.ts_eg2);

        if (payloadData != null) {
            bb.put(payloadData);
        }

        return data;
    }

    @Override
    public int hashCode() {
        final int prime = 2521;
        int result = super.hashCode();
        result = prime * result + this.pid;
        result = prime * result + this.dst_id;
        result = prime * result + this.nhop;
        result = prime * result + Arrays.hashCode(this.ts_ing1);
        result = prime * result + Arrays.hashCode(this.ts_eg1);
        result = prime * result + Arrays.hashCode(this.ts_is2);
        result = prime * result + Arrays.hashCode(this.ts_es2);
        result = prime * result + Arrays.hashCode(this.ts_ing2);
        result = prime * result + Arrays.hashCode(this.ts_eg2);
        return result;
    }

    /*
     * (non-Javadoc)
     *
     * @see java.lang.Object#equals(java.lang.Object)
     */
    @Override
    public boolean equals(final Object obj) {
        if (this == obj) {
            return true;
        }
        if (!super.equals(obj)) {
            return false;
        }
        if (!(obj instanceof myTunnel)) {
            return false;
        }
        final myTunnel other = (myTunnel) obj;
        if (this.pid != other.pid) {
            return false;
        }
        if (this.dst_id != other.dst_id) {
            return false;
        }
        if (this.nhop != other.nhop) {
            return false;
        }
        if (this.ts_ing1 != other.ts_ing1) {
            return false;
        }
        if (this.ts_eg1 != other.ts_eg1) {
            return false;
        }
        if (this.ts_is2 != other.ts_is2) {
            return false;
        }
        if (this.ts_es2 != other.ts_es2) {
            return false;
        }
        if (this.ts_ing2 != other.ts_ing2) {
            return false;
        }
        if (this.ts_eg2 != other.ts_eg2) {
            return false;
        }
        return true;
    }

    /**
     * Deserializer function for IPv4 packets.
     *
     * @return deserializer function
     */
    public static Deserializer<myTunnel> deserializer() {
        return (data, offset, length) -> {
            checkInput(data, offset, length, HEADER_LENGTH);

            myTunnel myTun = new myTunnel();

            byte[] addressBuffer = new byte[DATALAYER_TIMESTAMP_LENGTH];
            final ByteBuffer bb = ByteBuffer.wrap(data, offset, length);
            bb.get(addressBuffer);
            myTun.setDestinationMACAddress(addressBuffer);

            bb.get(addressBuffer);
            myTun.setSourceMACAddress(addressBuffer);

            short ethType = bb.getShort();
            myTun.setEtherType(ethType);

            myTun.pid = bb.getShort();
            myTun.dst_id = bb.getShort();
            myTun.nhop = bb.getShort();
            myTun.ts_ing1 = new byte[DATALAYER_TIMESTAMP_LENGTH];
            bb.get(myTun.ts_ing1);
            myTun.ts_eg1 = new byte[DATALAYER_TIMESTAMP_LENGTH];
            bb.get(myTun.ts_eg1);
            myTun.ts_is2 = new byte[DATALAYER_TIMESTAMP_LENGTH];
            bb.get(myTun.ts_is2);
            myTun.ts_es2 = new byte[DATALAYER_TIMESTAMP_LENGTH];
            bb.get(myTun.ts_es2);
            myTun.ts_ing2 = new byte[DATALAYER_TIMESTAMP_LENGTH];
            bb.get(myTun.ts_ing2);
            myTun.ts_eg2 = new byte[DATALAYER_TIMESTAMP_LENGTH];
            bb.get(myTun.ts_eg2);

            return myTun;
        };
    }

    @Override
    public String toString() {
        return toStringHelper(getClass())
                .add("pid", Short.toString(pid))
                .add("dst_id", Short.toString(dst_id))
                .add("nhop", Short.toString(nhop))
                .add("ts_ing1", byteArrayToLong(ts_ing1))
                .add("ts_eg1", byteArrayToLong(ts_eg1))
                .add("ts_is2", byteArrayToLong(ts_is2))
                .add("ts_es2", byteArrayToLong(ts_es2))
                .add("ts_ing2", byteArrayToLong(ts_ing2))
                .add("ts_eg2", byteArrayToLong(ts_eg2))
                .toString();
    }

    private static long byteArrayToLong(byte[] bytes) {
        long l = 0;
        for (int i=0; i<6; i++) {
            l <<= 8;
            l ^= (long) bytes[i] & 0xff;
        }
        return l;
    }
}