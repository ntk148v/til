# GraalVM

Source:

- <https://rieckpil.de/whatis-graalvm/>
- <https://www.cesarsotovalero.net/blog/aot-vs-jit-compilation-in-java.html>

Table of contents:

- [GraalVM](#graalvm)
  - [1. History of the HotSpot Java Virtual Machine, and JIT](#1-history-of-the-hotspot-java-virtual-machine-and-jit)
  - [2. AOT, and GraalVM](#2-aot-and-graalvm)
  - [3. JIT vs. AOT](#3-jit-vs-aot)

> **TL;DR**: GraalVM is an extension of the JVM written in pure Java, developed by Oracle and supporting a **polygot** programming model and **ahead-of-time (AOT)** compilation.

## 1. History of the HotSpot Java Virtual Machine, and JIT

- It was the main Java virtual machine maintained and distributed by Oracle to run Java program for many years.
- The main purpose is to run Java bytecode (`.class` files) and continuously analyze the program's performance for so-called _hot spots_ within the program, which are executed often and to **just-in-time (JIT)** compile them to native code (machine code) for improved performance.
- When compiling a Java program, we end up with our source code transformed into an intermediate representation which is platform-independent (aka. JVM bytecode).
- A compiler transforms JVM bytecode into a binary representation which is platform-dependent. This means that the program can be executed only in a computer with the architecture in which it was originally compiled.
- To transform JVM bytecode into machine code that is executable in a specific hardware architecture, the JVM **interprets the bytecode at runtime** and figures out in which architecture is the program running. The strategy is known as JIT compilation.
- The default JIT compiler in the JVM is known as the Hotspot compiler. The OpenJDK compiler is a free version of this interpreter written in Java.

![](https://www.cesarsotovalero.net/assets/resized/java_source_code_compilation-640x307.png)

- Despite the advances in JIT compilers, Java applications are still a lot slower than other languages such as C or Rust, which produce native code directly.

![](https://cdn-aoloc.nitrocdn.com/LjZAnpMBiKRdWkhommfnyugsAOnHWdxL/assets/images/optimized/rev-a07f7c6/rieckpil.de/wp-content/uploads/2019/03/hotSpotJITSimplified.png.webp)

## 2. AOT, and GraalVM

- With Java 9 and specially the [JEP 295](https://openjdk.java.net/jeps/295), the JDK got an AOT compiler `jaotc`. This compiler uses the OpenJDK project Graal for backend code generation.
- AOT compilation is a form of static compilation that consists in transforming the program into a machine code **before it is executed**.

![](https://cdn-aoloc.nitrocdn.com/LjZAnpMBiKRdWkhommfnyugsAOnHWdxL/assets/images/optimized/rev-a07f7c6/rieckpil.de/wp-content/uploads/2019/03/aotJavaSimplified.png.webp)

- It improves start-up time as the JIT compiler does have to intercept the program's execution. The main downside of this approach is the platform-depended native code. This may lead to a platform lock for this AOT compiled code.

- Based on the Graal Compiler, Oracle started to develop the GraalVM to avoid working with the big ad complex C/C++ codebase of the HotSpot JVM but also tackle the current polygot movement with a virtual machine written in Java.

![](https://cdn-aoloc.nitrocdn.com/LjZAnpMBiKRdWkhommfnyugsAOnHWdxL/assets/images/optimized/rev-a07f7c6/rieckpil.de/wp-content/uploads/2019/03/graalArchitectureOne.jpg.webp)

- The GraalVM compiler can perform a highly optimized AOT compilation of JVM bytecode. The focus of the GraalVM is on offering high performance and extensibility of modern Java applications. This mean it executes faster with less overhead, which translates into optimal resource consumption with less CPU and memory.
- AOT compilation process in the GraalVM compiler using its `native-image` technology.
  - It receives as input all classes from the application, libraries, the JDK, and the JVM.
  - An itertive bytecode search using state-of-the-art points-to-analysis is performed until a fixed point is reached.
  - During this process all the safe classes are initialized upfront statically.
  - The class data of the initialized classes is loaded into the image heap which then, in turn, gets saved into standalone executable.
  - The result is a native image executable that can be shipped and deployed directly in a container.

![](https://www.cesarsotovalero.net/assets/resized/native_image_creation_process-768x228.png)

## 3. JIT vs. AOT

- Which approach is the best to use? **It depends**.
- JIT compilers make programs cross-platform. It also reduce latency thanks to the ability to use concurrent garbage collectors and increase the resilience under peak throughput conditions.
- AOT compilers run programs more efficiently.
  - Suit for cloud applications, containerized.

![](https://www.cesarsotovalero.net/assets/resized/aot_vs_jit-768x472.jpeg)
