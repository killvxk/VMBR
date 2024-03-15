#include <boot/mmap.h>
#include <hardware/apic.h>
#include <vmm/vmm.h>
#include <lib/debug.h>
#include <vmm/vmcs.h>
#include <lib/instr.h>
#include <lib/msr.h>
#include <hardware/idt.h>
#include <hardware/pic8259.h>
#include <hardware/nic.h>
#include <lib/util.h>
#include <network/ethernet.h>
#include <network/ip.h>
#include <network/udp.h>
#include <network/dhcp.h>

int cboot(){

    init_real();
    init_mmap();

    init_pic();
    init_idt();
    init_nic();

    generate_dhcp_dora();

    LOG_DEBUG("IP: %x, Router: %x, Subnet: %x\n", get_ip_addr(), get_router_ip_addr(), get_subnet_mask());

    LOG_DEBUG("OVER\n");

    for(;;);
}
