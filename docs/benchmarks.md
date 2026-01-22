# Performance Benchmarks

This page presents performance benchmarks for ECUtils across different configurations and elliptic curves. These benchmarks help you understand the trade-offs between different coordinate systems and caching strategies.

## Test Environment

- **Python Version:** 3.13
- **Platform:** Linux
- **Methodology:** Each operation was measured using `timeit` with multiple iterations to ensure statistical significance.

## Configuration Options

ECUtils supports two main performance optimization options:

1. **Coordinate System:**
   - **Jacobian (Projective):** Uses projective coordinates to avoid expensive modular inversions during intermediate calculations. This is the default and recommended setting.
   - **Affine:** Traditional coordinate system with modular inversion at each step.

2. **LRU Cache:**
   - **Enabled (default):** Caches results of point operations, dramatically improving performance for repeated operations.
   - **Disabled:** No caching, useful for memory-constrained environments.

## Benchmark Results

### Jacobian Coordinates with LRU Cache (Recommended)

This is the default and fastest configuration for most use cases.

| Curve | Point Addition (us) | Point Doubling (us) | Scalar Multiplication (ms) | Koblitz Encoding (ms) | Signature Generation (ms) | Signature Verification (ms) | Diffie-Hellman (ms) | Massey-Omura (ms) |
|-------|---------------------|---------------------|----------------------------|-----------------------|---------------------------|-----------------------------|--------------------|-------------------|
| secp192k1 | 3.64 | 2.18 | 0.01 | 0.02 | 0.01 | 0.03 | 0.01 | 0.01 |
| secp192r1 | 3.60 | 2.20 | 0.02 | 0.01 | 0.01 | 0.03 | 0.01 | 0.02 |
| secp224k1 | 3.39 | 2.26 | 0.02 | N/A | 0.02 | 0.04 | 0.02 | N/A |
| secp224r1 | 3.34 | 2.38 | 0.02 | N/A | 0.02 | 0.04 | 0.02 | N/A |
| secp256k1 | 3.52 | 2.32 | 0.02 | 0.02 | 0.02 | 0.04 | 0.02 | 0.02 |
| secp256r1 | 3.65 | 2.29 | 0.02 | 0.03 | 0.02 | 0.04 | 0.02 | 0.02 |
| secp384r1 | 3.51 | 2.28 | 0.05 | 0.06 | 0.05 | 0.09 | 0.05 | 0.05 |
| secp521r1 | 4.04 | 2.52 | 0.09 | 0.20 | 0.09 | 0.18 | 0.09 | 0.09 |

**Note:** N/A indicates that Koblitz encoding is not supported for curves with cofactor != 1.

### Jacobian Coordinates without LRU Cache

| Curve | Point Addition (us) | Point Doubling (us) | Scalar Multiplication (ms) | Koblitz Encoding (ms) | Signature Generation (ms) | Signature Verification (ms) | Diffie-Hellman (ms) | Massey-Omura (ms) |
|-------|---------------------|---------------------|----------------------------|-----------------------|---------------------------|-----------------------------|--------------------|-------------------|
| secp192k1 | 139.88 | 96.80 | 9.89 | 1.57 | 9.73 | 29.10 | 0.99 | 9.96 |
| secp192r1 | 151.30 | 95.38 | 10.25 | 1.01 | 10.26 | 30.69 | 1.02 | 10.33 |
| secp224k1 | 168.39 | 106.10 | 12.34 | N/A | 12.55 | 38.15 | 1.25 | N/A |
| secp224r1 | 165.98 | 120.51 | 13.42 | N/A | 13.20 | 40.23 | 1.40 | N/A |
| secp256k1 | 189.12 | 135.68 | 15.79 | 1.81 | 16.34 | 47.26 | 1.57 | 15.61 |
| secp256r1 | 196.16 | 140.40 | 17.35 | 2.29 | 17.51 | 53.48 | 1.74 | 17.39 |
| secp384r1 | 312.98 | 249.14 | 39.42 | 6.29 | 39.34 | 119.26 | 4.02 | 39.66 |
| secp521r1 | 465.60 | 355.00 | 79.38 | 19.38 | 80.78 | 240.85 | 7.95 | 79.34 |

### Affine Coordinates with LRU Cache

| Curve | Point Addition (us) | Point Doubling (us) | Scalar Multiplication (ms) | Koblitz Encoding (ms) | Signature Generation (ms) | Signature Verification (ms) | Diffie-Hellman (ms) | Massey-Omura (ms) |
|-------|---------------------|---------------------|----------------------------|-----------------------|---------------------------|-----------------------------|--------------------|-------------------|
| secp192k1 | 3.69 | 2.18 | 0.04 | 0.02 | 0.04 | 0.06 | 0.03 | 0.03 |
| secp192r1 | 3.57 | 2.21 | 0.04 | 0.01 | 0.04 | 0.07 | 0.04 | 0.04 |
| secp224k1 | 3.47 | 2.40 | 0.05 | N/A | 0.05 | 0.08 | 0.04 | N/A |
| secp224r1 | 3.29 | 2.20 | 0.05 | N/A | 0.05 | 0.08 | 0.05 | N/A |
| secp256k1 | 3.44 | 2.26 | 0.07 | 0.02 | 0.07 | 0.12 | 0.06 | 0.07 |
| secp256r1 | 3.65 | 2.32 | 0.07 | 0.03 | 0.07 | 0.11 | 0.06 | 0.07 |
| secp384r1 | 3.55 | 2.32 | 0.15 | 0.07 | 0.15 | 0.26 | 0.15 | 0.16 |
| secp521r1 | 3.63 | 2.32 | 0.30 | 0.20 | 0.29 | 0.49 | 0.31 | 0.31 |

### Affine Coordinates without LRU Cache

| Curve | Point Addition (us) | Point Doubling (us) | Scalar Multiplication (ms) | Koblitz Encoding (ms) | Signature Generation (ms) | Signature Verification (ms) | Diffie-Hellman (ms) | Massey-Omura (ms) |
|-------|---------------------|---------------------|----------------------------|-----------------------|---------------------------|-----------------------------|--------------------|-------------------|
| secp192k1 | 113.92 | 99.93 | 30.68 | 1.60 | 9.77 | 28.49 | 0.94 | 9.42 |
| secp192r1 | 110.87 | 94.18 | 31.64 | 1.00 | 10.17 | 31.00 | 1.02 | 10.25 |
| secp224k1 | 121.29 | 108.45 | 44.08 | N/A | 12.55 | 37.55 | 1.25 | N/A |
| secp224r1 | 126.18 | 124.80 | 43.43 | N/A | 13.16 | 40.18 | 1.26 | N/A |
| secp256k1 | 146.20 | 134.37 | 57.40 | 1.80 | 16.26 | 49.53 | 1.61 | 16.12 |
| secp256r1 | 156.11 | 145.07 | 57.87 | 2.32 | 17.24 | 51.21 | 1.65 | 16.42 |
| secp384r1 | 240.58 | 247.35 | 141.55 | 6.27 | 39.11 | 118.42 | 4.04 | 40.46 |
| secp521r1 | 392.27 | 359.29 | 301.78 | 19.41 | 80.98 | 245.52 | 8.31 | 83.39 |

## Key Insights

### LRU Cache Impact

The LRU cache provides dramatic performance improvements:

- **Point Addition:** ~38x faster with cache (e.g., 139.88us -> 3.64us for secp192k1)
- **Scalar Multiplication:** ~500-1000x faster with cache for repeated operations
- **Signature Operations:** Significantly faster due to cached intermediate results

### Coordinate System Comparison

When LRU cache is enabled:

- Jacobian and Affine coordinates perform similarly for basic operations
- Jacobian coordinates show slight advantages in scalar multiplication

When LRU cache is disabled:

- Jacobian coordinates are faster for scalar multiplication (fewer modular inversions)
- The difference becomes more pronounced with larger curves

### Curve Size Impact

As expected, larger curves require more computation:

- secp521r1 operations take approximately 2-4x longer than secp256k1
- This is due to the larger field arithmetic operations

## Recommendations

1. **For most applications:** Use the default settings (Jacobian coordinates with LRU cache enabled).

2. **For memory-constrained environments:** Consider disabling LRU cache, but expect significant performance degradation.

3. **For high-throughput applications:** The LRU cache is essential for achieving optimal performance.

4. **For security-critical applications:** secp256r1 or secp384r1 offer a good balance of security and performance.

## Running Your Own Benchmarks

You can run the benchmarks yourself using the included benchmark script:

```bash
python benchmarks.py
```

This will generate performance data for your specific hardware and Python environment.
