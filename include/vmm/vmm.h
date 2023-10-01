#ifndef __VMM_H
#define __VMM_H
#include <lib/types.h>

extern void vmentry_handler();
extern void vmexit_handler();

#define CPUID_VMXON (1<<5)
#define CR4_VMXE (1 << 13)
#define CR0_NE (1 << 5)

typedef struct __attribute__((__packed__)) {
    union {
        uint32_t revision_id;
        struct __attribute__((__packed__)){
            uint32_t : 31;
            uint32_t shadow_vmcs_indicator : 1;
        };
    };
    uint32_t vmx_abort;
    // vmcs data
} vmcs_t;

extern void init_vmm(void);
#endif