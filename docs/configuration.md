# Configuration

ECUtils provides configuration options to customize its behavior for different use cases. This guide covers all available settings and how to use them effectively.

## LRU Cache Configuration

ECUtils uses an LRU (Least Recently Used) cache to dramatically improve performance by caching the results of expensive elliptic curve operations.

### Setting Cache Size

The cache size can be configured via environment variable or programmatically.

#### Environment Variable

Set the `LRU_CACHE_MAXSIZE` environment variable before running your application:

```bash
# Set cache size to 2048 entries
export LRU_CACHE_MAXSIZE=2048
python your_script.py
```

Or inline:

```bash
LRU_CACHE_MAXSIZE=2048 python your_script.py
```

#### Programmatic Configuration

You can also modify the cache size in your code, but this must be done **before** importing any ECUtils modules that use the cache:

```python
import os
os.environ["LRU_CACHE_MAXSIZE"] = "2048"

# Now import ecutils
from ecutils.algorithms import DigitalSignature
```

Alternatively, modify the settings module directly (also before first use):

```python
from ecutils import settings
settings.LRU_CACHE_MAXSIZE = 2048
```

### Cache Size Guidelines

| Use Case | Recommended Size | Notes |
|----------|------------------|-------|
| Default | 1024 | Good balance for most applications |
| High-throughput | 4096+ | More memory, better cache hits |
| Memory-constrained | 256 | Reduced memory footprint |
| Disabled | 0 | No caching (significant performance impact) |

### Disabling the Cache

To disable caching entirely:

```bash
export LRU_CACHE_MAXSIZE=0
```

Or programmatically:

```python
import os
os.environ["LRU_CACHE_MAXSIZE"] = "0"
```

**Warning:** Disabling the cache will significantly impact performance. See the [Benchmarks](benchmarks.md) page for performance comparisons.

## Coordinate System Configuration

ECUtils supports two coordinate systems for elliptic curve operations:

1. **Jacobian (Projective) Coordinates** - Default, faster for most operations
2. **Affine Coordinates** - Traditional representation

### Per-Curve Configuration

When retrieving a curve, you can specify the coordinate system:

```python
from ecutils.curves import get

# Use Jacobian coordinates (default, recommended)
curve_jacobian = get("secp256r1", use_projective_coordinates=True)

# Use Affine coordinates
curve_affine = get("secp256r1", use_projective_coordinates=False)
```

### Algorithm Configuration

Algorithms and protocols accept a `curve_name` parameter and inherit the coordinate system from the retrieved curve:

```python
from ecutils.algorithms import DigitalSignature
from ecutils.curves import get

# Method 1: Using curve_name (uses default Jacobian coordinates)
ds = DigitalSignature(private_key, curve_name="secp256r1")

# Method 2: Using a pre-configured curve
curve = get("secp256r1", use_projective_coordinates=False)
ds = DigitalSignature(private_key, curve=curve)
```

### When to Use Each Coordinate System

| Scenario | Recommended | Reason |
|----------|-------------|--------|
| General use | Jacobian | Faster scalar multiplication |
| Memory-critical | Affine | Slightly less memory per point |
| Debugging | Affine | Easier to verify calculations |
| Interoperability | Affine | Standard representation for export |

## Configuration Examples

### High-Performance Server

For a server handling many cryptographic operations:

```python
import os
os.environ["LRU_CACHE_MAXSIZE"] = "8192"

from ecutils.algorithms import DigitalSignature
from ecutils.curves import get

# Use Jacobian coordinates for speed
curve = get("secp256r1", use_projective_coordinates=True)
```

### Memory-Constrained Environment

For IoT or embedded systems:

```python
import os
os.environ["LRU_CACHE_MAXSIZE"] = "128"

from ecutils.curves import get

# Affine coordinates use slightly less memory per operation
curve = get("secp256r1", use_projective_coordinates=False)
```

### Development and Testing

For debugging and development:

```python
import os
os.environ["LRU_CACHE_MAXSIZE"] = "0"  # Disable cache for predictable behavior

from ecutils.curves import get

# Affine coordinates are easier to verify manually
curve = get("secp256r1", use_projective_coordinates=False)
```

## Configuration Reference

### Environment Variables

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `LRU_CACHE_MAXSIZE` | int | 1024 | Maximum number of cached operation results |

### Module Settings

| Setting | Location | Type | Default | Description |
|---------|----------|------|---------|-------------|
| `LRU_CACHE_MAXSIZE` | `ecutils.settings` | int | 1024 | Cache size |

### Curve Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `use_projective_coordinates` | bool | True | Use Jacobian coordinates |
