import json
import secrets
import sys
import timeit

from ecutils.algorithms import DigitalSignature, Koblitz
from ecutils.curves import get
from ecutils.protocols import DiffieHellman, MasseyOmura


def run_single_benchmark(curve_name, use_projective):
    """Runs the benchmarks for a single configuration."""

    curve = get(curve_name, use_projective_coordinates=use_projective)
    p1 = curve.G
    p2 = curve.multiply_point(2, curve.G)
    scalar = secrets.randbelow(curve.n)
    message = "This is a test message for Koblitz encoding."
    message_hash = secrets.randbits(256)

    results = {}

    # Benchmark point addition
    add_time = timeit.timeit(lambda: curve.add_points(p1, p2), number=10000)
    results["Point Addition (µs)"] = add_time / 1000 * 1e6

    # Benchmark point doubling
    double_time = timeit.timeit(lambda: curve.double_point(p1), number=10000)
    results["Point Doubling (µs)"] = double_time / 1000 * 1e6

    # Benchmark scalar multiplication
    mult_time = timeit.timeit(lambda: curve.multiply_point(scalar, p1), number=1000)
    results["Scalar Multiplication (ms)"] = mult_time / 100 * 1e3

    # Benchmark Koblitz encoding
    koblitz = Koblitz(curve_name=curve_name)
    koblitz.curve.use_projective_coordinates = use_projective
    try:
        koblitz_time = timeit.timeit(lambda: koblitz.encode(message), number=100)
        results["Koblitz Encoding (ms)"] = koblitz_time / 10 * 1e3
    except ValueError:
        results["Koblitz Encoding (ms)"] = "N/A"

    # Benchmark Digital Signature
    ds = DigitalSignature(private_key=scalar, curve_name=curve_name)
    ds.curve.use_projective_coordinates = use_projective
    sig_gen_time = timeit.timeit(
        lambda: ds.generate_signature(message_hash), number=1000
    )
    results["Signature Generation (ms)"] = sig_gen_time / 100 * 1e3
    r, s = ds.generate_signature(message_hash)
    sig_ver_time = timeit.timeit(
        lambda: ds.verify_signature(ds.public_key, message_hash, r, s), number=1000
    )
    results["Signature Verification (ms)"] = sig_ver_time / 100 * 1e3

    # Benchmark Diffie-Hellman
    dh = DiffieHellman(private_key=scalar, curve_name=curve_name)
    dh.curve.use_projective_coordinates = use_projective
    other_public_key = dh.curve.multiply_point(
        secrets.randbelow(dh.curve.n), dh.curve.G
    )
    dh_time = timeit.timeit(
        lambda: dh.compute_shared_secret(other_public_key), number=100
    )
    results["Diffie-Hellman (ms)"] = dh_time / 100 * 1e3

    # Benchmark Massey-Omura
    mo = MasseyOmura(private_key=scalar, curve_name=curve_name)
    mo.curve.use_projective_coordinates = use_projective
    try:
        message_point, _ = koblitz.encode("test")
        mo_time = timeit.timeit(
            lambda: mo.first_encryption_step(message_point), number=1000
        )
        results["Massey-Omura (ms)"] = mo_time / 100 * 1e3
    except ValueError:
        results["Massey-Omura (ms)"] = "N/A"

    return results


if __name__ == "__main__":
    curve_name = sys.argv[1]
    use_projective = sys.argv[2] == "True"
    results = run_single_benchmark(curve_name, use_projective)
    print(json.dumps(results))
