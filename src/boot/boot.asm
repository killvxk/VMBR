%include "src/boot/macros.asm"

global _start

%define MEM_SIZE 512

section .rodata
%include "src/boot/gdt.asm"

section .bss

align 0x1000
    resb 0x2000
_sys_stack:

section .text


bits 32
_start:
    call InitializePageTables
    call ProtectedToLong

bits 64
    mov rsp, _sys_stack  ; stack initialization
    
    extern cboot:function
    call cboot
    hlt

%include "src/boot/paging.asm"
%include "src/boot/real_mode.asm"
;%include "src/boot/mode-transitions.asm"

section .mb2_header
%include "src/boot/mb2_header.asm"
