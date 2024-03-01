#ifndef __HOOKS_H
#define __HOOKS_H

#include <lib/types.h>

#define E820_MAGIC 0x0534D4150
#define RFLAGS_CARRY (1<<0)

extern void setup_int15h_hook();
extern void handle_int15h_hook();
#endif