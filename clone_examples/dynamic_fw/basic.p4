#include <core.p4>
#include <v1model.p4>

const bit<32> P2 = 2;
const bit<32> P3 = 3;

const bit<16> TYPE_IPV4 = 0x800;
const bit<16> PROGRAM_ETYPE = 0x1234;
const bit<8>  PROGRAM_P     = 0x50;   // 'P'

typedef bit<9>  egressSpec_t;
typedef bit<48> macAddr_t;
typedef bit<32> ip4Addr_t;

header program_t {
    bit<8>  flag;
    bit<32> operation;
}

struct intrinsic_metadata_t {
    bit<4>  mcast_grp;
    bit<4>  egress_rid;
    bit<16> mcast_hash;
    bit<32> lf_field_list;
}



header ethernet_t {
    bit<48> dstAddr;
    bit<48> srcAddr;
    bit<16> etherType;
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



struct metadata {
    @name(".intrinsic_metadata")
    intrinsic_metadata_t intrinsic_metadata;
}


struct headers {
    ethernet_t   ethernet;
    ipv4_t   ipv4;
    program_t program;
}



parser ParserImpl(packet_in packet, out headers hdr, inout metadata meta, inout standard_metadata_t standard_metadata) {
    @name(".start") state start {
        transition parse_ethernet;
    }
    @name(".parse_ethernet") state parse_ethernet {
        packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.etherType) {
            TYPE_IPV4: parse_ipv4;
            PROGRAM_ETYPE: parse_program;
            default: accept;
        }
    }
    @name(".parse_ipv4")state parse_ipv4 {
        packet.extract(hdr.ipv4);
        transition accept;
    }

    state parse_program {
        transition select(packet.lookahead<program_t>().flag) {
            (PROGRAM_P) : parse_progop;
            default : accept;
        }
    }

    state parse_progop {
        packet.extract(hdr.program);
        transition accept;
    }

}



control ingress(inout headers hdr, inout metadata meta, inout standard_metadata_t standard_metadata) {

    register<bit<32>>(1) set_flow;

    action drop() {
        mark_to_drop(standard_metadata);
    }

    action ipv4_forward(macAddr_t dstAddr, egressSpec_t port) {
        standard_metadata.egress_spec=port;
      	hdr.ethernet.srcAddr=hdr.ethernet.dstAddr;
      	hdr.ethernet.dstAddr=dstAddr;
      	hdr.ipv4.ttl=hdr.ipv4.ttl - 1;
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
        default_action = NoAction();
    }

    action do_clone(bit<32> session) {
          clone3(CloneType.I2E, session, { standard_metadata });
    }

    action do_program(bit<32> operation) {
          set_flow.write( (bit<32>)0 ,operation);
    }

    apply {
        bit<32> mod = 0;

        if (hdr.program.isValid()) {
            do_program(hdr.program.operation);
        }

        if(hdr.ipv4.isValid() && !hdr.program.isValid()){
          ipv4_lpm.apply();
          set_flow.read(mod,0);
        }

        // cloning to the right direction
        if(mod == P2) do_clone(32w251);
        if(mod == P3) do_clone(32w252);

    }
}

control egress(inout headers hdr, inout metadata meta, inout standard_metadata_t standard_metadata) {
    apply {}
}

control DeparserImpl(packet_out packet, in headers hdr) {
    apply {
        packet.emit(hdr.ethernet);
        packet.emit(hdr.ipv4);
        packet.emit(hdr.program);
    }
}

control verifyChecksum(inout headers hdr, inout metadata meta) {
    apply {}
}

control computeChecksum(inout headers hdr, inout metadata meta) {
    apply {}
}

V1Switch(ParserImpl(), verifyChecksum(), ingress(), egress(), computeChecksum(), DeparserImpl()) main;
