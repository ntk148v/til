# Use FIO for Block Volume Performance Tests

Source:

- <https://docs.oracle.com/en-us/iaas/Content/Block/References/samplefiocommandslinux.htm>
- <https://portal.nutanix.com/page/documents/kbs/details?targetId=kA07V000000LX7xSAG>

Table of contents:

- [Use FIO for Block Volume Performance Tests](#use-fio-for-block-volume-performance-tests)
  - [0. Before we start](#0-before-we-start)
  - [1. IOPS Performance Tests](#1-iops-performance-tests)
  - [2. Throughput Performance Tests](#2-throughput-performance-tests)
  - [3. Latency Performance Tests](#3-latency-performance-tests)

## 0. Before we start

- You can run the commands directly or create a job file with the command and then run the job file.
- **Do not run FIO tests with a write workload (`readwrite`, `randrw`, `write`, `trimwrite`) directly against a device that is in use.**

## 1. IOPS Performance Tests

- Test random reads:
  - Shell:

  ```shell
  sudo fio --filename=device name --direct=1 --rw=randread --bs=4k --ioengine=libaio --iodepth=256 --runtime=120 --numjobs=4 --time_based --group_reporting --name=iops-test-job --eta-newline=1 --readonly
  ```

  - Job `randomread.fio` file:

  ```fio
    [global]
    bs=4K
    iodepth=256
    direct=1
    ioengine=libaio
    group_reporting
    time_based
    runtime=120
    numjobs=4
    name=raw-randread
    rw=randread

    [job1]
    filename=device name
  ```

  ```shell
  fio randomread.fio
  ```

- Test file random read/writes:
  - Run the following command against the mount point to test file read/writes::

  ```shell
  sudo fio --filename=/custom mount point/file --size=500GB --direct=1 --rw=randrw --bs=4k --ioengine=libaio --iodepth=256 --runtime=120 --numjobs=4 --time_based --group_reporting --name=iops-test-job --eta-newline=1
  ```

- Test random read/writes:
  - Run the following command to test random read/writes::

  ```shell
  sudo fio --filename=device name --direct=1 --rw=randrw --bs=4k --ioengine=libaio --iodepth=256 --runtime=120 --numjobs=4 --time_based --group_reporting --name=iops-test-job --eta-newline=1
  ```

  - Job `randomreadwrite.fio` file:

  ```fio
  [global]
  bs=4K
  iodepth=256
  direct=1
  ioengine=libaio
  group_reporting
  time_based
  runtime=120
  numjobs=4
  name=raw-randreadwrite
  rw=randrw

  [job1]
  filename=device name
  ```

  ```shell
  fio randomreadwrite.fio
  ```

- Test sequential reads: For workloads that enable you to take advantage of sequential access patterns, such as database workloads, you can confirm performance for this pattern by testing sequential reads.
  - Run the following command to test sequential reads:

  ```shell
  sudo fio --filename=device name --direct=1 --rw=read --bs=4k --ioengine=libaio --iodepth=256 --runtime=120 --numjobs=4 --time_based --group_reporting --name=iops-test-job --eta-newline=1 --readonly
  ```

  - Job `fioread.fio` file:

  ```fio
  [global]
  bs=4K
  iodepth=256
  direct=1
  ioengine=libaio
  group_reporting
  time_based
  runtime=120
  numjobs=4
  name=raw-read
  rw=read

  [job1]
  filename=device name
  ```

  ```shell
  fio read.fio
  ```

## 2. Throughput Performance Tests

- Test random reads:
  - Run the following command to test random reads:

  ```shell
  sudo fio --filename=device name --direct=1 --rw=randread --bs=64k --ioengine=libaio --iodepth=64 --runtime=120 --numjobs=4 --time_based --group_reporting --name=throughput-test-job --eta-newline=1 --readonly
  ```

  - Job `randomread.fio` file:

  ```fio
  [global]
  bs=64K
  iodepth=64
  direct=1
  ioengine=libaio
  group_reporting
  time_based
  runtime=120
  numjobs=4
  name=raw-randread
  rw=randread

  [job1]
  filename=device name
  ```

  ```shell
  fio randomread.fio
  ```

- Test file random read/writes:
  - Run the following command against the mount point to test file read/writes:

  ```shell
  sudo fio --filename=/custom mount point/file --size=500GB --direct=1 --rw=randrw --bs=64k --ioengine=libaio --iodepth=64 --runtime=120 --numjobs=4 --time_based --group_reporting --name=throughput-test-job --eta-newline=1
  ```

- Test random read/writes:
  - Run the following command to test random read/writes:

  ```shell
  sudo fio --filename=device name --direct=1 --rw=randrw --bs=64k --ioengine=libaio --iodepth=64 --runtime=120 --numjobs=4 --time_based --group_reporting --name=throughput-test-job --eta-newline=1
  ```

  - Job `randomreadwrite.fio` file:

  ```fio
  [global]
  bs=64K
  iodepth=64
  direct=1
  ioengine=libaio
  group_reporting
  time_based
  runtime=120
  numjobs=4
  name=raw-randreadwrite
  rw=randrw

  [job1]
  filename=device name
  ```

  ```shell
  fio randomreadwrite.fio
  ```

- Test sequential reads: For workloads that enable you to take advantage of sequential access patterns, such as database workloads, you can confirm performance for this pattern by testing sequential reads.
  - Run the following command to test sequential reads:

  ```shell
  sudo fio --filename=device name --direct=1 --rw=read --bs=64k --ioengine=libaio --iodepth=64 --runtime=120 --numjobs=4 --time_based --group_reporting --name=throughput-test-job --eta-newline=1 --readonly
  ```

  - Job `read.fio` file:

  ```fio
  [global]
  bs=64K
  iodepth=64
  direct=1
  ioengine=libaio
  group_reporting
  time_based
  runtime=120
  numjobs=4
  name=raw-read
  rw=read

  [job1]
  filename=device name
  ```

  ```shell
  fio read.fio
  ```

## 3. Latency Performance Tests

- Test random reads for latency:
  - Run the following command directly to test random reads for latency:

  ```shell
  sudo fio --filename=device name --direct=1 --rw=randread --bs=4k --ioengine=libaio --iodepth=1 --numjobs=1 --time_based --group_reporting --name=readlatency-test-job --runtime=120 --eta-newline=1 --readonly
  ```

  - Job `randomreadlatency.fio` file:

  ```fio
  [global]
  bs=4K
  iodepth=1
  direct=1
  ioengine=libaio
  group_reporting
  time_based
  runtime=120
  numjobs=1
  name=readlatency-test-job
  rw=randread

  [job1]
  filename=device name
  ```

  ```shell
  fio randomreadlatency.fio
  ```

- Test random read/writes for latency:
  - Run the following command directly to test random read/writes for latency:

  ```shell
  sudo fio --filename=device name --direct=1 --rw=randrw --bs=4k --ioengine=libaio --iodepth=1 --numjobs=1 --time_based --group_reporting --name=rwlatency-test-job --runtime=120 --eta-newline=1
  ```

  - Job `randomrwlatency.fio` file:

  ```fio
  [global]
  bs=4K
  iodepth=1
  direct=1
  ioengine=libaio
  group_reporting
  time_based
  runtime=120
  numjobs=1
  name=rwlatency-test-job
  rw=randrw

  [job1]
  filename=device name
  ```

  ```shell
  fio randomrwlatency.fio
  ```
