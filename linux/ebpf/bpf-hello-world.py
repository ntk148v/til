from bcc import BPF

# Write the C program inside Python and store it as a string variable.
# or write it in a separate file and read that file into Python program.
#
# kprobe__sys_clone
# The name of the fucntion tells BCC where to attach it.
# `kprobe__` - a kprobe to trace a kernel function.
# `sys_clone` - which kernel function to trace.
#               The function can include as many of the probed function
#               arguments as you want, as long as the first argument `ctx`.
# `bpf_trace_printk` - print hello world to the kernel's common trace_pipe
program = """
int kprobe__sys_clone(void *ctx) {
    bpf_trace_printk("Hello World!\\n");
    return 0;
}
"""

# Load BPF program
b = BPF(text=program)

print("Tracing... Hit Ctrl+C to end")

# output
# Read kernel's trace_pipe and print the messages
print("%-18s %-16s %-6s %s" % ("TIME(s)", "COMMAND", "PID", "MESSAGE"))
while True:
    try:
        (task, pid, cpu, flags, ts, msg) = b.trace_fields()
    except ValueError:
        continue
    except KeyboardInterrupt:
        print("Bye bye!")
        break
    except Exception as e:
        raise e
    print("%-18.9f %-16s %-6d %s" % (ts, task.decode(), pid, msg.decode()))
