#include <linux/bpf.h>
#include <linux/pkt_cls.h>
#include <linux/if_ether.h>
#include <arpa/inet.h>

// For each packet (skb), locate the memory address that holds the starting address
// of the ethernet header
// Retrieve the next-proto-info in ethernet header
// - if h_proto == ARP, return a flag (TC_ACT_SHOT) dictating the kernel to drop this packet,
// - otherwise, return a TC_ACT_OK flag indicating the kernel to continue its subsequent processing.

// Filter the given traffic/packets
__attribute__((section("ingress"), used))
int drop(struct __sk_buff *skb) {
    void *data = (void*)(long)skb->data;
    void *data_end = (void*)(long)skb->data_end;

    if (data_end < data + ETH_HLEN)
        return TC_ACT_OK; // Not our packet, return it back to kernel

    struct ethhdr *eth = data;
    if (eth->h_proto != htons(ETH_P_ARP))
       return TC_ACT_OK;

    return TC_ACT_SHOT;
}
