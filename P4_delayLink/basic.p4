/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>


#define HASH_BASE 10w0
#define HASH_MAX 10w1023
const bit<16> TYPE_MYTUNNEL = 0x1212;
const bit<16> TYPE_IPV4 = 0x800;
#define CPU_MIRROR_SESSION_ID                  250
/*************************************************************************
*********************** H E A D E R S  ***********************************
*************************************************************************/

typedef bit<9>  egressSpec_t;
typedef bit<48> macAddr_t;
typedef bit<32> ip4Addr_t;

struct queueing_metadata_t {
    bit<48> enq_timestamp;
    bit<19> enq_qdepth;
    bit<32> deq_timedelta;
    bit<19> deq_qdepth;
}

header queueing_metadata_t_padded {
    bit<48> enq_timestamp;
    bit<19> enq_qdepth;
    bit<32> deq_timedelta;
    bit<19> deq_qdepth;
    bit<2>  pad;
}

header ethernet_t {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16>   etherType;
}

header myTunnel_t {
    bit<16> proto_id;
    bit<16> dst_id;
    bit<16> nhop;
    bit<48> ts_ing1;
    bit<48> ts_eg1;
    bit<48> ts_is2;
    bit<48> ts_es2;
    bit<48> ts_ing2;
    bit<48> ts_eg2;
}

header ipv4_t {
    bit<4>    version;
    bit<4>    ihl;
    bit<8>    diffserv;
    bit<16>   totalLen;
    bit<16>   identification;
    bit<3>    flags;
    bit<13>   fragOffset;
    bit<8>    ttl;
    bit<8>    protocol;
    bit<16>   hdrChecksum;
    ip4Addr_t srcAddr;
    ip4Addr_t dstAddr;
}

struct ingress_metadata_t {

    bit<64> my_flowID;
    bit<64> my_estimated_count;
    bit<1> already_matched;
    bit<32> nhop_ipv4;
    bit<64> carry_min;
    bit<64> carry_min_plus_one;
    bit<8> min_stage;
    bit<1> do_recirculate;
    bit<9> orig_egr_port;

    bit<32> hashed_first;
    bit<32> hashed_second;
    bit<32> hashed_address_s3;

    bit<64> random_bits;
    bit<12> random_bits_short;
}

struct metadata {
    @name("ingress_metadata")
    ingress_metadata_t   ingress_metadata;
}

struct headers {
    ethernet_t   ethernet;
    myTunnel_t   myTunnel;
    ipv4_t       ipv4;
    @name(".queueing_hdr")
    queueing_metadata_t_padded queueing_hdr;
}

/*************************************************************************
*********************** P A R S E R  ***********************************
*************************************************************************/

parser MyParser(packet_in packet,
                out headers hdr,
                inout metadata meta,
                inout standard_metadata_t standard_metadata) {

    state start {
        transition parse_ethernet;
    }

    state parse_ethernet {
        packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.etherType) {
            TYPE_MYTUNNEL: parse_myTunnel;
            TYPE_IPV4: parse_ipv4;
            default: accept;
        }
    }

    state parse_myTunnel {
        packet.extract(hdr.myTunnel);
        packet.extract(hdr.queueing_hdr);
        transition select(hdr.myTunnel.proto_id) {
            TYPE_IPV4: parse_ipv4;
            default: accept;
        }
    }

    state parse_ipv4 {
        packet.extract(hdr.ipv4);
        transition accept;
    }

}

/*************************************************************************
************   C H E C K S U M    V E R I F I C A T I O N   *************
*************************************************************************/

control MyVerifyChecksum(inout headers hdr, inout metadata meta) {
    apply {  }
}


/*************************************************************************
**************  I N G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyIngress(inout headers hdr,
                  inout metadata meta,
                  inout standard_metadata_t standard_metadata) {

    action drop() {
        mark_to_drop(standard_metadata);
    }

    action ipv4_forward(macAddr_t dstAddr, egressSpec_t port) {
        standard_metadata.egress_spec = port;
        hdr.ethernet.srcAddr = hdr.ethernet.dstAddr;
        hdr.ethernet.dstAddr = dstAddr;
        hdr.ipv4.ttl = hdr.ipv4.ttl - 1;
    }

    table ipv4_lpm {
        key = {
            hdr.ipv4.dstAddr: lpm;
        }
        actions = {
            ipv4_forward;
            drop;
            NoAction;
        }
        size = 1024;
        default_action = NoAction();
    }

    action myTunnel_forward(egressSpec_t port) {
      standard_metadata.egress_spec = port;
      hdr.myTunnel.dst_id = (bit<16>)port;
    }

    table myTunnel_exact {
        key = {
            hdr.myTunnel.dst_id: exact;
        }
        actions = {
            myTunnel_forward;
            drop;
        }
        size = 1024;
        default_action = drop();
    }

    apply {
        if (hdr.ipv4.isValid() && !hdr.myTunnel.isValid()) {
            // Process only non-tunneled IPv4 packets
            ipv4_lpm.apply();
        }else if (hdr.myTunnel.isValid()) {
            hdr.myTunnel.nhop = hdr.myTunnel.nhop + 1;
            myTunnel_exact.apply();
        }
    }
}

/*************************************************************************
****************  E G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyEgress(inout headers hdr,
                 inout metadata meta,
                 inout standard_metadata_t standard_metadata) {
     action copy_queueing_data() {
         hdr.queueing_hdr.setValid();
         hdr.queueing_hdr.enq_timestamp = (bit<48>)standard_metadata.enq_timestamp;
         hdr.queueing_hdr.enq_qdepth = standard_metadata.enq_qdepth;
         hdr.queueing_hdr.deq_timedelta = standard_metadata.deq_timedelta;
         hdr.queueing_hdr.deq_qdepth = standard_metadata.deq_qdepth;
         hdr.queueing_hdr.pad = 2w0;
     }

     apply {
         //copy_queueing_data();
         if (hdr.myTunnel.isValid()) {
             if (hdr.myTunnel.nhop >= 2) {
                 if (hdr.myTunnel.nhop == 2) {
                      hdr.myTunnel.ts_ing1 = standard_metadata.ingress_global_timestamp;
                      hdr.myTunnel.ts_eg1 = standard_metadata.egress_global_timestamp;
                 }
                 if (hdr.myTunnel.nhop == 3) {
                      hdr.myTunnel.ts_is2 = standard_metadata.ingress_global_timestamp;
                      hdr.myTunnel.ts_es2 = standard_metadata.egress_global_timestamp;
                 }
                 if (hdr.myTunnel.nhop == 4) {
                      hdr.myTunnel.ts_ing2 = standard_metadata.ingress_global_timestamp;
                      hdr.myTunnel.ts_eg2 = standard_metadata.egress_global_timestamp;
                 }
             }
         }
     }
}

/*************************************************************************
*************   C H E C K S U M    C O M P U T A T I O N   **************
*************************************************************************/

control MyComputeChecksum(inout headers  hdr, inout metadata meta) {
     apply {
	update_checksum(
	    hdr.ipv4.isValid(),
            { hdr.ipv4.version,
	      hdr.ipv4.ihl,
              hdr.ipv4.diffserv,
              hdr.ipv4.totalLen,
              hdr.ipv4.identification,
              hdr.ipv4.flags,
              hdr.ipv4.fragOffset,
              hdr.ipv4.ttl,
              hdr.ipv4.protocol,
              hdr.ipv4.srcAddr,
              hdr.ipv4.dstAddr },
            hdr.ipv4.hdrChecksum,
            HashAlgorithm.csum16);

}
}
/*************************************************************************
***********************  D E P A R S E R  *******************************
*************************************************************************/

control MyDeparser(packet_out packet, in headers hdr) {
    apply {
        packet.emit(hdr.ethernet);
        packet.emit(hdr.myTunnel);
        packet.emit(hdr.ipv4);
    }
}

/*************************************************************************
***********************  S W I T C H  *******************************
*************************************************************************/

V1Switch(
MyParser(),
MyVerifyChecksum(),
MyIngress(),
MyEgress(),
MyComputeChecksum(),
MyDeparser()
) main;
