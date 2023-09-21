Hermes is a multi-tiered I/O buffering platform. This module encompasses
a series of microbenchmarks used to test the performance of the Hermes
native API

# Installation

```bash
spack install hermes@master
OR 
spack install hermes@dev-1.1
```

# Usage

```
spack load hermes
jarvis pipeline create hermes_bench
jarvis pipeline env build
jarvis pipeline append hermes --sleep=5
jarvis pipeline append hermes_api_bench
jarvis pipeline run
```

## PutGet benchmark

```
jarvis pkg configure hermes_bench \
mode=putget \
blob_size=1m \
blobs_per_rank=64 \
nprocs=64
```

## PartialPutGet benchmark

```
jarvis pkg configure hermes_bench \
mode=pputget \
blobs_per_rank=64 \
blob_size=1m \
part_size=4k \
nprocs=64
```

## Create Bucket benchmark

```
jarvis pkg configure hermes_bench \
mode=create_bkt \
bkts_per_rank=1024 \
nprocs=64
```

## Get Bucket benchmark

```
jarvis pkg configure hermes_bench \
mode=get_bkt \
bkts_per_rank=1024 \
nprocs=64
```

## Delete Bucket benchmark

```
jarvis pkg configure hermes_bench \
mode=del_bkt \
bkts_per_rank=1024 \
blobs_per_bkt=1024 \
nprocs=64
```
