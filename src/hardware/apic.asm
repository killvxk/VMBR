global InitializeSingleCore
global InitializeSingleCore_end
global cores_semaphore

section .real
cores_semaphore db 0

section .text

bits 16
InitializeSingleCore:

    cli

    mov eax, cr0
    or eax, CR0_PE
    mov cr0, eax

    lgdt [_gdt.pointer]

    jmp _gdt.code32:InitializeSingleCore.protected_mode
bits 32
    .protected_mode:

    UpdateSelectorsAX _gdt.data32

    ; Move p4 address to cr3
    mov eax, p4_table
    mov cr3, eax

    ; Enable PAE (Physical Address Extension)
    mov eax, cr4
    or eax, CR4_PAE
    mov cr4, eax

    ; Set long mode
    mov ecx, EFER_MSR
    rdmsr
    or eax, EFER_LM  
    wrmsr

    ; Enable paging
    mov eax, cr0
    or eax, CR0_PG
    mov cr0, eax

    jmp _gdt.code64:InitializeSingleCore.long_mode
bits 64
    .long_mode:
    
    UpdateSelectorsAX _gdt.data64

    xor rbx, rbx
    mov eax, 1
    xor ecx, ecx
    cpuid
    shr ebx, 24     ; now ebx = core id
    shl ebx, 12     ; now ebx = core id * 0x1000
    mov rsp, _sys_stack
    sub rsp, rbx

    mov al, 1
    mov byte [cores_semaphore], al

    hlt
    ret

InitializeSingleCore_end:
